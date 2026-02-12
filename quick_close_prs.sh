#!/bin/bash

# 빠른 PR 삭제 스크립트 (Quick PR Deletion Script)
# 사용법: ./quick_close_prs.sh

echo "🚀 빠른 PR 정리 모드 (Quick PR Cleanup Mode)"
echo ""

# GitHub CLI 확인
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI가 필요합니다. 설치: https://cli.github.com/"
    exit 1
fi

# 인증 확인
if ! gh auth status &> /dev/null; then
    echo "❌ 인증 필요: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI 준비 완료"
echo ""

# 열린 PR 개수 확인
OPEN_COUNT=$(gh pr list --state open --json number --template '{{len .}}')

if [ "$OPEN_COUNT" -eq 0 ]; then
    echo "✨ 닫을 PR이 없습니다. 모두 깨끗합니다!"
    exit 0
fi

echo "📊 현재 열린 PR: ${OPEN_COUNT}개"
echo ""
echo "📋 PR 목록:"
gh pr list --state open --json number,title --template '{{range .}}  #{{.number}} - {{.title}}{{"\n"}}{{end}}'
echo ""

# 확인 요청
read -p "⚠️  모든 PR을 닫으시겠습니까? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 취소되었습니다."
    exit 1
fi

echo ""
echo "🔄 PR 닫는 중..."
echo ""

# Process substitution으로 subshell 문제 해결
while read pr; do
    echo "⏳ PR #$pr 처리 중..."
    if gh pr close "$pr" --comment "🧹 일괄 정리: 모든 열린 PR 삭제 (Bulk cleanup)" 2>/dev/null; then
        echo "✅ PR #$pr 닫힘"
    else
        echo "⚠️  PR #$pr 건너뜀 (이미 닫혔거나 오류)"
    fi
done < <(gh pr list --state open --json number --template '{{range .}}{{.number}}{{"\n"}}{{end}}')

echo ""
echo "✨ 작업 완료!"
echo ""

# 최종 확인
REMAINING=$(gh pr list --state open --json number --template '{{len .}}')
if [ "$REMAINING" -eq 0 ]; then
    echo "🎉 모든 PR이 성공적으로 닫혔습니다!"
else
    echo "⚠️  아직 ${REMAINING}개의 PR이 남아있습니다:"
    gh pr list --state open --json number,title --template '{{range .}}  #{{.number}} - {{.title}}{{"\n"}}{{end}}'
fi
