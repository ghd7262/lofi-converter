export default function AudioPlayer({ src }) {
  if (!src) return null

  return (
    <div className="bg-white/5 border border-white/10 rounded-2xl p-5">
      <p className="text-white/40 text-xs uppercase tracking-widest mb-3">Preview</p>
      <audio
        controls
        src={src}
        className="w-full"
        aria-label="Lo-fi audio preview"
      />
    </div>
  )
}
