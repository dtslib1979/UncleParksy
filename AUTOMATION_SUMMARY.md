# 📋 자동화 분석 요약 (Summary)

> 상세 분석: [`AUTOMATION_ANALYSIS.md`](./AUTOMATION_ANALYSIS.md)

---

## 🎯 핵심 질문

> "지금 내가 `category/<Persona>/*.html`에 새 페이지를 올리고 카테고리 인덱스를 갱신하려고 해도, 다른 상위 자동화가 나중에 돌면서 그 결과를 다시 덮어씌우고 있냐?"

---

## ❌ 답변: NO — 광역 덮어쓰기 없음

**현재 자동화 구조는 정상적으로 설계되어 있으며, 각 파이프라인은 서로 다른 파일을 대상으로 합니다.**

---

## 📊 파이프라인 요약표

| 대상 파일 | 담당 워크플로우 | 역할 |
|-----------|----------------|------|
| `assets/home.json` | `category-index.yml` | 카테고리별 파일 개수만 저장 |
| `category/*/index.html` | `pages-maintenance.yml` | 폴더 내 HTML 기반으로 리스트 재생성 |
| `assets/manifest.json` | `build-textstory.yml` | `archive/` 폴더만 스캔 (category 무시) |
| `_obsidian/_imports/` | `obsidian-sync.yml` | category → _obsidian 복사 (충돌 없음) |

---

## 🔄 Push 시 실행 흐름

```
category/<Persona>/new-page.html 추가
              │
              ▼
      ┌───────────────────────────────────┐
      │  3개 워크플로우 동시 트리거       │
      └───────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
category   pages-     obsidian-
-index    maintenance   backup
  .yml       .yml        .yml
    │         │          │
    ▼         ▼          ▼
home.json  index.html  _obsidian/
(카운트)   (리스트)    (백업)
    │         │          │
    └─────────┴──────────┘
              │
    ✅ 서로 다른 파일 → 충돌 없음
```

---

## ✅ 왜 "덮어쓰기"가 아닌가?

1. **`pages-maintenance.yml`**: 폴더 내 실제 HTML 파일 기반으로 리스트 재생성 → 새 파일 자동 포함
2. **`generate_category_index.py`**: `index.html` 수정 안 함 (카운트만 저장)
3. **`auto_install.py`**: `archive/` 폴더만 처리 → `category/`와 무관

---

## 🔧 문제 발생 시 체크리스트

| 증상 | 확인 사항 | 해결 방법 |
|------|----------|----------|
| 카운트 미갱신 | Actions → `Category Index Builder` 실행 여부 | 수동 트리거: `Run workflow` |
| 리스트 비어있음 | index.html에 `<ul id="post-list">` 존재 여부 | 태그 추가 또는 AWK 스크립트 대상 확인 |
| manifest에 파일 없음 | `assets/manifest.json`은 archive만 스캔 | `category/*/manifest.json` 사용 |

---

## 📌 결론

| 항목 | 상태 |
|------|------|
| 광역 덮어쓰기 | ❌ 없음 |
| 파이프라인 분리 | ✅ 정상 |
| 권장 조치 | 현재 구조 유지, 문제 시 Actions 탭 확인 |

---

*상세 분석은 [`AUTOMATION_ANALYSIS.md`](./AUTOMATION_ANALYSIS.md) 참조*
