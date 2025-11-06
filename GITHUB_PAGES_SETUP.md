# 🌐 GitHub Pages 설정 가이드

> UncleParksy의 GitHub Pages 자동 발행 시스템 상세 설명

## 📋 현재 설정 상태

### ✅ 이미 완료된 설정

이 레포지토리는 **GitHub Pages**로 완벽하게 설정되어 있습니다:

1. **배포 방식**: Branch에서 직접 배포 (classic method)
2. **배포 브랜치**: `main` 브랜치
3. **배포 경로**: 루트 디렉토리 (`/`)
4. **커스텀 도메인**: `parksy.kr` (CNAME 파일로 설정됨)
5. **Jekyll 비활성화**: `.nojekyll` 파일로 비활성화

### 🎯 작동 원리

```
[파일 업로드/수정] 
    ↓
[main 브랜치에 push]
    ↓
[GitHub Pages 자동 감지]
    ↓
[pages-maintenance.yml 실행]
  - sitemap.xml 자동 생성
  - 카테고리 인덱스 정렬
    ↓
[GitHub Pages 자동 배포]
    ↓
[https://parksy.kr 에서 접근 가능]
```

## 🔧 설정 파일 설명

### 1. `.nojekyll`

```
목적: Jekyll 빌드 프로세스 비활성화
이유: 순수 HTML 파일을 있는 그대로 서빙하기 위함
```

- Jekyll을 사용하지 않고 정적 HTML을 직접 서빙
- `_`로 시작하는 폴더/파일도 서빙 가능 (`_obsidian/` 등)

### 2. `CNAME`

```
내용: parksy.kr
목적: 커스텀 도메인 설정
```

- GitHub Pages가 이 파일을 읽어 커스텀 도메인 적용
- DNS 설정도 필요 (A 레코드 또는 CNAME 레코드)

### 3. `.github/workflows/pages-maintenance.yml`

**트리거:**
- `main` 브랜치 push 시
- `category/**/*.html` 파일 변경 시
- `index.html` 또는 `assets/**` 변경 시

**수행 작업:**
1. `sitemap.xml` 자동 생성
2. 각 카테고리의 `index.html` 업데이트
3. 최신 글이 맨 위에 오도록 정렬
4. 변경사항 자동 커밋 & 푸시

## 📁 폴더 구조 및 접근 URL

```
UncleParksy/
├── index.html                    → https://parksy.kr/
├── about.html                    → https://parksy.kr/about.html
├── contact.html                  → https://parksy.kr/contact.html
├── category/
│   ├── writers-path/
│   │   ├── index.html           → https://parksy.kr/category/writers-path/
│   │   └── 2025-09-03-post.html → https://parksy.kr/category/writers-path/2025-09-03-post.html
│   └── thought-archaeology/
│       └── my-post.html         → https://parksy.kr/category/thought-archaeology/my-post.html
├── assets/
│   ├── css/style.css            → https://parksy.kr/assets/css/style.css
│   └── images/logo.png          → https://parksy.kr/assets/images/logo.png
└── TEMPLATE.html                → https://parksy.kr/TEMPLATE.html
```

## 🚀 새 페이지 발행 프로세스

### 단계별 설명

**1. 파일 준비**
```html
<!-- 예: category/writers-path/2025-09-03-my-post.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>내 글 제목</title>
</head>
<body>
  <h1>내 글 제목</h1>
  <p>내용...</p>
</body>
</html>
```

**2. GitHub에 업로드**
- 방법 A: GitHub 웹 인터페이스에서 파일 업로드
- 방법 B: Git 명령어로 push

**3. 자동 처리 (GitHub 내부)**
```
[업로드 완료]
    ↓
[pages-maintenance 워크플로우 실행]
  • sitemap.xml에 새 페이지 추가
  • category/writers-path/index.html 업데이트
    ↓
[변경사항 자동 커밋]
    ↓
[GitHub Pages 자동 재배포]
  • 약 30초-1분 소요
    ↓
[완료] https://parksy.kr/category/writers-path/2025-09-03-my-post.html
```

**4. 결과 확인**
- 브라우저에서 URL 접근
- SEO: sitemap.xml에 자동 등록
- 카테고리 인덱스에 자동 표시

## 🔍 GitHub Pages 설정 확인 방법

### GitHub 웹 인터페이스에서

1. 레포지토리 페이지 이동
2. `Settings` 탭 클릭
3. 왼쪽 메뉴에서 `Pages` 선택
4. 확인할 내용:
   ```
   Source: Deploy from a branch
   Branch: main / (root)
   Custom domain: parksy.kr
   Enforce HTTPS: ✅ (권장)
   ```

### Actions 탭에서 배포 상태 확인

1. `Actions` 탭 클릭
2. 최신 워크플로우 실행 확인
3. `pages-maintenance` 워크플로우 상태 확인
4. 녹색 체크마크(✅) = 성공

