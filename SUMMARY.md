# 📚 UncleParksy Repository Summary

> **Last Updated**: November 2025  
> **Repository Type**: AI Creator Liberal Arts Codex / Personal Operating System  
> **Primary URL**: [parksy.kr](https://parksy.kr) | [GitHub Pages](https://dtslib1979.github.io/UncleParksy/)

---

## 📁 Repository Structure Overview

```
UncleParksy/
├── .github/
│   └── workflows/           # 7 GitHub Actions automation workflows
│       ├── build-textstory.yml       # KR TextStory Archive automation
│       ├── category-index.yml        # Category index builder
│       ├── mobilize.yml              # Clean and mobilize archive pipeline
│       ├── obsidian-backup.yml       # Obsidian category auto backup
│       ├── obsidian-sync.yml         # GitHub → Obsidian sync
│       ├── pages-maintenance.yml     # Sitemap & index rebuilding
│       └── tistory-backup.yml        # Tistory blog backup
│
├── _obsidian/
│   └── _imports/            # Obsidian synchronization folder
│       ├── html_raw/        # Raw HTML backups
│       └── html_md/         # Converted Markdown files
│
├── archive/                 # KR TextStory chronological archive (24 HTML files)
│   ├── index.html
│   └── [dated HTML files]   # Format: YYYY-MM-DD-제목.html
│
├── assets/
│   ├── audio/              # Ambient BGM audio files
│   ├── categories-manifest.json
│   ├── css/                # Stylesheet resources
│   ├── home.json           # Static fallback for file counts
│   ├── icons/              # Hand-drawn SVG chapter icons
│   ├── img/                # Image assets
│   ├── js/                 # JavaScript resources
│   ├── manifest.json       # Archive manifest (auto-generated)
│   └── og/                 # Open Graph images
│
├── backup/
│   ├── raw/                # Raw Tistory backup HTML files
│   ├── simple-index-files/ # Simple index templates
│   ├── ADVANCED_INDEX_RESTORATION.md
│   ├── README.md
│   └── TRIGGER_AUTOMATION.md
│
├── category/               # 7 Persona-based content categories
│   ├── Blogger-Parksy/     # PWA Alchemist content
│   ├── Musician-Parksy/    # Sonic Architect content
│   ├── Orbit-Log/          # Life Archivist content
│   ├── Philosopher-Parksy/ # Essayist / Theorist content
│   ├── Protocol-Parksy/    # System Designer content
│   ├── Technician-Parksy/  # Device Whisperer content
│   └── Visualizer-Parksy/  # Diagram Shaman content
│
├── scripts/                # Python automation scripts
│   ├── auto_install.py            # Full automation system
│   ├── clean_and_mobilize.py      # Content extraction & mobile optimization
│   ├── clean_archive_for_foreigners.py
│   ├── generate_category_index.py # Category index generator
│   ├── generate_manifest.py       # Manifest generator
│   ├── mirror_backup.py           # Backup mirroring
│   ├── mobilize_archive.py        # Mobile CSS optimizer
│   └── tistory_backup.py          # Tistory RSS backup
│
├── index.html              # Main Codex entry (~802 lines, self-contained)
├── about.html              # About page
├── contact.html            # Contact page
├── feed.xml                # RSS feed
├── sitemap.xml             # Auto-generated sitemap
├── manifest.webmanifest    # PWA manifest
├── sw.js                   # Service Worker for offline support
├── CNAME                   # Custom domain (parksy.kr)
├── README.md               # Project documentation
├── 구조평가보고서.md        # Repository structure evaluation (Korean)
└── requirements.txt        # Python dependencies
```

---

## 🔑 Key Implementations Timeline

### Foundation Phase
- **Repository Creation**: UncleParksy established as the canonical entrypoint for Parksy World
- **8-Chapter Liberal Arts Model**: Implemented 7 distinct persona-based categories:
  - Philosopher-Parksy (Long-form thought, Korean Merit Theory)
  - Blogger-Parksy (Prompt engines, full-stack HTML labs)
  - Visualizer-Parksy (Systems mapping, sketch-note metaphysics)
  - Musician-Parksy (Emotion modeling, cinematic cue design)
  - Technician-Parksy (Keyboard rituals, tablet workflows)
  - Orbit-Log (Seasonal logs, meta-reflections)
  - Protocol-Parksy (Reproducible workflows, LLM constitutions)

### Core Technical Implementations
- **index.html Codex**: ~802 lines of self-contained HTML/CSS/JavaScript
  - Parchment-themed minimalist UI with book-cover hero
  - Eight interactive chapter cards with live file counters
  - Three.js floating glyphs (respects `prefers-reduced-motion`)
  - Optional ambient BGM with one-tap toggle
  - GitHub Contents API integration with graceful fallback to `assets/home.json`
  - Fully offline-capable via Service Worker
  - Print-optimized layout

### Automation Infrastructure
- **GitHub Actions Workflows**: 7 automated pipelines (see Workflows section below)
- **Python Automation Scripts**: 8 scripts handling backup, sync, and content processing
- **PWA Support**: Service Worker + manifest for offline capability

### Content Archive System
- **KR TextStory Archive**: Chronological archive with 24 HTML documents
- **Category Content**: 51 HTML files across 7 categories
- **Tistory Blog Integration**: Automated RSS-based backup from external blog

### Documentation & Guides
- **구조평가보고서.md**: Comprehensive repository evaluation (Score: 85/100, Grade: A)
- **PR_CLEANUP_GUIDE.md**: Guide for PR management
- **QUICK_COMMANDS.md**: GitHub CLI shortcuts

---

## ⚙️ Workflows Explanation

### 1. 🤖 build-textstory.yml — KR TextStory Complete Automation

**Purpose**: Fully automated KR TextStory Archive management system with zero manual intervention.

**Triggers**:
- Push to `backup/**`, `scripts/**`, `.github/workflows/**`
- Schedule: Every 3 hours (`0 */3 * * *`)
- Manual workflow dispatch

**Pipeline Steps**:
1. **Checkout**: Full repository with fetch-depth: 0
2. **Python Setup**: Python 3.11 with pip caching
3. **Dependencies**: beautifulsoup4, lxml, requests
4. **Execute**: `python scripts/auto_install.py`
   - Environment auto-setup
   - Mirror backup files (original HTML preserved)
   - Mobile optimization via `mobilize_archive.py`
   - Generate `assets/manifest.json`
   - Auto-verification of results
5. **Statistics Reporting**: Backup count, archive count, manifest items
6. **Auto-commit & Push**: Commits to `archive/` and `assets/manifest.json`
7. **Deployment Verification**: Tests GitHub Pages accessibility

**Key Script**: `scripts/auto_install.py`
- `AutoInstallSystem` class handles full automation
- `_mirror_backup_files()`: Smart file mirroring with modification time checking
- `_mobilize_archive_files()`: Calls mobile optimization subprocess
- `_generate_manifest()`: Creates JSON manifest with title extraction from HTML
- `_auto_recovery()`: Fallback recovery mechanism

---

### 2. 🗂️ category-index.yml — Category Index Builder

**Purpose**: Rebuilds category index files and triggers Obsidian sync on content changes.

**Triggers**:
- Push to `main` branch affecting `category/**.html` or `scripts/generate_category_index.py`
- Manual workflow dispatch

**Concurrency**: `category-index-build` group (no cancellation of in-progress)

**Pipeline Steps**:
1. **Checkout**: Repository checkout
2. **Python Setup**: Python 3.11
3. **Execute**: `python scripts/generate_category_index.py`
   - Scans `category/` directories
   - Counts HTML files (excluding index.html)
   - Updates `assets/home.json` with category counts
4. **Commit & Push**: Updates `category/*/index.html` and `assets/home.json`
5. **Trigger Obsidian Sync**: Dispatches `obsidian-sync.yml` workflow for immediate synchronization

**Key Script**: `scripts/generate_category_index.py`
- Iterates through category directories
- Generates file counts for home.json
- Note: Advanced index.html files are preserved (not overwritten)

---

### 3. 🧹 mobilize.yml — Clean and Mobilize Archive

**Purpose**: Extracts main content from Tistory backup HTML and rebuilds with clean mobile-optimized templates.

**Triggers**:
- Schedule: Every 6 hours, 30 minutes after backup (`30 */6 * * *`)
- Push to `backup/raw/*.html` or `scripts/clean_and_mobilize.py`
- Manual workflow dispatch

**Pipeline Steps**:
1. **Checkout**: Repository checkout
2. **Python Setup**: Python 3.11
3. **Dependencies**: beautifulsoup4, lxml
4. **Execute**: `python scripts/clean_and_mobilize.py`
   - Scans `backup/raw/` or `archive/` for input files
   - Extracts content using priority CSS selectors:
     - Primary: `.tt_article_useless_p_margin.contents_style`
     - Secondary: `#article-view`
     - Fallback: article, main, .post-content, etc.
   - Cleans unwanted elements (scripts, ads, navigation)
   - Applies minimal mobile template with viewport-fit cover
5. **Commit & Push**: Updates `archive/` directory

**Key Script**: `scripts/clean_and_mobilize.py`
- `get_mini_template()`: Returns minimal mobile HTML template
- `extract_title()`: Extracts title from HTML or filename
- `extract_content_by_selectors()`: Priority-based content extraction
- `clean_extracted_content()`: Removes unwanted HTML elements
- Output: Clean, mobile-friendly archive files

---

### 4. 📥 obsidian-backup.yml — Obsidian Category Auto Backup

**Purpose**: Automatically backs up category files to Obsidian import folder when category content changes.

**Triggers**:
- Push affecting `category/**`

**Condition**: Skips if actor is `github-actions[bot]`

**Pipeline Steps**:
1. **Checkout**: Repository checkout
2. **rsync Copy**: 
   ```bash
   rsync -a --exclude='.git/' category/ _obsidian/_imports/category/
   ```
3. **Commit & Push**: Updates `_obsidian/_imports/category/`

---

### 5. 📥 obsidian-sync.yml — GitHub → Obsidian Full Sync

**Purpose**: Comprehensive synchronization from GitHub to Obsidian with HTML→Markdown conversion.

**Triggers**:
- Push to `main` branch affecting `category/**`
- Schedule: Every 3 hours (`0 */3 * * *`)
- Manual workflow dispatch

**Condition**: Skips if actor is `github-actions[bot]`

**Pipeline Steps**:
1. **Checkout**: Repository checkout
2. **Git Configuration**: Sets up obsidian-backup-bot identity
3. **Install Tools**: rsync, pandoc (for HTML→MD conversion)
4. **Prepare Folders**: Creates `_obsidian/_imports/html_raw/` and `_obsidian/_imports/html_md/`
5. **Analyze Content**: Counts HTML files and folders in `category/`
6. **RAW HTML Backup**: Syncs entire `category/` to `html_raw/`
7. **HTML → Markdown Conversion**: 
   - Uses pandoc to convert HTML to GitHub Flavored Markdown
   - Fallback: sed-based HTML tag removal
8. **Generate Sync Report**: Creates `동기화_보고서.md` with:
   - Execution timestamp
   - Processing statistics
   - Category breakdown
   - Usage instructions
9. **Commit & Push**: Detailed commit message with statistics

**Strategy**: Public GitHub (portfolio) → Private Obsidian (commercial content development)

---

### 6. 📄 pages-maintenance.yml — Pages Maintenance

**Purpose**: Generates sitemap and rebuilds category indexes on content changes.

**Triggers**:
- Push to `main` branch affecting:
  - `category/**.html`, `category/**/**.html`
  - `index.html`, `assets/**`
  - `.github/workflows/pages-maintenance.yml`

**Pipeline Steps**:
1. **Checkout**: Repository checkout
2. **Generate sitemap.xml**: 
   - Scans all HTML files
   - Excludes assets and 404.html
   - Creates XML sitemap for SEO
3. **Verify Directory Structure**: Ensures `category/` exists
4. **Rebuild Category Indexes**:
   - Processes 7 category directories
   - Finds HTML files sorted newest-first
   - Supports both Korean date format (`2025년 8월 27일`) and ISO format (`2025-08-27`)
   - Updates post lists in index.html files using AWK
5. **Commit & Push**: Updates `sitemap.xml` and category indexes

---

### 7. 🔄 tistory-backup.yml — Tistory Blog Backup

**Purpose**: Periodically backs up Tistory blog posts via RSS feed.

**Triggers**:
- Schedule: Every 6 hours (`0 */6 * * *`)
- Manual workflow dispatch

**Pipeline Steps**:
1. **Checkout**: Repository checkout
2. **Python Setup**: Python 3.11
3. **Dependencies**: requests, feedparser
4. **Execute**: `python scripts/tistory_backup.py`
   - Parses RSS feed from `https://dtslib1k.tistory.com/rss`
   - Downloads full HTML for each blog post
   - Saves to `backup/raw/` with format `YYYY-MM-DD-title.html`
   - Skips already existing files
5. **Commit & Push**: Updates `backup/raw/`

**Key Script**: `scripts/tistory_backup.py`
- `clean_filename()`: Sanitizes titles for filesystem
- Downloads with User-Agent header
- 30-second timeout per request

---

## 🔄 Workflow Dependency Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        WORKFLOW DEPENDENCY FLOW                     │
└─────────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │   tistory-backup.yml │
                    │   (Every 6 hours)    │
                    └──────────┬───────────┘
                               │ Creates: backup/raw/*.html
                               ▼
                    ┌──────────────────────┐
                    │    mobilize.yml      │
                    │ (Every 6h +30min)    │
                    └──────────┬───────────┘
                               │ Creates: archive/*.html (clean, mobile)
                               ▼
                    ┌──────────────────────┐
                    │  build-textstory.yml │
                    │   (Every 3 hours)    │
                    └──────────┬───────────┘
                               │ Creates: assets/manifest.json
                               │          archive/*.html (mirrored)
                               ▼
    ┌───────────────────────────────────────────────────────┐
    │                                                       │
    │  ┌──────────────────────┐    ┌──────────────────────┐ │
    │  │  category-index.yml  │───▶│   obsidian-sync.yml  │ │
    │  │  (On category push)  │    │  (Triggered + 3h)    │ │
    │  └──────────────────────┘    └──────────────────────┘ │
    │           │                           │               │
    │           │ Updates:                  │ Creates:      │
    │           │ • assets/home.json        │ • html_raw/   │
    │           │ • category/*/index.html   │ • html_md/    │
    │           │                           │ • 보고서.md    │
    └───────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │pages-maintenance.yml │
                    │   (On HTML push)     │
                    └──────────────────────┘
                               │ Creates: sitemap.xml
                               │          category/*/index.html updates

              ┌──────────────────────┐
              │ obsidian-backup.yml  │
              │  (On category push)  │
              └──────────────────────┘
                         │ Syncs: category/ → _obsidian/_imports/
```

---

## 🧠 Technical Stack Summary

| Component | Technology |
|-----------|------------|
| **Frontend** | HTML5, CSS3, JavaScript ES6+, Three.js |
| **Backend** | None (pure static site) |
| **Automation** | GitHub Actions, Python 3.11 |
| **Deployment** | GitHub Pages |
| **Domain** | Custom domain via CNAME (parksy.kr) |
| **PWA** | Service Worker + Web App Manifest |
| **Build Tools** | Python scripts (beautifulsoup4, lxml, requests, feedparser, pandoc) |

---

## 📊 Current Statistics

- **Total Workflows**: 7 GitHub Actions
- **Automation Scripts**: 8 Python scripts
- **Category Content**: 51 HTML files across 7 personas
- **Archive Content**: 24 chronological HTML files
- **Automation Frequency**: 
  - Tistory backup: Every 6 hours
  - Archive mobilization: Every 6 hours (+30 min offset)
  - TextStory automation: Every 3 hours
  - Obsidian sync: Every 3 hours + on-demand

---

## 🎯 Design Philosophy

1. **Compress → Structure → Publish**: Voice-first capture → AI condensation → human structuring → instant publish
2. **Liberal Arts × Engineering Equilibrium**: Philosophy, aesthetics, and code as equal propulsion systems
3. **Strict Persona Modularity**: No overlap, no competition — only precise interlocking
4. **Zero Dependencies**: Pure HTML + CSS + vanilla JS, no build step, no frameworks, no backend
5. **Mobile-First**: Optimized for flagship Android reading experience

---

## 🔗 Related Documentation

- [README.md](README.md) — Project overview and mission
- [구조평가보고서.md](구조평가보고서.md) — Repository structure evaluation report (Korean)
- [backup/README.md](backup/README.md) — Backup system documentation
- [backup/TRIGGER_AUTOMATION.md](backup/TRIGGER_AUTOMATION.md) — Automation trigger documentation

---

*Generated for UncleParksy repository documentation*  
*Made with disciplined joy by Parksy and his silent AI triumvirate.*
