# 🧹 Pull Request 일괄 정리 가이드

> **모든 열린 PR을 한 번에 정리하는 완전한 가이드**

## 📋 목차

1. [개요](#개요)
2. [사전 준비](#사전-준비)
3. [실행 방법](#실행-방법)
4. [문제 해결](#문제-해결)

## 개요

이 가이드는 UncleParksy 저장소의 모든 열린 Pull Request를 효율적으로 정리하는 방법을 제공합니다.

### 제공되는 도구

- **🔧 close_all_prs.sh** - 자동화된 PR 삭제 스크립트
- **📖 PR_CLEANUP_GUIDE.md** - 상세 매뉴얼
- **⚡ QUICK_COMMANDS.md** - 빠른 실행 명령어

## 사전 준비

### 1. GitHub CLI 설치

#### macOS
```bash
brew install gh
```

#### Ubuntu/Debian
```bash
sudo apt update && sudo apt install gh
```

#### Windows (Chocolatey)
```bash
choco install gh
```

#### Windows (Scoop)
```bash
scoop install gh
```

### 2. GitHub CLI 인증

```bash
gh auth login
```

인증 과정에서:
1. GitHub.com 선택
2. HTTPS 선택
3. 웹 브라우저로 인증하거나 토큰 입력

### 3. 저장소 확인

```bash
cd /path/to/UncleParksy
gh repo view
```

## 실행 방법

### 방법 1: 자동화 스크립트 사용 (권장) ⭐

가장 안전하고 확실한 방법입니다.

```bash
# 스크립트에 실행 권한 부여 (이미 부여되어 있음)
chmod +x close_all_prs.sh

# 스크립트 실행
./close_all_prs.sh
```

스크립트는 다음을 수행합니다:
- ✅ GitHub CLI 설치 확인
- ✅ 인증 상태 확인
- ✅ 현재 열린 PR 목록 표시
- ✅ 사용자 확인 요청
- ✅ PR 하나씩 안전하게 닫기
- ✅ 진행 상황 표시
- ✅ 최종 결과 보고

### 방법 2: 원라이너 명령어 사용

한 줄로 모든 PR을 닫습니다:

```bash
gh pr list --state open --json number --template '{{range .}}{{.number}}{{"\n"}}{{end}}' | xargs -I {} gh pr close {} --comment "일괄 정리: 모든 열린 PR 삭제"
```

### 방법 3: 수동으로 개별 실행

```bash
# 1. 열린 PR 목록 확인
gh pr list --state open

# 2. 각 PR 번호로 하나씩 닫기
gh pr close 29 --comment "일괄 정리"
gh pr close 24 --comment "일괄 정리"
gh pr close 23 --comment "일괄 정리"
# ... 계속
```

## 실행 전 체크리스트

- [ ] GitHub CLI가 설치되어 있나요?
- [ ] `gh auth status`로 인증 확인했나요?
- [ ] 중요한 PR의 내용을 백업했나요?
- [ ] 병합이 필요한 PR은 없나요?
- [ ] UncleParksy 저장소 디렉토리에 있나요?

## 실행 후 확인

### 모든 PR이 닫혔는지 확인

```bash
gh pr list --state open
```

결과가 비어있으면 성공! 🎉

### 닫힌 PR 확인

```bash
gh pr list --state closed --limit 20
```

## 문제 해결

### ❌ "gh: command not found"

**해결책**: GitHub CLI 설치 필요
```bash
# macOS
brew install gh

# Ubuntu/Debian  
sudo apt install gh
```

### ❌ "authentication required"

**해결책**: GitHub CLI 재인증
```bash
gh auth login
gh auth status  # 확인
```

### ❌ "pull request not found"

**원인**: PR이 이미 닫혔거나 존재하지 않음  
**해결책**: 무시하고 계속 진행

### ⚠️ 스크립트가 일부 PR을 건너뜀

**원인**: 
- PR이 이미 닫힘
- PR 번호가 잘못됨
- 권한 부족

**해결책**: 
```bash
# 남아있는 PR 확인
gh pr list --state open

# 수동으로 닫기
gh pr close <PR번호> --comment "일괄 정리"
```

## 안전 수칙

1. **백업 먼저**: 중요한 변경사항이 있는 PR은 먼저 백업
2. **검토 필수**: 병합이 필요한 PR이 있는지 확인
3. **점진적 실행**: 불안하면 스크립트 대신 수동으로 하나씩
4. **로그 저장**: 실행 결과를 기록으로 남기기

## 추가 유용한 명령어

```bash
# 열린 PR 개수만 확인
gh pr list --state open --json number --template '{{len .}}'

# 특정 상태의 PR 목록
gh pr list --state all  # 모든 PR
gh pr list --state merged  # 병합된 PR만

# PR 상세 정보 보기
gh pr view <PR번호>

# Draft PR 목록
gh pr list --state open --json number,title,isDraft --template '{{range .}}{{if .isDraft}}#{{.number}} - {{.title}} [DRAFT]{{"\n"}}{{end}}{{end}}'
```

## 참고 문서

- [PR_CLEANUP_GUIDE.md](./PR_CLEANUP_GUIDE.md) - 상세 가이드
- [QUICK_COMMANDS.md](./QUICK_COMMANDS.md) - 빠른 명령어
- [GitHub CLI 공식 문서](https://cli.github.com/manual/)

---

**✨ 마지막 업데이트**: 2025-11-24  
**📝 작성자**: UncleParksy Team  
**🤖 AI 협업**: Claude AI
