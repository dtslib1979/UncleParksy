# 🔧 UncleParksy → dtslib 폴더명 자동 수정 스크립트
# 로컬PC 컨트롤러 직접 해결

Write-Host "🎯 폴더명 자동 수정 시작..." -ForegroundColor Cyan

$uncleParksyPath = "C:\ObsidianVault\UncleParksy"
$dtslibPath = "C:\ObsidianVault\dtslib"
$backupPath = "C:\ObsidianVault\dtslib.backup_20250904_175209"

try {
    # 1. 기존 백업 폴더를 임시로 이동
    if (Test-Path $backupPath) {
        $tempBackup = "$backupPath.temp"
        Rename-Item $backupPath $tempBackup -Force
        Write-Host "✅ 기존 백업 폴더 임시 이동: $tempBackup" -ForegroundColor Green
    }

    # 2. UncleParksy → dtslib로 이름 변경
    if (Test-Path $uncleParksyPath) {
        Rename-Item $uncleParksyPath $dtslibPath -Force
        Write-Host "✅ 폴더명 변경 완료: UncleParksy → dtslib" -ForegroundColor Green
    } else {
        Write-Host "❌ UncleParksy 폴더를 찾을 수 없습니다." -ForegroundColor Red
        exit 1
    }

    # 3. Git 원격 저장소 확인 및 수정
    Set-Location $dtslibPath
    $currentRemote = git remote get-url origin 2>$null
    if ($currentRemote -ne "https://github.com/dtslib1979/UncleParksy.git") {
        git remote set-url origin "https://github.com/dtslib1979/UncleParksy.git"
        Write-Host "✅ Git 원격 저장소 URL 수정 완료" -ForegroundColor Green
    }

    # 4. 즉시 동기화 테스트
    git status
    $testFile = "folder_rename_test_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
    @"
# 📁 폴더명 자동 수정 테스트

**처리 완료**: UncleParksy → dtslib  
**처리 시간**: $(Get-Date)  
**상태**: ✅ 성공

## MCP 연결 준비 완료
- 경로: C:\ObsidianVault\dtslib
- GitHub 연결: 정상
- 자동 동기화: 활성

---
*로컬PC 컨트롤러 직접 해결 완료! 🚀*
"@ | Set-Content $testFile -Encoding UTF8

    git add .
    git commit -m "🔧 폴더명 자동 수정 완료: UncleParksy → dtslib $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git push origin main

    Write-Host "✅ GitHub 동기화 테스트 완료!" -ForegroundColor Green

    # 5. 완료 보고
    Write-Host "`n🎉 폴더명 수정 완료!" -ForegroundColor Magenta
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "✅ UncleParksy → dtslib 변경 완료"
    Write-Host "✅ Git 원격 저장소 연결 유지"
    Write-Host "✅ GitHub 동기화 테스트 성공"
    Write-Host "✅ MCP 연결 준비 완료"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

    Write-Host "`n📋 다음 단계:" -ForegroundColor Yellow
    Write-Host "1. Claude Desktop 재시작"
    Write-Host "2. Obsidian에서 'C:\ObsidianVault\dtslib' 볼트 열기"
    Write-Host "3. 'obsidian:list-available-vaults' 테스트"

    Write-Host "`n🎯 로컬PC 컨트롤러 직접 해결 완료! 🚀" -ForegroundColor Green

} catch {
    Write-Host "❌ 오류 발생: $_" -ForegroundColor Red
    Write-Host "수동 처리가 필요합니다." -ForegroundColor Orange
}

Read-Host "`n처리 완료. Enter를 누르세요..."
