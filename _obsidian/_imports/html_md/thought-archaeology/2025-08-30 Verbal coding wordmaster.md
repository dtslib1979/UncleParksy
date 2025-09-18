# Practical Architect Verb Whitepaper (v1.0) — Promptbook for Verbal Coding

  :root{
    --papyrus:#f4e5c9;
    --clay:#cd853f;
    --gold:#daa520;
    --ink:#2b2b2b;
    --muted:#6b5e4a;
    --card:#fff8e6;
    --ring:rgba(205,133,63,.25);
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0;background:var(--papyrus);color:var(--ink);font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
  header{padding:28px 16px 10px;text-align:center}
  .title{font-size:clamp(22px,4.5vw,34px);font-weight:800;letter-spacing:.2px}
  .subtitle{color:var(--muted);margin-top:6px}
  .meta{color:var(--muted);font-size:13px;margin-top:4px}
  main{padding:16px;max-width:1100px;margin:0 auto}
  .actions{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:12px 0 22px}
  button.copy-btn{
    border:1.5px solid var(--clay);background:linear-gradient(180deg,#ffe7c0,#ffd28c);
    color:#3a2a17;padding:10px 14px;border-radius:12px;cursor:pointer;font-weight:700
  }
  button.copy-btn:active{transform:translateY(1px)}
  .grid{display:grid;grid-template-columns:1fr;gap:14px}
  @media(min-width:720px){.grid{grid-template-columns:repeat(2,1fr)}}
  @media(min-width:1024px){.grid{grid-template-columns:repeat(3,1fr)}}
  .card{
    background:var(--card);border:1.5px solid var(--ring);border-radius:16px;padding:14px 14px 10px;
    box-shadow:0 1px 0 rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.05)
  }
  h2,h3{margin:.2em 0 .4em}
  h2{font-size:clamp(18px,3.4vw,22px)}
  h3{font-size:clamp(16px,3vw,20px);color:#2b2216}
  .kicker{
    display:inline-block;font-weight:800;letter-spacing:.4px;color:#2b2216;
    background:linear-gradient(180deg,#ffeabf,#ffd07a);border:1.5px solid var(--clay);
    padding:4px 9px;border-radius:999px;margin-bottom:8px
  }
  ul.verb{margin:8px 0 0;padding-left:18px}
  ul.verb li{margin:2px 0}
  .badge{display:inline-block;font-size:12px;padding:2px 8px;border-radius:999px;background:#fff3d6;border:1px solid var(--gold);color:#5a3d18;margin-left:6px}
  details{border:1.5px solid var(--ring);border-radius:14px;background:#fffaf0;padding:10px 12px;margin:8px 0}
  details>summary{cursor:pointer;font-weight:700;list-style:none}
  details>summary::-webkit-details-marker{display:none}
  details[open]{background:#fff4da}
  pre.code{white-space:pre-wrap;background:#fff;border:1px dashed #e6caa2;padding:10px;border-radius:10px;font-size:13px}
  .ring-wrap{display:grid;place-items:center;margin:10px 0 18px}
  .ring{
    width:min(800px,100%);height:auto;background:
      radial-gradient(120px 120px at 50% 50%, rgba(218,165,32,.15), transparent 60%),
      radial-gradient(350px 350px at 50% 50%, rgba(205,133,63,.12), transparent 70%);
    border-radius:18px;padding:10px;border:1.5px dashed var(--ring)
  }
  .legend{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:8px}
  .legend span{font-size:12px;background:#fff3d6;border:1px solid var(--gold);border-radius:999px;padding:2px 8px}
  footer{margin:28px 0 40px;text-align:center;color:var(--muted);font-size:13px}
  .visually-hidden{position:absolute !important;left:-9999px !important;top:auto !important;width:1px !important;height:1px !important;overflow:hidden !important}

    Practical Architect Verb Whitepaper (v1.0) — Promptbook for Verbal Coding
    150 core verbs & 10 prompt templates covering the full DevOps lifecycle
    Author: EduArt Engineer · © dtslib.com

      📋 Copy full HTML/CSS
      📄 Copy whitepaper text

      SVG Infographic · 10 Stages

        LIFECYCLE
        Architect · Prompt · Orchestrate
        1 Setup
        2 Data
        3 Backend
        4 Frontend
        5 Logic
        6 Test
        7 Debug
        8 Ops
        9 Sec
        10 Collab

        1 Setup2 Data3 Backend4 Frontend5 Logic6 Test7 Debug8 Ops9 Sec10 Collab

    © dtslib.com · Author: EduArt Engineer

function copyToClipboard(text){
  if(navigator.clipboard && window.isSecureContext){
    return navigator.clipboard.writeText(text);
  }else{
    const ta=document.createElement('textarea');
    ta.value=text; document.body.appendChild(ta); ta.select();
    try{ document.execCommand('copy'); }catch(e){}
    document.body.removeChild(ta);
    return Promise.resolve();
  }
}
function serializePage(){
  const style = document.getElementById('main-style')?.outerHTML || '';
  const bodyInner = document.body.innerHTML;
  const doc = `

# Practical Architect Verb Whitepaper (v1.0)${style}
${bodyInner}
`;
  return doc;
}
function copyFullHTML(){
  copyToClipboard(serializePage()).then(()=>alert('Full HTML/CSS copied to clipboard.'));
}
function copyWhitepaper(){
  const text = document.getElementById('whitepaper')?.innerText || document.getElementById('whitepaper-raw').value;
  copyToClipboard(text).then(()=>alert('Whitepaper text copied.'));
}