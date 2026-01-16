# ═══════════════════════════════════════════════════════════════
#  DTSLIB PLANT - New Source Creator
#  "원석 빠르게 던지기"
# ═══════════════════════════════════════════════════════════════

param(
    [Parameter(Position=0)]
    [string]$Content,

    [string]$Type = "text",    # text, voice, visual, mixed
    [string]$Mood,             # excited, calm, frustrated, curious
    [string]$Domain,           # parksy, eae, dtslib
    [switch]$Edit              # 메모장에서 편집
)

$INBOX = "D:\DTSLIB\INBOX"

# ID 생성
$date = Get-Date -Format "yyyyMMdd"
$existing = Get-ChildItem -Path "$INBOX\$Type" -Filter "src-$date-*.txt" -ErrorAction SilentlyContinue
$seq = ($existing.Count + 1).ToString("000")
$sourceId = "src-$date-$seq"

# 파일 경로
$filePath = "$INBOX\$Type\$sourceId.txt"

# 콘텐츠 작성
if ($Edit) {
    # 메모장에서 편집
    $template = @"
# 원석 ID: $sourceId
# 생성: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# 타입: $Type
$(if ($Mood) { "# 감정: $Mood" })
$(if ($Domain) { "# 힌트: $Domain" })

---

여기에 내용을 작성하세요...

"@
    $template | Out-File -FilePath $filePath -Encoding UTF8
    notepad $filePath
    Write-Host "✨ 편집 완료 후 저장하세요: $filePath" -ForegroundColor Yellow
}
elseif ($Content) {
    # 직접 입력
    $header = @"
# 원석 ID: $sourceId
# 생성: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# 타입: $Type
$(if ($Mood) { "# 감정: $Mood" })
$(if ($Domain) { "# 힌트: $Domain" })

---

$Content
"@
    $header | Out-File -FilePath $filePath -Encoding UTF8
    Write-Host "✨ 원석 생성됨: $sourceId" -ForegroundColor Green
    Write-Host "   경로: $filePath" -ForegroundColor Gray
}
else {
    # 클립보드에서 가져오기
    $clipboard = Get-Clipboard
    if ($clipboard) {
        $header = @"
# 원석 ID: $sourceId
# 생성: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# 타입: $Type
# 소스: clipboard

---

$clipboard
"@
        $header | Out-File -FilePath $filePath -Encoding UTF8
        Write-Host "✨ 클립보드에서 원석 생성됨: $sourceId" -ForegroundColor Green
    }
    else {
        Write-Host "❌ 내용이 필요합니다." -ForegroundColor Red
        Write-Host ""
        Write-Host "사용법:" -ForegroundColor Yellow
        Write-Host "  new_source '내용...'"
        Write-Host "  new_source -Edit           # 메모장에서 편집"
        Write-Host "  new_source -Type voice     # 음성 타입"
        Write-Host "  new_source -Mood excited   # 감정 추가"
        Write-Host "  new_source -Domain eae     # 도메인 힌트"
    }
}
