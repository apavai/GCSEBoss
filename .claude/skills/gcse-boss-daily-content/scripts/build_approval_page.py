#!/usr/bin/env python3
"""ClinicMembership-pattern dark-card approval page for GCSE Boss.

Reads a JSON manifest and emits a fully self-contained HTML file with every
asset base64-embedded. Opens by double-click, no server, no network.

The agent NEVER auto-posts. This page is the publish gate: Ben reviews here,
then posts via Upload-Post.

Manifest shape:
{
  "date": "2026-08-24", "weekday": "Monday", "angle": "...", "slug": "...",
  "audience": "Student", "keyword": "...", "blog_path": "...",
  "blog_url": "...", "qa_summary": [["check","PASS"],...],
  "notes": ["..."],
  "cards": [{"platform":"TikTok","voice":"Student","dims":"1080x1920",
             "media":"/abs/path.mp4","type":"video","caption":"...",
             "routing":"profile=GCSEBoss . platform[]=tiktok"}]
}
"""
import base64, html, json, mimetypes, sys
from pathlib import Path

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#0b1220;color:#e8eef7;
 font:15px/1.6 'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
a{color:#2ea8e0}
.wrap{max-width:1400px;margin:0 auto;padding:32px 24px 80px}
header.top{border-bottom:1px solid #1d2b3f;padding-bottom:22px;margin-bottom:28px}
header.top h1{margin:0 0 6px;font-size:27px;letter-spacing:-.02em}
.meta{color:#8fa3bd;font-size:14px}
.pill{display:inline-block;background:#2ea8e0;color:#fff;border-radius:999px;
 padding:3px 12px;font-size:12px;font-weight:700;margin-right:8px}
.pill.grey{background:#1d2b3f;color:#8fa3bd}
.pill.warn{background:#7a5c14;color:#ffe9a8}
.card{background:#111a2a;border:1px solid #1d2b3f;border-radius:14px;
 padding:18px;margin-bottom:22px}
.card h2{margin:0 0 4px;font-size:18px}
.card h3{margin:0 0 10px;font-size:16px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(400px,1fr));gap:20px}
.grid .card{margin:0;display:flex;flex-direction:column}
.asset{background:#050a12;border-radius:10px;overflow:hidden;margin:10px 0;
 display:flex;justify-content:center}
.asset img,.asset video{max-width:100%;max-height:520px;display:block}
.cap{background:#0b1220;border:1px solid #1d2b3f;border-radius:10px;padding:12px;
 white-space:pre-wrap;font-size:13.5px;color:#cddcef;flex:1;
 max-height:340px;overflow:auto}
.route{font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:#7f93ad;
 margin-top:10px;word-break:break-all}
.blogframe{background:#fff;border-radius:10px;height:640px;width:100%;border:0}
table{border-collapse:collapse;width:100%;font-size:13.5px}
td,th{border-bottom:1px solid #1d2b3f;padding:7px 10px;text-align:left}
th{color:#8fa3bd;font-weight:600}
.PASS{color:#41d18b;font-weight:700}
.FAIL{color:#ff6b6b;font-weight:700}
.NOTE{color:#ffc857;font-weight:700}
ul.notes{margin:8px 0 0;padding-left:20px;color:#cddcef;font-size:14px}
ul.notes li{margin-bottom:6px}
.copybtn{background:#1d2b3f;border:1px solid #2a3d57;color:#e8eef7;
 border-radius:8px;padding:7px 13px;font-size:13px;cursor:pointer;margin-top:10px}
.copybtn:hover{background:#26384f}
"""

JS = """
document.querySelectorAll('.copybtn').forEach(function(b){
  b.addEventListener('click', function(){
    var t = b.parentElement.querySelector('.cap').innerText;
    navigator.clipboard.writeText(t).then(function(){
      var o=b.innerText; b.innerText='Copied'; setTimeout(function(){b.innerText=o;},1400);
    });
  });
});
"""


def b64(path):
    p = Path(path)
    if not p.exists():
        return None, None
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    return mime, base64.b64encode(p.read_bytes()).decode()


def build(manifest, out_path):
    m = manifest
    e = html.escape
    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>",
        f"<title>GCSE Boss approval {e(m['date'])}</title>",
        f"<style>{CSS}</style></head><body><div class='wrap'>",
        "<header class='top'>",
        f"<h1>GCSE Boss daily bundle: {e(m['weekday'])} {e(m['date'])}</h1>",
        f"<p class='meta'>{e(m['angle'])}</p>",
        f"<p><span class='pill'>{e(m['audience'])} blog</span>"
        f"<span class='pill grey'>keyword: {e(m['keyword'])}</span>"
        f"<span class='pill grey'>{len(m['cards'])} social assets</span>"
        "<span class='pill grey'>nothing published yet</span></p>",
        "</header>",
    ]

    if m.get("notes"):
        parts.append("<div class='card'><h2>Run notes</h2><ul class='notes'>")
        parts += [f"<li>{e(n)}</li>" for n in m["notes"]]
        parts.append("</ul></div>")

    # Blog card
    bmime, bdata = b64(m["blog_path"])
    parts.append("<div class='card'><h2>Blog post</h2>")
    parts.append(f"<p class='meta'>{e(m['blog_url'])}</p>")
    if bdata:
        parts.append(
            f"<iframe class='blogframe' src='data:text/html;base64,{bdata}'></iframe>")
    else:
        parts.append("<p class='FAIL'>Blog HTML missing on disk.</p>")
    parts.append("</div>")

    # Social grid
    parts.append("<div class='grid'>")
    for c in m["cards"]:
        mime, data = b64(c["media"])
        parts.append("<div class='card'>")
        parts.append(f"<h3>{e(c['platform'])}</h3>")
        parts.append(
            f"<p class='meta'><span class='pill grey'>{e(c['voice'])} voice</span>"
            f"<span class='pill grey'>{e(c['dims'])}</span></p>")
        if data and c.get("type") == "video":
            parts.append(
                f"<div class='asset'><video controls loop muted playsinline "
                f"src='data:{mime};base64,{data}'></video></div>")
        elif data:
            parts.append(
                f"<div class='asset'><img src='data:{mime};base64,{data}' "
                f"alt='{e(c['platform'])} asset'></div>")
        else:
            parts.append("<p class='FAIL'>Asset missing on disk.</p>")
        parts.append(f"<div class='cap'>{e(c['caption'])}</div>")
        parts.append("<button class='copybtn'>Copy caption</button>")
        parts.append(f"<div class='route'>{e(c['routing'])}</div>")
        parts.append("</div>")
    parts.append("</div>")

    # QA table
    parts.append("<div class='card'><h2>Self-QA hard-gate</h2>"
                 "<table><tr><th>Check</th><th>Result</th><th>Detail</th></tr>")
    for row in m.get("qa_summary", []):
        chk, res = row[0], row[1]
        det = row[2] if len(row) > 2 else ""
        parts.append(f"<tr><td>{e(chk)}</td><td class='{e(res)}'>{e(res)}</td>"
                     f"<td>{e(det)}</td></tr>")
    parts.append("</table></div>")

    parts.append(
        "<div class='card'><h2>Posting checklist</h2><ul class='notes'>"
        "<li>Every platform routes to <code>profile=GCSEBoss</code>. "
        "Never Ben Norman / Benjamin Norman personal feeds.</li>"
        "<li>Facebook needs <code>facebook_page_id</code>; LinkedIn needs "
        "<code>target_linkedin_page_id</code>. Both from <code>.env</code>.</li>"
        "<li>Instagram: omit <code>media_type</code> entirely or the API rejects it.</li>"
        "<li>TikTok ships MEDIA_UPLOAD. The MP4 lands in drafts, paste the caption "
        "in the TikTok app. Re-fire if still processing after 5 minutes.</li>"
        "<li>Pinterest: set <code>pinterest_link</code> to the blog URL as well as "
        "putting it in the description.</li>"
        "<li>Push the blog commit after approval. Cloudflare deploys on push.</li>"
        "</ul></div>")

    parts.append(f"</div><script>{JS}</script></body></html>")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text("".join(parts), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    mf = json.loads(Path(sys.argv[1]).read_text())
    out = build(mf, sys.argv[2])
    print(f"OUT={out}")
    print(f"SIZE_MB={Path(out).stat().st_size/1e6:.1f}")
