export default function Page(){
  return (
    <main className="min-h-screen p-8 md:p-16">
      <div className="max-w-4xl mx-auto grid gap-6">
        <header className="grid gap-2">
          <span className="text-sm opacity-70">ThemeExtractor Engine</span>
          <h1 className="text-3xl md:text-5xl font-bold tracking-tight">Your Theme, Instantly</h1>
          <p className="opacity-80">URL → Extract → Tokens → Templates → Deploy</p>
        </header>
        <section className="grid gap-4">
          <div className="rounded-xl p-6 shadow-card border border-black/5 bg-white/60 dark:bg-black/20">
            <h2 className="text-xl font-semibold mb-2">Buttons</h2>
            <div className="flex gap-3 flex-wrap">
              <button className="px-4 py-2 rounded-lg bg-brand text-white">Primary</button>
              <button className="px-4 py-2 rounded-lg border">Secondary</button>
              <button className="px-4 py-2 rounded-lg bg-accent/20">Ghost</button>
            </div>
          </div>
          <div className="rounded-xl p-6 shadow-card border border-black/5">
            <h2 className="text-xl font-semibold mb-2">Typography</h2>
            <p className="leading-relaxed">Font: <code>var(--font-sans)</code></p>
            <p>Border radius: <code>var(--radius)</code></p>
          </div>
        </section>
      </div>
    </main>
  )
}