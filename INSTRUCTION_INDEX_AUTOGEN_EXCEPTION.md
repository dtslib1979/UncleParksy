# [작업지시서] category/system-configuration/index.html 자동 롤백(덮어쓰기) 방지 인스트럭션

## 문제 상황
- `category/system-configuration/index.html` 파일이 자동화(Actions, 스크립트) 실행 시마다 과거 상태(자동 생성본)으로 계속 덮어써집니다.
- 수동으로 직접 수정해도, 폴더 내 파일(HTML 등) 업로드/변경 시 자동화가 동작해 index.html을 롤백시킵니다.
- 원인: auto_install.py 등 자동화 스크립트와 GitHub Actions 워크플로가 폴더 내 파일 변화를 감지해 index.html을 자동 생성/복원하도록 설계되어 있음.

## 해결 방법 (구현 완료)
1. **index.html을 자동 생성/덮어쓰기 하기 전, 수동 변경본(직접 수정본)이 있는지 확인합니다.**
2. **수동 변경본이 있을 경우, 자동화에서 index.html을 절대 덮어쓰지 않습니다.**
3. **수동 변경본 판별 기준: `<!-- MANUAL EDIT -->` 마크**
   - index.html 파일 최상단에 `<!-- MANUAL EDIT -->` 마크가 있으면 자동화에서 건드리지 않습니다.

## 적용된 수정 사항
- `scripts/generate_category_index.py` 스크립트에 수동 편집본 감지 기능 추가
- `is_manual_edit()` 함수를 통해 `<!-- MANUAL EDIT -->` 마크 확인
- 수동 편집본 감지 시 자동 갱신을 건너뛰고 경고 메시지 출력

## 사용 방법
1. **수동 편집 시 반드시 다음과 같이 마크를 추가하세요:**
   ```html
   <!-- MANUAL EDIT -->
   <!doctype html><html lang='ko'><meta charset='utf-8'>
   <!-- 이하 수동으로 작성한 내용 -->
   ```

2. **자동화 실행 시 다음과 같은 메시지가 출력됩니다:**
   ```
   ⚠️ 수동 편집본 감지됨: category/system-configuration/index.html - 자동 갱신 건너뜀
   ```

## 구현된 보호 로직 (Python)
```python
def is_manual_edit(index_path):
    """
    수동 편집본인지 확인하는 함수
    파일 최상단에 <!-- MANUAL EDIT --> 마크가 있으면 수동 편집본으로 판단
    """
    if not os.path.exists(index_path):
        return False
    
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read(100)  # 처음 100자만 확인하면 충분
            return "<!-- MANUAL EDIT -->" in content
    except:
        return False

# 사용 예시
index_path = os.path.join(path, "index.html")
if is_manual_edit(index_path):
    print(f"⚠️ 수동 편집본 감지됨: {index_path} - 자동 갱신 건너뜀")
    continue
```

## 적용 프로세스
1. **수동 수정 시:** 반드시 상단에 `<!-- MANUAL EDIT -->` 주석 추가
2. **자동화 실행 시:** 해당 마크 감지 시 index.html 자동 생성/갱신을 건너뜀
3. **확인:** 자동화 로그에서 "수동 편집본 감지됨" 메시지 확인

## 보호 대상 범위
- **보호됨:** `scripts/generate_category_index.py`에 의한 자동 덮어쓰기
- **이미 안전:** 다른 모든 스크립트들(`auto_install.py`, `mobilize_archive.py` 등)은 이미 index.html 파일을 제외하고 처리

## 주의 사항
- `<!-- MANUAL EDIT -->` 마크는 HTML 파일의 **맨 첫 줄**에 추가해야 합니다.
- 마크를 제거하면 다음 자동화 실행 시 자동 생성본으로 덮어써집니다.
- 수동 편집본이라도 카테고리의 파일 개수는 home.json에 정상적으로 반영됩니다.

## 참고
- 자동화로 인한 의도치 않은 롤백 방지는 협업 및 데이터 보호에 필수적입니다.
- 관련 문의는 리포지토리 관리자에게 문의하세요.
- 이 기능은 GitHub Actions 워크플로우에서도 동일하게 작동합니다.