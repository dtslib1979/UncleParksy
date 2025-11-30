#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Category Index Generator for UncleParksy
Generates both assets/home.json (counts) and category/*/manifest.json (file lists)
"""

import os
import json
import re
from pathlib import Path

def extract_date(filename):
    """Extract date from various filename formats"""
    # Remove .html extension
    name = filename.replace('.html', '')
    
    # Pattern 1: ISO format (2025-08-29)
    if re.match(r'^\d{4}-\d{2}-\d{2}', name):
        return name[:10]
    
    # Pattern 2: Korean format (2025년 8월 29일)
    korean_match = re.match(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', name)
    if korean_match:
        year, month, day = korean_match.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    return None

def determine_section(category, filename):
    """Determine section based on category and filename"""
    filename_lower = filename.lower()
    
    # Category-based rules
    if 'Visualizer' in category:
        if 'mermaid' in filename_lower or 'diagram' in filename_lower:
            return "Diagrams"
        return "Visuals"
    elif 'Blogger' in category:
        if 'webapps' in filename_lower or 'pwa' in filename_lower:
            return "WebAppsBook"
        return "Blog"
    elif 'Philosopher' in category:
        if 'trial' in filename_lower or 'test' in filename_lower:
            return "Experiments"
        return "Essays"
    elif 'Musician' in category:
        return "Audio"
    elif 'Technician' in category:
        return "Devices"
    elif 'Protocol' in category:
        return "Protocols"
    elif 'Orbit' in category:
        return "Logs"
    
    # Filename-based fallback
    if 'test' in filename_lower or 'trial' in filename_lower:
        return "Experiments"
    
    return "Documents"

def extract_tags(filename):
    """Extract potential tags from filename"""
    tags = []
    name = filename.replace('.html', '').lower()
    
    # Common tags
    if 'test' in name:
        tags.append('test')
    if 'trial' in name:
        tags.append('trial')
    if 'mermaid' in name:
        tags.append('mermaid')
    if 'diagram' in name:
        tags.append('diagram')
    if 'upload' in name:
        tags.append('upload')
    if '깃허브' in name or 'github' in name:
        tags.append('github')
    if '설정' in name or 'setup' in name or 'config' in name:
        tags.append('setup')
    if 'korean' in name or '한글' in name or '년' in name:
        tags.append('korean')
    
    return tags

def main():
    root = "category"
    home_data = {}
    
    print("🚀 Starting category index generation...")
    
    # Process each category directory
    for cat in os.listdir(root):
        path = os.path.join(root, cat)
        if not os.path.isdir(path):
            continue
        
        print(f"\n📁 Processing {cat}...")
        
        # Find all HTML files (excluding index.html)
        files = [f for f in os.listdir(path) if f.endswith(".html") and f != "index.html"]
        files.sort(reverse=True)  # Newest first
        count = len(files)
        
        # Update home.json data
        home_data[cat] = count
        
        # Generate manifest items
        manifest_items = []
        for filename in files:
            # Extract metadata
            date = extract_date(filename)
            section = determine_section(cat, filename)
            tags = extract_tags(filename)
            
            # Clean title
            title = filename.replace('.html', '')
            # Replace common separators with spaces
            title = title.replace('-', ' ').replace('_', ' ')
            # Clean up multiple spaces
            title = ' '.join(title.split())
            
            manifest_items.append({
                "title": title,
                "path": f"./{filename}",
                "section": section,
                "type": "HTML",
                "date": date,
                "tags": tags
            })
        
        # Write category manifest.json
        manifest_path = os.path.join(path, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump({"items": manifest_items}, f, ensure_ascii=False, indent=2)
        
        print(f"  ✅ Generated {manifest_path}")
        print(f"  📊 {len(manifest_items)} items")
        
        # Show first few items as preview
        if manifest_items:
            print(f"  📄 Preview:")
            for item in manifest_items[:3]:
                date_str = f" ({item['date']})" if item['date'] else ""
                print(f"    - {item['title']}{date_str}")
            if len(manifest_items) > 3:
                print(f"    ... and {len(manifest_items) - 3} more")
    
    # Write assets/home.json
    os.makedirs("assets", exist_ok=True)
    with open("assets/home.json", "w", encoding="utf-8") as f:
        json.dump(home_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Updated assets/home.json")
    print(f"📊 Total categories: {len(home_data)}")
    print(f"📚 Total documents: {sum(home_data.values())}")
    
    # Summary
    print("\n📋 Summary:")
    for cat, count in home_data.items():
        print(f"  - {cat}: {count} files")

if __name__ == "__main__":
    main()
