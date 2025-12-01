#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manifest Generator for UncleParksy KR TextStory Archive
Scans /archive/*.html files and generates assets/manifest.json

This is the canonical generator for assets/manifest.json used by archive/index.html.

Behavior:
- Scan archive/*.html (exclude index.html)
- For filenames matching YYYY-MM-DD-제목.html: extract date and title
- For other filenames: use file modification time as date and filename as title
- Build manifest JSON with structure: {"count": N, "items": [...]}
- Sort items by date (newest first), items without valid date at the end
- Validate count matches discovered files, exit non-zero on mismatch
- Overwrite assets/manifest.json atomically
"""

import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path


def extract_metadata(filepath):
    """
    Extract date and title from file.
    
    For 'YYYY-MM-DD-Title.html' format: extract date and title from filename
    For other files: use file modification time and filename (without extension) as title
    
    Returns (title, date_str) tuple where date_str is YYYY-MM-DD format or None
    """
    stem = filepath.stem  # filename without extension
    
    # Pattern for YYYY-MM-DD-Title.html
    date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})-(.+)$')
    match = date_pattern.match(stem)
    
    if match:
        # Dated filename format
        date_str = match.group(1)
        title = match.group(2).strip()
        # Validate date format
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            # Invalid date format (e.g., 9999-99-99), treat as non-dated file
            print(f"⚠️ Warning: Invalid date format in filename: {filepath.name}")
            date_str = None
            title = stem.strip()
    else:
        # Non-dated filename: use file modification time
        title = stem.strip()
        date_str = None
        try:
            mtime = filepath.stat().st_mtime
            date_obj = datetime.fromtimestamp(mtime)
            date_str = date_obj.strftime('%Y-%m-%d')
        except OSError:
            # If mtime unavailable, use current date
            date_str = datetime.now().strftime('%Y-%m-%d')
    
    return title, date_str


def validate_manifest(manifest, html_files):
    """
    Validate the generated manifest.
    
    Checks:
    - count matches actual file count
    - items count matches file count
    
    Returns list of error messages (empty if valid)
    """
    errors = []
    
    actual_count = len(html_files)
    if manifest['count'] != actual_count:
        errors.append(f"Count mismatch: manifest has {manifest['count']}, but {actual_count} files found")
    
    if len(manifest['items']) != actual_count:
        errors.append(f"Items count mismatch: {len(manifest['items'])} items, but {actual_count} files found")
    
    return errors


def write_atomic(filepath, content):
    """
    Write content to file atomically using a temporary file and rename.
    """
    directory = filepath.parent
    directory.mkdir(parents=True, exist_ok=True)
    
    # Write to temp file in same directory, then rename (atomic on same filesystem)
    fd, tmp_path = tempfile.mkstemp(suffix='.json', dir=directory)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        os.replace(tmp_path, filepath)
    except Exception:
        # Clean up temp file on error
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def main():
    """Generate manifest.json from archive HTML files"""
    SCAN_DIR = Path("archive")
    OUT_FILE = Path("assets/manifest.json")
    
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
    items_with_date = []
    items_without_date = []
    
    for filepath in html_files:
        title, date_str = extract_metadata(filepath)
        
        item = {
            "path": f"archive/{filepath.name}",  # Relative path, no leading slash
            "title": title,
            "date": date_str
        }
        
        if date_str:
            items_with_date.append(item)
        else:
            items_without_date.append(item)
    
    # Sort items with dates by date (newest first)
    items_with_date.sort(key=lambda x: x['date'], reverse=True)
    
    # Sort items without dates alphabetically by title
    items_without_date.sort(key=lambda x: x['title'])
    
    # Combine: dated items first (newest first), then undated items at the end
    items = items_with_date + items_without_date
    
    # Build manifest
    manifest = {
        "count": len(items),
        "items": items
    }
    
    # Validate manifest
    errors = validate_manifest(manifest, html_files)
    if errors:
        for error in errors:
            print(f"❌ Validation error: {error}", file=sys.stderr)
        return 1
    
    # Validate JSON serialization
    try:
        json_str = json.dumps(manifest, ensure_ascii=False, indent=2)
    except (TypeError, ValueError) as e:
        print(f"❌ JSON validation error: {e}", file=sys.stderr)
        return 1
    
    # Write manifest atomically
    try:
        write_atomic(OUT_FILE, json_str)
    except Exception as e:
        print(f"❌ Failed to write manifest: {e}", file=sys.stderr)
        return 1
    
    print(f"✅ Generated {OUT_FILE} with {len(items)} items")
    
    # Print summary
    if items:
        print("\n📋 Archive contents (newest first):")
        for item in items[:5]:
            print(f"  • [{item['date'] or 'no date'}] {item['title']}")
        if len(items) > 5:
            print(f"  ... and {len(items) - 5} more items")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
