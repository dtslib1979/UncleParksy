import os, datetime, json

root = "category"
home_data = {}

# Category display names
category_names = {
    "system-configuration": "System Configuration",
    "device-chronicles": "Device Chronicles", 
    "writers-path": "Writer's Path",
    "blog-transformation": "Blog Transformation",
    "webappsbook-codex": "WebAppsBook Codex",
    "webappsbookcast": "WebAppsBookCast",
    "thought-archaeology": "Thought Archaeology"
}

# Category icons
category_icons = {
    "system-configuration": "⚙️",
    "device-chronicles": "📱", 
    "writers-path": "🗺️",
    "blog-transformation": "🎨",
    "webappsbook-codex": "💻",
    "webappsbookcast": "🎬",
    "thought-archaeology": "💭"
}

def generate_category_html(cat, count, files):
    """Generate styled HTML for category index page"""
    
    display_name = category_names.get(cat, cat)
    icon = category_icons.get(cat, "📄")
    
    # Generate posts list HTML
    posts_html = ""
    for file in files:
        title = file.replace(".html", "")
        # Make title more readable
        if title.startswith("20"):  # Date format
            parts = title.split("-", 3)
            if len(parts) >= 4:
                date_part = f"{parts[0]}-{parts[1]}-{parts[2]}"
                title_part = parts[3].replace("-", " ").title()
                display_title = f"{date_part} | {title_part}"
            else:
                display_title = title.replace("-", " ").title()
        else:
            display_title = title.replace("-", " ").title()
            
        posts_html += f'''
        <div class="post-card" onclick="location.href='./{file}'" role="button" tabindex="0">
            <div class="post-content">
                <h3 class="post-title">{display_title}</h3>
                <div class="post-meta">
                    <span class="post-date">{file.replace(".html", "")}</span>
                </div>
            </div>
        </div>'''
    
    if not posts_html:
        posts_html = '''
        <div class="no-posts">
            <p>📜 No scrolls found in this chapter yet...</p>
            <p style="opacity: 0.7; font-size: 0.9rem;">The ancient knowledge awaits to be inscribed.</p>
        </div>'''
    
    html_content = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{display_name} — UncleParksy Archive</title>
<meta name="description" content="{display_name} archives from the EduArt Engineer's digital grimoire" />

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pirata+One&family=Philosopher:wght@400;700&display=swap" rel="stylesheet">

<style>
:root{{
  --primary-gold:#d4af37; --dark-gold:#b8860b; --light-gold:#f4e4aa;
  --parchment:#f7f3e8; --dark-parchment:#e8dcc0;
  --ink:#1a0f0a; --ink-2:#2d1b12; --ink-3:#4a2c1a;
  --purple:#6a4c93; --blue:#4a90e2; --red:#c44536;
  --shadow-d:rgba(26,15,10,.4); --shadow-m:rgba(26,15,10,.2); --shadow-l:rgba(26,15,10,.1);
  --ring:rgba(0,0,0,.08);
}}

*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{
  font-family: 'Philosopher', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  color:var(--ink);
  background:
    radial-gradient(circle at 15% 25%, rgba(212,175,55,.05) 0%, transparent 40%),
    radial-gradient(circle at 85% 75%, rgba(106,76,147,.04) 0%, transparent 40%),
    linear-gradient(135deg, var(--parchment) 0%, var(--dark-parchment) 100%);
  min-height:100vh; overflow-x:hidden; position:relative;
}}

/* parchment grain */
body::before{{
  content:""; position:fixed; inset:0; z-index:1; pointer-events:none;
  background:
    repeating-linear-gradient(45deg, transparent,transparent 1px, rgba(212,175,55,.015) 1px, rgba(212,175,55,.015) 2px),
    repeating-linear-gradient(-45deg, transparent,transparent 1px, rgba(74,44,26,.015) 1px, rgba(74,44,26,.015) 2px);
}}

/* layout */
.container{{position:relative; z-index:10; max-width:1200px; margin:0 auto; padding:clamp(1rem,4vw,3rem); min-height:100vh}}

