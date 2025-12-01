#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archive Manifest Generator for UncleParksy PWA ER RUN
Scans /archive/*.html files and generates assets/manifest.archive.json

Requirements:
- Scan /archive/*.html (excluding index.html)
- Extract date/title from 'YYYY-MM-DD-제목.html' format
- For non-dated files, use file modification time
- Output JSON with count and items sorted by date (newest first)
"""

import os
import json
import re
import shutil
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
    """
    errors = []
    
    actual_count = len(html_files)
    if manifest['count'] != actual_count:
        errors.append(f"Count mismatch: manifest has {manifest['count']}, but {actual_count} files found")
    
    if len(manifest['items']) != actual_count:
        errors.append(f"Items count mismatch: {len(manifest['items'])} items, but {actual_count} files found")
    
    return errors


def backup_existing_manifest(manifest_path):
    """
    Create a backup of existing manifest if it exists.
    Returns True if backup was created, False otherwise.
    """
    if manifest_path.exists():
        backup_path = manifest_path.with_suffix('.json.backup')
        shutil.copy2(manifest_path, backup_path)
        print(f"📋 Created backup: {backup_path}")
        return True
    return False


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
    
    # Backup existing manifest on first run
    backup_existing_manifest(OUT_FILE)
    
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
    
    # Sort by date (newest first)
    items.sort(key=lambda x: x['date'], reverse=True)
    
    # Build manifest
    manifest = {
        "count": len(items),
        "items": items
    }
    
    # Validate manifest
    errors = validate_manifest(manifest, html_files)
    if errors:
        for error in errors:
            print(f"❌ Validation error: {error}")
        return 1
    
    # Validate JSON serialization
    try:
        json_str = json.dumps(manifest, ensure_ascii=False, indent=2)
    except (TypeError, ValueError) as e:
        print(f"❌ JSON validation error: {e}")
        return 1
    
    # Write manifest (complete overwrite)
    OUT_FILE.write_text(json_str, encoding='utf-8')
    
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
