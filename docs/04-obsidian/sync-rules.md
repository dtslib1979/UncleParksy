---
title: "GitHub-Obsidian 동기화 규칙"
slug: "sync-rules"
last_updated: 2025-12-10
category: "obsidian"
tags: ["obsidian", "sync", "github", "automation"]
summary: "GitHub 레포와 Obsidian Vault 간 동기화 규칙 및 구조"
---

# 🔮 GitHub-Obsidian 동기화 규칙

> 🎯 목표: GitHub 콘텐츠를 Obsidian에서 편집·활용

---

## 📊 동기화 개요

| 항목 | 값 |
|------|-----|
| 방향 | GitHub → Obsidian (단방향) |
| 주기 | 3시간마다 + push 트리거 |
| 일일 실행 | 8회 + α |
| 워크플로우 | `obsidian-sync.yml` |

---

## 🗂 동기화 구조

### GitHub 소스
```
category/
├── Philosopher-Parksy/*.html
├── Technician-Parksy/*.html
└── ...
```

### Obsidian 출력
```
_obsidian/_imports/
├── category/      # HTML 원본 복사
├── html_raw/      # RAW HTML
└── html_md/       # Markdown 변환 (pandoc)
```

---

## 🔄 데이터 흐름

```
category/*.html
       │
       ▼ rsync
_obsidian/_imports/category/
       │
       ▼ pandoc (HTML → MD)
_obsidian/_imports/html_md/
       │
       ▼ git push
GitHub Repository
       │
       ▼ git pull (로컬)
Obsidian Vault (로컬 PC)
```

---

## 🖥 로컬 연동 설정

### 현재 경로

| 항목 | 경로 |
|------|------|
| 로컬 레포 | `C:\Users\dtsli\UncleParksy_Local\UncleParksy` |
| Obsidian 볼트 | `C:\Users\dtsli\Documents\Obsidian Vault` |
| GitHub 백업 | `📥 GitHub 백업\UncleParksy\` |

### 동기화 명령

```powershell
cd C:\Users\dtsli\UncleParksy_Local\UncleParksy
git pull origin main
```

---

## ⚠️ 주의사항

1. **단방향 동기화**: Obsidian에서 수정해도 GitHub에 반영 안 됨
2. **충돌 방지**: 로컬에서 `_obsidian/` 폴더 직접 수정 금지
3. **변환 손실**: pandoc 변환 시 일부 HTML 태그 손실 가능

---

## 🔧 수동 트리거

```bash
gh workflow run obsidian-sync.yml
```

---

*🌊 Deep Sea Librarian | Obsidian Document*
