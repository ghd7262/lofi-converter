import { useState } from 'react'

export default function FileUpload({ onFileSelect }) {
  const [dragging, setDragging] = useState(false)
  const [fileName, setFileName] = useState(null)

  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) {
      setFileName(file.name)
      onFileSelect?.(file)
    }
  }

  function handleChange(e) {
    const file = e.target.files[0]
    if (file) {
      setFileName(file.name)
      onFileSelect?.(file)
    }
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      className={`
        relative border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-300
        ${dragging
          ? 'border-amber-400 bg-amber-400/10 shadow-[0_0_24px_rgba(244,162,97,0.2)]'
          : 'border-white/10 hover:border-amber-400/50 hover:bg-white/5'
        }
      `}
    >
      <input
        type="file"
        accept=".mp3,.wav"
        onChange={handleChange}
        className="absolute inset-0 opacity-0 cursor-pointer"
        aria-label="Upload audio file"
      />

      <div className="text-4xl mb-3">🎵</div>

      {fileName ? (
        <p className="text-amber-400 font-medium">{fileName}</p>
      ) : (
        <>
          <p className="text-white/80 font-medium mb-1">Drop your file here</p>
          <p className="text-white/30 text-sm">MP3 or WAV · Click or drag to upload</p>
        </>
      )}
    </div>
  )
}
