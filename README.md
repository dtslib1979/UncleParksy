# 🎨 Theme Extractor Engine

> **Automated theme extraction from any website → CSS tokens → Platform-specific outputs**

![Preview](https://github.com/user-attachments/assets/3dfb57b5-3bce-470f-acac-07597086253a)

## 🚀 Features

- **🕸️ Web Crawling**: Extract colors, fonts, and design tokens from any website
- **🎯 Smart Analysis**: Use AI-powered color extraction with node-vibrant
- **🎨 CSS Generation**: Automatic CSS custom properties generation
- **📱 Multi-Platform**: Generate code for Tistory, WordPress, and GitHub Pages
- **♿ Accessibility**: Built-in WCAG contrast checking
- **⚡ Automated**: GitHub Actions workflows for extraction and deployment

## 📁 Project Structure

```
theme-extractor-engine/
├── app/                    # Next.js application (preview interface)
├── scripts/                # Core extraction and generation scripts
│   ├── crawl.ts           # Web crawling with Playwright
│   ├── extract.ts         # Theme extraction with node-vibrant
│   ├── tokens.ts          # CSS token generation
│   ├── audit.ts           # Accessibility auditing
│   └── adapters/          # Platform-specific generators
├── styles/                # Global styles and generated tokens
├── config/                # Platform configurations
├── data/themes/           # Extracted theme data
├── dist/                  # Generated platform outputs
└── reports/               # Analysis and audit reports
```

## 🛠️ Usage

### Manual Execution

1. **Install dependencies:**
```bash
npm install
```

2. **Install Playwright browsers:**
```bash
npx playwright install --with-deps
```

3. **Extract theme from a website:**
```bash
# Crawl and analyze
npm run analyze https://vercel.com

# Extract theme data
npm run extract

# Generate CSS tokens
npm run tokens

# Create platform outputs
npm run build:platforms

# Run accessibility audit
npm run audit
```

### GitHub Actions (Recommended)

1. Go to **Actions** → **Analyze & Generate**
2. Click **Run workflow**
3. Enter:
   - **URL**: `https://vercel.com` (or any website)
   - **Platforms**: `tistory,wordpress,pages` (or subset)

### Results

After processing, you'll get:

- **`styles/tokens.css`** - CSS custom properties
- **`data/themes/latest.json`** - Extracted theme data
- **`dist/tistory-snippet.html`** - Tistory skin code
- **`dist/wp-additional-css.css`** - WordPress additional CSS
- **`reports/audit.json`** - Accessibility audit results

## 🎯 Platform Integration

### Tistory
```html
<!-- Copy from dist/tistory-snippet.html -->
<style>
:root {
  --bg: 255 255 255;
  --fg: 17 24 39;
  --brand: 124 58 237;
  /* ... */
}
</style>
```

### WordPress
Copy contents of `dist/wp-additional-css.css` to **Appearance** → **Customize** → **Additional CSS**

### GitHub Pages
The `styles/tokens.css` file is ready to use directly in your static site.

## ⚡ Development

```bash
# Start Next.js preview server
npm run dev

# Build for production
npm run build
```

## 🎯 Acceptance Criteria

✅ **Contrast Requirements:**
- Text contrast ≥ 7.0 (AAA level)
- UI elements contrast ≥ 4.5 (AA level)

✅ **Platform Compatibility:**
- Tistory: Scoped CSS with specificity boost
- WordPress: Additional CSS ready
- GitHub Pages: Direct integration

✅ **Automation:**
- GitHub Actions workflows
- Automatic Pages deployment
- Commit generated artifacts

## 📄 License

MIT License - Feel free to use for personal and commercial projects.

---

**"Extract → Tokenize → Synthesize"** 🎨
