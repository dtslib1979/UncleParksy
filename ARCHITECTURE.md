# PARKSY.KR Architecture Report v1.0

> 작성일: 2025-01-17
> 작성자: Claude (Architect Review)
> 대상: parksy.kr 리포지토리 전면 재설계

---

## Executive Summary

parksy.kr은 단순 웹사이트가 아닌 **"1인 미디어 제국의 엔드포인트"**다.
YouTube에서 할 수 없는 몰입 경험을 제공하는 동굴(CAVE)이자 놀이동산이다.

**핵심 전환:**
- FROM: 티스토리/Obsidian → parksy.kr (백업/수집)
- TO: parksy.kr → 외부 배포 (콘텐츠 공장)

**핵심 제약:**
- 모바일/태블릿 ONLY (PC 무시)
- 인체공학적 터치 경험
- 감정 드라이브 인터랙션

---

## 1. 철학 (Philosophy)

### 1.1 KR Merit - 한국 정체성 소스

| 코드명 | 의미 | 콘텐츠 활용 |
|--------|------|-------------|
| **허세 (Flex)** | 과시, 있어빌리티 | 비주얼 임팩트, "있어 보이는" 연출 |
| **편집/평가 강박** | 눈치, 남 의식, 완벽주의 | 디테일 집착, 마감 퀄리티 |
| **민주주의 판타지** | 집단 환상, 여론 | 커뮤니티, 참여형 콘텐츠 |
| **Half-blood 언어** | 한영 혼합, 코드스위칭 | 바이링구얼 톤앤매너 |

### 1.2 With AI - 철학

```
"뻔한 생각, 집단지성은 AI로 대체 가능하다.
 그래서 '나'만의 것을 만든다."
```

- AI = 도구 (증폭기)
- Human = 소스 (원천)
- Output = 팔 수 있는 것 (상품)

### 1.3 Trilogy Structure

```
parksy.kr     →  eae.kr        →  dtslib.kr
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
개체(Entity)     정체성(Identity)   회사(Company)
샘               정수기             병에 담긴 물
날것/감정        구조/방법론        상품/완성
raw              structured         published
```

---

## 2. 현황 분석 (As-Is)

### 2.1 리포지토리 구조

```
parksy.kr/
├── index.html          # 1035줄, Grimoire 테마 (문제)
├── FACTORY.json        # 새 아키텍처 정의 (유지)
│
├── design/             # CAVE UI 시스템 (유지)
│   ├── cave-ui.css
│   ├── cave-effects.js
│   ├── meaning-layer.yaml
│   └── CAVE-UI.md
│
├── specs/              # 아키텍처 스펙 (유지)
│   ├── layers.yaml     # 4-Layer 시스템
│   ├── plant.yaml      # 로컬 공장 스펙
│   ├── parksy.yaml
│   ├── eae.yaml
│   └── dtslib.yaml
│
├── backup/             # 티스토리 백업 (삭제)
├── archive/            # 정제된 옛날 글 (삭제)
├── docs/04-obsidian/   # Obsidian 연동 (삭제)
├── docs/99-archive/    # 아카이브 문서 (삭제)
│
└── platform/           # 프론트엔드 (리팩토링)
```

### 2.2 문제점

| 문제 | 설명 |
|------|------|
| **컨셉 충돌** | Grimoire(양피지/금색) vs CAVE(동굴/어둠) 혼재 |
| **역방향 유물** | 티스토리/Obsidian 백업 파이프라인 잔존 |
| **PC 코드 과잉** | Three.js, cursor, hover 등 불필요 |
| **복잡한 반응형** | PC/태블릿/모바일 분기 코드 |
| **정체성 불명확** | "뭘 하는 사이트인지" 첫 화면에서 안 보임 |

---

## 3. 목표 설계 (To-Be)

### 3.1 4-Layer Showroom Architecture

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 0: External World                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │  YouTube, Social Media                          │   │
│  │  → 발견 & 첫 접촉                               │   │
│  │  → CTA: "더 보려면 parksy.kr"                   │   │
│  │  → 직행: 설명란 비밀번호로 Layer 2 스킵 가능    │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  LAYER 1: Public Portal (parksy.kr)                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  브랜드 경험 & 깊은 탐색                        │   │
│  │  → 선별된 콘텐츠만 공개                         │   │
│  │  → 숨겨진 입구 (찾는 자만 발견)                 │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  LAYER 2: Inner Portal                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │  비밀번호 게이트                                │   │
│  │  → 월간 비밀번호 (뉴스레터/멤버십)              │   │
│  │  → 진지한 팔로워 필터링                         │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  LAYER 3: Inner World                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │  parksy.zone │ eae.zone │ dtslib.zone          │   │
│  │  (정/Thesis)   (반/Anti)   (합/Synthesis)       │   │
│  │  날것의 감정   구조화 지식   완성된 상품         │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

Funnel: 넓은 입구 → 좁은 출구 (진지한 사람만 안으로)
```

### 3.2 CAVE UI Design System

#### 철학
```
AI 시대 = 모두가 대시보드를 만든다
DTSLIB  = 동굴을 만든다

