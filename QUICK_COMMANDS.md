# GitHub CLI 원라이너 명령어들 (GitHub CLI One-liner Commands)

## 모든 열린 PR 한 번에 닫기 (Close all open PRs at once)

### 기본 명령어 (Basic command)
```bash
gh pr list --state open --json number --template '{{range .}}{{.number}}{{"\n"}}{{end}}' | xargs -I {} gh pr close {} --comment "일괄 정리: 모든 열린 PR 삭제"
```

### 개별 실행 (Individual execution)
```bash
# 먼저 목록 확인
gh pr list --state open

# 개별로 닫기 (주요 PR 번호들)
gh pr close 24 --comment "일괄 정리" && \
gh pr close 23 --comment "일괄 정리" && \
gh pr close 21 --comment "일괄 정리" && \
gh pr close 18 --comment "일괄 정리" && \
gh pr close 17 --comment "일괄 정리" && \
gh pr close 16 --comment "일괄 정리" && \
gh pr close 15 --comment "일괄 정리" && \
gh pr close 14 --comment "일괄 정리" && \
gh pr close 13 --comment "일괄 정리" && \
gh pr close 12 --comment "일괄 정리" && \
gh pr close 4 --comment "일괄 정리" && \
gh pr close 3 --comment "일괄 정리" && \
gh pr close 29 --comment "일괄 정리"
```

### 확인 명령어 (Verification commands)
```bash
# 열린 PR 개수 확인
gh pr list --state open --json number --template '{{len .}}'

# 열린 PR이 없으면 "0"이 출력됨
```

## 사용 전 준비사항 (Prerequisites)

1. GitHub CLI 설치:
   ```bash
   # macOS
   brew install gh
   
   # Ubuntu/Debian
   sudo apt update && sudo apt install gh
   
   # Windows (using Chocolatey)
   choco install gh
   ```

2. 인증:
   ```bash
   gh auth login
   ```

3. 저장소로 이동:
   ```bash
   cd /path/to/UncleParksy
   ```

## 실행 순서 (Execution order)

1. 먼저 현재 상태 확인:
   ```bash
   gh pr list --state open
   ```

2. 스크립트 실행 또는 원라이너 사용

3. 완료 후 확인:
   ```bash
   gh pr list --state open
   ```