#!/bin/bash

# PR 일괄 삭제 스크립트 (Bulk PR Deletion Script)
# 사용법: ./close_all_prs.sh

echo "🚨 모든 열린 PR을 닫는 작업을 시작합니다..."
echo "This script will close all open pull requests in the repository."
echo ""

# GitHub CLI가 설치되어 있는지 확인
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh)가 설치되지 않았습니다."
    echo "설치 방법: https://cli.github.com/"
    exit 1
fi

# 인증 확인
if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLI에 로그인이 필요합니다."
    echo "다음 명령어를 실행하세요: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI가 준비되었습니다."
echo ""

# 현재 열린 PR 목록 표시
echo "📋 현재 열린 PR 목록:"
gh pr list --state open --json number,title --template '{{range .}}{{printf "#%v - %v\n" .number .title}}{{end}}'
echo ""

# 사용자 확인
read -p "정말로 모든 열린 PR을 닫으시겠습니까? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 작업이 취소되었습니다."
    exit 1
fi

echo ""
echo "🔄 PR들을 닫는 중..."

# PR 번호 배열 (현재 열린 PR들)
# 주의: PR #29는 현재 작업 중인 PR이므로 마지막에 처리
PR_NUMBERS=(24 23 21 18 17 16 15 14 13 12 4 3 29)

SUCCESS_COUNT=0
FAILED_COUNT=0

for pr in "${PR_NUMBERS[@]}"; do
    echo "⏳ PR #$pr 닫는 중..."
    
    if gh pr close "$pr" --comment "🧹 일괄 정리: 모든 열린 PR 삭제 (Bulk cleanup: Closing all open PRs)" &> /dev/null; then
        echo "✅ PR #$pr 성공적으로 닫혔습니다."
        ((SUCCESS_COUNT++))
    else
        echo "❌ PR #$pr 닫기 실패 (이미 닫혔거나 존재하지 않을 수 있습니다)"
        ((FAILED_COUNT++))
    fi
    
    # API 제한 방지를 위한 짧은 대기
    sleep 1
done

echo ""
echo "📊 작업 완료:"
echo "   ✅ 성공: $SUCCESS_COUNT개"
echo "   ❌ 실패: $FAILED_COUNT개"
echo ""

# 최종 확인
echo "🔍 현재 열린 PR 확인:"
REMAINING_PRS=$(gh pr list --state open --json number --template '{{len .}}')

if [ "$REMAINING_PRS" -eq 0 ]; then
    echo "🎉 모든 PR이 성공적으로 닫혔습니다!"
else
    echo "⚠️  아직 $REMAINING_PRS개의 PR이 열려있습니다:"
    gh pr list --state open --json number,title --template '{{range .}}{{printf "#%v - %v\n" .number .title}}{{end}}'
fi

echo ""
echo "✨ PR 정리 작업이 완료되었습니다."