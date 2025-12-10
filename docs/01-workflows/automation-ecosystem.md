---
title: "외부 생태계 연동 현황"
slug: "automation-ecosystem"
last_updated: 2025-12-10
category: "workflows"
tags: ["tistory", "obsidian", "sync", "rss", "ecosystem"]
summary: "Tistory↔GitHub↔Obsidian 3자 연동 구조 및 실행 주기"
---

# 🔄 외부 생태계 연동 현황

> 🌐 3자 연동: Tistory → GitHub → Obsidian

---

## 📊 연동 요약

| 연동 | 방향 | 주기 | 상태 |
|------|------|------|------|
| Tistory → GitHub | RSS 백업 | 6시간 | ✅ 활성 |
| GitHub → Obsidian | HTML/MD 동기화 | 3시간 | ✅ 활성 |

---

## 1️⃣ Tistory RSS 백업

| 항목 | 값 |
|------|-----|
| RSS URL | `https://dtslib1k.tistory.com/rss` |
| 실행 주기 | 매 6시간 (00:00, 06:00, 12:00, 18:00 UTC) |
| 저장 경로 | `backup/raw/*.html` |
| 파일명 형식 | `YYYY-MM-DD-제목.html` |
| 워크플로우 | `tistory-backup.yml` |
| 스크립트 | `scripts/tistory_backup.py` |

### 데이터 흐름
```
Tistory Blog → RSS Feed → feedparser → backup/raw/*.html
```

---

## 2️⃣ GitHub → Obsidian 동기화

| 항목 | 값 |
|------|-----|
| 실행 주기 | 매 3시간 + push 트리거 |
| 소스 | `category/**` |
| 출력 경로 | `_obsidian/_imports/` |
| 변환 도구 | pandoc (HTML → MD) |
| 워크플로우 | `obsidian-sync.yml` |

### 출력 구조
```
_obsidian/_imports/
├── category/    # HTML 원본 복사
├── html_raw/    # RAW HTML
└── html_md/     # Markdown 변환
```

---

## 3️⃣ 전체 데이터 흐름

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Tistory   │────▶│   GitHub    │────▶│  Obsidian   │
│    Blog     │ 6h  │  Repository │ 3h  │   Vault     │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
   RSS Feed          backup/raw/        _obsidian/
                     archive/           _imports/
                     category/
```

---

## 4️⃣ 일일 실행 현황

| 워크플로우 | 주기 | 일일 실행 |
|-----------|------|----------|
| `tistory-backup.yml` | 6시간 | 4회 |
| `obsidian-sync.yml` | 3시간 | 8회 |
| `build-textstory.yml` | 3시간 | 8회 |
| `mobilize.yml` | 6시간 | 4회 |

**총 자동 실행**: 24회/일

---

## 5️⃣ 수동 트리거

```bash
# Tistory 백업 즉시 실행
gh workflow run tistory-backup.yml

# Obsidian 동기화 즉시 실행
gh workflow run obsidian-sync.yml
```

---

*🌊 Deep Sea Librarian | Ecosystem Document*
