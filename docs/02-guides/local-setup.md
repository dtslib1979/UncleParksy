---
title: "로컬 개발 환경 설정 가이드"
slug: "local-setup"
last_updated: 2025-12-10
category: "guides"
tags: ["setup", "local", "development", "guide"]
summary: "UncleParksy 로컬 개발 환경 구축 및 동기화 방법"
---

# 📖 로컬 개발 환경 설정 가이드

> 🎯 목표: 로컬 PC에서 UncleParksy 레포 작업 + Obsidian 연동

---

## 🔧 사전 요구사항

| 도구 | 버전 | 용도 |
|------|------|------|
| Git | 2.x+ | 버전 관리 |
| Python | 3.11+ | 스크립트 실행 |
| Obsidian | 1.10+ | 로컬 문서 관리 |

---

## 1️⃣ 레포지토리 클론

```powershell
# 작업 디렉토리 생성
mkdir C:\Users\dtsli\UncleParksy_Local
cd C:\Users\dtsli\UncleParksy_Local

# 클론
git clone https://github.com/dtslib1979/UncleParksy.git
cd UncleParksy
```

---

## 2️⃣ Python 의존성 설치

```powershell
pip install requests feedparser beautifulsoup4 lxml
```

---

## 3️⃣ Obsidian 연동

### 방법 A: Junction 링크 (권장)

```powershell
# 기존 Obsidian 볼트에 GitHub 데이터 연결
$source = "C:\Users\dtsli\UncleParksy_Local\UncleParksy\_obsidian\_imports"
$dest = "C:\Users\dtsli\Documents\Obsidian Vault\📥 GitHub 백업\UncleParksy"

cmd /c mklink /J "$dest" "$source"
```

### 방법 B: 직접 복사

```powershell
Copy-Item -Recurse $source $dest
```

---

## 4️⃣ 동기화 명령어

### GitHub → 로컬

```powershell
cd C:\Users\dtsli\UncleParksy_Local\UncleParksy
git pull origin main
```

### 로컬 → GitHub

```powershell
git add .
git commit -m "설명"
git push origin main
```

---

## 5️⃣ 로컬 서버 실행

```powershell
cd C:\Users\dtsli\UncleParksy_Local\UncleParksy
python -m http.server 8000
```

브라우저: `http://localhost:8000`

---

## 📁 주요 경로

| 용도 | 경로 |
|------|------|
| 로컬 레포 | `C:\Users\dtsli\UncleParksy_Local\UncleParksy` |
| Obsidian 볼트 | `C:\Users\dtsli\Documents\Obsidian Vault` |
| GitHub 백업 | `📥 GitHub 백업\UncleParksy\` |

---

*🌊 Deep Sea Librarian | Setup Guide*
