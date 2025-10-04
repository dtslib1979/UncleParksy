# 📝 UncleParksy 컨텐츠 발행 가이드

> GitHub Pages를 통한 자동 웹페이지 발행 시스템

## 🚀 빠른 시작

이 레포지토리는 **GitHub Pages**로 설정되어 있어, 파일을 업로드하면 자동으로 웹페이지로 발행됩니다.

### 📍 웹사이트 주소
- **커스텀 도메인**: https://parksy.kr
- **GitHub Pages**: https://dtslib1979.github.io/UncleParksy/

## 📁 컨텐츠 업로드 방법

### 방법 1: GitHub 웹 인터페이스 (가장 쉬운 방법)

1. **GitHub에서 파일 업로드**
   - GitHub 레포지토리 페이지로 이동
   - 원하는 폴더로 이동 (예: `category/writers-path/`)
   - `Add file` → `Upload files` 클릭
   - HTML 파일을 드래그 앤 드롭
   - `Commit changes` 클릭

2. **자동 발행**
   - 파일이 커밋되면 GitHub Actions가 자동 실행
   - 약 1-2분 후 웹페이지로 접근 가능
   - URL: `https://parksy.kr/category/카테고리명/파일명.html`

### 방법 2: Git 명령어 사용

```bash
# 1. 레포지토리 클론
git clone https://github.com/dtslib1979/UncleParksy.git
cd UncleParksy

# 2. 파일 추가 (예: 새 글 작성)
# category/writers-path/ 폴더에 HTML 파일 추가

# 3. 변경사항 커밋
git add .
git commit -m "feat: 새 글 추가 - 제목"

# 4. 푸시 (자동 발행 트리거)
git push origin main
```

### 방법 3: GitHub Desktop 사용

1. GitHub Desktop 설치
2. 레포지토리 클론
3. 로컬에서 파일 추가/수정
4. GitHub Desktop에서 변경사항 확인
5. Commit → Push (자동 발행)

## 📂 폴더 구조 및 규칙

### 권장 폴더 구조

```
UncleParksy/
├── category/              # 카테고리별 컨텐츠
│   ├── writers-path/      # 작가의 길
│   ├── thought-archaeology/  # 사고 고고학
│   ├── device-chronicles/    # 장비 연대기
│   ├── blog-transformation/  # 블로그 트랜스포메이션
│   ├── system-configuration/ # 시스템 설정
│   ├── webappsbook-codex/   # 웹앱북 코덱스
│   ├── webappsbookcast/     # 웹앱북캐스트
│   └── test-category/       # 테스트용 (원하는 이름으로 추가 가능)
├── assets/                # 이미지, CSS, JS 등 정적 파일
└── index.html            # 메인 페이지
```

### 파일명 규칙

**권장 형식 (자동 정렬 지원):**
```
2025-09-03-제목.html          # 영문 날짜 형식
2025년 9월 3일 제목.html       # 한글 날짜 형식
제목.html                     # 날짜 없는 형식
```

**예시:**
- `2025-09-03-github-pages-setup.html`
- `2025년 9월 3일 깃허브 페이지 설정.html`
- `my-awesome-post.html`

## 🎨 HTML 파일 작성 가이드

### 기본 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>페이지 제목</title>
  <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
  <article>
    <h1>페이지 제목</h1>
    <p>내용을 여기에 작성하세요...</p>
  </article>
</body>
</html>
```

### 모바일 최적화 간단 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{제목}}</title>
<style>
body{font-family:-apple-system,sans-serif;max-width:800px;margin:0 auto;padding:20px;line-height:1.6}
h1{font-size:1.5rem;margin:.8rem 0}
h2{font-size:1.25rem;margin:.7rem 0}
.card{background:#fff8ea;border:1px solid rgba(0,0,0,.06);border-radius:14px;padding:14px;margin:10px 0}
</style>
</head>
<body>
<article class="card">
<h1>{{제목}}</h1>
{{내용}}
</article>
</body>
</html>
```

## 🤖 자동화 기능

### 1. 자동 카테고리 인덱스 생성

`category/*/index.html` 파일이 자동으로 업데이트됩니다:
- 최신 글이 맨 위에 표시
- 날짜 자동 파싱 및 정렬
- 한글/영문 날짜 모두 지원

