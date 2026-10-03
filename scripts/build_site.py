#!/usr/bin/env python3
"""public/ を dist/ にコピーし、HTML 一覧ページ (index.html) を自動生成する。"""
import html
import re
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public"
DIST = ROOT / "dist"
SITE_TITLE = "事前指導2D"
SITE_LEAD = "インターンに行く前に読んでおく資料"
JST = timezone(timedelta(hours=9))
# カードの色と絵文字を順番に割り当てる
COLORS = ["pink", "orange", "blue", "green", "purple", "yellow"]
EMOJIS = ["📝", "🤝", "💼", "📣", "🌱", "⭐"]


def page_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    return html.unescape(m.group(1).strip()) if m and m.group(1).strip() else path.stem


def split_title(title: str) -> tuple[str, str, str]:
    """「Day3 本題 - 副題」を (Day3, 本題, 副題) に分ける。"""
    m = re.match(r"(Day\s*\d+)\s*(.*)", title)
    day, rest = (m.group(1), m.group(2)) if m else ("", title)
    main, _, sub = rest.partition(" - ")
    return day, main.strip(), sub.strip()


def card(i: int, path: Path) -> str:
    href = html.escape(path.relative_to(DIST).as_posix())
    day, main, sub = split_title(page_title(path))
    badge = f'<span class="day">{html.escape(day)}</span>' if day else ""
    subline = f'<span class="sub">{html.escape(sub)}</span>' if sub else ""
    return (
        f'    <li><a class="card c-{COLORS[i % len(COLORS)]}" href="{href}">'
        f'{badge}<span class="emoji">{EMOJIS[i % len(EMOJIS)]}</span>'
        f'<span class="ttl">{html.escape(main)}</span>{subline}'
        f'<span class="go">読む →</span></a></li>'
    )


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC, DIST)

    pages = sorted(
        (p for p in DIST.rglob("*.html") if p.name != "index.html" or p.parent != DIST),
        key=lambda p: str(p.relative_to(DIST)),
    )
    items = "\n".join(card(i, p) for i, p in enumerate(pages)) or (
        '    <li class="empty">まだ資料はありません。</li>'
    )

    updated = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    (DIST / "index.html").write_text(
        f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{SITE_TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700;800&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg:#fff8ee; --dots:#ffd9b8; --card:#ffffff; --ink:#22202b; --muted:#6c6878; --edge:#22202b;
    --pink:#ff5c8a; --pink-bg:#ffe3ec; --orange:#ff8a3d; --orange-bg:#ffe9d9;
    --yellow:#e0a800; --yellow-bg:#fff4cc; --green:#2bb673; --green-bg:#dcf7e8;
    --blue:#3d8bff; --blue-bg:#e0edff; --purple:#9b5cff; --purple-bg:#efe4ff;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg:#1b1824; --dots:#2c2738; --card:#262233; --ink:#f4f1fa; --muted:#b2acc2; --edge:#0c0a12;
      --pink-bg:#40202d; --orange-bg:#40291b; --yellow-bg:#3d3418; --green-bg:#173528;
      --blue-bg:#1a2a45; --purple-bg:#2e2147;
    }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; color:var(--ink); line-height:1.7;
    font-family:"M PLUS Rounded 1c","Hiragino Maru Gothic ProN","Hiragino Sans","Noto Sans JP",sans-serif;
    background-color:var(--bg);
    background-image:radial-gradient(var(--dots) 1.5px, transparent 1.5px); background-size:22px 22px; }}
  main {{ max-width:760px; margin:0 auto; padding:28px 16px 64px; }}
  .hero {{ position:relative; overflow:hidden; padding:30px 24px 26px; border:3px solid var(--edge); border-radius:28px;
    background:linear-gradient(135deg,#ff5c8a 0%,#ff8a3d 45%,#ffc531 100%); color:#fff; box-shadow:6px 6px 0 var(--edge); }}
  .hero::after {{ content:""; position:absolute; right:-40px; top:-40px; width:170px; height:170px; border-radius:50%;
    background:rgba(255,255,255,.18); }}
  .hero .chip {{ display:inline-block; background:#fff; color:#22202b; font-weight:800; font-size:.8rem;
    border:2px solid #22202b; border-radius:999px; padding:2px 12px; transform:rotate(-2deg); }}
  .hero h1 {{ margin:12px 0 4px; font-size:clamp(2rem,8vw,2.8rem); font-weight:800; line-height:1.2;
    text-shadow:3px 3px 0 rgba(34,32,43,.35); }}
  .hero p {{ margin:0; font-weight:700; }}
  .hero .deco {{ position:absolute; right:20px; bottom:10px; font-size:3rem; transform:rotate(10deg); }}
  @media (max-width:600px) {{ .hero .deco {{ top:12px; bottom:auto; right:14px; font-size:2.2rem; }} .hero h1 {{ margin-top:20px; }} }}
  .updated {{ display:inline-block; margin:18px 0 22px; font-size:.8rem; font-weight:700; color:var(--muted);
    background:var(--card); border:2px solid var(--edge); border-radius:999px; padding:2px 12px; }}
  ul {{ list-style:none; padding:0; margin:0; display:grid; gap:18px; }}
  .card {{ position:relative; display:block; text-decoration:none; color:var(--ink); background:var(--card);
    border:3px solid var(--edge); border-radius:22px; padding:18px 20px 16px; box-shadow:5px 5px 0 var(--edge);
    transition:transform .12s, box-shadow .12s; }}
  .card:hover, .card:focus-visible {{ transform:translate(-2px,-2px); box-shadow:7px 7px 0 var(--edge); outline:none; }}
  .card:active {{ transform:translate(3px,3px); box-shadow:2px 2px 0 var(--edge); }}
  .card::before {{ content:""; position:absolute; inset:0 auto 0 0; width:12px; background:var(--c);
    border-radius:19px 0 0 19px; border-right:3px solid var(--edge); }}
  .card > * {{ margin-left:8px; }}
  .day {{ display:inline-block; background:var(--c); color:#fff; font-weight:800; font-size:.95rem; letter-spacing:.04em;
    border:2px solid var(--edge); border-radius:10px; padding:0 12px; transform:rotate(-4deg); }}
  .emoji {{ position:absolute; right:18px; top:14px; font-size:2rem; transform:rotate(8deg); }}
  .ttl {{ display:block; font-size:clamp(1.15rem,4.5vw,1.4rem); font-weight:800; line-height:1.4; margin-top:8px; padding-right:44px; }}
  .sub {{ display:inline-block; margin-top:6px; font-size:.9rem; font-weight:700; background:var(--cb);
    border-radius:999px; padding:1px 12px; }}
  .go {{ display:block; text-align:right; margin-top:6px; font-weight:800; font-size:.9rem; color:var(--c); }}
  .c-pink {{ --c:var(--pink); --cb:var(--pink-bg); }} .c-orange {{ --c:var(--orange); --cb:var(--orange-bg); }}
  .c-yellow {{ --c:var(--yellow); --cb:var(--yellow-bg); }} .c-green {{ --c:var(--green); --cb:var(--green-bg); }}
  .c-blue {{ --c:var(--blue); --cb:var(--blue-bg); }} .c-purple {{ --c:var(--purple); --cb:var(--purple-bg); }}
  .empty {{ background:var(--card); border:3px dashed var(--muted); border-radius:22px; padding:20px; text-align:center; }}
  footer {{ text-align:center; margin-top:40px; font-weight:800; color:var(--muted); }}
</style>
</head>
<body>
<main>
  <header class="hero">
    <span class="chip">インターン事前指導</span>
    <h1>{SITE_TITLE}</h1>
    <p>{SITE_LEAD}</p>
    <span class="deco">🎒</span>
  </header>
  <span class="updated">最終更新 {updated}（JST）</span>
  <ul>
{items}
  </ul>
  <footer>がんばれ、インターン生！ 🎉</footer>
</main>
</body>
</html>
""",
        encoding="utf-8",
    )
    print(f"Built {len(pages)} page(s) into {DIST}")


if __name__ == "__main__":
    main()
