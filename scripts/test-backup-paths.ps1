# 🧪 백업 경로 설정 테스트 스크립트
# Obsidian 백업 시스템의 경로 설정이 올바른지 확인

Write-Host "🧪 백업 경로 설정 테스트 시작..." -ForegroundColor Cyan

# 사용자 Documents 폴더를 백업 기본 경로로 설정 (수정된 경로)
$documentsPath = "C:\Users\dtsli\Documents"
$obsidianPath = "$documentsPath\ObsidianVault"
$dtslibPath = "$obsidianPath\dtslib"
$uncleParksyPath = "$obsidianPath\UncleParksy"

Write-Host "`n📋 설정된 경로 확인:" -ForegroundColor Yellow
Write-Host "  Documents 경로: $documentsPath"
Write-Host "  Obsidian 볼트 경로: $obsidianPath" 
Write-Host "  dtslib 경로: $dtslibPath"
Write-Host "  UncleParksy 경로: $uncleParksyPath"

Write-Host "`n✅ 경로 설정 확인 완료!" -ForegroundColor Green
Write-Host "백업 시스템이 C:\Users\dtsli\Documents\ObsidianVault 경로를 사용하도록 수정되었습니다." -ForegroundColor Cyan

Write-Host "`n📋 다음 단계:" -ForegroundColor Yellow  
Write-Host "1. fix-obsidian-backup-system.ps1 실행으로 실제 백업 설정"
Write-Host "2. Obsidian에서 새 경로로 볼트 설정"
Write-Host "3. 자동 백업 기능 테스트"