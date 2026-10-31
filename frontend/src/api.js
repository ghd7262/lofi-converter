async function json(res) {
  const body = await res.json()
  if (!res.ok) throw new Error(body.detail ?? `Request failed (${res.status})`)
  return body
}

export function uploadBatch(files) {
  const form = new FormData()
  files.forEach((file) => form.append('files', file))
  return fetch('/jobs', { method: 'POST', body: form }).then(json)
}

export function getBatch(batchId) {
  return fetch(`/batches/${batchId}`).then(json)
}

export const downloadUrl = (jobId) => `/jobs/${jobId}/download`
