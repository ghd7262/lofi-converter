import { useState } from 'react'
import FileUpload from './components/FileUpload'
import URLInput from './components/URLInput'
import AudioPlayer from './components/AudioPlayer'
import DownloadButton from './components/DownloadButton'
import './index.css'

export default function App() {
  const [file, setFile] = useState(null)
  const [url, setUrl] = useState('')
  const [converting, setConverting] = useState(false)
  const [previewSrc, setPreviewSrc] = useState(null)

  const hasInput = file !== null || url.trim() !== ''

  function handleConvert() {
    if (!hasInput) return
    setConverting(true)
    // Static mockup: simulate a conversion delay
    setTimeout(() => {
      setConverting(false)
      setPreviewSrc('#') // real src will come from backend later
    }, 2000)
  }

  return (
    <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4 py-16">

      {/* Header */}
      <div className="text-center mb-12">
        <h1
          className="text-5xl font-semibold text-white mb-3"
          style={{ fontFamily: "'Playfair Display', serif" }}
        >
          lo-fi converter
        </h1>
        <p className="text-white/30 text-sm tracking-wide">
          drop a track. get the vibe.
        </p>
      </div>

      {/* Card */}
      <div className="w-full max-w-lg bg-white/[0.03] border border-white/10 rounded-3xl p-8 shadow-2xl flex flex-col gap-6">

        <FileUpload onFileSelect={setFile} />

        {/* Divider */}
        <div className="flex items-center gap-3">
          <div className="flex-1 h-px bg-white/10" />
          <span className="text-white/20 text-xs uppercase tracking-widest">or</span>
          <div className="flex-1 h-px bg-white/10" />
        </div>

        <URLInput value={url} onChange={setUrl} />

        {/* Convert Button */}
        <button
          onClick={handleConvert}
          disabled={!hasInput || converting}
          className={`
            w-full py-4 rounded-xl font-semibold text-sm tracking-wide transition-all duration-300
            ${hasInput && !converting
              ? 'bg-amber-400 text-[#0f0e17] hover:bg-amber-300 shadow-[0_0_32px_rgba(244,162,97,0.35)] hover:shadow-[0_0_48px_rgba(244,162,97,0.5)]'
              : 'bg-white/5 text-white/20 cursor-not-allowed'
            }
          `}
        >
          {converting ? 'Converting...' : 'Convert to Lo-fi'}
        </button>

        <AudioPlayer src={previewSrc} />

        <DownloadButton href={previewSrc} disabled={!previewSrc} />
      </div>

      {/* Footer */}
      <p className="text-white/15 text-xs mt-10 tracking-wide">
        supports mp3 · wav · youtube links
      </p>
    </div>
  )
}