## 💡 Best Practices

### ✅ 권장사항

1. **파일명 규칙 준수**
   - 날짜 포함: `YYYY-MM-DD-title.html`
   - 소문자 사용
   - 하이픈으로 단어 구분
   - 한글보다 영문 권장 (URL 가독성)

2. **카테고리 구조 활용**
   - 관련 글들을 같은 카테고리에 모으기
   - 카테고리별 `index.html` 자동 관리됨

3. **이미지 최적화**
   - 웹 최적화된 포맷 사용 (WebP, 최적화된 JPEG/PNG)
   - 적절한 크기로 리사이즈
   - `assets/images/` 폴더에 정리

4. **메타 태그 포함**
   ```html
   <meta name="description" content="페이지 설명">
   <meta property="og:title" content="제목">
   <meta property="og:image" content="이미지URL">
   ```

### ⚠️ 주의사항

1. **대용량 파일 금지**
   - GitHub는 50MB 권고, 100MB 제한
   - Pages는 1GB 레포지토리 크기 권고

2. **빌드 시간**
   - 첫 배포: 최대 10분
   - 재배포: 30초-2분
   - 인내심을 가지고 기다리기

3. **캐시 문제**
   - 브라우저 캐시로 인해 변경사항이 안 보일 수 있음
   - 강력 새로고침: `Ctrl + Shift + R` (Windows/Linux)
   - 강력 새로고침: `Cmd + Shift + R` (Mac)

4. **민감정보 제외**
   - API 키, 비밀번호 등 절대 업로드 금지
   - 공개 레포지토리임을 항상 인지

## 🔧 문제 해결

### 문제: 페이지가 404 오류

**원인:**
- 파일이 실제로 레포지토리에 없음
- URL 경로가 잘못됨
- 배포가 아직 완료되지 않음

**해결:**
1. GitHub 레포에서 파일 존재 확인
2. URL 대소문자 확인 (대소문자 구분함)
3. 1-2분 대기 후 재시도
4. Actions 탭에서 배포 완료 확인

### 문제: 변경사항이 반영되지 않음

**원인:**
- 브라우저 캐시
- GitHub Pages 재배포 대기 중

**해결:**
1. 강력 새로고침 (`Ctrl + Shift + R`)
2. 시크릿 모드로 접속
3. Actions 탭에서 워크플로우 완료 확인
4. 최대 10분 대기

### 문제: 카테고리 인덱스에 글이 안 나옴

**원인:**
- `pages-maintenance` 워크플로우 실패
- 파일명 형식 문제

**해결:**
1. Actions 탭에서 워크플로우 로그 확인
2. 파일명이 규칙에 맞는지 확인
3. `category/카테고리명/index.html` 파일 존재 확인

## 📊 성능 최적화

### 권장 사항

1. **HTML 최소화**
   - 불필요한 공백, 주석 제거
   - 인라인 CSS/JS 최소화

2. **이미지 최적화**
   - WebP 포맷 사용
   - Lazy loading 적용
   - 적절한 크기로 리사이즈

3. **캐싱 활용**
   - 정적 자산에 버전 번호 추가
   - `style.css?v=1.0.0`

4. **CDN 활용**
   - 외부 라이브러리는 CDN 사용
   - Google Fonts, Font Awesome 등

## 🎯 추가 기능

### PWA (Progressive Web App) 지원

레포지토리에 이미 포함:
- `manifest.webmanifest`: 앱 설정
- 오프라인 지원 가능 (Service Worker 추가 시)

### RSS Feed

- `feed.xml` 자동 생성 가능
- 블로그 구독자를 위한 RSS 제공

### SEO 최적화

- `sitemap.xml` 자동 생성됨
- 검색 엔진 크롤러 지원
- Open Graph 메타 태그 사용 권장

## 📞 추가 리소스

- **GitHub Pages 공식 문서**: https://docs.github.com/pages
- **커스텀 도메인 설정**: https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site
- **GitHub Actions**: https://docs.github.com/actions

---

## ✅ 체크리스트

이 레포지토리의 GitHub Pages 설정 완료 여부:

- [x] `.nojekyll` 파일 존재
- [x] `CNAME` 파일로 커스텀 도메인 설정
- [x] `main` 브랜치에서 배포 설정
- [x] `pages-maintenance.yml` 자동화 워크플로우
- [x] `sitemap.xml` 자동 생성
- [x] 카테고리 인덱스 자동 정렬
- [x] 접근 가능한 메인 페이지 (`index.html`)
- [x] 반응형 디자인
- [x] PWA manifest 파일

**결론: 완벽하게 설정됨! 🎉**

---

*Last Updated: 2025-09-03*
*Made with ❤️ by UncleParksy Team*
