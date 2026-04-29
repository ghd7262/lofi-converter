export default function URLInput({ value, onChange }) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-white/40 text-xs uppercase tracking-widest">
        Or paste a link
      </label>
      <input
        type="url"
        value={value}
        onChange={(e) => onChange?.(e.target.value)}
        placeholder="https://youtube.com/watch?v=..."
        className="
          w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3
          text-white/80 placeholder-white/20 text-sm
          focus:outline-none focus:border-amber-400/60 focus:shadow-[0_0_16px_rgba(244,162,97,0.15)]
          transition-all duration-300
        "
        aria-label="YouTube URL"
      />
    </div>
  )
}
