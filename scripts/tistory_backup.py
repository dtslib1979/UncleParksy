import os, re, requests, feedparser
from datetime import datetime

RSS_URL = "https://dtslib1k.tistory.com/rss"
SAVE_DIR = "backup/raw"

def clean_filename(title):
    """파일명으로 사용할 수 없는 문자 제거"""
    return re.sub(r'[<>:"/\\|?*]', '-', title).strip('-')[:100]

def main():
    print("🔄 Tistory 백업 시작...")
    
    # RSS 파싱
    feed = feedparser.parse(RSS_URL)
    
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    new_files = 0
    
    for entry in feed.entries:
        try:
            url = entry.link
            title = clean_filename(entry.title)
            
            # 날짜 처리
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
            else:
                date = datetime.now().strftime("%Y-%m-%d")
            
            filename = f"{SAVE_DIR}/{date}-{title}.html"
            
            # 기존 파일 존재하면 스킵
            if os.path.exists(filename):
                print(f"⏭️  이미 존재: {filename}")
                continue
            
            # HTML 다운로드
            print(f"📥 다운로드 중: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.encoding = 'utf-8'
            
            # 파일 저장
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            
            print(f"✅ 저장 완료: {filename}")
            new_files += 1
            
        except Exception as e:
            print(f"❌ 에러 발생 ({entry.title}): {str(e)}")
            continue
    
    print(f"🎉 백업 완료! 새 파일: {new_files}개")

if __name__ == "__main__":
    main()