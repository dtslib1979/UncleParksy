#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Category Manifest Generator for UncleParksy
Generates manifest.json files for each category directory
"""

import os
import json
import datetime
import re
from pathlib import Path

def extract_date_from_filename(filename):
    """Extract date from filename if possible"""
    # Try to find YYYY-MM-DD pattern
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        try:
            return datetime.date.fromisoformat(date_match.group(1)).isoformat()
        except:
            pass
    
    # Try to find Korean date pattern like "2025년 8월 27일"
    korean_date_match = re.search(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', filename)
    if korean_date_match:
        try:
            year, month, day = korean_date_match.groups()
            date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            return datetime.date.fromisoformat(date_str).isoformat()
        except:
            pass
    
    return None

def generate_category_manifest(category_path):
    """Generate manifest for a specific category"""
    category_name = category_path.name
    
    # Find all HTML files except index.html
    html_files = [f for f in category_path.glob("*.html") if f.name != "index.html"]
    
    items = []
    for html_file in html_files:
        title = html_file.stem  # filename without extension
        date_str = extract_date_from_filename(html_file.name)
        
        item = {
            "path": f"category/{category_name}/{html_file.name}",
            "title": title,
            "date": date_str
        }
        items.append(item)
    
    # Sort by date (newest first), then by title
    items.sort(key=lambda x: (x['date'] or '0000-00-00', x['title']), reverse=True)
    
    # Generate manifest
    manifest = {
        "generated": datetime.datetime.utcnow().isoformat() + "Z",
        "category": category_name,
        "count": len(items),
        "items": items
    }
    
    return manifest

def main():
    """Main function to generate all category manifests"""
    category_root = Path("category")
    assets_dir = Path("assets")
    
    # Create assets directory if it doesn't exist
    assets_dir.mkdir(exist_ok=True)
    
    if not category_root.exists():
        print(f"❌ Category directory {category_root} does not exist")
        return 1
    
    categories = [
        "blog-transformation",
        "device-chronicles", 
        "system-configuration",
        "thought-archaeology",
        "webappsbook-codex",
        "webappsbookcast",
        "writers-path"
    ]
    
    for category_name in categories:
        category_path = category_root / category_name
        
        if not category_path.exists():
            print(f"⚠️ Category {category_name} does not exist, skipping")
            continue
        
        print(f"📁 Processing category: {category_name}")
        
        # Generate manifest
        manifest = generate_category_manifest(category_path)
        
        # Save manifest file
        manifest_file = assets_dir / f"{category_name}-manifest.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Generated {manifest_file} with {manifest['count']} items")
        
        # Print summary
        if manifest['items']:
            print(f"📄 {category_name} contents:")
            for item in manifest['items'][:3]:  # Show first 3 items
                print(f"  • {item['title']} ({item['date'] or 'no date'})")
            if len(manifest['items']) > 3:
                print(f"  ... and {len(manifest['items']) - 3} more items")
        
        print()
    
    print("🎉 All category manifests generated successfully!")
    return 0

if __name__ == "__main__":
    exit(main())