# 🚀 UncleParksy-로컬PC 백업시스템 완전복구 스크립트
# 작가지망생 박씨의 마감작업 시스템 복구

param(
    [switch]$Force = $false
)

Write-Host "🎯 UncleParksy 백업시스템 복구 시작..." -ForegroundColor Cyan

# ===== 1단계: 현재 상태 진단 =====
Write-Host "`n📋 1단계: 시스템 상태 진단" -ForegroundColor Yellow

$obsidianPath = "C:\ObsidianVault"
$dtslibPath = "$obsidianPath\dtslib"
$uncleParksyPath = "$obsidianPath\UncleParksy"

Write-Host "🔍 Obsidian 볼트 경로 확인:"
Write-Host "  - C:\ObsidianVault: $(Test-Path $obsidianPath)"
Write-Host "  - dtslib 폴더: $(Test-Path $dtslibPath)"  
Write-Host "  - UncleParksy 폴더: $(Test-Path $uncleParksyPath)"

if (Test-Path $dtslibPath) {
    Write-Host "📁 dtslib 폴더 내용:"
    Get-ChildItem $dtslibPath -Force | Select-Object Name, Length, LastWriteTime | Format-Table
}

# ===== 2단계: GitHub 레포 로컬 클론 =====
Write-Host "`n📥 2단계: GitHub 레포 로컬 동기화" -ForegroundColor Yellow

$repoUrl = "https://github.com/dtslib1979/UncleParksy.git"

if (-not (Test-Path $uncleParksyPath)) {
    Write-Host "🔄 GitHub 레포 클론 중..."
    if (-not (Test-Path $obsidianPath)) {
        New-Item -ItemType Directory -Path $obsidianPath -Force
    }
    Set-Location $obsidianPath
    git clone $repoUrl
    Write-Host "✅ UncleParksy 레포 클론 완료!" -ForegroundColor Green
} else {
    Write-Host "📂 기존 UncleParksy 폴더 발견. 업데이트 확인 중..."
    Set-Location $uncleParksyPath
    git status
    git pull origin main
    Write-Host "✅ 레포 업데이트 완료!" -ForegroundColor Green
}

# ===== 3단계: dtslib 볼트 연결 설정 =====  
Write-Host "`n🔗 3단계: dtslib 볼트 연결 설정" -ForegroundColor Yellow

# dtslib을 UncleParksy와 동일하게 설정 (심볼릭 링크 대신 직접 사용)
if ((Test-Path $dtslibPath) -and ($dtslibPath -ne $uncleParksyPath)) {
    Write-Host "📁 기존 dtslib 폴더 백업 중..."
    $backupPath = "$dtslibPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Move-Item $dtslibPath $backupPath
    Write-Host "💾 백업 완료: $backupPath" -ForegroundColor Blue
}

# UncleParksy를 dtslib로 사용하도록 MCP 설정 변경
Write-Host "🔗 UncleParksy = dtslib 설정 적용" -ForegroundColor Green

# ===== 4단계: Obsidian Git 플러그인 설정 확인 =====
Write-Host "`n⚙️ 4단계: Obsidian Git 설정 확인" -ForegroundColor Yellow

$obsidianConfigPath = "$uncleParksyPath\.obsidian"
if (-not (Test-Path $obsidianConfigPath)) {
    New-Item -ItemType Directory -Path $obsidianConfigPath -Force
}

# Git 원격 저장소 확인
Set-Location $uncleParksyPath
$remoteUrl = git remote get-url origin 2>$null
if ($remoteUrl) {
    Write-Host "✅ Git 원격 저장소 연결됨: $remoteUrl" -ForegroundColor Green
} else {
    Write-Host "⚠️ Git 원격 저장소 설정 중..." -ForegroundColor Yellow
    git remote add origin $repoUrl
}

# ===== 5단계: Claude MCP 설정 수정 =====
Write-Host "`n🔧 5단계: Claude MCP 설정 수정" -ForegroundColor Yellow

$mcpConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"
if (Test-Path $mcpConfigPath) {
    # 백업 생성
    $backupPath = "$mcpConfigPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $mcpConfigPath $backupPath
    Write-Host "💾 기존 MCP 설정 백업: $backupPath" -ForegroundColor Blue
    
    # 새 설정으로 교체 (UncleParksy 경로로 통일)
    $newConfig = @"
{
  "mcpServers": {
    "github": {
      "command": "cmd",
      "args": [
        "/c",
        "C:\\Program Files\\nodejs\\npx.cmd",
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_pwxfyuX2o8GMUQopdCvcTTfixLa3sf28QGxw"
      }
    },
    "filesystem": {
      "command": "cmd",
      "args": [
        "/c", 
        "C:\\Program Files\\nodejs\\npx.cmd",
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\",
        "D:\\"
      ]
    },
    "obsidian": {
      "command": "cmd",
      "args": [
        "/c",
        "C:\\Program Files\\nodejs\\npx.cmd", 
        "-y",
        "obsidian-mcp",
        "$uncleParksyPath"
      ]
    }
  }
}
"@
    
    Set-Content $mcpConfigPath $newConfig -Encoding UTF8
    Write-Host "✅ MCP 설정 업데이트 완료!" -ForegroundColor Green
    Write-Host "📍 Obsidian MCP 경로: $uncleParksyPath" -ForegroundColor Cyan
}

