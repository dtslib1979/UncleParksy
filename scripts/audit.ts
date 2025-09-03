import * as fs from 'fs'
import { hex as contrast } from 'wcag-contrast'
function toHex(tri: string){ const [r,g,b]=tri.split(/\s+/).map(Number); return '#' + [r,g,b].map(v=>v.toString(16).padStart(2,'0')).join('') }
async function main(){
  const latest = JSON.parse(await fs.promises.readFile('data/themes/latest.json','utf-8'))
  const t = latest.tokens
  const report = {
    pairs: {
      fg_on_bg: contrast(toHex(t.fg), toHex(t.bg)),
      brand_on_bg: contrast(toHex(t.brand), toHex(t.bg)),
      accent_on_bg: contrast(toHex(t.accent), toHex(t.bg))
    },
    notes: '4.5 이상이면 본문 텍스트 AA 통과'
  }
  await fs.promises.writeFile('reports/audit.json', JSON.stringify(report,null,2))
  console.log('✓ wrote reports/audit.json')
}
main().catch(e=>{ console.error(e); process.exit(1) })