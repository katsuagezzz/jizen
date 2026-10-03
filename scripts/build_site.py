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
JST = timezone(timedelta(hours=9))


def page_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    return html.unescape(m.group(1).strip()) if m and m.group(1).strip() else path.stem


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC, DIST)

    pages = sorted(
        (p for p in DIST.rglob("*.html") if p.name != "index.html" or p.parent != DIST),
        key=lambda p: str(p.relative_to(DIST)),
    )
    items = "\n".join(
        f'      <li><a href="{html.escape(p.relative_to(DIST).as_posix())}">'
        f"{html.escape(page_title(p))}</a>"
        f'<span class="path">{html.escape(p.relative_to(DIST).as_posix())}</span></li>'
        for p in pages
    ) or "      <li>まだ資料はありません。</li>"

    updated = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    (DIST / "index.html").write_text(
        f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{SITE_TITLE}</title>
<style>
  :root {{ --bg:#fafaf9; --fg:#1c1917; --muted:#78716c; --link:#1d4ed8; --line:#e7e5e4; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#1c1917; --fg:#f5f5f4; --muted:#a8a29e; --link:#93c5fd; --line:#44403c; }}
  }}
  body {{ margin:0; background:var(--bg); color:var(--fg);
         font-family:system-ui,-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif; }}
  main {{ max-width:720px; margin:0 auto; padding:32px 16px; }}
  h1 {{ font-size:1.5rem; margin:0 0 4px; }}
  .updated {{ color:var(--muted); font-size:.85rem; margin:0 0 24px; }}
  ul {{ list-style:none; padding:0; margin:0; }}
  li {{ padding:12px 0; border-bottom:1px solid var(--line); }}
  a {{ color:var(--link); text-decoration:none; font-weight:600; }}
  a:hover {{ text-decoration:underline; }}
  .path {{ display:block; color:var(--muted); font-size:.8rem; margin-top:2px; }}
</style>
</head>
<body>
<main>
  <h1>{SITE_TITLE}</h1>
  <p class="updated">最終更新: {updated} (JST)</p>
  <ul>
{items}
  </ul>
</main>
</body>
</html>
""",
        encoding="utf-8",
    )
    print(f"Built {len(pages)} page(s) into {DIST}")


if __name__ == "__main__":
    main()
