# 📤 자동 포스팅 가이드

## ✅ 수정 완료!

자동 포스팅 시스템이 이제 정상적으로 작동합니다.

## 🎯 문제 해결

### 이전 문제
- `scripts/auto_install.py`가 `backup/*.html`을 찾았지만, 실제 파일은 `backup/raw/*.html`에 있었습니다.
- 결과: "0개 파일 처리" - 아무것도 포스팅되지 않음

### 수정 사항
- `backup/raw/` 디렉토리에서 파일을 검색하도록 수정
- 통계 보고도 올바른 위치를 확인하도록 업데이트

## 📝 사용 방법

### 1️⃣ 파일 업로드
```bash
# HTML 파일을 backup/raw/ 디렉토리에 추가
cp your-post.html backup/raw/2025-10-14-제목.html
git add backup/raw/2025-10-14-제목.html
git commit -m "포스트: 새 글 추가"
git push
```

### 2️⃣ 자동 처리
GitHub Actions가 자동으로:
1. ✅ 파일 감지 (`backup/**` 경로 모니터링)
2. ✅ `archive/`로 미러링
3. ✅ 모바일 최적화 적용
4. ✅ `manifest.json` 업데이트
5. ✅ 자동 커밋 & 푸시

### 3️⃣ 확인
- 🌐 웹사이트: https://parksy.kr
- 📋 매니페스트: https://dtslib1979.github.io/UncleParksy/assets/manifest.json

## 🤖 자동화 트리거

### 자동 실행
- ⏰ 매 3시간마다 자동 실행 (cron: `0 */3 * * *`)
- 📁 `backup/**` 파일 변경 시 즉시 실행
- 🔧 `scripts/**` 파일 변경 시 실행

### 수동 실행
GitHub Actions → "🤖 완전 자동화 KR TextStory Archive" → "Run workflow"

## 📊 처리 흐름

```
📁 backup/raw/*.html
    ↓ (자동 감지)
🤖 GitHub Actions
    ↓ (auto_install.py 실행)
📂 archive/*.html (원본 복사)
    ↓ (모바일 최적화)
📱 archive/*.html (모바일 버전)
    ↓ (매니페스트 생성)
📋 assets/manifest.json
    ↓ (자동 커밋)
✅ GitHub Pages 배포
```

## 🧪 테스트 결과

### 수정 전
```
⚠️ 백업 HTML 파일 없음
📊 백업: 0개, 아카이브: 21개
0개 파일 처리
```

### 수정 후
```
✅ 21개 파일 원본 그대로 미러링 완료
✅ 모바일 최적화 완료: 21개 파일
📊 백업: 21개, 아카이브: 21개
```

## 💡 팁

1. **파일명 규칙**: `YYYY-MM-DD-제목.html` 형식 권장
2. **제목 추출**: HTML의 `<title>` 태그에서 자동 추출
3. **중복 방지**: 같은 이름 파일은 최신 것으로 덮어씀
4. **로그 확인**: GitHub Actions 탭에서 실행 로그 확인 가능

## 🔍 문제 해결

### 파일이 포스팅되지 않는 경우
1. ✅ 파일이 `backup/raw/` 디렉토리에 있는지 확인
2. ✅ 파일 확장자가 `.html`인지 확인
3. ✅ GitHub Actions 워크플로우가 실행되었는지 확인
4. ✅ 워크플로우 로그에서 에러 메시지 확인

### 수동으로 실행하기
```bash
# 로컬에서 테스트
cd /path/to/UncleParksy
python scripts/auto_install.py

# 결과 확인
ls -l archive/
cat assets/manifest.json
```

## 🎉 완료!

이제 `backup/raw/`에 HTML 파일을 추가하기만 하면 자동으로 아카이브에 게시됩니다!

---
📅 수정일: 2025-10-14
🔧 수정자: GitHub Copilot Agent
📝 PR: copilot/fix-auto-posting-issue
