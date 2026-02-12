#!/bin/bash

# PR 삭제 도구 검증 스크립트
# 이 스크립트는 PR 삭제 도구가 올바르게 설정되었는지 확인합니다.

echo "🔍 PR 삭제 도구 검증 시작..."
echo ""

ERRORS=0
WARNINGS=0

# 1. 스크립트 파일 존재 확인
echo "📂 1. 스크립트 파일 확인"
FILES=("close_all_prs.sh" "quick_close_prs.sh")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file 존재"
    else
        echo "  ❌ $file 없음"
        ((ERRORS++))
    fi
done
echo ""

# 2. 실행 권한 확인
echo "🔑 2. 실행 권한 확인"
for file in "${FILES[@]}"; do
    if [ -f "$file" ] && [ -x "$file" ]; then
        echo "  ✅ $file 실행 가능"
    elif [ -f "$file" ]; then
        echo "  ⚠️  $file 실행 권한 없음 (chmod +x $file로 해결 가능)"
        ((WARNINGS++))
    fi
done
echo ""

# 3. 스크립트 문법 확인
echo "📝 3. 스크립트 문법 검증"
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        if bash -n "$file" 2>/dev/null; then
            echo "  ✅ $file 문법 OK"
        else
            echo "  ❌ $file 문법 오류"
            ((ERRORS++))
        fi
    fi
done
echo ""

# 4. 문서 파일 확인
echo "📖 4. 문서 파일 확인"
DOCS=("HOW_TO_DELETE_ALL_PRS.md" "PR_CLEANUP_README.md" "PR_CLEANUP_GUIDE.md" "QUICK_COMMANDS.md")
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ✅ $doc 존재"
    else
        echo "  ⚠️  $doc 없음"
        ((WARNINGS++))
    fi
done
echo ""

# 5. GitHub CLI 확인
echo "🔧 5. GitHub CLI 확인"
if command -v gh &> /dev/null; then
    GH_VERSION=$(gh --version | head -n 1)
    echo "  ✅ GitHub CLI 설치됨 ($GH_VERSION)"
    
    # 인증 상태 확인
    if gh auth status &> /dev/null; then
        echo "  ✅ GitHub CLI 인증 완료"
    else
        echo "  ⚠️  GitHub CLI 인증 필요 (gh auth login)"
        ((WARNINGS++))
    fi
else
    echo "  ⚠️  GitHub CLI 미설치 (https://cli.github.com/)"
    ((WARNINGS++))
fi
echo ""

# 6. 저장소 확인
echo "📍 6. Git 저장소 확인"
if git rev-parse --git-dir > /dev/null 2>&1; then
    REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
    echo "  ✅ Git 저장소: $REPO_NAME"
    
    BRANCH=$(git branch --show-current)
    echo "  ℹ️  현재 브랜치: $BRANCH"
else
    echo "  ❌ Git 저장소 아님"
    ((ERRORS++))
fi
echo ""

# 결과 요약
echo "===================================="
echo "📊 검증 결과 요약"
echo "===================================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "🎉 완벽합니다! 모든 검사를 통과했습니다."
    echo ""
    echo "✨ PR 삭제 준비 완료!"
    echo ""
    echo "다음 명령어로 시작하세요:"
    echo "  ./quick_close_prs.sh"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "✅ 기본 검사 통과"
    echo "⚠️  경고: $WARNINGS개"
    echo ""
    echo "경고 사항을 확인하고 필요시 조치하세요."
    echo "대부분의 경고는 실행에 영향을 주지 않습니다."
    exit 0
else
    echo "❌ 오류: $ERRORS개"
    echo "⚠️  경고: $WARNINGS개"
    echo ""
    echo "오류를 해결한 후 다시 실행하세요."
    exit 1
fi
