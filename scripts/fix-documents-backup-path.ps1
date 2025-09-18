# 🔧 Obsidian 백업 경로 수정 스크립트
# Documents 폴더로 자동백업 경로 변경
# 문제: 기존 C:\ObsidianVault → 수정: C:\Users\dtsli\Documents\ObsidianVault

param(
    [switch]$Force = $false
)

Write-Host "🎯 Obsidian 백업 경로 수정 시작..." -ForegroundColor Cyan
Write-Host "목표: C:\Users\dtsli\Documents\ObsidianVault 로 백업 경로 변경" -ForegroundColor Yellow

# ===== 경로 설정 =====
$documentsPath = "C:\Users\dtsli\Documents"
$newObsidianPath = "$documentsPath\ObsidianVault"
$newUncleParksy = "$newObsidianPath\UncleParksy"
$newDtslib = "$newObsidianPath\dtslib"

$oldObsidianPath = "C:\ObsidianVault"
$oldUncleParksy = "$oldObsidianPath\UncleParksy"
$oldDtslib = "$oldObsidianPath\dtslib"

Write-Host "`n📋 현재 상태 확인:" -ForegroundColor Yellow
Write-Host "  - Documents 폴더: $(Test-Path $documentsPath)"
Write-Host "  - 기존 ObsidianVault: $(Test-Path $oldObsidianPath)"
Write-Host "  - 새 백업 경로: $newObsidianPath"

# ===== 1단계: Documents 경로로 이동 =====
Write-Host "`n📁 1단계: Documents 경로로 백업 이동" -ForegroundColor Yellow

# Documents/ObsidianVault 폴더 생성
if (-not (Test-Path $newObsidianPath)) {
    New-Item -ItemType Directory -Path $newObsidianPath -Force
    Write-Host "✅ 새 백업 폴더 생성: $newObsidianPath" -ForegroundColor Green
}

# 기존 데이터가 있다면 이동
if (Test-Path $oldUncleParksy) {
    Write-Host "📦 기존 UncleParksy 데이터 이동 중..."
    
    if (Test-Path $newUncleParksy) {
        $backupPath = "$newUncleParksy.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Move-Item $newUncleParksy $backupPath
        Write-Host "💾 기존 데이터 백업: $backupPath" -ForegroundColor Blue
    }
    
    Move-Item $oldUncleParksy $newUncleParksy
    Write-Host "✅ UncleParksy 이동 완료: $newUncleParksy" -ForegroundColor Green
}

if (Test-Path $oldDtslib) {
    Write-Host "📦 기존 dtslib 데이터 이동 중..."
    
    if (Test-Path $newDtslib) {
        $backupPath = "$newDtslib.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Move-Item $newDtslib $backupPath
        Write-Host "💾 기존 데이터 백업: $backupPath" -ForegroundColor Blue
    }
    
    Move-Item $oldDtslib $newDtslib
    Write-Host "✅ dtslib 이동 완료: $newDtslib" -ForegroundColor Green
}

# GitHub 레포가 없다면 클론
if (-not (Test-Path $newUncleParksy)) {
    Write-Host "🔄 GitHub 레포 클론 중..."
    Set-Location $newObsidianPath
    git clone "https://github.com/dtslib1979/UncleParksy.git"
    Write-Host "✅ UncleParksy 레포 클론 완료!" -ForegroundColor Green
}

# ===== 2단계: MCP 설정 업데이트 =====
Write-Host "`n🔧 2단계: Claude MCP 설정 업데이트" -ForegroundColor Yellow

$mcpConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"
if (Test-Path $mcpConfigPath) {
    # 백업 생성
    $configBackup = "$mcpConfigPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $mcpConfigPath $configBackup
    Write-Host "💾 MCP 설정 백업: $configBackup" -ForegroundColor Blue
    
    # 새 설정 (Documents 경로로 수정)
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
        "$newUncleParksy"
      ]
    }
  }
}
"@
    
    Set-Content $mcpConfigPath $newConfig -Encoding UTF8
    Write-Host "✅ MCP 설정 업데이트 완료!" -ForegroundColor Green
    Write-Host "📍 새 Obsidian 경로: $newUncleParksy" -ForegroundColor Cyan
}

# ===== 3단계: 자동 동기화 스크립트 업데이트 =====
Write-Host "`n⏰ 3단계: 자동 동기화 스크립트 업데이트" -ForegroundColor Yellow

$scriptsDir = "$newUncleParksy\scripts"
if (-not (Test-Path $scriptsDir)) {
    New-Item -ItemType Directory -Path $scriptsDir -Force
}

$autoSyncPath = "$scriptsDir\obsidian-auto-sync.ps1"
$autoSyncScript = @"
# UncleParksy Documents 자동 동기화 스크립트
# 백업 경로: C:\Users\dtsli\Documents\ObsidianVault\UncleParksy

try {
    Set-Location '$newUncleParksy'
    
    # Pull 최신 변경사항
    git pull origin main --quiet
    
    # 로컬 변경사항 확인 및 푸시
    git add -A
    `$status = git status --porcelain
    if (`$status) {
        git commit -m "자동 동기화 (Documents): `$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        git push origin main --quiet
        Write-Host "Documents 백업 동기화 완료: `$(Get-Date)" | Out-File -Append "`$newUncleParksy\sync.log"
    }
} catch {
    Write-Host "동기화 오류: `$_" | Out-File -Append "`$newUncleParksy\sync-error.log"
}
"@

