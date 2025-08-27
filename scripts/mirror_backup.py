#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backup Mirroring Script for UncleParksy KR TextStory Archive
Mirrors /backup/*.html files directly to /archive/ directory
"""

from pathlib import Path
import shutil
import os

def main():
    """Mirror backup HTML files directly to archive directory"""
    SRC = Path("backup")
    DST = Path("archive")
    
    # Create destination directory if it doesn't exist
    DST.mkdir(parents=True, exist_ok=True)
    
    mirrored_count = 0
    
    if not SRC.exists():
        print(f"Source directory {SRC} does not exist")
        return
    
    # Mirror all HTML files (excluding README.md)
    for src_file in SRC.glob("*.html"):
        dst_file = DST / src_file.name
        
        # Check if file needs to be copied (new or modified)
        should_copy = False
        if not dst_file.exists():
            should_copy = True
            print(f"New file: {src_file.name}")
        elif src_file.stat().st_mtime > dst_file.stat().st_mtime:
            should_copy = True
            print(f"Updated file: {src_file.name}")
        
        if should_copy:
            shutil.copy2(src_file, dst_file)
            mirrored_count += 1
    
    # Count total HTML files in archive (excluding index.html)
    total_files = len([f for f in DST.glob("*.html") if f.name != "index.html"])
    print(f"✅ Mirrored {mirrored_count} files. Total HTML files in archive: {total_files}")

if __name__ == "__main__":
    main()
