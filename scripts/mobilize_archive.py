#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archive HTML Mobile Optimization Script
Mobilizes Tistory archive HTML files with responsive design patterns.

Features:
- Idempotent viewport injection (width=device-width, initial-scale=1, viewport-fit=cover)
- Idempotent mobile CSS link injection (/assets/css/mobile-override.css)
- Remove fixed dimensions from media elements (img/table/iframe/video)
- Add loading=lazy to images
- Remove sidebars and force single-column layout
- Make content areas 100% width
"""

import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import re
import argparse


def setup_parser():
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(description='Mobilize archive HTML files')
    parser.add_argument('--archive-dir', default='archive', 
                       help='Archive directory path (default: archive)')
    parser.add_argument('--css-path', default='/assets/css/mobile-override.css',
                       help='Mobile CSS path (default: /assets/css/mobile-override.css)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without modifying files')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    return parser


def inject_viewport_meta(soup, verbose=False):
    """Inject or update viewport meta tag idempotently"""
    head = soup.find('head')
    if not head:
        if verbose:
            print("  ⚠️  No <head> found, skipping viewport injection")
        return False
    
    # Target viewport content
    target_viewport = "width=device-width, initial-scale=1, viewport-fit=cover"
    
    # Find ALL existing viewport meta tags (including those in nested structures)
    viewport_tags = soup.find_all('meta', attrs={'name': 'viewport'})
    
    # Check if we already have the correct viewport tag
    has_correct_viewport = False
    for tag in viewport_tags:
        if tag.get('content') == target_viewport:
            has_correct_viewport = True
            break
    
    # Remove all existing viewport tags
    removed_count = 0
    for tag in viewport_tags:
        tag.decompose()
        removed_count += 1
    
    # Inject the standardized viewport tag only once
    viewport_meta = soup.new_tag('meta')
    viewport_meta['name'] = 'viewport'
    viewport_meta['content'] = target_viewport
    
    # Insert after charset if exists, otherwise at the beginning of head
    charset_tag = head.find('meta', attrs={'charset': True})
    if charset_tag:
        charset_tag.insert_after(viewport_meta)
    else:
        head.insert(0, viewport_meta)
    
    if verbose:
        if has_correct_viewport and removed_count == 1:
            print("  → Viewport meta already correct")
            return False
        else:
            print(f"  ✓ Viewport meta injected (removed {removed_count} existing)")
            return True
    
    return not (has_correct_viewport and removed_count == 1)


def inject_mobile_css_link(soup, css_path, verbose=False):
    """Inject mobile CSS link idempotently"""
    head = soup.find('head')
    if not head:
        if verbose:
            print("  ⚠️  No <head> found, skipping CSS injection")
        return False
    
    # Check if mobile CSS link already exists
    existing_links = head.find_all('link', href=css_path)
    if existing_links:
        if verbose:
            print(f"  → Mobile CSS link already exists ({len(existing_links)} found)")
        return False
    
    # Create mobile CSS link
    css_link = soup.new_tag('link')
    css_link['rel'] = 'stylesheet'
    css_link['type'] = 'text/css'
    css_link['href'] = css_path
    
    # Insert at the end of head (so it overrides other styles)
    head.append(css_link)
    
    if verbose:
        print(f"  ✓ Mobile CSS link injected: {css_path}")
    
    return True


def remove_fixed_dimensions(soup, verbose=False):
    """Remove fixed width/height from media elements and add loading=lazy to images"""
    changes = 0
    
    # Process images, tables, iframes, videos
    media_selectors = ['img', 'table', 'iframe', 'video']
    
    for selector in media_selectors:
        elements = soup.find_all(selector)
        for element in elements:
            # Remove width and height attributes
            if element.get('width'):
                del element['width']
                changes += 1
            if element.get('height'):
                del element['height']
                changes += 1
            
            # Remove width/height from style attribute
            style = element.get('style', '')
            if style:
                # Remove width and height from inline styles
                style = re.sub(r'\b(width|height)\s*:\s*[^;]+;?', '', style, flags=re.IGNORECASE)
                style = re.sub(r';\s*;', ';', style)  # Clean up double semicolons
                style = style.strip().strip(';')
                if style:
                    element['style'] = style
                else:
                    if element.get('style'):
                        del element['style']
                        changes += 1
            
            # Add loading=lazy to images
            if selector == 'img' and not element.get('loading'):
                element['loading'] = 'lazy'
                changes += 1
    
    if verbose and changes > 0:
        print(f"  ✓ Removed fixed dimensions and added lazy loading ({changes} changes)")
    
    return changes > 0


def remove_sidebars_and_fix_layout(soup, verbose=False):
    """Remove sidebars and force single-column layout"""
    changes = 0
    
    # Remove sidebar elements
    sidebar_selectors = ['.sidebar', '[class*="sidebar"]', '#sidebar']
    for selector in sidebar_selectors:
        elements = soup.select(selector)
        for element in elements:
            element.decompose()
            changes += 1
    
    # Force single column for grid/row layouts - only if not already applied
    grid_selectors = ['.grid', '.row', '[class*="grid"]', '[class*="row"]']
    for selector in grid_selectors:
        elements = soup.select(selector)
        for element in elements:
            style = element.get('style', '')
            
            # Check if mobile styles already applied
            if 'display: block' in style and 'grid-template-columns: 1fr' in style:
                continue
                
            # Add mobile-friendly styles
            if 'display:' not in style.lower():
                style += '; display: block'
            if 'grid-template-columns:' not in style.lower():
                style += '; grid-template-columns: 1fr'
            element['style'] = style.strip().strip(';')
            changes += 1
    
    # Make content areas 100% width - only if not already applied
    content_selectors = ['.content', '.main', '[id*="content"]']
    for selector in content_selectors:
        elements = soup.select(selector)
        for element in elements:
            style = element.get('style', '')
            
            # Check if mobile styles already applied
            if 'width: 100%' in style and 'max-width: 100%' in style:
                continue
            
            if 'width:' not in style.lower():
                style += '; width: 100%'
            if 'max-width:' not in style.lower():
                style += '; max-width: 100%'
            element['style'] = style.strip().strip(';')
            changes += 1
    
    if verbose and changes > 0:
        print(f"  ✓ Layout optimized for mobile ({changes} changes)")
    
    return changes > 0


def mobilize_html_file(file_path, css_path, dry_run=False, verbose=False):
    """Mobilize a single HTML file"""
    if verbose:
        print(f"\n📱 Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        return False
    
    # Parse with lxml parser for better HTML handling
    try:
        soup = BeautifulSoup(content, 'lxml')
    except:
        # Fallback to html.parser if lxml not available
        soup = BeautifulSoup(content, 'html.parser')
    
    # Track if any changes were made
    modified = False
    
    # Apply mobile optimizations
    if inject_viewport_meta(soup, verbose):
        modified = True
    
    if inject_mobile_css_link(soup, css_path, verbose):
        modified = True
    
    if remove_fixed_dimensions(soup, verbose):
        modified = True
    
    if remove_sidebars_and_fix_layout(soup, verbose):
        modified = True
    
    if not modified:
        if verbose:
            print("  → No changes needed (already optimized)")
        return False
    
    if dry_run:
        print(f"  🔍 Would modify: {file_path}")
        return False
    
    # Write back the modified content
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        if verbose:
            print(f"  ✅ File updated")
        return True
    except Exception as e:
        print(f"  ❌ Error writing file: {e}")
        return False


def main():
    """Main function"""
    parser = setup_parser()
    args = parser.parse_args()
    
    # Resolve paths
    archive_dir = Path(args.archive_dir)
    css_path = args.css_path
    
    if not archive_dir.exists():
        print(f"❌ Archive directory not found: {archive_dir}")
        sys.exit(1)
    
    # Find all HTML files (excluding index.html)
    html_files = []
    for file_path in archive_dir.glob('*.html'):
        if file_path.name != 'index.html':
            html_files.append(file_path)
    
    if not html_files:
        print(f"❌ No HTML files found in {archive_dir}")
        sys.exit(1)
    
    print(f"🏺 KR TextStory Archive Mobile Optimization")
    print(f"📁 Archive directory: {archive_dir}")
    print(f"🎨 Mobile CSS path: {css_path}")
    print(f"📄 Found {len(html_files)} HTML files to process")
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
    
    # Process each file
    processed_count = 0
    changed_count = 0
    
    for file_path in sorted(html_files):
        processed_count += 1
        if mobilize_html_file(file_path, css_path, args.dry_run, args.verbose):
            changed_count += 1
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"  📄 Processed: {processed_count} files")
    print(f"  ✨ Modified: {changed_count} files")
    
    if args.dry_run:
        print(f"  🔍 Dry run completed - no actual changes made")
    elif changed_count > 0:
        print(f"  ✅ Mobile optimization complete!")
    else:
        print(f"  ✨ All files already optimized!")


if __name__ == '__main__':
    main()