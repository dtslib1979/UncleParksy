# Obsidian 백업 경로 수정 가이드

## 문제 상황
기존 Obsidian 백업 시스템이 `C:\ObsidianVault` 경로를 사용하고 있어서 에러가 자주 발생했습니다.

## 해결책
백업 경로를 `C:\Users\dtsli\Documents\ObsidianVault`로 변경하여 Documents 폴더에 자동백업되도록 수정했습니다.

## 수정된 파일들

### 1. `scripts/fix-obsidian-backup-system.ps1`
- 백업 경로를 Documents 폴더로 변경
- MCP 설정에서 새 경로 사용

### 2. `scripts/fix-folder-rename.ps1` 
- dtslib 폴더 경로를 Documents로 변경
- 모든 경로 참조 업데이트

### 3. `scripts/fix-documents-backup-path.ps1` (새로 생성)
- Documents 폴더로 백업 시스템 완전 이전
- 기존 데이터 안전 이동
- MCP 설정 자동 업데이트
- 자동 동기화 스케줄 재설정

## 사용법

### 백업 경로 즉시 수정 (권장)
```powershell
.\scripts\fix-documents-backup-path.ps1
```

### 강제 정리 (기존 폴더 삭제)
```powershell
.\scripts\fix-documents-backup-path.ps1 -Force
```

## 변경된 경로

| 항목 | 이전 경로 | 새 경로 |
|------|-----------|---------|
| Obsidian 볼트 | `C:\ObsidianVault\UncleParksy` | `C:\Users\dtsli\Documents\ObsidianVault\UncleParksy` |
| dtslib 폴더 | `C:\ObsidianVault\dtslib` | `C:\Users\dtsli\Documents\ObsidianVault\dtslib` |
| 자동 동기화 | 15분마다 `UncleParksy-Auto-Sync` | 15분마다 `UncleParksy-Documents-Auto-Sync` |

## 완료 후 확인사항

1. **Claude Desktop 재시작** - MCP 설정 변경 반영
2. **Obsidian 볼트 재연결** - 새 경로로 볼트 열기
3. **자동 백업 확인** - Documents 폴더에 파일 생성되는지 확인
4. **동기화 로그 확인** - `sync.log` 파일에서 정상 작동 확인

## 문제 해결

### 동기화 로그 확인
```
C:\Users\dtsli\Documents\ObsidianVault\UncleParksy\sync.log
```

### 오류 로그 확인  
```
C:\Users\dtsli\Documents\ObsidianVault\UncleParksy\sync-error.log
```

### 수동 동기화 실행
```
C:\Users\dtsli\Documents\ObsidianVault\UncleParksy\scripts\obsidian-auto-sync.ps1
```

---
*🎯 Documents 백업 시스템으로 완전 전환 완료!*