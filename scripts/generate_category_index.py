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

    # 카테고리 index.html 갱신
    with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
        f.write("<!doctype html><html lang='ko'><meta charset='utf-8'>\n")
        f.write(f"<title>{cat} ({count})</title>\n")
        f.write(f"<h1>{cat} ({count})</h1><ul>\n")
        for file in files:
            title = file.replace(".html","")
            f.write(f"<li><a href='./{file}'>{title}</a></li>\n")
        f.write("</ul></html>")

    home_data[cat] = count

# 홈 카드 카운트 저장 (JSON으로)
os.makedirs("assets", exist_ok=True)
with open("assets/home.json", "w", encoding="utf-8") as f:
    json.dump(home_data, f, ensure_ascii=False, indent=2)