/* header */
.site-header{{
  display:flex; align-items:center; justify-content:space-between; gap:12px; 
  padding:12px 0; margin-bottom:2rem; border-bottom:2px solid rgba(212,175,55,.2);
}}
.brand{{display:flex; align-items:center; gap:10px; text-decoration:none; color:inherit}}
.brand-title{{font-family:'Pirata One',cursive; font-size:1.4rem; letter-spacing:1px}}
.nav a{{margin-left:12px; font-weight:700; text-decoration:none; color:inherit; transition:all 0.3s ease}}
.nav a:hover{{color:var(--primary-gold); text-decoration:underline}}

/* hero section */
.category-hero{{
  text-align:center; margin-bottom:clamp(2rem,6vw,4rem);
  padding:clamp(2rem,6vw,3rem);
  background:linear-gradient(135deg, rgba(247,243,232,.97) 0%, rgba(232,220,192,.94) 50%, rgba(228,216,188,.92) 100%);
  backdrop-filter: blur(18px); border-radius:26px;
  border:3px solid rgba(212,175,55,.4); 
  box-shadow:0 34px 110px var(--shadow-m), inset 0 2px 6px rgba(255,255,255,.5), inset 0 -2px 6px rgba(212,175,55,.15);
}}

.category-icon{{font-size:clamp(3rem,8vw,5rem); display:block; margin-bottom:1rem; filter:drop-shadow(0 4px 12px rgba(212,175,55,.4))}}

.category-title{{
  font-family:'Pirata One',cursive; font-size:clamp(2.4rem,7vw,4rem); 
  background:linear-gradient(135deg, var(--primary-gold) 0%, var(--light-gold) 25%, var(--dark-gold) 50%, var(--purple) 75%, var(--primary-gold) 100%);
  background-size:200% 200%; -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  text-shadow:2px 2px 4px var(--shadow-m), 0 0 20px rgba(212,175,55,.3);
  letter-spacing:clamp(2px,.5vw,4px); margin:0 0 1rem; line-height:1.1; text-transform:uppercase;
}}

.category-count{{
  display:inline-block; background:linear-gradient(135deg,var(--primary-gold),var(--dark-gold)); 
  color:#000; padding:0.8rem 1.5rem; border-radius:25px; font-weight:700; font-size:1.1rem; 
  box-shadow:0 6px 18px rgba(212,175,55,.45); margin-bottom:1rem;
}}

.category-description{{font-size:clamp(1rem,2.8vw,1.2rem); color:var(--ink-2); opacity:.9; margin:0 auto; max-width:600px}}

/* posts section */
.posts-section{{
  background:linear-gradient(135deg, rgba(247,243,232,.97) 0%, rgba(232,220,192,.94) 50%, rgba(228,216,188,.92) 100%);
  backdrop-filter: blur(18px); border-radius:26px; padding:clamp(1.6rem,5vw,3rem);
  border:3px solid rgba(212,175,55,.4); 
  box-shadow:0 34px 110px var(--shadow-m), inset 0 2px 6px rgba(255,255,255,.5), inset 0 -2px 6px rgba(212,175,55,.15);
}}

.posts-title{{
  font-family:'Pirata One',cursive; font-size:clamp(1.8rem,5vw,2.4rem); 
  color:var(--ink); letter-spacing:1px; text-transform:uppercase;
  text-shadow:2px 2px 4px var(--shadow-m), 0 0 15px rgba(212,175,55,.2); 
  margin:0 0 2rem; text-align:center; position:relative
}}

.posts-title::after{{
  content:""; position:absolute; left:50%; transform:translateX(-50%); bottom:-12px;
  width:clamp(60px,20vw,150px); height:3px; border-radius:2px;
  background:linear-gradient(to right, transparent, var(--primary-gold) 20%, var(--dark-gold) 50%, var(--primary-gold) 80%, transparent);
}}

.posts-grid{{display:grid; gap:clamp(1rem,3vw,1.5rem); grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr))}}

.post-card{{
  position:relative; min-height:120px; 
  background:linear-gradient(135deg, rgba(255,255,255,.15) 0%, rgba(247,243,232,.92) 30%, rgba(232,220,192,.88) 100%);
  border-radius:16px; padding:clamp(1rem,3vw,1.5rem); border:2px solid rgba(212,175,55,.3);
  cursor:pointer; transition:transform .35s ease, box-shadow .35s ease, border-color .35s ease;
  overflow:hidden;
}}

