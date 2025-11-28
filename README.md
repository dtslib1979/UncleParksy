```markdown
# 📚 AI Creator Liberal Arts Codex — UncleParksy

> **One single HTML file that functions as a personal operating system  
> for the 21st-century AI-native creator.**

This repository is the official front door to Parksy World —  
a meticulously handcrafted, mobile-first, zero-dependency **Codex**  
that serves as both gateway and table of contents to an entire multi-persona creative universe.

`index.html` is not a website.  
It is the **cover of a living digital grimoire** — a book you scroll infinitely,  
rather than a site you navigate with menus.

---

## ✨ Mission of This Repository

- Serve as the canonical entrypoint (`uncleparksy.github.io`)
- Present every creative persona as a distinct **Chapter of Wisdom**
- Seamlessly route visitors into dedicated category folders
- Establish a permanent, elegant, creator-OS aesthetic identity
- Prove that an entire lifework can be orchestrated from **one HTML file**

Deliberately constrained to:
- Pure HTML + CSS + vanilla JS
- No build step, no frameworks, no backend
- Optimized for flagship Android reading experience (Galaxy S25 Ultra et al.)
- Built by and for creators who treat AI as co-pilot, not crutch

---

## 🧠 The 8-Chapter Liberal Arts Model

Eight disciplines. Eight personas. Eight autonomous yet interlocked worlds.

| Chapter                    | Persona              | Folder Path                          | Core Domain                              |
|----------------------------|----------------------|--------------------------------------|------------------------------------------|
| Philosopher-Parksy         | Essayist / Theorist  | `/category/Philosopher-Parksy/`      | Long-form thought, Korean Merit Theory   |
| Blogger-Parksy             | PWA Alchemist        | `/category/Blogger-Parksy/`          | Prompt engines, full-stack HTML labs     |
| Visualizer-Parksy          | Diagram Shaman       | `/category/Visualizer-Parksy/`       | Systems mapping, sketch-note metaphysics |
| Musician-Parksy            | Sonic Architect      | `/category/Musician-Parksy/`         | Emotion modeling, cinematic cue design   |
| Technician-Parksy          | Device Whisperer     | `/category/Technician-Parksy/`       | Keyboard rituals, tablet workflows       |
| Orbit-Log                  | Life Archivist       | `/category/Orbit-Log/`               | Seasonal logs, meta-reflections          |
| Protocol-Parksy            | System Designer      | `/category/Protocol-Parksy/`         | Reproducible workflows, LLM constitutions|
| All Archives · KR TextStory| Historian            | `/archive/`                          | Chronological master archive             |

The Codex renders these as tactile chapter cards with live file counters, custom icons, and subtle atmospheric animation.

---

## 🏛 Philosophical Foundation

Three unbreakable pillars:

1. **Compress → Structure → Publish**  
   Voice-first capture → AI condensation → human structuring → instant publish.

2. **Liberal Arts × Engineering Equilibrium**  
   Philosophy, aesthetics, and code are equal propulsion systems.

3. **Strict Persona Modularity**  
   No overlap, no competition — only precise interlocking.

---

## 🧩 Technical Essence of index.html

- Parchment-themed minimalist UI with book-cover hero
- Eight interactive chapter cards
- Gentle Three.js floating glyphs (respecting `prefers-reduced-motion`)
- Optional ambient BGM with one-tap toggle
- Live folder counters via GitHub Contents API → graceful fallback to `assets/home.json`
- Fully offline-capable
- Print-optimized (turns into a beautiful booklet)
- Semantic HTML + focused keyboard navigation + skip link

---

## 📂 Repository Structure

```
UncleParksy/
├── index.html                # The entire Codex (~720 lines of self-contained magic)
├── assets/
│   ├── icons/                # Hand-drawn SVG chapter icons
│   ├── audio/                # Looped ambient BGM
│   └── home.json             # Static fallback for file counts
├── category/
│   ├── Philosopher-Parksy/
│   ├── Blogger-Parksy/
│   ├── Visualizer-Parksy/
│   ├── Musician-Parksy/
│   ├── Technician-Parksy/
│   ├── Orbit-Log/
│   └── Protocol-Parksy/
├── archive/                  # Complete chronological vault
├── backup/
└── .github/
```

---

## 🧪 Local Development

```bash
git clone https://github.com/UncleParksy/UncleParksy.git
cd UncleParksy
python -m http.server 8000   # or any static server
```

→ http://localhost:8000

Zero dependencies. Instant.

---

## 🧬 Content Ingestion Workflow

1. Decide which persona speaks  
2. Create a dated `.html` file in the matching folder  
3. Commit & push  
4. Codex auto-refreshes counts on next visitor load

Example:  
`category/Visualizer-Parksy/2025-11-28-shamanic-vector-map.html`

---

## 🤖 AI Collaboration Hierarchy (Current Stack)

- ChatGPT → High-level architecture & prose sculpting  
- Claude   → Surgical code, refactoring, systems rigor  
- Grok     → Hook crafting, cultural scanning, wit calibration  

Parksy → Final arbiter, voice, and publish trigger.

---

## 🧭 Roadmap

- [x] Codex V1 launch  
- [x] Live chapter counters  
- [x] Three.js atmospheric layer  
- [x] Mobile-first perfection  
- [ ] Rotating “Featured Chapter” hero slot  
- [ ] Optional dark parchment mode  
- [ ] One-click fork template for other multi-persona creators  

---

## 📜 License

MIT License — fork, remix, attribute.

---

## 🖊 Author

**UncleParksy (박씨)**  
EduArt Engineer · AI-Augmented Creator · Keeper of Eight Personas

> “A book is no longer bound paper.  
> A book is now a single HTML file that breathes and points to your entire universe.”

Made with disciplined joy by Parksy and his silent AI triumvirate.
