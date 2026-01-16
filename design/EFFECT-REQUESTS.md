# CAVE UI - Effect Request Guide

## 사용법

이 파일은 Claude에게 효과 업데이트를 요청할 때 참고하는 가이드입니다.

---

## 1. 특정 요소 효과 변경

```
"cave-door 효과를 2024 최신 트렌드로 바꿔줘"
```

```
"torch-input에 더 dramatic한 glow 효과 넣어줘"
```

```
"monument 텍스트에 glitch 효과 추가해"
```

---

## 2. 전체 분위기 변경

```
"전체적으로 더 mystical한 느낌으로 바꿔줘"
```

```
"minimal-dark 무드로 통일해줘"
```

```
"좀 더 organic하고 살아있는 느낌 줘"
```

---

## 3. 특정 사이트 참고

```
"이 사이트 느낌으로 cave-door 바꿔줘: [URL]"
```

```
"Awwwards에서 최근 수상한 dark 테마 사이트 참고해서 전체 업데이트해"
```

---

## 4. 특정 기술 적용

```
"Three.js로 배경에 파티클 효과 넣어줘"
```

```
"GSAP ScrollTrigger로 스크롤 애니메이션 강화해줘"
```

```
"WebGL shader로 노이즈 텍스처 만들어줘"
```

---

## 5. 성능/호환성 요청

```
"모바일에서 더 가볍게 돌아가게 최적화해줘"
```

```
"prefers-reduced-motion 지원 추가해줘"
```

---

## Element 목록

| Class | 의미 |
|-------|------|
| `.cave-door` | 문 - 다른 공간으로 가는 입구 |
| `.torch-input` | 횃불 - 비밀번호 입력 |
| `.cave-path` | 길 - 링크, 이동 |
| `.cave-crack` | 균열 - 구분선 |
| `.cave-wall` | 벽 - 배경 |
| `.torch-light` | 횃불 빛 - 커서 조명 |
| `.zone-marker` | 영역 표시 - 방 구분 |
| `.monument` | 기념비 - 큰 제목 |
| `.statement` | 선언문 - 핵심 문장 |
| `.whisper` | 속삭임 - 힌트 |

---

## Mood 목록

| Mood | 설명 |
|------|------|
| `ancient` | 고대, 시간의 무게, warm earth |
| `mystical` | 신비로운, 마법적, glowing |
| `minimal-dark` | 미니멀, 깨끗한 어둠 |
| `organic` | 유기적, 살아있는, morphing |
| `glitch` | 디지털 노이즈, RGB split |

---

## Claude가 하는 일

1. **웹서치** - Awwwards, Codepen에서 최신 효과 찾기
2. **분석** - 의미(meaning)와 매칭되는지 확인
3. **생성** - CSS/JS 코드 작성
4. **적용** - cave-effects.css/js 업데이트
5. **테스트** - examples/ 페이지에서 확인

---

## 예시 대화

**User:**
> "cave-door가 좀 밋밋해. 더 dramatic하게 바꿔줘. Awwwards에서 최근 본 거 참고해서."

**Claude:**
> [웹서치: "awwwards button hover effect 2024"]
> [분석: magnetic effect + glow + scale 조합 발견]
> [코드 생성 및 적용]

---

*"의미는 고정, 표현은 그때그때 최신으로"*
