# ═══════════════════════════════════════════════════════════════
#  DTSLIB PLANT - Initial Setup Script
#  "플랜트 초기 설치"
# ═══════════════════════════════════════════════════════════════

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         DTSLIB PLANT - Initial Setup" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# === 설정 ===
$PLANT_ROOT = "D:\DTSLIB"

# === 디렉토리 생성 ===
Write-Host "▶ 디렉토리 구조 생성 중..." -ForegroundColor Cyan

$dirs = @(
    "$PLANT_ROOT\INBOX\voice",
    "$PLANT_ROOT\INBOX\text",
    "$PLANT_ROOT\INBOX\visual",
    "$PLANT_ROOT\INBOX\mixed",
    "$PLANT_ROOT\WORK\queue",
    "$PLANT_ROOT\WORK\processing",
    "$PLANT_ROOT\WORK\review",
    "$PLANT_ROOT\WORK\done",
    "$PLANT_ROOT\OUTPUT\parksy",
    "$PLANT_ROOT\OUTPUT\eae",
    "$PLANT_ROOT\OUTPUT\dtslib",
    "$PLANT_ROOT\PLANT",
    "$PLANT_ROOT\BACKUP"
)

foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✓ Created: $dir" -ForegroundColor Green
    }
    else {
        Write-Host "  - Exists: $dir" -ForegroundColor Gray
    }
}

# === 설정 파일 생성 ===
Write-Host ""
Write-Host "▶ 설정 파일 생성 중..." -ForegroundColor Cyan

$config = @{
    plant_root = $PLANT_ROOT
    github_repo = "C:\Users\$env:USERNAME\repos\parksy.kr"
    created_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    version = "1.0.0"
}

$config | ConvertTo-Json | Out-File "$PLANT_ROOT\PLANT\config.json" -Encoding UTF8
Write-Host "  ✓ config.json 생성됨" -ForegroundColor Green

# === 상태 파일 초기화 ===
$status = @{
    last_scan = $null
    inbox_count = 0
    processed_today = 0
    total_processed = 0
    by_domain = @{
        parksy = 0
        eae = 0
        dtslib = 0
    }
}

$status | ConvertTo-Json | Out-File "$PLANT_ROOT\PLANT\status.json" -Encoding UTF8
Write-Host "  ✓ status.json 생성됨" -ForegroundColor Green

# === 바로가기 생성 ===
Write-Host ""
Write-Host "▶ 바탕화면 바로가기 생성 중..." -ForegroundColor Cyan

$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = "$desktop\DTSLIB Plant.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoExit -File `"$PLANT_ROOT\PLANT\run_all.ps1`""
$shortcut.WorkingDirectory = $PLANT_ROOT
$shortcut.Description = "DTSLIB Production Plant"
$shortcut.Save()

Write-Host "  ✓ 바탕화면 바로가기 생성됨" -ForegroundColor Green

# === README 생성 ===
$readme = @"
# DTSLIB Production Plant

## 디렉토리 구조

\`\`\`
D:\DTSLIB\
├── INBOX\        ← 원석 투입구
│   ├── voice\    음성 메모
│   ├── text\     텍스트 메모
│   ├── visual\   이미지
│   └── mixed\    복합
│
├── WORK\         ← 작업 공간
│   ├── queue\    대기열
│   ├── processing\  처리 중
│   ├── review\   검토 대기
│   └── done\     완료
│
├── OUTPUT\       ← 결과물
│   ├── parksy\   → parksy.kr
│   ├── eae\      → eae.kr
│   └── dtslib\   → dtslib.kr
│
├── PLANT\        ← 제어 센터
│   ├── run_all.ps1
│   ├── config.json
│   └── status.json
│
└── BACKUP\       ← 백업
\`\`\`

## 사용법

1. **원석 던지기**
   - INBOX 폴더에 파일 넣기
   - 또는: \`new_source "내용..."\`

2. **처리 실행**
   - 바탕화면 "DTSLIB Plant" 클릭
   - 또는: \`run_all.ps1\`

3. **상태 확인**
   - \`run_all.ps1 -Status\`

## 생산량 = 성공의 척도

"오늘 뭐 만들까?" → "오늘 몇 톤 생산했냐?"
"@

$readme | Out-File "$PLANT_ROOT\README.md" -Encoding UTF8
Write-Host "  ✓ README.md 생성됨" -ForegroundColor Green

# === 완료 ===
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                    Setup Complete!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  플랜트 위치: $PLANT_ROOT" -ForegroundColor White
Write-Host "  바탕화면 바로가기가 생성되었습니다." -ForegroundColor White
Write-Host ""
Write-Host "  시작하려면:" -ForegroundColor Yellow
Write-Host "    1. INBOX\text 폴더에 .txt 파일 넣기" -ForegroundColor Gray
Write-Host "    2. 바탕화면의 'DTSLIB Plant' 실행" -ForegroundColor Gray
Write-Host ""
