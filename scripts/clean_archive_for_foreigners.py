#!/usr/bin/env python3
"""
Archive Cleanup Script for Foreign Users
클린업 스크립트 - 외국인을 위한 아카이브 정리

This script cleans up Tistory auto-posted HTML files in the archive folder to make them
more appealing to foreign users interested in Korean content by:
1. Removing post view categories and cluttered UI elements
2. Applying a unified, clean design
3. Keeping only the essential content (Q&A sections)
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def get_clean_css():
    """Return the clean, unified CSS for foreign-friendly design"""
    return """
<style>
:root {
  --papyrus: #f4e5c9;
  --clay: #cd853f;
  --gold: #daa520;
  --ink: #2b2b2b;
  --muted: #5a4b3a;
  --card: #fff8e8;
  --paper: #fef9e7;
}

html, body {
  margin: 0;
  padding: 0;
  background: var(--papyrus);
  color: var(--ink);
  font-family: ui-sans-serif, system-ui, 'Apple SD Gothic Neo', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
}

.container {
  max-width: 920px;
  margin: 0 auto;
  padding: 20px;
}

header {
  padding: 12px 0 20px;
}

.title {
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: 0.2px;
  margin-bottom: 8px;
}

.subtitle {
  color: var(--muted);
  font-size: 0.95rem;
  margin-bottom: 4px;
}

.meta {
  color: var(--muted);
  font-size: 0.85rem;
  margin-bottom: 16px;
}

.bar {
  height: 4px;
  background: linear-gradient(90deg, var(--clay), var(--gold));
  border-radius: 999px;
  margin: 12px 0 24px;
}

/* Main content area */
main {
  background: var(--card);
  border: 1px solid #e9d7b6;
  border-radius: 16px;
  padding: 20px;
  margin: 20px 0;
}

/* Q&A Accordion styles */
.qa-section {
  background: var(--paper);
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 16px;
  padding: 10px;
  margin: 16px 0;
}

details {
  background: #fff;
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 14px;
  margin: 10px 0;
  overflow: hidden;
}

summary {
  list-style: none;
  cursor: pointer;
  padding: 14px 16px;
  font-weight: 800;
  background: linear-gradient(180deg, #fff, #fff7e3);
  color: #3b2a15;
  border-bottom: 1px solid rgba(0,0,0,0.06);
  position: relative;
}

summary::-webkit-details-marker {
  display: none;
}

summary:after {
  content: "＋";
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-weight: 900;
  color: #7a4d1b;
}

details[open] summary:after {
  content: "－";
}

.a, .a-body, .panel {
  padding: 12px 16px;
  background: #fffef9;
  border-top: 1px dashed #e7cfa1;
}

.badge, .q-tag, .a-tag {
  background: var(--gold);
  color: #1f1706;
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 0.8rem;
  font-weight: 700;
}

.q-tag, .a-tag {
  margin-right: 8px;
}

/* Copy buttons */
.copy-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 16px 0;
}

button {
  background: var(--clay);
  color: #fff;
  border: none;
  border-bottom: 2px solid #8d5d2b;
  padding: 10px 14px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.92rem;
  box-shadow: 0 1px 0 rgba(0,0,0,0.05);
  cursor: pointer;
}

button:hover {
  filter: brightness(0.98);
}

button.alt {
  background: var(--gold);
  border-bottom: 2px solid #a58016;
  color: #2b2008;
}

/* Pattern questions */
.patterns-section {
  background: var(--card);
  border: 1px solid #e9d7b6;
  border-radius: 16px;
  padding: 16px;
  margin: 20px 0;
}

.patterns-section h2 {
  margin: 0 0 12px;
  font-size: 1.1rem;
  color: var(--clay);
}

.patterns-section ol {
  margin: 8px 0;
  padding-left: 1.5rem;
}

.patterns-section li {
  margin: 8px 0;
  line-height: 1.5;
}

/* Footer */
footer {
  text-align: center;
  padding: 20px 0;
  color: var(--muted);
  font-size: 0.85rem;
}

.pill {
  background: rgba(205, 133, 63, 0.1);
  padding: 4px 12px;
  border-radius: 999px;
  margin: 0 4px;
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    padding: 12px;
  }
  
  .title {
    font-size: 1.2rem;
  }
  
  .copy-buttons {
    flex-direction: column;
  }
  
  button {
    width: 100%;
  }
}

