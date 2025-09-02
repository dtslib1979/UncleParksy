import * as fs from 'fs'
import Vibrant from 'node-vibrant'
import { colord, extend } from 'colord'
import namesPlugin from 'colord/plugins/names'
extend([namesPlugin])
function rgbTriplet(input: string) { const c = colord(input); const { r, g, b } = c.toRgb(); return `${r} ${g} ${b}` }
async function main() {
  const raw = JSON.parse(await fs.promises.readFile('reports/raw.json', 'utf-8'))
  const palette = await Vibrant.from('reports/source.png').getPalette()
  const primary = palette.Vibrant?.hex || '#7c3aed'
  const accent = palette.LightVibrant?.hex || palette.Muted?.hex || '#22d3ee'
  const sorted = raw.colors.map((c: string) => ({ c, l: colord(c).toHsl().l })).sort((a: any, b: any) => a.l - b.l)
  const bg = sorted[0]?.c || '#ffffff'
  const fg = sorted.at(-1)?.c || '#111827'
  const radii = (raw.radii as string[]).map(r => parseFloat(r)).filter(n => !isNaN(n)).sort((a,b)=>a-b)
  const radius = (radii.find(n => n >= 8) ?? radii.pop() ?? 12) + 'px'
  const font = (raw.fonts as string[]).find(f => !/sans-serif|serif|monospace/i.test(f)) || '"Noto Sans KR", ui-sans-serif, system-ui, -apple-system, sans-serif'
  const theme = { meta: { source: raw.url, title: raw.title, createdAt: new Date().toISOString() },
    tokens: { bg: rgbTriplet(bg), fg: rgbTriplet(fg), brand: rgbTriplet(primary), accent: rgbTriplet(accent),
      radius, fontSans: font, spaceBase: '1rem', shadowCard: '0 4px 24px rgba(0,0,0,0.08)' } }
  await fs.promises.mkdir('data/themes', { recursive: true })
  await fs.promises.writeFile('data/themes/latest.json', JSON.stringify(theme, null, 2))
  console.log('✓ extracted → data/themes/latest.json')
}
main().catch(e => { console.error(e); process.exit(1) })