그 순간, 서비스가 아니라 세계가 된다.
```

#### Anti-Patterns (하지 말 것)
- ❌ 밝은 UI
- ❌ 카드형 레이아웃
- ❌ "친절한 웹사이트"
- ❌ 설명이 먼저
- ❌ 모든 것을 보여주기

#### Design Principles (할 것)
- ✓ 어둡고 (동굴은 빛이 없다)
- ✓ 여백 많고 (비어있음이 깊이)
- ✓ 텍스트 적고 (한 마디가 무겁게)
- ✓ 클릭 = "이동" (페이지가 아니라 장소)
- ✓ 스크롤 = "더 깊이" (내려갈수록 진짜)

#### Spatial Metaphor
```
YouTube        = 바깥 세상
Public Portal  = 동굴 입구 (바위, 어둠, 문장 하나)
Inner Portal   = 좁은 통로 (비밀번호 = 횃불)
Inner World    = 동굴 내부의 방들
```

#### Color Palette
| Variable | Hex | Usage |
|----------|-----|-------|
| `--cave-void` | #0a0a0a | 가장 깊은 어둠 |
| `--cave-deep` | #111111 | 깊은 곳 |
| `--cave-wall` | #1a1a1a | 동굴 벽 |
| `--cave-glow` | #e8e8e8 | 횃불에 비친 텍스트 |
| `--flame-core` | #ff6b35 | 횃불 중심 |

### 3.3 Mobile-Only Architecture

#### 핵심 원칙
```css
/* 전체 컨테이너 */
max-width: 430px;    /* iPhone Pro Max 기준 */
margin: 0 auto;      /* PC에서도 모바일처럼 */
min-height: 100dvh;  /* Dynamic viewport height */
```

#### Touch Interaction Model
```
┌─────────────────────────┐
│    Safe Area (노치)     │  ← 건드리지 않음
├─────────────────────────┤
│                         │
│    View Zone            │  ← 보기만 (스크롤)
│    (상단 60%)           │
│                         │
├─────────────────────────┤
│    Thumb Zone           │  ← 인터랙션 집중
│    (하단 40%)           │     (버튼, 네비게이션)
├─────────────────────────┤
│    Home Bar Area        │  ← 건드리지 않음
└─────────────────────────┘
```

#### Gestures
| 제스처 | 의미 | 액션 |
|--------|------|------|
| Tap | 선택 | 문 열기, 진입 |
| Swipe Up | 더 깊이 | 스크롤, 다음 섹션 |
| Swipe Left/Right | 방 이동 | Zone 전환 |
| Long Press | 숨겨진 것 | 이스터에그, 메뉴 |
| Pull Down | 새로고침 | 동굴 입구로 |

#### 삭제할 PC 코드
- Three.js 배경
- Custom cursor
- Magic circle 애니메이션
- hover 효과 전체
- 복잡한 @media 분기

### 3.4 Meaning Layer System

```yaml
# 의미는 고정, 표현은 그때그때 생성
philosophy: |
  컨셉은 박씨가 만든다.
  감각은 전 세계에서 훔친다.

elements:
  cave-door:
    meaning: "문 - 다른 공간으로 가는 입구"
    behavior: [클릭하면 "들어간다", 호버하면 "열릴 것 같다"]

  torch-input:
    meaning: "횃불 - 어둠을 밝히는 도구"
    behavior: [입력하면 "빛이 켜진다", 틀리면 "꺼진다"]

  monument:
    meaning: "기념비 - 크고 중요한 텍스트"
    behavior: [첫 눈에 들어옴, 무겁고 중요함]

  whisper:
    meaning: "속삭임 - 힌트, 부가 정보"
    behavior: [거의 안 보임, 찾는 자만 봄]
```

---

## 4. 폴더 구조 (Proposed)

```
parksy.kr/
│
├── index.html              # 엔트리 (Public Portal)
├── inner/                  # Inner Portal (비밀번호 게이트)
│   └── index.html
│
├── zone/                   # Inner World
│   ├── parksy/            # parksy.zone
│   ├── eae/               # eae.zone
│   └── dtslib/            # dtslib.zone
│
├── design/                 # UI 시스템
│   ├── cave.css           # 통합 스타일시트
│   ├── cave.js            # 모바일 인터랙션
│   └── meaning-layer.yaml # 의미 정의
│
├── specs/                  # 아키텍처 스펙
│   ├── layers.yaml
│   ├── plant.yaml
│   └── domains/
│       ├── parksy.yaml
│       ├── eae.yaml
│       └── dtslib.yaml
│
├── api/                    # 데이터 엔드포인트
│   └── content.json
│
├── assets/                 # 정적 자산
│   ├── icons/
│   ├── og/
│   └── audio/
│
├── scripts/                # 빌드/배포 스크립트
│   ├── factory.py
│   └── youtube_sync.py
│
├── FACTORY.json            # 핵심 설정
└── .github/
    └── workflows/
        ├── repo-guard.yml
        └── youtube-sync.yml
