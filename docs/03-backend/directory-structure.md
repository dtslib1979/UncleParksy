---
title: "디렉토리 구조 규칙"
slug: "directory-structure"
last_updated: 2025-12-10
category: "backend"
tags: ["directory", "structure", "paths", "rules"]
summary: "UncleParksy 레포지토리의 폴더 구조와 경로 규칙"
---

# 📦 디렉토리 구조 규칙

> 🌊 모든 경로는 Source of Truth

---

## 🗂 전체 구조

```
UncleParksy/
├── .github/workflows/     # GitHub Actions (7개)
├── scripts/               # Python 자동화 (7개)
├── docs/                  # 문서관 (이 문서)
│   ├── 00-architecture/
│   ├── 01-workflows/
│   ├── 02-guides/
│   ├── 03-backend/
│   ├── 04-obsidian/
│   └── 99-archive/
├── category/              # 8개 페르소나 콘텐츠
│   ├── Philosopher-Parksy/
│   ├── Technician-Parksy/
│   ├── Visualizer-Parksy/
│   ├── Musician-Parksy/
│   ├── Protocol-Parksy/
│   ├── Blogger-Parksy/
│   ├── Orbit-Log/
│   └── Tester-Parksy/
├── archive/               # Tistory 백업 아카이브
├── backup/                # 원본 백업
│   └── raw/               # Tistory RSS 원본
├── assets/                # 정적 자원
│   ├── manifest.json
│   ├── home.json
│   └── css/, js/, icons/
├── _obsidian/             # Obsidian 동기화
│   └── _imports/
│       ├── category/
│       ├── html_raw/
│       └── html_md/
├── index.html             # 메인 Codex (777줄)
└── sw.js                  # Service Worker
```

---

## 📋 폴더별 역할

| 폴더 | 역할 | 자동화 |
|------|------|--------|
| `category/` | 페르소나별 콘텐츠 | push 시 index 자동생성 |
| `archive/` | Tistory 정제본 | mobilize.yml |
| `backup/raw/` | Tistory RSS 원본 | tistory-backup.yml |
| `assets/` | JSON 매니페스트 | category-index.yml |
| `_obsidian/_imports/` | Obsidian용 변환본 | obsidian-sync.yml |
| `docs/` | 문서관 | 수동 관리 |

---

## 🏷 파일명 규칙

### HTML 콘텐츠
```
YYYY-MM-DD-제목.html
예: 2025-12-10-system-guide.html
```

### 매니페스트
```
manifest.json     # 각 카테고리별
home.json         # 전체 카운트
```

---

## 🚫 금지 경로

| 경로 | 이유 |
|------|------|
| `node_modules/` | 불필요 |
| `.env` | 보안 |
| `*.log` | 임시 파일 |

---

*🌊 Deep Sea Librarian | Backend Document*
