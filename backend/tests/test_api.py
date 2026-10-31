import time

from app import config, jobs
from app.cleanup import cleanup_expired


def upload(client, *files):
    return client.post("/jobs", files=[("files", f) for f in files])


def test_batch_accepts_valid_and_rejects_invalid(client, tone_mp3, monkeypatch):
    data = tone_mp3.read_bytes()
    monkeypatch.setattr(config, "MAX_FILE_MB", 1)
    big = ("big.mp3", b"x" * (1024 * 1024 + 1))
    res = upload(client, ("a.mp3", data), ("a.mp3", data), ("notes.txt", b"hi"), big, ("c.M4A", data))

    assert res.status_code == 202
    body = res.json()
    assert [j["file_name"] for j in body["jobs"]] == ["a.mp3", "c.M4A"]
    assert {r["file_name"]: r["error"]["code"] for r in body["rejected"]} == {
        "a.mp3": "duplicate_name",
        "notes.txt": "unsupported_format",
        "big.mp3": "too_large",
    }


def test_batch_converts_and_downloads(client, tone_mp3):
    body = upload(client, ("song.mp3", tone_mp3.read_bytes())).json()

    # TestClient runs background tasks before returning, so the batch is done by now.
    batch = client.get(f"/batches/{body['batch_id']}").json()
    assert batch["jobs"][0]["status"] == "succeeded"

    res = client.get(f"/jobs/{body['jobs'][0]['job_id']}/download")
    assert res.status_code == 200
    assert res.headers["content-type"] == "audio/mpeg"
    assert "song-lofi.mp3" in res.headers["content-disposition"]


def test_corrupt_mp3_fails_with_conversion_error(client):
    body = upload(client, ("fake.mp3", b"not audio")).json()
    job = client.get(f"/batches/{body['batch_id']}").json()["jobs"][0]
    assert job["status"] == "failed"
    assert job["error"]["code"] == "conversion_error"
    assert client.get(f"/jobs/{job['job_id']}/download").status_code == 409


def test_too_many_or_zero_files_is_400(client, tone_mp3):
    data = tone_mp3.read_bytes()
    assert upload(client, *[(f"{i}.mp3", data) for i in range(11)]).status_code == 400
    assert client.post("/jobs").status_code == 400


def test_unknown_ids_are_404(client):
    assert client.get("/batches/nope").status_code == 404
    assert client.get("/jobs/nope/download").status_code == 404


def test_cleanup_deletes_files_after_expiry(client, tone_mp3):
    body = upload(client, ("song.mp3", tone_mp3.read_bytes())).json()
    job = jobs.jobs[body["jobs"][0]["job_id"]]
    assert job.output_path.exists()

    cleanup_expired(now=job.finished_at + config.CLEANUP_AFTER_SECONDS - 1)
    assert job.output_path.exists()

    cleanup_expired(now=job.finished_at + config.CLEANUP_AFTER_SECONDS)
    assert not job.input_path.parent.exists()
    assert client.get(f"/jobs/{job.job_id}/download").status_code == 404
    assert client.get(f"/batches/{body['batch_id']}").status_code == 404
