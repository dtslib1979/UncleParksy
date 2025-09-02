import * as fs from 'fs'
async function main(){ await fs.promises.mkdir('dist', { recursive: true }); console.log('✓ synthesize ready') }
main().catch(e=>{ console.error(e); process.exit(1) })