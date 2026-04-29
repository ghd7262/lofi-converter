import pytest

@pytest.mark.asyncio
async def test_upload_returns_filename(client):
    response = await client.post(
        "/api/upload",
        files={"file": ("test.mp3", b"fake-audio-data", "audio/mpeg")},
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "test.mp3"
