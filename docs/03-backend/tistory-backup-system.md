---
title: "Tistory 백업 시스템"
slug: "tistory-backup-system"
last_updated: 2025-12-10
category: "backend"
tags: ["tistory", "backup", "rss", "archive"]
summary: "Tistory 블로그 자동 백업 시스템 구조 및 설정"
---

# 💾 Tistory 백업 시스템

> 🎯 목적: Tistory 블로그 콘텐츠 자동 백업 및 아카이브

---

## 📊 시스템 개요

| 항목 | 값 |
|------|-----|
| RSS URL | `https://dtslib1k.tistory.com/rss` |
| 실행 주기 | 매 6시간 (4회/일) |
| 저장 경로 | `backup/raw/*.html` |
| 파일명 형식 | `YYYY-MM-DD-제목.html` |
| 워크플로우 | `tistory-backup.yml` |
| 스크립트 | `scripts/tistory_backup.py` |

---

## 🔄 데이터 흐름

```
Tistory Blog
    │
    ▼ RSS Feed
feedparser (Python)
    │
    ▼ HTML 다운로드
backup/raw/*.html
    │
    ▼ clean_and_mobilize.py
archive/*.html (정제본)
    │
    ▼ generate_archive_manifest.py
assets/manifest.archive.json
```

---

## 📁 디렉토리 구조

```
backup/
├── raw/                    # Tistory RSS 원본
│   ├── 2025-08-27-글1.html
│   └── 2025-08-28-글2.html
└── simple-index-files/     # 인덱스 템플릿

archive/                    # 정제된 아카이브
├── 2025-08-27-글1.html
└── 2025-08-28-글2.html
```

---

## ⚙️ 워크플로우 설정

### tistory-backup.yml
```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # 6시간마다
  workflow_dispatch:        # 수동 실행

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install requests feedparser
      - run: python scripts/tistory_backup.py
      - run: git add backup/ && git commit -m "auto: tistory backup" && git push
```

---

## 🛠 수동 실행

```bash
# GitHub CLI
gh workflow run tistory-backup.yml

# 로컬 실행
python scripts/tistory_backup.py
```

---

## 📋 현재 상태

- ✅ 백업 활성화
- ✅ 아카이브 연동
- ✅ 매니페스트 자동 생성

---

*🌊 Deep Sea Librarian | Backend Document*
