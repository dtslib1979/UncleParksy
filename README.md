# parksy.kr — Single-File Codex

> **START HERE**

---

## 이 레포는 뭔가?

단일 `index.html` 파일로 동작하는 HTML 캔버스.  
빌드 없음. 프레임워크 없음. push하면 바로 배포된다.

---

## 작업 규칙

```
허용되는 작업:
  1. index.html 수정
  2. assets/* 추가/수정
  3. archive/* 콘텐츠 보관

금지되는 것:
  - PWA (sw.js, manifest.*)
  - 빌드 시스템 (npm, vite, webpack)
  - 루트에 잡동사니
```

---

## 루트 화이트리스트

```
index.html        ← 유일한 본체
README.md         ← 지금 이 파일
CNAME             ← 도메인
.nojekyll         ← Jekyll 비활성화
.gitignore        ← Git 규칙
favicon.*         ← (선택)
robots.txt        ← (선택)
sitemap.xml       ← (선택)
feed.xml          ← (선택)
```

**이 외의 파일은 루트에 두지 않는다.**

---

## 폴더 구조

```
parksy.kr/
├── index.html          # 본체
├── assets/             # 이미지, 폰트, 정적 파일
├── archive/            # HTML 콘텐츠 아카이브
├── category/           # 카테고리별 콘텐츠
├── docs/               # 기술 문서
└── backup/             # 백업
```

---

## 배포

```bash
git add .
git commit -m "update"
git push
```

→ GitHub Pages 자동 반영

---

## Author

**UncleParksy (박씨)**  
EduArt Engineer · AI-Augmented Creator
