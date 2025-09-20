import os, datetime, json

root = "category"
home_data = {}

for cat in os.listdir(root):
    path = os.path.join(root, cat)
    if not os.path.isdir(path): 
        continue

    files = [f for f in os.listdir(path) if f.endswith(".html") and f != "index.html"]
    files.sort(reverse=True)
    count = len(files)

    # Note: Advanced index.html files are now preserved
    # Only update home_data for count tracking
    home_data[cat] = count

# 홈 카드 카운트 저장 (JSON으로)
os.makedirs("assets", exist_ok=True)
with open("assets/home.json", "w", encoding="utf-8") as f:
    json.dump(home_data, f, ensure_ascii=False, indent=2)