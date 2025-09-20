import os, datetime, json

def is_manual_edit(index_path):
    """
    수동 편집본인지 확인하는 함수
    파일 최상단에 <!-- MANUAL EDIT --> 마크가 있으면 수동 편집본으로 판단
    """
    if not os.path.exists(index_path):
        return False
    
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read(100)  # 처음 100자만 확인하면 충분
            return "<!-- MANUAL EDIT -->" in content
    except:
        return False

root = "category"
home_data = {}

for cat in os.listdir(root):
    path = os.path.join(root, cat)
    if not os.path.isdir(path): 
        continue

    files = [f for f in os.listdir(path) if f.endswith(".html") and f != "index.html"]
    files.sort(reverse=True)
    count = len(files)

    index_path = os.path.join(path, "index.html")
    
    # 수동 편집본 확인 - 수동 편집본이면 자동 갱신 건너뜀
    if is_manual_edit(index_path):
        print(f"⚠️  수동 편집본 감지됨: {index_path} - 자동 갱신 건너뜀")
        home_data[cat] = count
        continue

    # 카테고리 index.html 갱신 (자동 생성본만)
    with open(index_path, "w", encoding="utf-8") as f:
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