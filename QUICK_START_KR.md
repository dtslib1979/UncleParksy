# 🚀 빠른 시작 가이드

> **GitHub Pages 자동 발행 시스템** - 파일 업로드만 하면 자동으로 웹페이지 발행!

## ⚡ 3분 만에 시작하기

### 방법 1: GitHub 웹에서 바로 업로드 (추천)

```
1. GitHub 레포지토리 페이지 열기
   → https://github.com/dtslib1979/UncleParksy

2. category/ 폴더로 이동
   → 원하는 카테고리 선택 (예: writers-path/)

3. "Add file" → "Upload files" 클릭

4. HTML 파일 드래그 & 드롭

5. "Commit changes" 클릭

6. ✅ 완료! 1-2분 후 웹에서 확인
   → https://parksy.kr/category/카테고리명/파일명.html
```

### 방법 2: Git 명령어로 업로드

```bash
# 1. 클론 (처음 한 번만)
git clone https://github.com/dtslib1979/UncleParksy.git
cd UncleParksy

# 2. 파일 추가
# category/writers-path/ 폴더에 HTML 파일 추가

# 3. 커밋 & 푸시
git add .
git commit -m "feat: 새 글 추가"
git push

# 4. ✅ 완료! 자동 발행됨
```

## 📝 HTML 파일 만들기

### 템플릿 사용하기

1. **TEMPLATE.html** 복사
2. 내용 수정 (제목, 본문 등)
3. 파일명 변경: `2025-09-03-my-post.html`
4. 업로드!

### 파일명 규칙

**좋은 예시:**
- ✅ `2025-09-03-github-setup.html` (날짜 + 제목)
- ✅ `2025년-9월-3일-깃허브-설정.html` (한글 날짜)
- ✅ `my-awesome-post.html` (간단한 제목)

**피해야 할 예시:**
- ❌ `새 글.html` (공백, 한글)
- ❌ `post@2025.html` (특수문자)

## 🎯 카테고리 선택

```
category/
├── writers-path/          # 작가의 길
├── thought-archaeology/   # 사고 고고학
├── device-chronicles/     # 장비 연대기
├── blog-transformation/   # 블로그 트랜스포메이션
├── system-configuration/  # 시스템 설정
├── webappsbook-codex/    # 웹앱북 코덱스
├── webappsbookcast/      # 웹앱북캐스트
└── (새 카테고리 추가 가능)
```

## 🔍 결과 확인

### 웹사이트에서 확인
```
https://parksy.kr/category/카테고리명/파일명.html
```

### GitHub Actions에서 확인
1. GitHub 레포 → "Actions" 탭
2. 최신 워크플로우 확인
3. ✅ = 성공, ❌ = 실패

## 💡 자주 묻는 질문

**Q: 얼마나 걸리나요?**
A: 파일 업로드 후 약 1-2분

**Q: 이미지는 어떻게 올리나요?**
A: `assets/images/` 폴더에 이미지 업로드 후
   HTML에서 `/assets/images/파일명.png` 로 참조

**Q: 수정하려면?**
A: GitHub에서 파일 수정 → Commit → 자동 재발행

**Q: 삭제하려면?**
A: GitHub에서 파일 삭제 → Commit → 자동 반영

**Q: 로컬에서 테스트하려면?**
A: `python -m http.server 8000`
   → http://localhost:8000

## 📚 더 자세한 가이드

- **전체 가이드**: [PUBLISHING_GUIDE.md](./PUBLISHING_GUIDE.md)
- **HTML 템플릿**: [TEMPLATE.html](./TEMPLATE.html)
- **프로젝트 README**: [README.md](./README.md)

## 🎉 시작하세요!

이제 자유롭게 컨텐츠를 업로드하고 발행하세요!

**웹사이트**: https://parksy.kr  
**레포지토리**: https://github.com/dtslib1979/UncleParksy

---

*Made with ❤️ by UncleParksy Team*
