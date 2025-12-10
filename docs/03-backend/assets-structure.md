---
title: "Assets 폴더 구조"
slug: "assets-structure"
last_updated: 2025-12-10
category: "backend"
tags: ["assets", "icons", "images", "static"]
summary: "정적 자원 폴더 (icons, img, og) 구조 및 용도"
---

# 📦 Assets 폴더 구조

> 🎯 정적 자원 관리

---

## 📁 디렉토리 구조

```
assets/
├── css/                 # 스타일시트
├── js/                  # JavaScript
├── icons/               # 앱 아이콘 (PWA)
├── img/                 # 일반 이미지
├── og/                  # Open Graph 이미지
├── manifest.json        # 아카이브 매니페스트
├── home.json            # 카테고리 카운트
└── categories-manifest.json
```

---

## 1️⃣ icons/

### 용도
PWA 앱 아이콘 및 파비콘

### 파일
- `favicon.ico`
- `icon-192.png`
- `icon-512.png`
- `apple-touch-icon.png`

---

## 2️⃣ img/

### 용도
페이지 내 일반 이미지

### 파일
- 콘텐츠 이미지
- 배경 이미지
- UI 요소

---

## 3️⃣ og/

### 용도
Open Graph 메타 이미지 (소셜 공유용)

### 파일
- `og-default.png` (1200×630)
- 카테고리별 OG 이미지

---

## 4️⃣ JSON 매니페스트

| 파일 | 용도 | 자동생성 |
|------|------|---------|
| `home.json` | 카테고리별 파일 개수 | ✅ |
| `manifest.json` | 아카이브 메타데이터 | ✅ |
| `manifest.archive.json` | 아카이브 전용 | ✅ |

---

*🌊 Deep Sea Librarian | Backend Document*