```

### 삭제 대상
```
❌ backup/              # 티스토리 백업
❌ archive/             # 옛날 글 아카이브
❌ docs/04-obsidian/    # Obsidian 연동
❌ docs/99-archive/     # 아카이브 문서
❌ docs/01-workflows/   # 옛날 워크플로우 (선별 후 삭제)
❌ docs/03-backend/tistory-backup-system.md
❌ category/            # 옛날 카테고리 구조 (검토 필요)
```

---

## 5. 기술 스택 (Proposed)

| 영역 | 기술 | 이유 |
|------|------|------|
| **마크업** | HTML5 Semantic | 단순함 |
| **스타일** | Vanilla CSS | 빌드 불필요 |
| **인터랙션** | Vanilla JS | 의존성 최소화 |
| **호스팅** | GitHub Pages | 무료, 자동 배포 |
| **도메인** | parksy.kr | 브랜딩 |
| **자동화** | GitHub Actions | CI/CD |
| **콘텐츠** | JSON/YAML | 정적 데이터 |

### 의존성 (최소화)
```
필수:
- 없음 (Vanilla only)

선택 (필요시):
- GSAP (애니메이션)
- Lenis (스무스 스크롤)
```

---

## 6. 콘텐츠 플로우

```
┌─────────────┐
│   INBOX     │  ← 던지기 (음성, 메모, 생각)
│   (로컬)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   FACTORY   │  ← Claude가 처리
│   (로컬)    │     분류 → 변환 → 라우팅
└──────┬──────┘
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   parksy    │ │    eae      │ │   dtslib    │
│   OUTPUT    │ │   OUTPUT    │ │   OUTPUT    │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │              │              │
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ parksy.kr   │ │  eae.kr     │ │ dtslib.kr   │
│ (GitHub)    │ │  (GitHub)   │ │ (GitHub)    │
└─────────────┘ └─────────────┘ └─────────────┘
```

---

## 7. 실행 계획

### Phase 1: 청소 (Cleanup)
- [ ] `backup/` 폴더 삭제
- [ ] `archive/` 폴더 삭제
- [ ] `docs/04-obsidian/` 삭제
- [ ] `docs/99-archive/` 삭제
- [ ] 불필요한 워크플로우 문서 삭제

### Phase 2: 리셋 (Reset)
- [ ] `index.html` 완전 새로 작성 (CAVE UI)
- [ ] PC 전용 코드 제거 (Three.js, cursor 등)
- [ ] `design/cave.css` 모바일 전용으로 통합
- [ ] `design/cave.js` 터치 인터랙션 전용으로 재작성

### Phase 3: 구조화 (Structure)
- [ ] `inner/` 디렉토리 생성 (Inner Portal)
- [ ] `zone/` 디렉토리 생성 (Inner World)
- [ ] 라우팅 구조 확립

### Phase 4: 콘텐츠 (Content)
- [ ] Public Portal 첫 화면 콘텐츠 정의
- [ ] Inner Portal 게이트 로직 구현
- [ ] Zone별 초기 콘텐츠 배치

---

## 8. 성공 지표

| 지표 | 목표 |
|------|------|
| **첫 화면 로드** | < 1초 |
| **Lighthouse 모바일** | > 95점 |
| **JS 번들 크기** | < 50KB |
| **CSS 크기** | < 30KB |
| **터치 반응** | < 100ms |
| **"뭔지 알겠다" 시간** | < 3초 |

---

## 9. 열린 질문

1. **archive 글들 중 살릴 것 있는가?**
   - 27개 티스토리 백업 글 → 전부 삭제? 선별?

2. **category/ 폴더는?**
   - 8개 페르소나 구조 → 유지? 리팩토링?

3. **Inner Portal 인증 방식은?**
   - 클라이언트 JS (단순)
   - Cloudflare Access (중간)
   - 별도 서버 (복잡)

4. **eae.kr, dtslib.kr 도메인은?**
   - 별도 리포지토리?
   - 서브디렉토리? (/eae, /dtslib)

---

## Appendix: 핵심 문서 위치

| 문서 | 경로 | 용도 |
|------|------|------|
| CAVE UI 스펙 | `design/CAVE-UI.md` | UI 철학/컴포넌트 |
| Meaning Layer | `design/meaning-layer.yaml` | 의미-표현 분리 |
| Effect 요청 가이드 | `design/EFFECT-REQUESTS.md` | Claude 효과 요청법 |
| 4-Layer 아키텍처 | `specs/layers.yaml` | 관객 깔때기 |
| Factory 설정 | `FACTORY.json` | 콘텐츠 공장 정의 |
| Plant 스펙 | `specs/plant.yaml` | 로컬 생산 공장 |

---

*"이 트릴로지는 플랫폼이 아니다. 한 인간의 생존 구조다."*
*"그 물은 박씨만 만들 수 있다."*

---
End of Report