.post-card::before{{
  content:""; position:absolute; inset:0; left:-100%;
  background:linear-gradient(90deg, transparent, rgba(212,175,55,.15), transparent); 
  transition:left .55s ease; z-index:1;
}}

.post-card:hover{{
  transform:translateY(-4px); border-color:var(--primary-gold); 
  box-shadow:0 18px 45px var(--shadow-d), 0 0 30px rgba(212,175,55,.35);
}}

.post-card:hover::before{{left:100%}}

.post-content{{position:relative; z-index:2}}

.post-title{{
  font-weight:700; font-size:clamp(1.1rem,2.5vw,1.3rem); color:var(--ink); 
  margin:0 0 0.8rem; line-height:1.3;
}}

.post-meta{{display:flex; align-items:center; gap:0.5rem; font-size:0.9rem; color:var(--ink-2); opacity:0.8}}

.post-date{{
  background:rgba(212,175,55,.15); padding:0.3rem 0.6rem; border-radius:12px; 
  font-family:monospace; font-size:0.85rem;
}}

.no-posts{{
  text-align:center; padding:3rem 1rem; color:var(--ink-2);
}}

.no-posts p{{margin:0.5rem 0; font-size:1.1rem}}

/* footer */
.footer{{
  margin-top:3rem; padding:2rem 0; text-align:center; 
  border-top:2px solid rgba(212,175,55,.2); color:var(--ink-2); font-size:0.9rem;
}}

.footer a{{color:var(--purple); text-decoration:none}}
.footer a:hover{{text-decoration:underline}}

/* responsive */
@media (max-width:768px){{
  .site-header{{flex-direction:column; gap:1rem}}
  .nav{{display:flex; gap:1rem}}
  .posts-grid{{grid-template-columns:1fr}}
}}

@media (prefers-reduced-motion:reduce){{
  *{{animation-duration:.01ms !important; animation-iteration-count:1 !important; transition-duration:.01ms !important}}
}}
</style>
</head>
<body>

<div class="container">
  <!-- Header -->
  <header class="site-header">
    <a class="brand" href="../../" aria-label="UncleParksy home">
      <span class="brand-title">📚 UncleParksy Archive</span>
    </a>
    <nav class="nav">
      <a href="../../">Home</a>
      <a href="../../archive/">Archive</a>
      <a href="../">Categories</a>
    </nav>
  </header>

  <!-- Hero Section -->
  <section class="category-hero">
    <span class="category-icon">{icon}</span>
    <h1 class="category-title">{display_name}</h1>
    <div class="category-count">{count} Posts</div>
    <p class="category-description">Explore the chronicles and wisdom preserved in this sacred chapter of knowledge.</p>
  </section>

  <!-- Posts Section -->
  <section class="posts-section">
    <h2 class="posts-title">📜 Ancient Scrolls</h2>
    <div class="posts-grid">
      {posts_html}
    </div>
  </section>
</div>

<!-- Footer -->
<footer class="footer">
  <p>© dtslib.com • <a href="../../">UncleParksy</a> • <a href="../../archive/">Full Archive</a></p>
</footer>

<script>
// Add keyboard navigation
document.addEventListener('keydown', function(e) {{
  if (e.target.classList.contains('post-card') && (e.key === 'Enter' || e.key === ' ')) {{
    e.preventDefault();
    e.target.click();
  }}
}});

// Add focus styles for accessibility
document.querySelectorAll('.post-card').forEach(card => {{
  card.addEventListener('focus', () => card.style.outline = '3px solid var(--primary-gold)');
  card.addEventListener('blur', () => card.style.outline = 'none');
}});
</script>

</body>
</html>'''
    
    return html_content

for cat in os.listdir(root):
    path = os.path.join(root, cat)
    if not os.path.isdir(path): 
        continue

    files = [f for f in os.listdir(path) if f.endswith(".html") and f != "index.html"]
    files.sort(reverse=True)
    count = len(files)

    # 카테고리 index.html 갱신 - 새로운 디자인으로
    with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_category_html(cat, count, files))

    home_data[cat] = count

# 홈 카드 카운트 저장 (JSON으로)
os.makedirs("assets", exist_ok=True)
with open("assets/home.json", "w", encoding="utf-8") as f:
    json.dump(home_data, f, ensure_ascii=False, indent=2)