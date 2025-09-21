// Copy all Tistory URLs listed on the current index by scanning each HTML file.
//
// Public API:
//   window.CopyTistoryURLs.copyFromItems(() => allItems.map(i => i.path), { button })
//
(function () {
  function extractOgUrl(html) {
    const m = html && html.match(/<meta\s+property=["']og:url["']\s+content=["']([^"']+)["']/i);
    return m ? m[1] : null;
  }
  function extractBaseUrl(html) {
    // window.TistoryBlog = { ..., url: "https://dtslib1k.tistory.com", ... }
    const m = html && html.match(/window\.TistoryBlog\s*=\s*{[^}]*\burl:\s*"([^"]+)"/);
    return m ? m[1] : null;
  }
  function extractPlink(html) {
    // ..."plink":"/188"...
    const m = html && html.match(/["']plink["']\s*:\s*["']([^"']+)["']/);
    return m ? m[1] : null;
  }
  function extractEntryId(html) {
    // "entryId":202 or "entryId":"202"
    const m = html && html.match(/["']entryId["']\s*:\s*"?(\d+)"?/);
    return m ? m[1] : null;
  }
  function absoluteFrom(base, path) {
    try { return new URL(path, base).href; } catch { return null; }
  }
  function deriveBackupPathIfPossible(path) {
    // Try mapping archive → backup/raw (best-effort)
    if (typeof path === 'string' && path.includes('archive/')) {
      return path.replace('archive/', 'backup/raw/');
    }
    return null;
  }
  async function fetchTextSafe(path) {
    try {
      const res = await fetch(path, { headers: { 'Accept': 'text/html' } });
      if (!res.ok) return null;
      return await res.text();
    } catch {
      return null;
    }
  }
  async function extractUrlFromPath(path) {
    // 1) Try the page itself
    let html = await fetchTextSafe(path);
    let url = extractOgUrl(html);
    if (!url && html) {
      const base = extractBaseUrl(html);
      const plink = extractPlink(html);
      const id = extractEntryId(html);
      if (base && plink) url = absoluteFrom(base, plink);
      else if (base && id) url = absoluteFrom(base, '/' + id);
    }
    // 2) Fallback: mapped backup/raw file (often contains Tistory script blocks)
    if (!url) {
      const alt = deriveBackupPathIfPossible(path);
      if (alt) {
        const altHtml = await fetchTextSafe(alt);
        if (altHtml) {
          const og2 = extractOgUrl(altHtml);
          if (og2) url = og2;
          else {
            const base2 = extractBaseUrl(altHtml);
            const plink2 = extractPlink(altHtml);
            const id2 = extractEntryId(altHtml);
            if (base2 && plink2) url = absoluteFrom(base2, plink2);
            else if (base2 && id2) url = absoluteFrom(base2, '/' + id2);
          }
        }
      }
    }
    return url || null;
  }
  async function copyText(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.top = '-1000px';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      const ok = document.execCommand('copy');
      document.body.removeChild(ta);
      return ok;
    }
  }
  async function copyFromPaths(paths, opts = {}) {
    const btn = opts.button || null;
    const setStatus = (s) => { if (btn) btn.textContent = s; else console.log(s); };
    const urls = [];
    const seen = new Set();
    setStatus(`🔎 Scanning 0/${paths.length}...`);
    let i = 0;
    for (const p of paths) {
      i++;
      setStatus(`🔎 Scanning ${i}/${paths.length}...`);
      const u = await extractUrlFromPath(p);
      if (u && !seen.has(u)) { seen.add(u); urls.push(u); }
    }
    if (urls.length === 0) { setStatus('⚠️ No Tistory URLs found'); return []; }
    const txt = urls.join('\n');
    const ok = await copyText(txt);
    setStatus(ok ? `✅ Copied ${urls.length} URLs` : '⚠️ Copy failed');
    return urls;
  }
  window.CopyTistoryURLs = {
    copyFromItems(getItems, opts = {}) {
      const items = (typeof getItems === 'function') ? getItems() : [];
      const paths = items.map(v => (typeof v === 'string' ? v : v.path)).filter(Boolean);
      const btn = opts.button || null;
      if (btn) {
        btn.disabled = true;
        const restore = () => { btn.disabled = false; btn.textContent = '🔗 Copy Tistory URLs'; };
        return copyFromPaths(paths, { button: btn }).finally(() => setTimeout(restore, 1500));
      }
      return copyFromPaths(paths, opts);
    }
  };
})();