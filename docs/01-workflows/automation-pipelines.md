---
title: "자동화 파이프라인 전체 현황"
slug: "automation-pipelines"
last_updated: 2025-12-10
category: "workflows"
tags: ["github-actions", "automation", "ci-cd", "workflows"]
summary: "UncleParksy의 7개 GitHub Actions 워크플로우 상세 설명"
---

# ⚙️ 자동화 파이프라인 전체 현황

> 🔄 수동 작업 비율: **0%**  
> 모든 콘텐츠 처리는 자동화됨

---

## 📊 워크플로우 요약

| 워크플로우 | 주기 | 일일 실행 | 상태 |
|-----------|------|----------|------|
| `tistory-backup.yml` | 6시간 | 4회 | ✅ 활성 |
| `obsidian-sync.yml` | 3시간 | 8회 | ✅ 활성 |
| `obsidian-backup.yml` | push | - | ✅ 활성 |
| `category-index.yml` | push | - | ✅ 활성 |
| `pages-maintenance.yml` | push | - | ✅ 활성 |
| `build-textstory.yml` | 3시간 | 8회 | ✅ 활성 |
| `mobilize.yml` | 6시간 | 4회 | ✅ 활성 |

---

## 1️⃣ tistory-backup.yml

### 목적
Tistory 블로그 RSS를 파싱하여 HTML 백업

### 설정
```yaml
schedule: "0 */6 * * *"  # 6시간마다
trigger: workflow_dispatch
```

### 흐름
```
Tistory RSS → feedparser → backup/raw/*.html → git push
```

---

## 2️⃣ obsidian-sync.yml

### 목적
category/ 콘텐츠를 Obsidian용으로 변환·동기화

### 설정
```yaml
schedule: "0 */3 * * *"  # 3시간마다
trigger: push to category/**, workflow_dispatch
```

### 출력
```
_obsidian/_imports/
├── category/   (HTML 복사)
├── html_raw/   (원본)
└── html_md/    (Markdown 변환)
```

---

## 3️⃣ category-index.yml

### 목적
카테고리별 index.html 및 manifest.json 자동 생성

### 트리거
```yaml
push: category/**/*.html, archive/*.html
```

### 출력
- `category/*/index.html`
- `category/*/manifest.json`
- `assets/home.json`

---

## 4️⃣ pages-maintenance.yml

### 목적
sitemap.xml 생성 및 카테고리 인덱스 리빌드

### 트리거
```yaml
push: category/**/*.html, index.html
```

---

## 5️⃣ build-textstory.yml

### 목적
backup → archive 미러링, 모바일 최적화, manifest 생성

### 설정
```yaml
schedule: "0 */3 * * *"  # 3시간마다
```

---

## 6️⃣ mobilize.yml

### 목적
HTML 본문 추출 + 모바일 템플릿 적용

### 설정
```yaml
schedule: "0 */6 * * *"  # 6시간마다
```

---

## 7️⃣ obsidian-backup.yml

### 목적
category/ 변경 시 _obsidian/_imports/category/로 자동 복사

### 트리거
```yaml
push: category/**
```

---

## 🔧 수동 실행 명령어

```bash
# Tistory 백업
gh workflow run tistory-backup.yml

# Obsidian 동기화
gh workflow run obsidian-sync.yml

# 카테고리 인덱스 재생성
gh workflow run category-index.yml
```

---

*🌊 Deep Sea Librarian | Workflows Document*
