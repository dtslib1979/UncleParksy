# Tistory Blog Backup

이 폴더에는 https://dtslib1k.tistory.com의 자동 백업된 HTML 파일들이 저장됩니다.

## 자동화 시스템
- **실행 주기**: 6시간마다
- **파일명 형식**: `YYYY-MM-DD-제목.html`
- **백업 범위**: RSS에 포함된 모든 글의 전체 HTML

## KR TextStory 아카이브 연동
- 이 백업 파일들은 `/archive/backup/`으로 자동 미러링됩니다
- `assets/manifest.json` 매니페스트 자동 생성
- 보물 서류철 디자인의 웹 인터페이스로 제공

## 수동 실행
GitHub Actions → "Build KR TextStory Archive" → "Run workflow"

---
*자동 생성된 백업 파일들 - KR TextStory Archive 시스템과 연동*
