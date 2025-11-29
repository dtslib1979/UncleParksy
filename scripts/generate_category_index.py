import os, datetime, json, re

root = "category"
home_data = {}

# Date pattern for extracting date from filename
DATE_PATTERNS = [
    re.compile(r'^(\d{4})-(\d{2})-(\d{2})'),  # 2025-08-29
    re.compile(r'^(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일'),  # 2025년 8월 29일
]

def extract_date_from_filename(filename):
    """Extract date from filename in various formats."""
    for pattern in DATE_PATTERNS:
        m = pattern.match(filename)
        if m:
            try:
                y, mo, d = m.groups()
                return f"{y}-{int(mo):02d}-{int(d):02d}"
            except (ValueError, TypeError):
                continue
    return None

def extract_title_from_filename(filename):
    """Extract title from filename by removing date prefix and extension."""
    name = filename
    if name.endswith('.html'):
        name = name[:-5]
    # Remove date prefixes
    name = re.sub(r'^\d{4}-\d{2}-\d{2}[-_\s]*', '', name)
    name = re.sub(r'^\d{4}년\s*\d{1,2}월\s*\d{1,2}일\s*', '', name)
    name = name.strip()
    if not name:
        name = filename[:-5] if filename.endswith('.html') else filename
    return name

# Section mapping based on category name
SECTION_MAP = {
    "Philosopher-Parksy": "Essays",
    "Blogger-Parksy": "WebAppsBook",
    "Visualizer-Parksy": "Diagrams",
    "Musician-Parksy": "Audio",
    "Technician-Parksy": "Devices",
    "Orbit-Log": "Logs",
    "Protocol-Parksy": "Protocols",
}

for cat in os.listdir(root):
    path = os.path.join(root, cat)
    if not os.path.isdir(path): 
        continue

    files = [f for f in os.listdir(path) if f.endswith(".html") and f != "index.html"]
    files.sort(reverse=True)
    count = len(files)

    # Update home_data for count tracking
    home_data[cat] = count
    
    # Also update category manifest.json with current file list
    manifest_path = os.path.join(path, "manifest.json")
    section = SECTION_MAP.get(cat, "General")
    items = []
    for f in files:
        date_str = extract_date_from_filename(f)
        title = extract_title_from_filename(f)
        items.append({
            "title": title,
            "path": f"./{f}",
            "section": section,
            "type": "HTML",
            "date": date_str,
            "tags": []
        })
    
    manifest_data = {"items": items}
    with open(manifest_path, "w", encoding="utf-8") as mf:
        json.dump(manifest_data, mf, ensure_ascii=False, indent=2)

# 홈 카드 카운트 저장 (JSON으로)
os.makedirs("assets", exist_ok=True)
with open("assets/home.json", "w", encoding="utf-8") as f:
    json.dump(home_data, f, ensure_ascii=False, indent=2)