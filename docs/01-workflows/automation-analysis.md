---
title: "자동화 파이프라인 충돌 분석"
slug: "automation-analysis"
last_updated: 2025-12-10
category: "workflows"
tags: ["automation", "workflows", "conflict-analysis", "overwrite-map"]
summary: "워크플로우별 쓰기 주체, 덮어쓰기 그래프, 파이프라인 충돌 분석"
---

# 🔍 자동화 파이프라인 충돌 분석

> 🎯 핵심 질문: "상위 자동화가 내 작업을 덮어쓰고 있는가?"  
> 📋 답변: **NO** — 광역 덮어쓰기 없음, 파이프라인 정상 분리

---

## 1️⃣ 파일별 쓰기 주체 (Writers Table)

| Target File | Writer | Trigger | Priority |
|-------------|--------|---------|----------|
| `assets/home.json` | `category-index.yml` → `generate_category_index.py` | push `category/**/*.html` | HIGH |
| `category/*/index.html` | `pages-maintenance.yml` (AWK) | push `category/**.html` | HIGH |
| `assets/manifest.json` | `build-textstory.yml` → `auto_install.py` | schedule 3h | CRITICAL |
| `archive/*.html` | `build-textstory.yml` / `mobilize.yml` | schedule 3h/6h | MEDIUM |
| `sitemap.xml` | `pages-maintenance.yml` | push | LOW |
| `_obsidian/_imports/` | `obsidian-sync.yml` / `obsidian-backup.yml` | schedule 3h / push | LOW |
| `backup/raw/*.html` | `tistory-backup.yml` | schedule 6h | LOW |

---

## 2️⃣ Push 트리거 실행 흐름

```
category/<Persona>/new-page.html 추가
              │
              ▼
      ┌───────────────────────────────────┐
      │  3개 워크플로우 동시 트리거       │
      └───────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
category   pages-     obsidian-
-index    maintenance   backup
  .yml       .yml        .yml
    │         │          │
    ▼         ▼          ▼
home.json  index.html  _obsidian/
(카운트)   (리스트)    (백업)
    │         │          │
    └─────────┴──────────┘
              │
    ✅ 서로 다른 파일 → 충돌 없음
```

---

## 3️⃣ Schedule 기반 자동화

| 주기 | 워크플로우 | 출력 |
|------|-----------|------|
| 3시간 | `build-textstory.yml` | `archive/*.html`, `assets/manifest.json` |
| 3시간 | `obsidian-sync.yml` | `_obsidian/_imports/` |
| 6시간 | `mobilize.yml` | `archive/*.html` |
| 6시간 | `tistory-backup.yml` | `backup/raw/*.html` |

---

## 4️⃣ 충돌 분석 결과

| 파일 | 문제 여부 | 설명 |
|-----|---------|------|
| `category/*/index.html` | ✅ 정상 | push마다 최신 HTML 목록으로 갱신 |
| `assets/home.json` | ✅ 정상 | 카테고리별 파일 개수만 저장 |
| `assets/manifest.json` | ⚠️ 주의 | `archive/` 폴더만 스캔 (category 무시) |

---

## 5️⃣ 트러블슈팅

### 카운트 미갱신
```bash
gh workflow run category-index.yml
```

### index.html 리스트 비어있음
```bash
grep -n 'post-list' category/<Persona>/index.html
```

### manifest.json에 파일 없음
- 원인: `assets/manifest.json`은 `archive/`만 스캔
- 해결: `category/*/manifest.json` 사용

---

*🌊 Deep Sea Librarian | Workflow Analysis*
