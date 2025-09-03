import * as fs from 'fs'
import { execSync } from 'child_process'
async function main(){
  const platformsArg = process.argv[2] || 'tistory,wordpress,pages'
  const list = platformsArg.split(',').map(s=>s.trim()).filter(Boolean)
  const cfg = JSON.parse(await fs.promises.readFile('config/platforms.json','utf-8'))
  for (const name of list){
    const p = cfg[name]; if(!p){ console.warn(`! Unknown platform: ${name}`); continue }
    if (name==='tistory') execSync(`npx tsx scripts/adapters/tistory.ts "${p.scopeSelector}" ${p.specificityBoost}`, {stdio:'inherit'})
    else if (name==='wordpress') execSync(`npx tsx scripts/adapters/wordpress.ts "${p.scopeSelector}" ${p.specificityBoost}`, {stdio:'inherit'})
    else if (name==='pages') execSync(`npx tsx scripts/adapters/pages.ts`, {stdio:'inherit'})
  }
}
main().catch(e=>{ console.error(e); process.exit(1) })