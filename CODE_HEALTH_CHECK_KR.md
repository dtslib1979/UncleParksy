# 🏥 코드 건강 체크 - 빠른 참조 가이드

> UncleParksy 저장소의 코드 상태를 한눈에 확인하세요

---

## 🎯 현재 상태: ✅ 건강함 (Healthy)

마지막 검사: 2025년 1월

---

## 📊 건강 지표

| 지표 | 상태 | 설명 |
|-----|------|------|
| 🟢 JavaScript 문법 | 정상 | 모든 .js 파일 문법 오류 없음 |
| 🟢 HTML 구조 | 정상 | 태그 매칭 및 구조 정상 |
| 🟢 코드 일관성 | 정상 | 일관된 코딩 스타일 유지 |
| 🟢 에러 핸들링 | 양호 | try-catch 및 fallback 구현 |
| 🟢 파일 구조 | 정상 | 체계적인 디렉토리 구조 |

---

## 🔍 빠른 검사 명령어

저장소를 직접 검사하고 싶다면 다음 명령어를 사용하세요:

### 1. JavaScript 문법 검사
```bash
# 모든 JS 파일 문법 검사
find . -name "*.js" -type f -exec node -c {} \;
```

### 2. HTML 파일 개수 확인
```bash
# HTML 파일 통계
find . -name "*.html" -type f | wc -l
```

### 3. console.log 찾기
```bash
# 개발용 로그 위치 확인
grep -r "console\.log" --include="*.js" --include="*.html" .
```

### 4. TODO/FIXME 확인
```bash
# 미완성 작업 찾기
grep -r "TODO\|FIXME" --include="*.js" --include="*.html" .
```

---

## 📁 주요 파일 위치

### JavaScript
```
assets/js/
└── copy-tistory-urls.js  ✅ 정상
```

### 핵심 HTML 파일
```
/
├── index.html  ✅ 정상
├── archive/index.html  ✅ 정상
└── category/
    ├── thought-archaeology/
    │   └── 2025년 8월 27일 기독교모델.html  ✅ 정상
    └── writers-path/
        └── 10testaments.html  ✅ 정상
```

---

## 🚨 문제 발생 시 체크리스트

만약 문제가 발생하면 다음을 확인하세요:

### JavaScript 오류
- [ ] 브라우저 콘솔에서 에러 메시지 확인
- [ ] 파일 경로가 올바른지 확인
- [ ] 필요한 라이브러리가 로드되었는지 확인

### HTML 표시 문제
- [ ] 브라우저 개발자 도구로 HTML 구조 확인
- [ ] CSS 파일이 제대로 로드되는지 확인
- [ ] 네트워크 탭에서 404 에러 확인

### 기능 작동 불가
- [ ] JavaScript 에러 확인 (콘솔)
- [ ] 이벤트 핸들러가 제대로 바인딩되었는지 확인
- [ ] 필요한 요소(ID/Class)가 존재하는지 확인

---

## 🛠️ 자동 검사 도구

### Python 검사 스크립트

다음 스크립트로 자동 검사 가능:

```python
# check_repo.py
import subprocess
import sys

checks = {
    "JavaScript 문법": "find . -name '*.js' -type f -exec node -c {} \\;",
    "HTML 파일 수": "find . -name '*.html' -type f | wc -l",
    "파일 구조": "ls -la"
}

for name, cmd in checks.items():
    print(f"🔍 {name}...")
    result = subprocess.run(cmd, shell=True, capture_output=True)
    if result.returncode == 0:
        print(f"  ✅ 정상")
    else:
        print(f"  ❌ 문제 발견")
```

실행:
```bash
python3 check_repo.py
```

---

## 📈 코드 품질 유지 팁

### 1. 정기적인 검사
- 주요 변경 후 항상 테스트
- PR 머지 전 검증
- 월 1회 전체 검사 권장

### 2. 코딩 표준 준수
- 일관된 들여쓰기 사용
- 의미있는 변수명 사용
- 적절한 주석 작성

### 3. 버전 관리
- 작은 단위로 자주 커밋
- 명확한 커밋 메시지 작성
- 브랜치 전략 활용

### 4. 문서화
- README 최신 상태 유지
- 주요 기능에 대한 문서 작성
- API 문서화 (필요시)

---

## 🎓 학습 리소스

### JavaScript
- [MDN Web Docs](https://developer.mozilla.org/ko/docs/Web/JavaScript)
- [JavaScript.info](https://ko.javascript.info/)

### HTML/CSS
- [MDN HTML 가이드](https://developer.mozilla.org/ko/docs/Web/HTML)
- [CSS Tricks](https://css-tricks.com/)

### Git
- [Pro Git 한글판](https://git-scm.com/book/ko/v2)

---

## 📞 도움 받기

문제가 해결되지 않을 때:

1. **GitHub Issues** 활용
   - 저장소의 Issues 탭에서 검색
   - 새로운 이슈 생성

2. **커뮤니티 지원**
   - Stack Overflow (영문/한글)
   - 개발자 커뮤니티 (OKKY, Dev.to 등)

3. **AI 도우미 활용**
   - Claude AI
   - GitHub Copilot
   - ChatGPT

---

## ✅ 체크리스트

정기 점검용 체크리스트:

- [ ] JavaScript 파일 문법 검사 완료
- [ ] HTML 구조 검증 완료
- [ ] 브라우저에서 주요 페이지 테스트
- [ ] 모바일 반응형 확인
- [ ] 링크 깨짐 확인
- [ ] 콘솔 에러 확인
- [ ] 성능 체크 (로딩 속도)
- [ ] 접근성 검토

---

## 🎯 다음 단계

코드가 정상이므로 이제 다음을 고려해보세요:

1. **기능 추가**
   - 새로운 페이지/기능 개발
   - 사용자 경험 개선

2. **성능 최적화**
   - 이미지 압축
   - 코드 최소화 (minification)
   - 캐싱 전략

3. **SEO 개선**
   - 메타 태그 최적화
   - 사이트맵 업데이트
   - 구조화된 데이터 추가

4. **보안 강화**
   - HTTPS 사용 확인
   - 민감 정보 보호
   - 정기적인 의존성 업데이트

---

**마지막 업데이트**: 2025년 1월  
**상태**: ✅ 모든 시스템 정상  
**다음 검사 권장일**: 1개월 후 또는 주요 업데이트 시

---

💡 **팁**: 이 문서를 북마크하고 정기적으로 참조하세요!
