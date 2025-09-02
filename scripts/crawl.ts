import { chromium } from 'playwright'
import * as fs from 'fs'
const url = process.argv[2]
if (!url) { console.error('Usage: ts-node scripts/crawl.ts <url>'); process.exit(1) }
async function main() {
  const browser = await chromium.launch()
  const page = await browser.newPage({ viewport: { width: 1366, height: 900 } })
  await page.goto(url, { waitUntil: 'networkidle' })
  await fs.promises.mkdir('reports', { recursive: true })
  await page.screenshot({ path: 'reports/source.png', fullPage: true })
  const data = await page.evaluate(() => {
    const nodes = Array.from(document.querySelectorAll('*')).slice(0, 800)
    const uniq = (arr: any[]) => Array.from(new Set(arr.filter(Boolean)))
    const fonts = uniq(nodes.map(el => getComputedStyle(el as Element).fontFamily))
    const radii = uniq(nodes.map(el => getComputedStyle(el as Element).borderTopLeftRadius))
    const shadows = uniq(nodes.map(el => getComputedStyle(el as Element).boxShadow))
    const colors = uniq(nodes.flatMap(el => {
      const cs = getComputedStyle(el as Element)
      return [cs.color, cs.backgroundColor]
    }))
    return { title: document.title, url: location.href, fonts, radii, shadows, colors }
  })
  await fs.promises.writeFile('reports/raw.json', JSON.stringify(data, null, 2))
  await browser.close()
}
main().catch(e => { console.error(e); process.exit(1) })