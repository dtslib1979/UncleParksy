import type { Config } from 'tailwindcss'
const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx,mdx}', './components/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        bg: 'rgb(var(--bg) / <alpha-value>)',
        fg: 'rgb(var(--fg) / <alpha-value>)',
        brand: 'rgb(var(--brand) / <alpha-value>)',
        accent: 'rgb(var(--accent) / <alpha-value>)'
      },
      fontFamily: { sans: ['var(--font-sans)'] },
      borderRadius: { lg: 'var(--radius)' },
      spacing: { base: 'var(--space-base)' },
      boxShadow: { card: 'var(--shadow-card)' }
    }
  }
}
export default config