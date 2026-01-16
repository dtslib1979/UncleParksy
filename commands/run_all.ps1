# ═══════════════════════════════════════════════════════════════
#  DTSLIB PLANT - Master Control Script
#  "버튼 하나로 모든 것을 실행"
# ═══════════════════════════════════════════════════════════════

param(
    [switch]$Scan,      # 스캔만
    [switch]$Process,   # 처리만
    [switch]$Publish,   # 출판만
    [switch]$Status,    # 상태만
    [switch]$All        # 전체 (기본값)
)

$ErrorActionPreference = "Stop"

# === 설정 ===
$PLANT_ROOT = "D:\DTSLIB"
$INBOX = "$PLANT_ROOT\INBOX"
$WORK = "$PLANT_ROOT\WORK"
$OUTPUT = "$PLANT_ROOT\OUTPUT"
$GITHUB_REPO = "C:\Users\$env:USERNAME\repos\parksy.kr"  # GitHub 레포 경로

# === 색상 출력 ===
function Write-Step($msg) { Write-Host "▶ $msg" -ForegroundColor Cyan }
function Write-OK($msg) { Write-Host "✓ $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "⚠ $msg" -ForegroundColor Yellow }
function Write-Err($msg) { Write-Host "✗ $msg" -ForegroundColor Red }

# === 배너 ===
function Show-Banner {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor DarkCyan
    Write-Host "         DTSLIB PRODUCTION PLANT - Control Center" -ForegroundColor White
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor DarkCyan
    Write-Host ""
}

# === 디렉토리 확인 ===
function Ensure-Directories {
    Write-Step "디렉토리 확인 중..."

    $dirs = @(
        "$INBOX\voice",
        "$INBOX\text",
        "$INBOX\visual",
        "$INBOX\mixed",
        "$WORK\queue",
        "$WORK\processing",
        "$WORK\review",
        "$WORK\done",
        "$OUTPUT\parksy",
        "$OUTPUT\eae",
        "$OUTPUT\dtslib"
    )

    foreach ($dir in $dirs) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }

    Write-OK "디렉토리 준비 완료"
}

# === 인박스 스캔 ===
function Scan-Inbox {
    Write-Step "인박스 스캔 중..."

    $files = @()
    $extensions = @("*.txt", "*.md", "*.m4a", "*.mp3", "*.wav", "*.png", "*.jpg")

    foreach ($ext in $extensions) {
        $found = Get-ChildItem -Path $INBOX -Recurse -Filter $ext -File
        $files += $found
    }

    $count = $files.Count
    Write-OK "발견된 원석: $count 개"

    if ($count -gt 0) {
        Write-Host ""
        foreach ($f in $files) {
            $relPath = $f.FullName.Replace($INBOX, "").TrimStart("\")
            Write-Host "  📄 $relPath" -ForegroundColor Gray
        }
    }

    return $files
}

# === 처리 실행 ===
function Invoke-Processing {
    Write-Step "Claude Code 처리 실행 중..."

    # Python factory.py 실행
    $pythonScript = Join-Path $GITHUB_REPO "scripts\factory.py"

    if (Test-Path $pythonScript) {
        Push-Location $GITHUB_REPO
        try {
            # 인박스 파일들을 GitHub 레포 inbox로 복사
            $sourceFiles = Get-ChildItem -Path "$INBOX\text" -Filter "*.txt" -File
            foreach ($f in $sourceFiles) {
                Copy-Item $f.FullName -Destination "$GITHUB_REPO\inbox\text\" -Force
            }

            # factory.py 실행
            python $pythonScript process

            Write-OK "처리 완료"
        }
        catch {
            Write-Err "처리 실패: $_"
        }
        finally {
            Pop-Location
        }
    }
    else {
        Write-Warn "factory.py를 찾을 수 없습니다: $pythonScript"
    }
}

# === 출판 ===
function Invoke-Publishing {
    Write-Step "출판 및 커밋 중..."

    Push-Location $GITHUB_REPO
    try {
        # 처리된 원석 찾기
        $doneFiles = Get-ChildItem -Path "$GITHUB_REPO\process\done" -Filter "*.json" -File

        foreach ($f in $doneFiles) {
            $sourceId = $f.BaseName
            python "$GITHUB_REPO\scripts\factory.py" publish $sourceId
        }

        # Git 커밋
        git add -A
        $changes = git status --porcelain
        if ($changes) {
            $date = Get-Date -Format "yyyy-MM-dd HH:mm"
            git commit -m "auto: plant production $date"
            git push

            Write-OK "커밋 및 푸시 완료"
        }
        else {
            Write-Warn "변경사항 없음"
        }
    }
    catch {
        Write-Err "출판 실패: $_"
    }
    finally {
        Pop-Location
    }
}

# === 상태 표시 ===
function Show-Status {
    Write-Step "플랜트 상태"
    Write-Host ""

    # 인박스
    $inboxCount = (Get-ChildItem -Path $INBOX -Recurse -File).Count
    Write-Host "  📥 인박스: $inboxCount 개" -ForegroundColor White

    # 작업중
    $workCount = (Get-ChildItem -Path "$WORK\queue" -File -ErrorAction SilentlyContinue).Count
    Write-Host "  ⚙️  대기열: $workCount 개" -ForegroundColor White

    # 완료
    $doneCount = (Get-ChildItem -Path "$WORK\done" -File -ErrorAction SilentlyContinue).Count
    Write-Host "  ✓ 처리됨: $doneCount 개" -ForegroundColor White

    Write-Host ""
    Write-Host "  📤 출력:" -ForegroundColor White

    $domains = @("parksy", "eae", "dtslib")
    foreach ($d in $domains) {
        $count = (Get-ChildItem -Path "$OUTPUT\$d" -File -ErrorAction SilentlyContinue).Count
        $bar = "█" * [Math]::Min($count, 20)
        Write-Host "     $($d.PadRight(8)) [$bar] $count" -ForegroundColor Gray
    }

    Write-Host ""
}

# === 메인 실행 ===
Show-Banner
Ensure-Directories

if ($Status -or (!$Scan -and !$Process -and !$Publish -and !$All)) {
    Show-Status
}

if ($Scan -or $All) {
    $files = Scan-Inbox
}

if ($Process -or $All) {
    Invoke-Processing
}

if ($Publish -or $All) {
    Invoke-Publishing
}

if ($All) {
    Show-Status
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor DarkCyan
Write-Host "                    Production Complete" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor DarkCyan
Write-Host ""
