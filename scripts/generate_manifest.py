#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manifest Generator for UncleParksy KR TextStory Archive
Scans /archive/*.html files and generates assets/manifest.json
"""

from pathlib import Path
from bs4 import BeautifulSoup
import json
import re
import datetime

def main():
    """Generate manifest.json from archive HTML files"""
    SCAN = Path("archive")
    OUT = Path("assets/manifest.json")
    
    # Create assets directory if it doesn't exist
    OUT.parent.mkdir(parents=True, exist_ok=True)
    
    items = []
    date_re = re.compile(r"(\d{4}-\d{2}-\d{2})-(.+)\.html$", re.I)
    
    # Check if scan directory exists
    if not SCAN.exists():
        print(f"Warning: Scan directory {SCAN} does not exist")
        SCAN.mkdir(parents=True, exist_ok=True)
    
    # Process HTML files in reverse chronological order (newest first)
    # Exclude index.html from archive folder
    html_files = sorted([f for f in SCAN.glob("*.html") if f.name != "index.html"], 
                       key=lambda x: x.name, reverse=True)
    
    for p in html_files:
        title = p.stem
        date_str = None
        display = None
        
        # Extract date and title from filename
        m = date_re.match(p.name)
        if m:
            date_str = m.group(1)
            display = m.group(2).replace('-', ' ').replace('_', ' ')
        
        # Try to extract title from HTML content
        try:
            html_content = p.read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(html_content, "lxml")
            
            # Try to get title from <title> tag
            title_tag = soup.find('title')
            if title_tag and title_tag.string:
                extracted_title = title_tag.string.strip()
                if extracted_title:
                    display = extracted_title
            
        except Exception as e:
            print(f"Warning: Could not parse HTML for {p.name}: {e}")
            pass
        
        # Fallback to cleaned filename if no display title found
        if not display:
            display = title.replace('-', ' ').replace('_', ' ')
        
        # Convert date string to ISO format
        iso_date = None
        if date_str:
            try:
                iso_date = datetime.date.fromisoformat(date_str).isoformat()
            except Exception as e:
                print(f"Warning: Could not parse date {date_str} for {p.name}: {e}")
        
        # Add item to manifest - path is relative to root, not archive folder
        item = {
            "path": f"archive/{p.name}",  # Direct path: archive/filename.html
            "title": display,
            "date": iso_date
        }
        items.append(item)
    
    # Generate manifest object
    manifest = {
        "generated": datetime.datetime.utcnow().isoformat() + "Z",
        "count": len(items),
        "items": items
    }
    
    # Write manifest.json
    OUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), 
        encoding="utf-8"
    )
    
    print(f"✅ Generated {OUT} with {len(items)} items")
    
    # Print summary
    if items:
        print("📄 Archive contents:")
        for item in items[:5]:  # Show first 5 items
            print(f"  • {item['title']} ({item['date'] or 'no date'})")
        if len(items) > 5:
            print(f"  ... and {len(items) - 5} more items")

if __name__ == "__main__":
    main()
