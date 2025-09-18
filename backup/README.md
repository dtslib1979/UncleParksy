# 🎯 UncleParksy Obsidian Backup System

옵시디언 설정에 맞춘 완전한 백업 시스템 구현 완료!

## 🚀 시스템 개요

이 백업 시스템은 `fix-obsidian-backup-system.ps1`에서 설정한 Obsidian 볼트를 완전 자동화로 백업합니다.

### 주요 기능

- 🔄 **자동 티스토리 백업** - RSS 기반 콘텐츠 동기화
- 📦 **아카이브 미러링** - backup/raw → archive 자동 복사
- 📱 **모바일 최적화** - HTML 정리 및 모바일 친화적 변환
- ⚙️ **Obsidian 설정 백업** - 볼트 구성 및 플러그인 설정
- 📸 **볼트 스냅샷** - 전체 구조 및 파일 정보 기록
- 🔍 **백업 검증** - 무결성 확인 및 상태 모니터링
- 📊 **HTML 대시보드** - 시각적 상태 확인

## 📁 디렉토리 구조

```
UncleParksy/
├── backup/
│   ├── raw/                 # 티스토리 원본 HTML 파일
│   ├── json/               # 백업 메타데이터 및 설정
│   ├── snapshots/          # 볼트 구조 스냅샷
│   └── *.log               # 백업 로그 파일
├── _obsidian/
│   └── _imports/
│       ├── html_md/        # Markdown 변환 파일
│       └── html_raw/       # HTML 원본 분류
├── archive/                # 최종 아카이브 (미러링됨)
└── scripts/                # 백업 스크립트들
    ├── backup_automation.py      # 🎯 메인 자동화 스크립트
    ├── obsidian_full_backup.py   # 전체 백업 실행
    ├── backup_validator.py       # 백업 검증 및 대시보드
    ├── scheduled_backup.py       # 예약 백업 관리
    ├── tistory_backup.py         # 티스토리 RSS 백업
    ├── mirror_backup.py          # 아카이브 미러링
    └── clean_and_mobilize.py     # 모바일 최적화
```

## 🎯 사용법

### 1. 메인 자동화 스크립트 (권장)

```bash
# 대화형 메뉴
python scripts/backup_automation.py

# 전체 백업 실행
python scripts/backup_automation.py --full

# 백업 상태 확인
python scripts/backup_automation.py --status

# 백업 검증만 실행
python scripts/backup_automation.py --validate
```

### 2. 개별 스크립트 실행

```bash
# 전체 백업 (모든 구성요소 포함)
python scripts/obsidian_full_backup.py

# 백업 검증 및 대시보드 생성
python scripts/backup_validator.py

# 예약된 백업 작업
python scripts/scheduled_backup.py --mode=auto

# 티스토리만 백업
python scripts/tistory_backup.py
```

## ⚙️ 설정 연동

### Obsidian 볼트 경로
- **Windows**: `C:\ObsidianVault\UncleParksy`
- **MCP 연동**: Claude Desktop + GitHub 서버
- **Git 원격**: https://github.com/dtslib1979/UncleParksy

### 자동화 스케줄
- **전체 백업**: 24시간마다
- **검증**: 6시간마다
- **빠른 동기화**: 2시간마다
- **정리 작업**: 30일 이상 된 파일 자동 삭제

## 📊 모니터링

### 상태 대시보드
백업 완료 후 `backup/backup_status_dashboard.html`에서 상태 확인:
- 📁 각 디렉토리별 파일 수 및 크기
- ⏰ 마지막 백업 시간
- 🔍 무결성 검증 결과
- 📈 백업 트렌드 및 통계

### 로그 파일
- `backup/scheduled_backup.log` - 예약 백업 로그
- `backup.log` - 일반 백업 로그
- JSON 매니페스트 파일들 - 상세 백업 기록

## 🔧 백업 구성요소

### 1. 티스토리 백업 (`tistory_backup.py`)
- RSS 피드에서 새 글 자동 감지
- HTML 파일로 다운로드 및 저장
- 파일명: `YYYY-MM-DD-제목.html` 형식

### 2. 아카이브 미러링 (`mirror_backup.py`)
- `backup/raw/` → `archive/` 디렉토리 동기화
- 수정된 파일만 선택적 복사
- 중복 방지 및 증분 백업

### 3. 모바일 최적화 (`clean_and_mobilize.py`)
- 티스토리 HTML에서 불필요한 요소 제거
- 모바일 친화적 CSS 적용
- 가독성 향상 및 용량 최적화

### 4. Obsidian 설정 백업
- `.obsidian/` 디렉토리 구조 백업
- 플러그인 설정 및 워크스페이스 보존
- JSON 형태로 메타데이터 저장

### 5. 볼트 스냅샷
- 전체 파일 구조 및 통계 기록
- 체크섬 기반 무결성 확인
- 복원 가능한 상태 정보 보존

## 🚀 다음 단계 (PowerShell 설정과 연동)

1. **Claude Desktop 재시작** - MCP 설정 반영
2. **Obsidian 볼트 경로 확인** - `C:\ObsidianVault\UncleParksy`
3. **MCP 연결 테스트** - `obsidian:list-available-vaults`
4. **Git 동기화 확인** - 자동 커밋/푸시 작동 여부
5. **예약 작업 설정** - 시스템 스케줄러에 등록

## 📞 문제 해결

### 일반적인 문제
1. **파이썬 패키지 누락**
   ```bash
   pip install requests feedparser beautifulsoup4
   ```

2. **권한 문제**
   - Windows: PowerShell을 관리자 권한으로 실행
   - 스크립트 실행 정책 확인

3. **MCP 연결 실패**
   - Claude Desktop 재시작
   - `claude_desktop_config.json` 설정 확인

4. **백업 파일 누락**
   - 티스토리 RSS URL 접근 가능 여부 확인
   - 네트워크 연결 상태 점검

### 로그 확인
```bash
# 최근 백업 로그 확인
tail -f backup/scheduled_backup.log

# 백업 상태 검증
python scripts/backup_validator.py
```

## 📋 백업 체크리스트

- [x] 티스토리 RSS 백업 자동화
- [x] 아카이브 미러링 구현
- [x] 모바일 최적화 처리
- [x] Obsidian 설정 백업 (시뮬레이션)
- [x] 볼트 스냅샷 생성
- [x] 백업 검증 시스템
- [x] HTML 대시보드 구현
- [x] 예약 백업 관리자
- [x] 통합 자동화 스크립트
- [x] 로깅 및 모니터링
- [x] 오류 처리 및 복구

---

*🚀 로컬PC 컨트롤러 2.0 + EduArt Engineer CI 백업 시스템 완성!*

**Made with ❤️ by 작가지망생 박씨 & Claude AI**
