#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archive Manifest Generator for UncleParksy PWA ER RUN
Scans /archive/*.html files and generates assets/manifest.archive.json

NOTE: This file (assets/manifest.archive.json) is auto-generated.
      Do NOT edit manually - it will be overwritten by this script.

Requirements:
- Scan /archive/*.html (excluding index.html)
- Extract date/title from 'YYYY-MM-DD-제목.html' format
- For non-dated files, use file modification time
- Output JSON with count and items sorted by date (newest first)

Exit codes:
- 0: Success
- 3: Count mismatch (validation error)
- 4: Write failure
"""

import os
import json
import re
import sys
from pathlib import Path
from datetime import datetime


def extract_metadata(filepath):
    """
    Extract date and title from file.
    
    For 'YYYY-MM-DD-제목.html' format: extract date and title from filename
    For other files: use file modification time and filename as title
    
    Returns (title, date_str) tuple
    """
    filename = filepath.name
    stem = filepath.stem  # filename without extension
    
    # Pattern for YYYY-MM-DD-Title.html
    date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})-(.+)$')
    match = date_pattern.match(stem)
    
    if match:
        # Dated filename format
        date_str = match.group(1)
        title = match.group(2).strip()
    else:
        # Non-dated filename: use file modification time
        try:
            mtime = filepath.stat().st_mtime
            date_obj = datetime.fromtimestamp(mtime)
            date_str = date_obj.strftime('%Y-%m-%d')
        except OSError:
            date_str = datetime.now().strftime('%Y-%m-%d')
        title = stem.strip()
    
    return title, date_str


def validate_manifest(manifest, html_files):
    """
    Validate the generated manifest.
    
    Checks:
    - JSON is valid (already implicitly checked by json.dumps)
    - count matches actual file count
    
    Returns exit code: 0 for success, 3 for count mismatch
    """
    actual_count = len(html_files)
    if manifest['count'] != actual_count:
        print(f"❌ Count mismatch: manifest has {manifest['count']}, but {actual_count} files found")
        return 3
    
    if len(manifest['items']) != actual_count:
        print(f"❌ Items count mismatch: {len(manifest['items'])} items, but {actual_count} files found")
        return 3
    
    return 0


def atomic_write(filepath, content):
    """
    Atomically write content to filepath using temp file + os.replace.
    
    Returns exit code: 0 for success, 4 for write failure
    """
    tmp_path = filepath.with_suffix('.json.tmp')
    try:
        tmp_path.write_text(content, encoding='utf-8')
        os.replace(tmp_path, filepath)
        print(f"✅ Wrote {filepath}")
        return 0
    except OSError as e:
        print(f"❌ Write failure: {e}")
        # Clean up temp file if it exists
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass
        return 4


def main():
    """Generate manifest.archive.json from archive HTML files"""
    SCAN_DIR = Path("archive")
    OUT_FILE = Path("assets/manifest.archive.json")
    
    # Create assets directory if it doesn't exist
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if scan directory exists
    if not SCAN_DIR.exists():
        print(f"⚠️ Warning: Scan directory {SCAN_DIR} does not exist")
        SCAN_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all HTML files (excluding index.html)
    html_files = [
        f for f in SCAN_DIR.glob("*.html")
        if f.name.lower() != "index.html"
    ]
    
    print(f"📁 Scanning {SCAN_DIR}...")
    print(f"📄 Found {len(html_files)} HTML files (excluding index.html)")
    
    # Build items list
    items = []
    for filepath in html_files:
        title, date_str = extract_metadata(filepath)
        
        items.append({
            "title": title,
            "path": f"archive/{filepath.name}",
            "date": date_str
        })
    
    # Sort by date (newest first) - invalid dates go to the end
    def sort_key(item):
        try:
            return (1, datetime.fromisoformat(item['date']))
        except ValueError:
            return (0, datetime.min)  # Tuple ensures invalid dates sort last with reverse=True
    
    items.sort(key=sort_key, reverse=True)
    
    # Build manifest
    manifest = {
        "count": len(items),
        "items": items
    }
    
    # Validate manifest
    exit_code = validate_manifest(manifest, html_files)
    if exit_code != 0:
        return exit_code
    
    # Validate JSON serialization
    try:
        json_str = json.dumps(manifest, ensure_ascii=False, indent=2)
    except (TypeError, ValueError) as e:
        print(f"❌ JSON validation error: {e}")
        return 4
    
    # Atomic write manifest
    exit_code = atomic_write(OUT_FILE, json_str)
    if exit_code != 0:
        return exit_code
    
    print(f"✅ Generated {OUT_FILE} with {len(items)} items")
    
    # Print summary
    if items:
        print("\n📋 Archive contents (newest first):")
        for item in items[:5]:
            print(f"  • [{item['date']}] {item['title']}")
        if len(items) > 5:
            print(f"  ... and {len(items) - 5} more items")
    
    return 0


if __name__ == "__main__":
    exit(main())