/* Print styles */
@media print {
  body {
    background: white;
  }
  
  .copy-buttons {
    display: none;
  }
}
</style>
"""

def extract_title_from_filename(filename):
    """Extract a clean title from the filename"""
    # Remove date prefix and .html suffix
    title = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename)
    title = re.sub(r'\.html$', '', title)
    # Clean up common test file patterns
    title = re.sub(r'^test_file$', '티스토리 가치', title)
    return title

def extract_main_content(soup):
    """Extract the main Q&A content from the soup"""
    content_sections = []
    
    # Look for main content areas with different patterns
    qa_sections = soup.find_all(['section', 'div'], {'id': re.compile(r'qa|q\d+'), 'class': re.compile(r'qa')})
    
    if qa_sections:
        # Found dedicated QA sections, extract details from them
        for section in qa_sections:
            details = section.find_all('details')
            if details:
                content_sections.extend(details)
            else:
                # If no details found but section has content, take it
                if section.get_text(strip=True) and len(section.get_text(strip=True)) > 100:
                    content_sections.append(section)
    else:
        # Fallback: look for main elements or content areas
        main_elements = soup.find_all('main')
        for main in main_elements:
            details = main.find_all('details')
            if details:
                content_sections.extend(details)
                break  # Take first main with details
        
        # If still no content, look anywhere for details elements
        if not content_sections:
            all_details = soup.find_all('details')
            # Filter out details that are likely navigation or UI elements
            for detail in all_details:
                summary = detail.find('summary')
                if summary:
                    summary_text = summary.get_text(strip=True)
                    # Include if it looks like a question (has Korean question patterns)
                    if len(summary_text) > 10 and ('?' in summary_text or '까' in summary_text or '가?' in summary_text or 'Q' in summary_text):
                        content_sections.append(detail)
    
    return content_sections

def extract_pattern_questions(soup):
    """Extract pattern questions if they exist"""
    pattern_content = []
    
    # Look for sections with pattern in id or class
    pattern_sections = soup.find_all(['section', 'div'], {'id': re.compile(r'pattern'), 'class': re.compile(r'pattern')})
    
    for section in pattern_sections:
        # Look for ordered or unordered lists
        lists = section.find_all(['ol', 'ul'])
        for lst in lists:
            items = lst.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                if text and len(text) > 20:  # Only substantial questions
                    pattern_content.append(text)
    
    # Also look for lists that might contain pattern questions (broader search)
    if not pattern_content:
        # Look for lists with substantial content that might be questions
        all_lists = soup.find_all(['ol', 'ul'])
        for lst in all_lists:
            items = lst.find_all('li')
            # If this list has questions (contains question marks or is in a patterns-like context)
            if len(items) > 2:  # More than 2 items
                for item in items:
                    text = item.get_text(strip=True)
                    if text and len(text) > 40 and ('?' in text or '까' in text or '가?' in text):
                        pattern_content.append(text)
                if pattern_content:  # Found questions in this list, break
                    break
    
    return pattern_content

def create_clean_html(title, content_sections, pattern_questions=None):
    """Create a clean HTML structure with the extracted content"""
    
    # Create basic HTML structure
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title} — Korean Learning Archive</title>
    <meta name="description" content="Clean Q&A archive for learners interested in Korean content and culture">
    <meta name="author" content="Uncle Parksy - Korean Learning Archive">
    {get_clean_css()}
</head>
<body>
    <div class="container">
        <header>
            <div class="title">{title}</div>
            <div class="subtitle">Korean Learning Archive — Clean Q&A Format</div>
            <div class="meta">Optimized for learners interested in Korean content</div>
            <div class="bar"></div>
        </header>

        <main>
            <div class="qa-section">
"""

    # Add Q&A content
    for i, section in enumerate(content_sections, 1):
        if section.name == 'details':
            html += str(section)
        else:
            # Wrap content in details if not already
            summary_text = f"Question {i}"
            content_text = str(section)
            html += f"""
                <details>
                    <summary>{summary_text}</summary>
                    <div class="a">{content_text}</div>
                </details>
            """

    html += """
            </div>
        </main>
"""

    # Add pattern questions if they exist
    if pattern_questions:
        html += """
        <section class="patterns-section">
            <h2>Key Discussion Topics</h2>
            <ol>
"""
        for question in pattern_questions:
            html += f"                <li>{question}</li>\n"
        
        html += """
            </ol>
        </section>
"""

    # Add footer
    html += """
        <footer>
            <span class="pill">© Uncle Parksy Korean Learning Archive</span>
            <span class="pill">Optimized for Foreign Learners</span>
        </footer>
    </div>
</body>
</html>
"""
    
    return html

def clean_archive_file(file_path):
    """Clean a single archive file"""
    print(f"Processing: {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract title from filename
        title = extract_title_from_filename(file_path.name)
        
        # Extract main content
        content_sections = extract_main_content(soup)
        
        # Extract pattern questions
        pattern_questions = extract_pattern_questions(soup)
        
        if not content_sections:
            print(f"  Warning: No substantial content found in {file_path.name}")
            return False
        
        # Create clean HTML
        clean_html = create_clean_html(title, content_sections, pattern_questions)
        
        # Write cleaned file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(clean_html)
        
        print(f"  ✓ Cleaned successfully - {len(content_sections)} content sections, {len(pattern_questions) if pattern_questions else 0} pattern questions")
        return True
        
    except Exception as e:
        print(f"  ✗ Error processing {file_path.name}: {e}")
        return False

def main():
    """Main function to clean all archive files"""
    script_dir = Path(__file__).parent
    archive_dir = script_dir.parent / 'archive'
    
    if not archive_dir.exists():
        print(f"Archive directory not found: {archive_dir}")
        return
    
    print("🧹 Starting archive cleanup for foreign users...")
    print("=" * 50)
    
    # Find all HTML files except index.html
    html_files = [f for f in archive_dir.glob('*.html') if f.name != 'index.html']
    
    if not html_files:
        print("No HTML files found to process.")
        return
    
    processed = 0
    successful = 0
    
    for file_path in sorted(html_files):
        processed += 1
        if clean_archive_file(file_path):
            successful += 1
    
    print("=" * 50)
    print(f"📊 Processing complete:")
    print(f"   Total files: {processed}")
    print(f"   Successfully cleaned: {successful}")
    print(f"   Failed: {processed - successful}")
    print("\n✨ Archive files are now optimized for foreign users interested in Korean content!")

if __name__ == '__main__':
    main()