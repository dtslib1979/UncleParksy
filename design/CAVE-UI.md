# CAVE UI - Design System

> "여긴 전시관이 아니다. 누군가의 머릿속이다."

## Philosophy

```
AI 시대 = 모두가 대시보드를 만든다
DTSLIB  = 동굴을 만든다

그 순간, 서비스가 아니라 세계가 된다.
```

## Anti-Patterns (하지 말 것)

- ❌ 밝은 UI
- ❌ 카드형 레이아웃
- ❌ "친절한 웹사이트"
- ❌ 설명이 먼저
- ❌ 모든 것을 보여주기

## Design Principles (할 것)

- ✓ **어둡고** - 동굴은 빛이 없다
- ✓ **여백 많고** - 비어있음이 깊이
- ✓ **텍스트 적고** - 한 마디가 무겁게
- ✓ **클릭 = "이동"** - 페이지가 아니라 장소
- ✓ **스크롤 = "더 깊이"** - 내려갈수록 진짜

## Spatial Metaphor

```
YouTube        = 바깥 세상
Public Portal  = 동굴 입구 (바위, 어둠, 문장 하나)
Inner Portal   = 좁은 통로 (비밀번호 = 횃불)
Inner World    = 동굴 내부의 방들

   ├─ parksy.zone   = 벽화가 있는 방 (인간의 흔적)
   ├─ eae.zone      = 기호와 도식의 방 (구조)
   └─ dtslib.zone   = 작업실 / 제단 (생산)
```

## Color Palette

| Variable | Hex | Usage |
|----------|-----|-------|
| `--cave-void` | #0a0a0a | 가장 깊은 어둠 |
| `--cave-deep` | #111111 | 깊은 곳 |
| `--cave-wall` | #1a1a1a | 동굴 벽 |
| `--cave-stone` | #252525 | 돌 표면 |
| `--cave-glow` | #e8e8e8 | 횃불에 비친 텍스트 |
| `--cave-dim` | #888888 | 그림자 속 텍스트 |
| `--cave-faint` | #444444 | 거의 안 보임 |
| `--flame-core` | #ff6b35 | 횃불 중심 |
| `--flame-edge` | #f7931e | 횃불 가장자리 |

## Typography

```css
--font-body: 'Pretendard'     /* 일반 텍스트 */
--font-accent: 'Noto Serif KR' /* 중요한 선언문 */
--font-mono: 'JetBrains Mono'  /* 코드/기호 */
```

### Scale

| Class | Size | Usage |
|-------|------|-------|
| `.whisper` | 0.75rem | 힌트, 거의 안 보임 |
| (normal) | 1rem | 기본 |
| `.statement` | 1.5rem | 선언문 |
| `.monument` | 3rem | 기념비적 |

## Components

### `.cave-door` - 입장 버튼
```html
<a href="..." class="cave-door">enter the cave</a>
```

### `.torch-input` - 비밀번호 입력
```html
<input type="password" class="torch-input" placeholder="· · · · · ·">
```

### `.cave-crack` - 구분선
```html
<div class="cave-crack"></div>
```

### `.cave-path` - 링크
```html
<a href="..." class="cave-path">돌아가기</a>
```

## Layouts

### `.cave-entrance` - 입구 (전체화면 중앙)
### `.cave-passage` - 통로 (좁은 컨테이너)
### `.cave-chamber` - 방 (일반 컨테이너)

## Animation

모든 것은 **어둠에서 나타난다**:

```css
.emerge {
  animation: emerge 0.8s ease forwards;
}
```

순차적 등장:
```html
<p class="emerge" style="animation-delay: 0.3s;">...</p>
```

## Zone Colors

| Zone | Color | Metaphor |
|------|-------|----------|
| parksy | #6b8e9f | 차가운 청회색 - 벽화 |
| eae | #8b7355 | 따뜻한 갈색 - 기호 |
| dtslib | #9a8c7a | 중성 베이지 - 제단 |

## Files

```
design/
├── cave-ui.css           # 메인 스타일시트
├── CAVE-UI.md            # 이 문서
└── examples/
    ├── entrance.html     # Public Portal 예시
    ├── inner-portal.html # 비밀번호 입력 예시
    └── inner-world.html  # Inner World 예시
```

## Usage

```html
<link rel="stylesheet" href="/design/cave-ui.css">
```

---

*"아무나 들어오지 않는다. 설명보다 느낌이 먼저 온다."*
