---
title: "GitHub CLI 명령어 가이드"
slug: "github-cli-commands"
last_updated: 2025-12-10
category: "guides"
tags: ["github-cli", "commands", "workflow", "pr"]
summary: "GitHub CLI 원라이너 명령어 모음 (워크플로우, PR, 일괄 작업)"
---

# 🛠 GitHub CLI 명령어 가이드

> 🎯 목적: 자주 사용하는 GitHub CLI 원라이너 명령어 모음

---

## 1️⃣ 워크플로우 실행

### 수동 트리거
```bash
# 특정 워크플로우 실행
gh workflow run category-index.yml
gh workflow run obsidian-sync.yml
gh workflow run tistory-backup.yml

# 워크플로우 목록 확인
gh workflow list

# 실행 상태 확인
gh run list --workflow=category-index.yml
```

---

## 2️⃣ PR 관리

### PR 목록 확인
```bash
gh pr list --state open
gh pr list --state all
```

### 개별 PR 닫기
```bash
gh pr close <PR번호> --comment "정리 완료"
```

### 모든 열린 PR 일괄 닫기
```bash
gh pr list --state open --json number --template '{{range .}}{{.number}}{{"\n"}}{{end}}' | xargs -I {} gh pr close {} --comment "일괄 정리"
```

---

## 3️⃣ Issue 관리

```bash
# 이슈 목록
gh issue list

# 이슈 생성
gh issue create --title "제목" --body "내용"

# 이슈 닫기
gh issue close <번호>
```

---

## 4️⃣ 레포지토리 작업

```bash
# 클론
gh repo clone dtslib1979/UncleParksy

# 브라우저에서 열기
gh repo view --web

# 레포 정보
gh repo view
```

---

## 5️⃣ Actions 로그 확인

```bash
# 최근 실행 목록
gh run list

# 특정 실행 로그
gh run view <run-id> --log

# 실패한 실행만 보기
gh run list --status failure
```

---

## 6️⃣ 자주 쓰는 조합

### 워크플로우 실행 후 상태 확인
```bash
gh workflow run category-index.yml && sleep 5 && gh run list --limit 1
```

### PR 머지 후 삭제
```bash
gh pr merge <번호> --squash --delete-branch
```

---

*🌊 Deep Sea Librarian | CLI Guide*
