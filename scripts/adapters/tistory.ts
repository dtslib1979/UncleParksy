import * as fs from 'fs'
import { wrapWithScope, boostSpecificity } from './common.js'
async function main(){
  const scope = process.argv[2] || '#app'
  const boost = Number(process.argv[3] || 1)
  const css = await fs.promises.readFile('styles/tokens.css','utf-8')
  const scoped = boostSpecificity(wrapWithScope(css, scope), boost, scope)
  const snippet = `<!-- Paste into Tistory Skin HTML <head> or <style> -->
<style>
${scoped}
${scope} { color: rgb(var(--fg)); background: rgb(var(--bg)); font-family: var(--font-sans); }
</style>`
  await fs.promises.mkdir('dist',{recursive:true})
  await fs.promises.writeFile('dist/tistory-snippet.html', snippet)
  console.log('✓ Tistory: dist/tistory-snippet.html')
}
main().catch(e=>{ console.error(e); process.exit(1) })