---
title: "[Archive] 자동화 분석 요약"
slug: "automation-summary-archived"
last_updated: 2025-12-10
category: "archive"
tags: ["archived", "duplicate", "automation"]
summary: "[중복] AUTOMATION_ANALYSIS.md의 요약 버전 - automation-analysis.md로 통합됨"
---

# 📋 자동화 분석 요약 (Archived)

> ⚠️ **이 문서는 보관용입니다.**  
> 현행 문서: `/docs/01-workflows/automation-analysis.md`

---

## 📌 원본 요약

### 핵심 질문
> "상위 자동화가 내 작업을 덮어쓰고 있는가?"

### 답변
**NO** — 광역 덮어쓰기 없음, 파이프라인 정상 분리

### 파이프라인 요약

| 대상 파일 | 담당 워크플로우 |
|-----------|----------------|
| `assets/home.json` | `category-index.yml` |
| `category/*/index.html` | `pages-maintenance.yml` |
| `assets/manifest.json` | `build-textstory.yml` |

---

*🗄 Archived: 2025-12-10 | 원본 통합 완료*
