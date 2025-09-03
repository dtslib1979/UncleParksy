import * as fs from 'fs'
import { wrapWithScope, boostSpecificity } from './common.js'
async function main(){
  const scope = process.argv[2] || 'body'
  const boost = Number(process.argv[3] || 0)
  const css = await fs.promises.readFile('styles/tokens.css','utf-8')
  const scoped = boostSpecificity(wrapWithScope(css, scope), boost, scope)
  await fs.promises.mkdir('dist',{recursive:true})
  await fs.promises.writeFile('dist/wp-additional-css.css', scoped)
  console.log('✓ WordPress: dist/wp-additional-css.css')
}
main().catch(e=>{ console.error(e); process.exit(1) })