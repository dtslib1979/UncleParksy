# PR 삭제 가이드 (Pull Request Cleanup Guide)

## 현재 상황 (Current Status)
이 저장소에는 현재 **13개의 열려있는 Pull Request**가 있습니다.

## 삭제할 PR 목록 (PRs to Delete)

### 1. **PR #29** - [WIP] 지금 오픈되고 클로즈되지 않는 레포지토리 PR 모두 삭제
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/29
- **상태**: Draft, 현재 작업 중인 PR (이 작업 완료 후 마지막에 삭제)

### 2. **PR #24** - Roll back category/system-configuration/index.html to previous version
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/24
- **상태**: Draft

### 3. **PR #23** - Fix: Prevent automation from overwriting manually edited category index.html files
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/23
- **상태**: Draft

### 4. **PR #21** - Fix YAML syntax errors in obsidian-sync.yml workflow causing consistent failures
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/21
- **상태**: Draft

### 5. **PR #18** - Implement archive-style index pages for all 6 category directories
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/18
- **상태**: Ready for review

### 6. **PR #17** - Implement automated category index pages with main homepage design
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/17
- **상태**: Ready for review

### 7. **PR #16** - Fix GitHub Pages 404 error: Add deployment workflow and missing pages
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/16
- **상태**: Draft

### 8. **PR #15** - Implement comprehensive Obsidian backup system for complete content migration
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/15
- **상태**: Draft

### 9. **PR #14** - Implement comprehensive Obsidian backup system based on existing PowerShell configuration
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/14
- **상태**: Draft

### 10. **PR #13** - Fix Obsidian backup paths to use Documents folder instead of C:\ObsidianVault
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/13
- **상태**: Draft

### 11. **PR #12** - Fix Obsidian backup paths to use user Documents directory
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/12
- **상태**: Draft

### 12. **PR #4** - Rollback previous request - restore repository to clean state
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/4
- **상태**: Draft

### 13. **PR #3** - feat: implement theme-extractor-engine - automated website theme extraction system
- **URL**: https://github.com/dtslib1979/UncleParksy/pull/3
- **상태**: Ready for review

## 삭제 방법 (How to Delete)

### 옵션 1: 웹 인터페이스를 통한 수동 삭제 (Manual deletion via web interface)

1. 각 PR 페이지로 이동
2. 페이지 하단의 "Close pull request" 버튼 클릭
3. 필요한 경우 삭제 이유 코멘트 작성
4. "Close pull request" 확인

### 옵션 2: GitHub CLI를 사용한 일괄 삭제 (Batch deletion using GitHub CLI)

```bash
# GitHub CLI 설치 후 인증
gh auth login

# 모든 열린 PR 목록 확인
gh pr list --state open

# 개별 PR 닫기
gh pr close 29 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 24 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 23 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 21 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 18 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 17 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 16 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 15 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 14 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 13 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 12 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 4 --comment "일괄 정리: 열린 PR 모두 삭제"
gh pr close 3 --comment "일괄 정리: 열린 PR 모두 삭제"
```

### 옵션 3: 스크립트를 사용한 자동화 (Automated script)

```bash
#!/bin/bash
# 모든 열린 PR을 자동으로 닫는 스크립트

PR_NUMBERS=(29 24 23 21 18 17 16 15 14 13 12 4 3)

for pr in "${PR_NUMBERS[@]}"; do
    echo "Closing PR #$pr..."
    gh pr close "$pr" --comment "일괄 정리: 모든 열린 PR 삭제"
    echo "PR #$pr closed."
done

echo "모든 PR이 닫혔습니다."
```

## 주의사항 (Important Notes)

1. **백업**: 중요한 변경사항이 포함된 PR이 있다면 먼저 백업하세요.
2. **리뷰**: 각 PR의 내용을 검토하여 병합이 필요한 것이 있는지 확인하세요.
3. **순서**: PR #29 (현재 작업 중인 PR)는 마지막에 닫으세요.
4. **브랜치 정리**: PR을 닫은 후 관련된 브랜치도 삭제할 수 있습니다.

## 완료 후 확인 (Post-cleanup verification)

삭제 완료 후 다음 명령어로 확인:
```bash
gh pr list --state open
```

결과가 비어있으면 모든 PR이 성공적으로 정리된 것입니다.