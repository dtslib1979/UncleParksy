#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹📱 Clean and Mobilize Archive Pipeline
Extracts main content from Tistory backup HTML and rebuilds with clean mobile template.

Workflow:
1. Scan backup/raw/ or archive/ for input files
2. Extract content using priority selectors
3. Replace with minimal mobile-optimized template
4. Save to archive/ directory maintaining structure
"""

import os
import re
from pathlib import Path
import logging
from bs4 import BeautifulSoup

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_mini_template():
    """Return the minimal mobile template with placeholders"""
    return '''<!doctype html><html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{{TITLE}}</title>
<style>
html{box-sizing:border-box}*,*:before,*:after{box-sizing:inherit}
body{margin:0;font-size:16px;line-height:1.7;word-break:keep-all;background:#f4e5c9;color:#2b2116}
main{max-width:880px;margin:0 auto;padding:18px}
img,video,iframe{max-width:100%;height:auto}
[class*="wrap"],[class*="container"],[id*="content"]{max-width:100%!important;width:auto!important;margin:0!important;padding:0!important}
.grid,.row{display:block!important}.sidebar{display:none!important}.content,.main{width:100%!important}
table{display:block;width:100%;overflow-x:auto;border-collapse:collapse}
pre,code{white-space:pre-wrap;word-wrap:break-word}
h1{font-size:1.5rem;margin:.8rem 0} h2{font-size:1.25rem;margin:.7rem 0}
.card{background:#fff8ea;border:1px solid rgba(0,0,0,.06);border-radius:14px;padding:14px;margin:10px 0}
</style>
</head><body><main>
<article class="card">
<h1>{{TITLE}}</h1>
{{CONTENT}}
</article>
<footer style="opacity:.7;font-size:.9rem;margin:16px 0">© Uncle Parksy Korean Learning Archive</footer>
</main></body></html>'''

def extract_title(soup, filename):
    """Extract title from content or filename"""
    # Try to get title from HTML title tag first
    title_tag = soup.find('title')
    if title_tag and title_tag.get_text(strip=True):
        title = title_tag.get_text(strip=True)
        # Clean up Tistory blog title if present
        if ' :: ' in title:
            title = title.split(' :: ')[0]
        return title
    
    # Try to get title from first h1 tag in content
    h1_tag = soup.find('h1')
    if h1_tag and h1_tag.get_text(strip=True):
        return h1_tag.get_text(strip=True)
    
    # Fall back to filename-based title
    filename_stem = Path(filename).stem
    # Remove date pattern if present (e.g., 2025-08-25-)
    title = re.sub(r'^[\d-]+[-\s]*', '', filename_stem)
    title = title.replace('-', ' ').replace('_', ' ')
    return title.strip() or '제목 없음'

def extract_content_by_selectors(soup):
    """Extract content using priority selectors"""
    
    # Priority 1: .tt_article_useless_p_margin.contents_style
    primary_selector = soup.select('.tt_article_useless_p_margin.contents_style')
    if primary_selector:
        logger.info("✅ Found primary selector: .tt_article_useless_p_margin.contents_style")
        
        # Check if this contains a nested HTML document
        content_text = str(primary_selector[0])
        if '<!DOCTYPE' in content_text or content_text.strip().startswith('<html'):
            # Parse the nested document and extract the meaningful content
            nested_soup = BeautifulSoup(content_text, 'lxml')
            
            # Look for main QA content first
            qa_main = nested_soup.find('main', id='qa')
            if qa_main:
                logger.info("📄 Found QA main section in nested document")
                return qa_main
            
            # Look for other main content
            main_elem = nested_soup.find('main')
            if main_elem:
                logger.info("📄 Found main section in nested document")
                return main_elem
                
            # Fall back to body of nested document
            if nested_soup.body:
                logger.info("📄 Using body of nested document")
                return nested_soup.body
        
        return primary_selector[0]
    
    # Priority 2: #article-view content
    article_view = soup.find('div', id='article-view')
    if article_view:
        logger.info("✅ Found secondary selector: #article-view")
        # Look for content within article-view that isn't scripts/meta
        content_div = article_view.find('div', class_=['tt_article_useless_p_margin', 'contents_style'])
        if content_div:
            return content_div
        # If no specific content div, take the whole article-view but clean it
        return article_view
    
    # Priority 3: Fallback selectors - find the one with most text
    fallback_selectors = [
        'article',
        '.article', 
        '#content-inner',
        'main',
        '.main-content',
        '#main-content',
        '.post-content',
        '#post-content'
    ]
    
    best_element = None
    best_text_length = 0
    
    for selector in fallback_selectors:
        elements = soup.select(selector) if selector.startswith('.') or selector.startswith('#') else soup.find_all(selector)
        for element in elements:
            text_length = len(element.get_text(strip=True))
            if text_length > best_text_length:
                best_text_length = text_length
                best_element = element
                logger.info(f"🔍 Found fallback content in {selector} with {text_length} characters")
    
    if best_element:
        logger.info(f"✅ Using fallback selector with {best_text_length} characters")
        return best_element
    
    # Last resort: try to find largest text block
    all_divs = soup.find_all(['div', 'section', 'main'])
    for div in all_divs:
        text_length = len(div.get_text(strip=True))
        if text_length > best_text_length:
            best_text_length = text_length
            best_element = div
    
    if best_element and best_text_length > 100:
        logger.info(f"✅ Using largest text block with {best_text_length} characters")
        return best_element
    
    logger.warning("⚠️ No suitable content found, will use body")
    return soup.body or soup

def clean_extracted_content(content_element):
    """Clean the extracted content by removing unwanted elements"""
    if not content_element:
        return ""
    
    # Get raw content string
    raw_content = str(content_element)
    
    # If content starts with nested HTML document, extract the body content
    if raw_content.strip().startswith('<!DOCTYPE') or raw_content.strip().startswith('<html'):
        # Parse the nested document
        nested_soup = BeautifulSoup(raw_content, 'lxml')
        
        # Look for main content in nested document
        main_content = None
        
        # Try to find the main content section
        for selector in ['main#qa', 'main', '.qa', 'section.qa', 'article', 'body']:
            elements = nested_soup.select(selector) if selector.startswith('.') or selector.startswith('#') else nested_soup.find_all(selector)
            if elements:
                # Find the one with most content
                for element in elements:
                    text_length = len(element.get_text(strip=True))
                    if text_length > 200 and (not main_content or text_length > len(main_content.get_text(strip=True))):
                        main_content = element
        
        if main_content:
            content_element = main_content
            logger.info("📄 Extracted content from nested HTML document")
        else:
            # Fall back to body
            if nested_soup.body:
                content_element = nested_soup.body
            else:
                content_element = nested_soup
    
    # Create a copy to clean
    content_copy = BeautifulSoup(str(content_element), 'lxml')
    
    # Remove unwanted elements
    unwanted_selectors = [
        'script', 'style', 'noscript', 'meta', 'link', 'head', 'title',
        '.ad', '.advertisement', '.adsbygoogle',
        '.sidebar', '.widget', '.social-share',
        '.tistory-footer', '.blog-footer', 
        '.navigation', '.breadcrumb', '.nav',
        '.comment', '.comments',
        '.header', '.footer', 'header:not(.header-content)', 'footer:not(.footer-content)',
        '[class*="tistory"]', '[id*="tistory"]',
        '[class*="toolbox"]', '[class*="btnbar"]',
        '.wrap:has(header):not(:has(main))'  # Remove wrapper divs that only contain headers
    ]
    
    for selector in unwanted_selectors:
        try:
            for element in content_copy.select(selector):
                element.decompose()
        except:
            # Skip invalid CSS selectors
            pass
    
    # Also remove specific elements by content pattern
    for element in content_copy.find_all(['div', 'section']):
        if element.get_text(strip=True) == '' or len(element.get_text(strip=True)) < 10:
            element.decompose()
    
    # Get the meaningful content
    main_content = None
    
    # If we have body, get its content
    if content_copy.body:
        main_content = content_copy.body
    # If we have direct content without body wrapper
    elif content_copy.find(['main', 'article', 'section', 'div']):
        # Find the element with most substantial content
        best_element = None
        best_length = 0
        for tag in ['main', 'article', 'section', 'div']:
            for element in content_copy.find_all(tag):
                text_length = len(element.get_text(strip=True))
                if text_length > best_length:
                    best_length = text_length
                    best_element = element
        main_content = best_element if best_element else content_copy
    else:
        main_content = content_copy
    
    # Extract inner HTML
    if main_content:
        inner_content = ''.join(str(child) for child in main_content.children) if hasattr(main_content, 'children') else str(main_content)
    else:
        inner_content = str(content_copy)
    
    # Clean up the HTML
    inner_content = re.sub(r'<html[^>]*>', '', inner_content)
    inner_content = re.sub(r'</html>', '', inner_content)
    inner_content = re.sub(r'<body[^>]*>', '', inner_content)
    inner_content = re.sub(r'</body>', '', inner_content)
    
    # Clean up excessive whitespace
    inner_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', inner_content)
    inner_content = re.sub(r'<p>\s*</p>', '', inner_content)
    inner_content = re.sub(r'<div>\s*</div>', '', inner_content)
    
    return inner_content.strip()

def is_already_clean_template(html_content):
    """Check if HTML already uses our clean template"""
    return ('© Uncle Parksy Korean Learning Archive' in html_content and 
            'viewport-fit=cover' in html_content and
            '#f4e5c9' in html_content)

def process_html_file(input_path, output_path):
    """Process a single HTML file"""
    try:
        # Check if output already exists and is clean
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            if is_already_clean_template(existing_content):
                logger.info(f"⏭️ Already clean: {output_path.name}")
                return 'skipped'
        
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Extract title and content
        title = extract_title(soup, input_path.name)
        content_element = extract_content_by_selectors(soup)
        content = clean_extracted_content(content_element)
        
        if not content or len(content.strip()) < 50:
            logger.warning(f"⚠️ Very little content extracted from {input_path.name}")
            return 'skipped'
        
        # Generate clean HTML
        template = get_mini_template()
        clean_html = template.replace('{{TITLE}}', title).replace('{{CONTENT}}', content)
        
        # Write output file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(clean_html)
        
        logger.info(f"✅ Processed: {input_path.name} -> {output_path.name}")
        return 'processed'
        
    except Exception as e:
        logger.error(f"❌ Error processing {input_path.name}: {e}")
        return 'error'

def determine_input_directory():
    """Determine which directory to use as input"""
    backup_raw = Path("backup/raw")
    archive_dir = Path("archive")
    
    if backup_raw.exists() and list(backup_raw.glob("*.html")):
        logger.info("📂 Using backup/raw/ as input directory")
        return backup_raw
    elif archive_dir.exists() and list(archive_dir.glob("*.html")):
        logger.info("📂 Using archive/ as input directory (in-place conversion)")
        return archive_dir
    else:
        logger.error("❌ No HTML files found in backup/raw/ or archive/")
        return None

def main():
    """Main execution function"""
    logger.info("🧹📱 Starting clean and mobilize pipeline...")
    
    try:
        # Determine input and output directories
        input_dir = determine_input_directory()
        if not input_dir:
            return 1
        
        output_dir = Path("archive")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get all HTML files (excluding index.html)
        html_files = [f for f in input_dir.glob("*.html") if f.name != "index.html"]
        
        if not html_files:
            logger.warning("⚠️ No HTML files found to process")
            return 0
        
        # Process files
        stats = {'processed': 0, 'skipped': 0, 'errors': 0}
        
        for input_file in html_files:
            output_file = output_dir / input_file.name
            result = process_html_file(input_file, output_file)
            
            if result == 'processed':
                stats['processed'] += 1
            elif result == 'skipped':
                stats['skipped'] += 1
            else:
                stats['errors'] += 1
        
        # Report results
        logger.info(f"🎉 Pipeline complete!")
        logger.info(f"📊 Results: {stats['processed']} processed, {stats['skipped']} skipped, {stats['errors']} errors")
        
        print(f"Clean and mobilize complete:")
        print(f"  Processed: {stats['processed']}")
        print(f"  Skipped: {stats['skipped']}")
        print(f"  Errors: {stats['errors']}")
        
        return 0 if stats['errors'] == 0 else 1
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())