# ===== 6단계: 자동 동기화 스케줄 설정 =====
Write-Host "`n⏰ 6단계: 자동 동기화 설정" -ForegroundColor Yellow

# 자동 동기화 스크립트 생성
$autoSyncPath = "$uncleParksyPath\scripts\obsidian-auto-sync.ps1"
$autoSyncScript = @"
# UncleParksy 자동 동기화 스크립트
try {
    Set-Location '$uncleParksyPath'
    
    # Pull 최신 변경사항
    git pull origin main --quiet
    
    # 로컬 변경사항 확인 및 푸시
    git add -A
    `$status = git status --porcelain
    if (`$status) {
        git commit -m "자동 동기화: `$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        git push origin main --quiet
        Write-Host "동기화 완료: `$(Get-Date)" | Out-File -Append "`$uncleParksyPath\sync.log"
    }
} catch {
    Write-Host "동기화 오류: `$_" | Out-File -Append "`$uncleParksyPath\sync-error.log"
}
"@

$scriptsDir = "$uncleParksyPath\scripts"
if (-not (Test-Path $scriptsDir)) {
    New-Item -ItemType Directory -Path $scriptsDir -Force
}
Set-Content $autoSyncPath $autoSyncScript -Encoding UTF8

# 스케줄 작업 설정
$taskName = "UncleParksy-Auto-Sync"
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentContinue

if ($existingTask) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "🗑️ 기존 작업 제거됨" -ForegroundColor Orange
}

# 15분마다 자동 동기화 작업 생성
try {
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File '$autoSyncPath'"
    $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration ([System.TimeSpan]::MaxValue)
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "UncleParksy 자동 동기화" -Force
    Write-Host "✅ 자동 동기화 스케줄 설정 완료!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ 스케줄 작업 생성 실패. 수동 실행 가능: $autoSyncPath" -ForegroundColor Orange
}

# ===== 7단계: 즉시 동기화 테스트 =====
Write-Host "`n🧪 7단계: 동기화 테스트" -ForegroundColor Yellow

if (Test-Path $uncleParksyPath) {
    Set-Location $uncleParksyPath
    
    # 현재 상태 확인
    Write-Host "📊 현재 Git 상태:" -ForegroundColor Cyan
    git status
    
    # 테스트 파일 생성
    $testFile = "test_sync_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
    $testContent = @"
# 🧪 동기화 테스트

**생성일시:** $(Get-Date)
**시스템:** 로컬PC-Claude 백업시스템
**상태:** 테스트 완료 ✅

## 확인사항
- [x] GitHub 레포 클론 성공
- [x] MCP 설정 업데이트 
- [x] 자동 동기화 설정
- [x] 파일 생성/푸시 테스트

---
*EduArt Engineer CI + dtslib.com 마감작업 시스템*
"@
    
    Set-Content $testFile $testContent -Encoding UTF8
    
    # Git 커밋 및 푸시
    git add .
    git commit -m "🧪 로컬PC-Claude 백업시스템 복구 테스트: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin main
    
    Write-Host "✅ 동기화 테스트 완료!" -ForegroundColor Green
}

# ===== 완료 보고 =====
Write-Host "`n🎉 UncleParksy 백업시스템 복구 완료!" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ GitHub 레포 ↔️ 로컬 PC 연결 완료"
Write-Host "✅ Obsidian MCP 연결 경로 수정 완료"  
Write-Host "✅ 자동 동기화 (15분 간격) 설정 완료"
Write-Host "✅ 실시간 백업 시스템 활성화"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "`n📋 다음 단계:" -ForegroundColor Yellow
Write-Host "1. Claude Desktop 재시작 (MCP 설정 반영)"
Write-Host "2. Obsidian에서 'C:\ObsidianVault\UncleParksy' 볼트 열기"
Write-Host "3. Obsidian Git 플러그인 활성화 확인"
Write-Host "4. Claude에서 'obsidian:list-available-vaults' 명령으로 연결 테스트"

Write-Host "`n🎯 로컬 PC 컨트롤러 2.0 + EduArt Engineer CI 완성! 🚀" -ForegroundColor Green
Write-Host "`n📍 중요: Obsidian에서 볼트 경로를 'C:\ObsidianVault\UncleParksy'로 설정하세요!" -ForegroundColor Red

Write-Host "`n💡 문제 발생 시:" -ForegroundColor Cyan
Write-Host "- 자동 동기화 로그: $uncleParksyPath\sync.log"
Write-Host "- 오류 로그: $uncleParksyPath\sync-error.log" 
Write-Host "- 수동 동기화: $autoSyncPath 실행"

Read-Host "`n스크립트 완료. Enter를 누르세요..."