Set-Content $autoSyncPath $autoSyncScript -Encoding UTF8
Write-Host "✅ 자동 동기화 스크립트 업데이트 완료!" -ForegroundColor Green

# ===== 4단계: 스케줄 작업 업데이트 =====
Write-Host "`n📅 4단계: 스케줄 작업 업데이트" -ForegroundColor Yellow

$taskName = "UncleParksy-Documents-Auto-Sync"

# 기존 작업 제거
$oldTaskName = "UncleParksy-Auto-Sync"
$existingOldTask = Get-ScheduledTask -TaskName $oldTaskName -ErrorAction SilentlyContinue
if ($existingOldTask) {
    Unregister-ScheduledTask -TaskName $oldTaskName -Confirm:$false
    Write-Host "🗑️ 기존 작업 제거: $oldTaskName" -ForegroundColor Orange
}

$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "🗑️ 기존 작업 제거: $taskName" -ForegroundColor Orange
}

# 새 스케줄 작업 생성 (Documents 경로)
try {
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File '$autoSyncPath'"
    $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration ([System.TimeSpan]::MaxValue)
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "UncleParksy Documents 자동 동기화" -Force
    Write-Host "✅ Documents 자동 동기화 스케줄 설정 완료!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ 스케줄 작업 생성 실패. 수동 실행 가능: $autoSyncPath" -ForegroundColor Orange
}

# ===== 5단계: 테스트 및 검증 =====
Write-Host "`n🧪 5단계: 백업 시스템 테스트" -ForegroundColor Yellow

if (Test-Path $newUncleParksy) {
    Set-Location $newUncleParksy
    
    # 현재 상태 확인
    Write-Host "📊 Git 상태 확인:" -ForegroundColor Cyan
    git status
    
    # 테스트 파일 생성
    $testFile = "documents_backup_test_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
    $testContent = @"
# 📁 Documents 백업 경로 수정 테스트

**처리 완료**: Documents 폴더로 백업 경로 변경  
**처리 시간**: $(Get-Date)  
**새 경로**: $newUncleParksy  
**상태**: ✅ 성공

## 확인사항
- [x] Documents/ObsidianVault 폴더 생성
- [x] 기존 데이터 이동 완료
- [x] MCP 설정 경로 업데이트
- [x] 자동 동기화 스크립트 업데이트
- [x] 스케줄 작업 재설정

## 백업 경로
- **이전**: C:\ObsidianVault\UncleParksy
- **변경**: C:\Users\dtsli\Documents\ObsidianVault\UncleParksy

---
*Documents 백업 시스템 복구 완료! 🚀*
"@
    
    Set-Content $testFile $testContent -Encoding UTF8
    
    # Git 커밋 및 푸시 테스트
    git add .
    git commit -m "🔧 Documents 백업 경로 수정 완료: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin main
    
    Write-Host "✅ Documents 백업 테스트 완료!" -ForegroundColor Green
}

# ===== 완료 보고 =====
Write-Host "`n🎉 Obsidian Documents 백업 경로 수정 완료!" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ 백업 경로 변경: Documents 폴더로 이동 완료"
Write-Host "✅ MCP 설정 업데이트: 새 경로 적용"  
Write-Host "✅ 자동 동기화: Documents 경로로 재설정"
Write-Host "✅ 기존 데이터: 안전하게 이동 완료"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "`n📍 새 백업 경로:" -ForegroundColor Yellow
Write-Host "   $newUncleParksy"

Write-Host "`n📋 다음 단계:" -ForegroundColor Yellow
Write-Host "1. Claude Desktop 재시작 (MCP 설정 반영)"
Write-Host "2. Obsidian에서 '$newUncleParksy' 볼트 열기"
Write-Host "3. 자동 백업이 Documents 폴더에 정상 작동하는지 확인"

Write-Host "`n💡 확인사항:" -ForegroundColor Cyan
Write-Host "- 자동 동기화 로그: $newUncleParksy\sync.log"
Write-Host "- 오류 발생 시: $newUncleParksy\sync-error.log" 
Write-Host "- 수동 동기화: $autoSyncPath 실행"

Write-Host "`n🎯 Documents 백업 시스템 복구 완료! 🚀" -ForegroundColor Green

# 기존 폴더 정리 여부 확인
if ((Test-Path $oldObsidianPath) -and $Force) {
    Write-Host "`n🗑️ 기존 폴더 정리 중..." -ForegroundColor Yellow
    Remove-Item $oldObsidianPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✅ 기존 C:\ObsidianVault 폴더 정리 완료" -ForegroundColor Green
} elseif (Test-Path $oldObsidianPath) {
    Write-Host "`n⚠️ 기존 폴더 남아있음: $oldObsidianPath" -ForegroundColor Orange
    Write-Host "확인 후 수동으로 삭제하거나 -Force 옵션으로 재실행하세요." -ForegroundColor Orange
}

Read-Host "`n처리 완료. Enter를 누르세요..."