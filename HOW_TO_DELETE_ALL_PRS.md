# 🧹 PR 일괄 삭제 완전 가이드

> **UncleParksy 저장소의 모든 열린 Pull Request를 정리하는 완벽한 솔루션**

## 🎯 빠른 시작 (5초 안에!)

```bash
# 저장소로 이동
cd /path/to/UncleParksy

# 스크립트 실행 (가장 쉬운 방법)
./quick_close_prs.sh
```

**끝!** 이게 전부입니다. 🎉

---

## 📚 상세 가이드

### 제공되는 도구

| 파일 | 용도 | 추천 대상 |
|------|------|-----------|
| `quick_close_prs.sh` | 빠르고 간단한 PR 삭제 | ⭐ **초보자** |
| `close_all_prs.sh` | 상세한 진행 상황 표시 | 중급자 |
| `PR_CLEANUP_README.md` | 완전한 사용 설명서 | 모든 사용자 |
| `PR_CLEANUP_GUIDE.md` | 상세 매뉴얼 | 고급 사용자 |
| `QUICK_COMMANDS.md` | CLI 원라이너 명령어 | 전문가 |

## 🚀 실행 방법 (3가지)

### 방법 1: 빠른 스크립트 ⭐ 추천!

```bash
./quick_close_prs.sh
```

**장점:**
- 간단하고 빠름
- 자동으로 모든 체크 수행
- 깔끔한 진행 상황 표시

### 방법 2: 상세 스크립트

```bash
./close_all_prs.sh
```

**장점:**
- 더 상세한 진행 정보
- 개별 PR 성공/실패 카운트
- 수동 확인 프롬프트 포함

### 방법 3: 원라이너 명령어

```bash
gh pr list --state open --json number --template '{{range .}}{{.number}}{{"\n"}}{{end}}' | xargs -I {} gh pr close {} --comment "일괄 정리"
```

**장점:**
- 스크립트 없이 직접 실행
- 커스터마이징 가능

## 📋 사전 준비 체크리스트

실행 전에 다음을 확인하세요:

- [ ] **GitHub CLI 설치됨** (`gh --version`)
- [ ] **인증 완료** (`gh auth status`)
- [ ] **올바른 저장소** (`pwd` 확인)
- [ ] **중요 PR 백업** (필요시)

### GitHub CLI 설치

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Windows (Chocolatey)
choco install gh
```

### 인증

```bash
gh auth login
```

## 🎬 실행 예시

```bash
$ cd /home/user/UncleParksy
$ ./quick_close_prs.sh

🚀 빠른 PR 정리 모드 (Quick PR Cleanup Mode)

✅ GitHub CLI 준비 완료

📊 현재 열린 PR: 13개

📋 PR 목록:
  #29 - [WIP] 지금 오픈되고 클로즈되지 않는 레포지토리 PR 모두 삭제
  #24 - Roll back category/system-configuration/index.html
  #23 - Fix: Prevent automation from overwriting
  ...

⚠️  모든 PR을 닫으시겠습니까? (y/N): y

🔄 PR 닫는 중...

⏳ PR #29 처리 중...
✅ PR #29 닫힘
⏳ PR #24 처리 중...
✅ PR #24 닫힘
...

✨ 작업 완료!

🎉 모든 PR이 성공적으로 닫혔습니다!
```

## 🔍 실행 후 확인

### 모든 PR이 닫혔나요?

```bash
gh pr list --state open
```

출력이 비어있으면 성공! ✨

### 닫힌 PR 목록 보기

```bash
gh pr list --state closed --limit 20
```

## ❓ 문제 해결

### "gh: command not found"

```bash
# GitHub CLI 설치 필요
brew install gh  # macOS
```

### "authentication required"

```bash
gh auth login
gh auth status  # 확인
```

### 스크립트 권한 오류

```bash
chmod +x quick_close_prs.sh
chmod +x close_all_prs.sh
```

### 일부 PR이 닫히지 않음

```bash
# 남은 PR 확인
gh pr list --state open

# 수동으로 닫기
gh pr close <번호> --comment "일괄 정리"
```

## 📖 추가 문서

- **[PR_CLEANUP_README.md](./PR_CLEANUP_README.md)** - 전체 사용 설명서
- **[PR_CLEANUP_GUIDE.md](./PR_CLEANUP_GUIDE.md)** - 상세 가이드
- **[QUICK_COMMANDS.md](./QUICK_COMMANDS.md)** - 원라이너 명령어

## 🛡️ 안전 수칙

1. ✅ **백업 먼저**: 중요한 PR 내용 저장
2. ✅ **검토 필수**: 병합 필요한 PR 확인
3. ✅ **테스트 실행**: 작은 저장소에서 먼저 테스트
4. ✅ **로그 저장**: 실행 결과 기록

## 💡 유용한 팁

```bash
# PR 개수만 빠르게 확인
gh pr list --state open --json number --template '{{len .}}'

# Draft PR만 보기
gh pr list --state open --json isDraft,number,title

# 특정 PR 상세 정보
gh pr view 29
```

## 🎯 이 가이드의 목표

모든 열린 PR을 **안전하고**, **빠르고**, **확실하게** 정리하는 것!

---

**📅 최종 업데이트**: 2025-11-24  
**👨‍💻 작성**: UncleParksy Team  
**🤖 AI 협업**: Claude AI

**🌟 즐거운 PR 정리 되세요!**
