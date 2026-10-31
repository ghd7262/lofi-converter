import { useEffect, useRef, useState } from 'react'
import { downloadUrl, getBatch, uploadBatch } from '../api'

const MAX_FILES = 10
const POLL_MS = 1000
const ACTIVE = ['uploading', 'queued', 'converting']

export default function FileConverter() {
  // row: { file, checked, status, jobId, error }; status is null until the file is sent
  const [rows, setRows] = useState([])
  const [batchId, setBatchId] = useState(null)
  const [dragging, setDragging] = useState(false)
  const [error, setError] = useState(null)
  const inputRef = useRef(null)

  const busy = rows.some((row) => ACTIVE.includes(row.status))
  const checked = rows.filter((row) => row.checked)

  useEffect(() => {
    if (!batchId || !busy) return
    const timer = setInterval(async () => {
      try {
        const batch = await getBatch(batchId)
        const byId = Object.fromEntries(batch.jobs.map((job) => [job.job_id, job]))
        setRows((rows) =>
          rows.map((row) => {
            const job = byId[row.jobId]
            return job ? { ...row, status: job.status, error: job.error } : row
          }),
        )
      } catch (e) {
        setError(e.message)
      }
    }, POLL_MS)
    return () => clearInterval(timer)
  }, [batchId, busy])

  function addFiles(files) {
    if (busy) return
    setError(null)
    setRows((rows) => {
      // Picking files after a batch ran starts a fresh list.
      const kept = rows.some((row) => row.status) ? [] : rows
      const next = [...kept]
      for (const file of files) {
        if (!next.some((row) => row.file.name === file.name)) next.push({ file, checked: true, status: null })
      }
      return next.slice(0, MAX_FILES)
    })
  }

  function toggle(name) {
    setRows((rows) => rows.map((row) => (row.file.name === name ? { ...row, checked: !row.checked } : row)))
  }

  async function convert() {
    const names = new Set(checked.map((row) => row.file.name))
    setError(null)
    setRows((rows) => rows.map((row) => (names.has(row.file.name) ? { ...row, status: 'uploading' } : row)))
    try {
      const res = await uploadBatch(checked.map((row) => row.file))
      const accepted = Object.fromEntries(res.jobs.map((job) => [job.file_name, job.job_id]))
      const rejected = Object.fromEntries(res.rejected.map((r) => [r.file_name, r.error]))
      setRows((rows) =>
        rows.map((row) => {
          const name = row.file.name
          if (accepted[name]) return { ...row, status: 'queued', jobId: accepted[name] }
          if (rejected[name]) return { ...row, status: 'failed', error: rejected[name] }
          return row
        }),
      )
      setBatchId(res.batch_id)
    } catch (e) {
      setError(e.message)
      setRows((rows) => rows.map((row) => (row.status === 'uploading' ? { ...row, status: null } : row)))
    }
  }

  return (
    <div className="window w-full max-w-xl">
      <div className="title-bar">
        <div className="title-bar-text">lo-fi converter</div>
      </div>
      <div className="window-body">
        <div
          className={`sunken-panel p-6 mb-3 text-center ${busy ? 'opacity-50' : 'cursor-pointer'}`}
          style={{ background: dragging ? '#ffffcc' : 'white' }}
          onClick={() => !busy && inputRef.current.click()}
          onDragOver={(e) => {
            e.preventDefault()
            setDragging(true)
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault()
            setDragging(false)
            addFiles(e.dataTransfer.files)
          }}
        >
          <p>{busy ? 'Converting… please wait' : `Drop MP3 or M4A files here, or click to browse (max ${MAX_FILES})`}</p>
          <input
            ref={inputRef}
            type="file"
            accept=".mp3,.m4a,audio/mpeg,audio/mp4"
            multiple
            hidden
            disabled={busy}
            aria-label="Choose audio files"
            onChange={(e) => {
              addFiles(e.target.files)
              e.target.value = '' // allow picking the same file again later
            }}
          />
        </div>

        {rows.length > 0 && (
          <ul className="tree-view mb-3">
            {rows.map((row) => (
              <li key={row.file.name} className="flex items-center gap-2 py-1">
                <input
                  type="checkbox"
                  id={`check-${row.file.name}`}
                  checked={row.checked}
                  disabled={busy || !!row.status}
                  onChange={() => toggle(row.file.name)}
                />
                <label htmlFor={`check-${row.file.name}`} className="flex-1 truncate">
                  {row.file.name}
                </label>
                <span className="w-40 text-right">
                  {row.status === 'failed' ? `failed: ${row.error?.message}` : row.status}
                </span>
                {row.status === 'succeeded' && (
                  <button
                    aria-label={`Download ${row.file.name}`}
                    title="Download"
                    onClick={() => (window.location.href = downloadUrl(row.jobId))}
                  >
                    💾
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}

        {error && <p role="alert">⚠ {error}</p>}

        <section className="field-row justify-end">
          <button onClick={convert} disabled={busy || checked.length === 0 || rows.some((row) => row.status)}>
            Convert to lo-fi
          </button>
        </section>
      </div>
    </div>
  )
}
