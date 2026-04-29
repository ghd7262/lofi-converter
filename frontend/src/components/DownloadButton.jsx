export default function DownloadButton({ href, disabled }) {
  return (
    <a
      href={href ?? '#'}
      download="lofi-version.mp3"
      aria-disabled={disabled}
      className={`
        block w-full text-center py-3 rounded-xl font-medium text-sm transition-all duration-300
        ${disabled
          ? 'bg-white/5 text-white/20 pointer-events-none cursor-not-allowed'
          : 'bg-amber-400/20 text-amber-400 border border-amber-400/30 hover:bg-amber-400/30 hover:shadow-[0_0_20px_rgba(244,162,97,0.2)]'
        }
      `}
    >
      Download Lo-fi MP3
    </a>
  )
}
