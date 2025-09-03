#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 Mobile CSS Optimizer for Archive Files
Adds inline mobile-friendly CSS to archive HTML files to avoid GitHub Pages path issues.
"""

import os
import re
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_mobile_css():
    """📱 Return the mobile-optimized CSS for archive files"""
    return '''
/* Mobile-optimized CSS for archive files */
html {
  font-size: 16px;
  -webkit-text-size-adjust: 100%;
  -webkit-tap-highlight-color: transparent;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #333;
  background: #f7f5ef;
}

/* Responsive images */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1rem auto;
}

/* Mobile-friendly layout */
@media (max-width: 768px) {
  body {
    padding: 0 16px;
    font-size: 14px;
    line-height: 1.5;
  }
  
  /* 헤더 모바일 최적화 */
  .site-header, header {
    flex-wrap: wrap;
    align-items: flex-start;
    padding: 12px 16px;
    padding-left: max(16px, env(safe-area-inset-left));
    padding-right: max(16px, env(safe-area-inset-right));
  }
  
  /* 네비게이션 모바일 최적화 */
  .nav, nav {
    display: flex;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
    width: 100%;
  }
  
  .nav a, nav a {
    margin-left: 0;
    flex: 0 0 auto;
    padding: 8px 10px;
    display: inline-block;
  }
  
  /* 콘텐츠 영역 */
  .container, .content, main {
    max-width: 100%;
    padding: 0 16px;
    margin: 0 auto;
  }
  
  /* 카드/박스 요소들 */
  .card, .box, .widget {
    margin: 16px 0;
    padding: 16px;
    border-radius: 12px;
  }
  
  /* 텍스트 가독성 */
  h1, h2, h3, h4, h5, h6 {
    line-height: 1.3;
    margin: 1.5rem 0 1rem;
  }
  
  h1 { font-size: 1.8rem; }
  h2 { font-size: 1.6rem; }
  h3 { font-size: 1.4rem; }
  h4 { font-size: 1.2rem; }
  
  p {
    margin: 1rem 0;
    line-height: 1.6;
  }
  
  /* 리스트 요소 */
  ul, ol {
    margin: 1rem 0;
    padding-left: 2rem;
  }
  
  li {
    margin: 0.5rem 0;
  }
  
  /* 테이블 반응형 */
  table {
    width: 100%;
    display: block;
    overflow-x: auto;
    white-space: nowrap;
    font-size: 14px;
  }
  
  /* 버튼 터치 최적화 */
  button, .btn, input[type="button"], input[type="submit"] {
    min-height: 44px;
    padding: 12px 20px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
  }
  
  /* 폼 요소 */
  input, textarea, select {
    width: 100%;
    padding: 12px;
    font-size: 16px; /* iOS 줌 방지 */
    border: 1px solid #ddd;
    border-radius: 8px;
    box-sizing: border-box;
  }
  
  /* 검색 폼 */
  form[role="search"] {
    width: 100%;
    margin: 16px 0;
  }
  
  form[role="search"] input {
    width: calc(100% - 32px);
    margin: 8px 16px 0;
    padding: 12px 14px;
    border: 1px solid rgba(0,0,0,.25);
    border-radius: 999px;
    background: #fff;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
  }
  
  form[role="search"] input:focus {
    outline: none;
    border-color: #caa24b;
    box-shadow: 0 3px 14px rgba(202,162,75,.25);
  }
  
  /* 링크 터치 영역 확대 */
  a {
    min-height: 44px;
    display: inline-block;
    text-decoration: none;
  }
  
  a:hover, a:focus {
    text-decoration: underline;
  }
  
  /* 사이드바 요소들 */
  .sidebar, aside {
    margin: 20px 0;
  }
  
  .widget {
    margin: 16px 0;
    padding: 16px;
    background: #fff;
    border: 1px solid #eee;
    border-radius: 12px;
  }
}

/* 초소형 화면 (320px 이하) */
@media (max-width: 320px) {
  body {
    font-size: 13px;
    padding: 0 12px;
  }
  
  .container, .content, main {
    padding: 0 12px;
  }
  
  h1 { font-size: 1.6rem; }
  h2 { font-size: 1.4rem; }
  h3 { font-size: 1.2rem; }
  h4 { font-size: 1.1rem; }
}

/* 다크 모드 대응 */
@media (prefers-color-scheme: dark) {
  body {
    background: #1a1a1a;
    color: #e0e0e0;
  }
  
  .widget, .card, .box {
    background: #2a2a2a;
    border-color: #404040;
  }
  
  input, textarea, select {
    background: #2a2a2a;
    color: #e0e0e0;
    border-color: #404040;
  }
}

/* 애니메이션 줄이기 설정 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
'''

def has_mobile_css(html_content):
    """Check if the HTML already has mobile CSS"""
    return 'Mobile-optimized CSS for archive files' in html_content

def add_mobile_css_to_html(html_content):
    """Add inline mobile CSS to HTML content"""
    if has_mobile_css(html_content):
        logger.info("모바일 CSS가 이미 존재합니다. 건너뜀.")
        return html_content
    
    # Get the mobile CSS
    mobile_css = get_mobile_css()
    
    # Create the style tag
    style_tag = f'<style type="text/css">{mobile_css}</style>'
    
    # Find the best place to insert the CSS (preferably in <head>)
    if '<head>' in html_content and '</head>' in html_content:
        # Insert before closing head tag
        html_content = html_content.replace('</head>', f'{style_tag}\n</head>')
    elif '<head' in html_content:
        # Find end of opening head tag and insert after
        head_end = html_content.find('>', html_content.find('<head'))
        if head_end != -1:
            html_content = html_content[:head_end + 1] + f'\n{style_tag}' + html_content[head_end + 1:]
    else:
        # Fallback: insert at the beginning of the document after <!DOCTYPE>
        if '<!DOCTYPE' in html_content:
            doctype_end = html_content.find('>', html_content.find('<!DOCTYPE'))
            if doctype_end != -1:
                html_content = html_content[:doctype_end + 1] + f'\n{style_tag}' + html_content[doctype_end + 1:]
        else:
            # Last resort: prepend to document
            html_content = f'{style_tag}\n' + html_content
    
    return html_content

def process_archive_files():
    """Process all HTML files in the archive directory"""
    archive_dir = Path("archive")
    
    if not archive_dir.exists():
        logger.error("❌ Archive 디렉토리를 찾을 수 없습니다.")
        return 0
    
    html_files = list(archive_dir.glob("*.html"))
    # Exclude index.html as it's usually a directory listing
    html_files = [f for f in html_files if f.name != "index.html"]
    
    if not html_files:
        logger.warning("⚠️ 처리할 HTML 파일이 없습니다.")
        return 0
    
    processed_count = 0
    
    for html_file in html_files:
        try:
            logger.info(f"📱 처리 중: {html_file.name}")
            
            # Read the file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add mobile CSS
            updated_content = add_mobile_css_to_html(content)
            
            # Write back if changed
            if updated_content != content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                processed_count += 1
                logger.info(f"✅ 모바일 CSS 추가됨: {html_file.name}")
            else:
                logger.info(f"⏭️ 이미 처리됨: {html_file.name}")
                
        except Exception as e:
            logger.error(f"❌ 처리 실패 {html_file.name}: {e}")
    
    return processed_count

def main():
    """Main execution function"""
    logger.info("📱 아카이브 파일 모바일 최적화 시작...")
    
    try:
        processed_count = process_archive_files()
        
        if processed_count > 0:
            logger.info(f"🎉 성공적으로 {processed_count}개 파일에 모바일 CSS 추가됨")
            print(f"Successfully processed {processed_count} archive HTML files")
        else:
            logger.info("ℹ️ 처리할 새 파일이 없습니다.")
            print("No new files to process - all archive files already optimized")
            
        return 0
        
    except Exception as e:
        logger.error(f"❌ 실행 실패: {e}")
        return 1

if __name__ == "__main__":
    exit(main())