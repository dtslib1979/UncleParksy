#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backup Mirroring Script for UncleParksy KR TextStory Archive
Mirrors /backup/*.html files to /archive/backup/ directory
"""

from pathlib import Path
import shutil
import os

def main():
    """Mirror backup HTML files to archive/backup directory"""
    SRC = Path("backup")
    DST = Path("archive/backup")
    
    # Create destination directory if it doesn't exist
    DST.mkdir(parents=True, exist_ok=True)
    
    mirrored_count = 0
    
    if not SRC.exists():
        print(f"Source directory {SRC} does not exist")
        return
    
    # Mirror all HTML files
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
    
    total_files = len(list(DST.glob("*.html")))
    print(f"✅ Mirrored {mirrored_count} files. Total HTML files in archive/backup: {total_files}")

if __name__ == "__main__":
    main()
