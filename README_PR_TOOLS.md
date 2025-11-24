# 📦 PR 삭제 도구 패키지

> **UncleParksy 저장소의 모든 열린 Pull Request를 한 번에 정리하는 완전한 솔루션**

## 🚀 5초 안에 시작하기

```bash
./quick_close_prs.sh
```

그게 전부입니다! 🎉

---

## 📋 패키지 내용물

### 🔧 실행 스크립트 (3개)

| 파일 | 난이도 | 설명 |
|------|--------|------|
| `quick_close_prs.sh` | ⭐ 초급 | 빠르고 간단한 PR 삭제 |
| `close_all_prs.sh` | ⭐⭐ 중급 | 상세한 진행 상황 표시 |
| `verify_pr_tools.sh` | 🔍 검증 | 도구 설치 및 설정 확인 |

### 📖 사용 설명서 (4개)

| 파일 | 대상 | 설명 |
|------|------|------|
| `README_PR_TOOLS.md` | 📌 모든 사용자 | **시작 여기서!** 전체 개요 |
| `HOW_TO_DELETE_ALL_PRS.md` | ⚡ 빠른 사용 | 5초 시작 가이드 |
| `PR_CLEANUP_README.md` | 📚 완전 가이드 | 전체 사용 설명서 |
| `PR_CLEANUP_GUIDE.md` | 🎓 상세 매뉴얼 | 개별 PR 정보 포함 |
| `QUICK_COMMANDS.md` | 💻 전문가 | CLI 원라이너 명령어 |

---

## 🎯 사용 시나리오별 가이드

### 시나리오 1: 처음 사용하는 초보자

```bash
# 1단계: 도구 확인
./verify_pr_tools.sh

# 2단계: 필요시 GitHub CLI 설치 및 인증
gh auth login

# 3단계: PR 삭제 실행
./quick_close_prs.sh

# 완료! ✨
```

**추천 문서**: `HOW_TO_DELETE_ALL_PRS.md`

### 시나리오 2: 상세한 진행 상황을 보고 싶은 사용자

```bash
./close_all_prs.sh
```

이 스크립트는:
- 각 PR의 성공/실패 상태 표시
- 최종 통계 리포트 제공
- 더 많은 확인 단계 포함

**추천 문서**: `PR_CLEANUP_README.md`

### 시나리오 3: 명령줄을 직접 사용하고 싶은 전문가

```bash
# 원라이너로 실행
gh pr list --state open --json number --template '{{range .}}{{.number}}{{"\n"}}{{end}}' | xargs -I {} gh pr close {}
```

**추천 문서**: `QUICK_COMMANDS.md`

---

## ✅ 시작하기 전 체크리스트

실행 전에 다음을 확인하세요:

- [ ] GitHub CLI 설치됨 (`gh --version`)
- [ ] GitHub CLI 인증 완료 (`gh auth status`)
- [ ] 올바른 저장소 디렉토리 (`pwd` 확인)
- [ ] 중요한 PR 백업 완료 (필요시)
- [ ] 병합이 필요한 PR 없음 (확인 완료)

**자동 확인하기:**
```bash
./verify_pr_tools.sh
```

---

## 🎬 실행 예시

### 빠른 모드 (quick_close_prs.sh)

```bash
$ ./quick_close_prs.sh

🚀 빠른 PR 정리 모드 (Quick PR Cleanup Mode)

✅ GitHub CLI 준비 완료

📊 현재 열린 PR: 13개

📋 PR 목록:
  #29 - [WIP] PR 삭제
  #24 - Roll back
  #23 - Fix automation
  ...

⚠️  모든 PR을 닫으시겠습니까? (y/N): y

🔄 PR 닫는 중...
✅ PR #29 닫힘
✅ PR #24 닫힘
...

🎉 모든 PR이 성공적으로 닫혔습니다!
```

---

## 🔍 문제 해결

### ❌ GitHub CLI가 없다고 나옵니다

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Windows
choco install gh
```

### ❌ 인증이 필요하다고 나옵니다

```bash
gh auth login
```

그런 다음 화면의 지시를 따라 인증하세요.

### ❌ 스크립트 실행 권한 오류

```bash
chmod +x quick_close_prs.sh
chmod +x close_all_prs.sh
chmod +x verify_pr_tools.sh
```

### ⚠️ 일부 PR만 닫혔습니다

```bash
# 남은 PR 확인
gh pr list --state open

# 수동으로 닫기
gh pr close <PR번호> --comment "일괄 정리"
```

---

## 📚 문서 읽는 순서

1. **📌 README_PR_TOOLS.md** (이 파일) - 전체 개요
2. **⚡ HOW_TO_DELETE_ALL_PRS.md** - 빠른 시작
3. **📚 PR_CLEANUP_README.md** - 완전한 가이드
4. **🎓 PR_CLEANUP_GUIDE.md** - 상세 매뉴얼
5. **💻 QUICK_COMMANDS.md** - 고급 명령어

---

## 🎯 목표

**모든 열린 PR을 안전하고, 빠르고, 확실하게 정리하기!**

---

## 🛡️ 안전 원칙

1. ✅ **백업 먼저**: 중요한 변경사항 저장
2. ✅ **검토 필수**: 병합 필요 여부 확인
3. ✅ **확인 과정**: 스크립트가 실행 전 확인 요청
4. ✅ **오류 처리**: 실패해도 안전하게 계속 진행

---

## 📊 통계

- **스크립트**: 3개
- **문서**: 5개
- **지원 언어**: 한국어/영어
- **필수 도구**: GitHub CLI (gh)
- **실행 시간**: 약 1-2분 (PR 개수에 따라)

---

## 💡 추가 팁

```bash
# PR 개수만 확인
gh pr list --state open --json number --template '{{len .}}'

# Draft PR만 보기
gh pr list --state open --json isDraft,number,title

# 닫힌 PR 최근 10개 보기
gh pr list --state closed --limit 10
```

---

## 🤝 도움이 필요하신가요?

1. 먼저 `./verify_pr_tools.sh` 실행
2. 관련 문서 확인
3. 오류 메시지 복사하여 이슈 생성

---

## 📅 버전 정보

- **버전**: 1.0.0
- **최종 업데이트**: 2025-11-24
- **작성**: UncleParksy Team
- **AI 협업**: Claude AI

---

**🌟 성공적인 PR 정리를 기원합니다!**

_Made with ❤️ by 작가지망생 박씨 & Claude AI_