### 2. 자동 사이트맵 생성

`sitemap.xml`이 자동 생성되어 SEO 최적화:
- 모든 HTML 페이지 자동 인덱싱
- 검색 엔진 크롤러 지원

### 3. GitHub Pages 자동 배포

- `main` 브랜치에 푸시하면 자동 배포
- 약 1-2분 후 웹사이트 업데이트 완료
- Actions 탭에서 배포 상태 확인 가능

## 🔄 워크플로우

```
1. 파일 작성/수정
   ↓
2. GitHub에 업로드 (push/upload)
   ↓
3. GitHub Actions 자동 실행
   ↓
4. 사이트맵 & 인덱스 업데이트
   ↓
5. GitHub Pages 자동 배포
   ↓
6. 웹사이트에서 확인 가능!
```

## 📊 배포 상태 확인

### GitHub Actions에서 확인
1. GitHub 레포지토리 → `Actions` 탭
2. 최신 워크플로우 실행 확인
3. 녹색 체크마크(✅) = 성공
4. 빨간 X(❌) = 실패 (로그 확인 필요)

### 웹사이트에서 확인
```bash
# 브라우저에서 직접 접근
https://parksy.kr/category/카테고리명/파일명.html

# 또는
https://dtslib1979.github.io/UncleParksy/category/카테고리명/파일명.html
```

## 💡 팁과 권장사항

### ✅ 권장사항

1. **파일명은 영문으로**: URL에 한글이 들어가면 인코딩되어 복잡해집니다
2. **날짜 포함**: 파일명에 날짜를 포함하면 자동 정렬됩니다
3. **의미있는 이름**: SEO에 도움되는 명확한 파일명 사용
4. **작은 이미지**: 이미지는 최적화해서 업로드 (1MB 이하 권장)
5. **테스트 후 발행**: 중요한 컨텐츠는 로컬에서 먼저 테스트

### ⚠️ 주의사항

1. **대용량 파일 금지**: GitHub는 100MB 이상 파일 거부
2. **민감정보 제외**: 비밀번호, API 키 등 절대 업로드 금지
3. **저작권 준수**: 타인의 저작물 무단 사용 금지
4. **HTML 검증**: 깨진 HTML은 페이지가 제대로 표시안될 수 있음

## 🎯 자주 사용하는 명령어

```bash
# 현재 상태 확인
git status

# 모든 변경사항 추가
git add .

# 특정 폴더만 추가
git add category/writers-path/

# 커밋
git commit -m "feat: 새 글 추가"

# 푸시 (배포 트리거)
git push

# 최신 변경사항 받기
git pull

# 변경사항 되돌리기 (푸시 전)
git checkout -- 파일명
```

## 🔧 문제 해결

### Q: 파일을 업로드했는데 웹에서 안 보여요
**A:** 
1. GitHub Actions 탭에서 배포 완료 확인 (1-2분 소요)
2. 브라우저 캐시 삭제 후 새로고침 (Ctrl+Shift+R)
3. URL이 정확한지 확인

### Q: 카테고리 인덱스에 내 글이 안 나와요
**A:**
1. 파일이 `category/카테고리명/` 폴더에 있는지 확인
2. `index.html`이 해당 카테고리 폴더에 있는지 확인
3. GitHub Actions 워크플로우가 정상 실행되었는지 확인

### Q: 이미지가 안 보여요
**A:**
1. 이미지 경로를 절대 경로로 사용: `/assets/images/파일명.png`
2. 이미지 파일이 실제로 레포지토리에 업로드되었는지 확인
3. 파일명에 한글이나 특수문자가 없는지 확인

### Q: 모바일에서 레이아웃이 깨져요
**A:**
1. HTML `<head>`에 viewport 메타 태그 추가:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   ```
2. 반응형 CSS 사용 권장

## 📞 추가 도움말

- **GitHub 문서**: https://docs.github.com/pages
- **HTML/CSS 학습**: https://developer.mozilla.org/
- **Markdown 가이드**: https://www.markdownguide.org/

---

**🎉 이제 자유롭게 컨텐츠를 업로드하고 발행하세요!**

*Made with ❤️ by UncleParksy - EduArt Engineer's Grimoire*
