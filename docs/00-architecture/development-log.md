---
title: "프로젝트 개발 일지"
slug: "development-log"
last_updated: 2025-12-10
category: "architecture"
tags: ["history", "development", "changelog", "milestones"]
summary: "UncleParksy 구축 히스토리, 워크플로우/스크립트 목록, 기술 스택"
---

# 📚 프로젝트 개발 일지

> 🎯 목적: 프로그래머가 한눈에 파악할 수 있는 구축 작업 요약

---

## 📊 프로젝트 통계

| 구분 | 항목 | 수량 |
|------|------|------|
| 🔄 GitHub Actions | 워크플로우 | 7개 |
| 🐍 Python 스크립트 | 자동화 도구 | 7개 |
| 📁 콘텐츠 카테고리 | 페르소나 | 8개 |
| 📚 아카이브 문서 | HTML 파일 | 29개 |
| 📝 카테고리 문서 | HTML 파일 | 77개 |

---

## 1️⃣ GitHub Actions (7개)

| 워크플로우 | 트리거 | 기능 |
|-----------|--------|------|
| `category-index.yml` | push | 카테고리 인덱스 생성 |
| `pages-maintenance.yml` | push | sitemap 생성, 인덱스 리빌드 |
| `obsidian-sync.yml` | 3h | GitHub → Obsidian 동기화 |
| `obsidian-backup.yml` | push | category 백업 |
| `build-textstory.yml` | 3h | 아카이브 자동화 |
| `mobilize.yml` | 6h | 모바일 최적화 |
| `tistory-backup.yml` | 6h | RSS 백업 |

---

## 2️⃣ Python 스크립트 (7개)

| 스크립트 | 입력 | 출력 |
|---------|------|------|
| `generate_category_index.py` | `category/*/*.html` | `home.json`, `index.html` |
| `generate_archive_manifest.py` | `archive/*.html` | `manifest.archive.json` |
| `auto_install.py` | `backup/*.html` | `archive/*.html` |
| `tistory_backup.py` | RSS URL | `backup/raw/*.html` |
| `clean_and_mobilize.py` | `backup/raw/` | `archive/*.html` |
| `mobilize_archive.py` | `archive/*.html` | 모바일 CSS 삽입 |
| `mirror_backup.py` | `backup/` | `archive/` |

---

## 3️⃣ 개발 타임라인

| Phase | 시기 | 작업 | 상태 |
|-------|------|------|------|
| 1 | 2025-08 | Codex 시스템 (index.html) | ✅ |
| 2 | 2025-08 | 8개 페르소나 구조 | ✅ |
| 3 | 2025-08 | Tistory RSS 백업 | ✅ |
| 4 | 2025-09 | 모바일 최적화 | ✅ |
| 5 | 2025-09 | Obsidian 동기화 | ✅ |
| 6 | 2025-09 | 완전 자동화 CI | ✅ |
| 7 | 2025-11 | 매니페스트 시스템 | ✅ |
| 8 | 2025-12 | Deep Sea 문서관 | ✅ |

---

## 4️⃣ 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | HTML5, CSS3, JS ES6+, Three.js |
| Backend | Python 3.11, BeautifulSoup, feedparser |
| CI/CD | GitHub Actions |
| Hosting | GitHub Pages |
| Domain | parksy.kr |

---

## 5️⃣ 의존성

```
requests==2.31.0
feedparser==6.0.10
beautifulsoup4
lxml
pandoc (apt)
```

---

*🌊 Deep Sea Librarian | Development History*
