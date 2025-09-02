import * as fs from 'fs'
async function main() {
  const latest = JSON.parse(await fs.promises.readFile('data/themes/latest.json', 'utf-8'))
  const t = latest.tokens
  const css = `:root {
  --bg: ${t.bg};
  --fg: ${t.fg};
  --brand: ${t.brand};
  --accent: ${t.accent};
  --radius: ${t.radius};
  --font-sans: ${t.fontSans};
  --space-base: ${t.spaceBase};
  --shadow-card: ${t.shadowCard};
}

[data-theme="dark"] {
  /* TODO: dark tokens if needed */
}
`
  await fs.promises.writeFile('styles/tokens.css', css)
  console.log('✓ wrote styles/tokens.css')
}
main().catch(e => { console.error(e); process.exit(1) })