#!/usr/bin/env python3
"""md2pdf.py entrada.md salida.pdf — Markdown sencillo a PDF A4 (Chromium)."""
import re, html, sys, tempfile, os
from playwright.sync_api import sync_playwright
md = open(sys.argv[1], encoding="utf-8").read(); out = []
for line in md.split("\n"):
    l = html.escape(line); l = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", l); l = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<i>\1</i>", l)
    if line.startswith("### "): out.append(f"<h3>{l[4:]}</h3>")
    elif line.startswith("## "): out.append(f"<h2>{l[3:]}</h2>")
    elif line.startswith("# "): out.append(f"<h1>{l[2:]}</h1>")
    elif line.startswith("> "): out.append(f"<blockquote>{l[5:]}</blockquote>")
    elif line.startswith("---"): out.append("<hr>")
    elif re.match(r"^(\d+\.|-) ", line): out.append('<p class="li">' + re.sub(r"^- ", "• ", l).replace("[ ]", "☐") + "</p>")
    elif line.strip(): out.append(f"<p>{l}</p>")
css = """body{font:11pt/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#111}h1{font-size:19pt;color:#1c3041;margin:0 0 8pt}h2{font-size:14pt;color:#1c3041;border-bottom:3px solid #3f88c5;padding-bottom:3pt;margin:18pt 0 6pt}h3{font-size:12pt;color:#2f74ad;margin:14pt 0 4pt;page-break-after:avoid}blockquote{margin:3pt 0;padding:4pt 10pt;border-left:4px solid #3f88c5;background:#f3f9fe}p{margin:3pt 0}p.li{margin:1pt 0 1pt 10pt}hr{border:0;border-top:1px solid #ddd}b{color:#1c3041}"""
f = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8"); f.write('<!doctype html><meta charset="utf-8"><style>' + css + "</style>" + "\n".join(out)); f.close()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"); pg = b.new_page(); pg.goto("file://" + f.name)
    pg.pdf(path=sys.argv[2], format="A4", margin={"top": "16mm", "bottom": "16mm", "left": "16mm", "right": "16mm"})
os.unlink(f.name)
