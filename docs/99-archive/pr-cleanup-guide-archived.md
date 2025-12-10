---
title: "[Archive] PR 정리 가이드"
slug: "pr-cleanup-guide-archived"
last_updated: 2025-12-10
category: "archive"
tags: ["archived", "pr", "cleanup", "historical"]
summary: "[과거 작업] 2025년 PR 일괄 정리 작업 기록"
---

# 🗑 PR 정리 가이드 (Archived)

> ⚠️ **이 문서는 과거 작업 기록입니다.**  
> 작업 완료일: 2025년

---

## 📌 작업 내용

당시 13개의 열린 PR을 일괄 정리한 기록입니다.

### 삭제된 PR 목록
- PR #29, #24, #23, #21, #18, #17, #16, #15, #14, #13, #12, #4, #3

### 사용된 명령어
```bash
gh pr list --state open --json number --template '{{range .}}{{.number}}{{"\n"}}{{end}}' | xargs -I {} gh pr close {} --comment "일괄 정리"
```

---

*🗄 Archived: 2025-12-10 | 과거 작업 기록*
