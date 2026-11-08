#!/usr/bin/env python3
"""Monta un cliente como UNA sola página (artifact multi-archivo).

Uso: python3 tools/hub.py clientes/<cliente> "Nombre visible"
Crea clientes/<cliente>/_hub/:
  index.html            -> índice del sistema (página principal del artifact)
  p/<parte>.html        -> cada parte envuelta como página propia, con botón "Índice"
  p/casos/*, p/*.jpg    -> imágenes que usan las partes
Imprime el mapa `files` para publicar con la herramienta Artifact.
"""
import html, json, os, re, shutil, sys

ORDEN = [
    ("index.html", "Landing", "La página para sus clientes potenciales"),
    ("partes/1-perfil.html", "1 · Perfil y nicho", "Nicho, método, bio, destacados y escaparate"),
    ("partes/2-oferta.html", "2 · Oferta", "Fases, precios, garantía y back-end"),
    ("partes/3-contenido.html", "3 · Contenido", "Plan semanal, ángulos, carruseles, guiones y Claude Code"),
    ("partes/4-embudo.html", "4 · Embudo", "Conversaciones, WhatsApp, anuncios y cierre paso a paso"),
    ("partes/5-formacion.html", "5 · Formación", "Plan de estudio"),
    ("partes/6-guion-cierre.html", "6 · Guion de cierre", "La llamada de venta, objeciones y seguimiento"),
    ("partes/crm.html", "7 · CRM", "Leads, clientes y escalera de precios (guarda datos)"),
    ("partes/7-reportes.html", "8 · Reporte", "Reporte diario y semanal para Alberto (guarda datos)"),
]

SKEL = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>*,*::before,*::after{box-sizing:border-box}body{margin:0}</style></head><body>')
BACK = ('<a href="{href}" style="position:fixed;left:12px;bottom:12px;z-index:9999;'
        'font:600 13px/1 system-ui,sans-serif;background:#111;color:#fff;padding:10px 14px;'
        'border-radius:999px;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.25)">← Índice</a>')


def main(folder, nombre):
    out = os.path.join(folder, "_hub")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(os.path.join(out, "p"))
    files, cards = {}, []
    for src, titulo, desc in ORDEN:
        path = os.path.join(folder, src)
        if not os.path.exists(path):
            continue
        name = "landing.html" if src == "index.html" else os.path.basename(src)
        body = open(path, encoding="utf-8").read()
        # imágenes relativas: copiar junto a la parte
        base = os.path.dirname(path)
        for ref in set(re.findall(r'(?:src|poster|href)="((?!https?:|data:|#|mailto:|tel:)[^"]+\.(?:jpg|jpeg|png|webp|mp4))"', body)):
            f = os.path.normpath(os.path.join(base, ref))
            if os.path.exists(f):
                dst = os.path.join(out, "p", ref)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy(f, dst)
                files["p/" + ref] = dst
        page = SKEL + body + BACK.format(href="../index.html") + "</body></html>"
        dst = os.path.join(out, "p", name)
        open(dst, "w", encoding="utf-8").write(page)
        files["p/" + name] = dst
        cards.append((f"p/{name}", titulo, desc))
    lis = "\n".join(
        f'<a class="card" href="{h}"><b>{html.escape(t)}</b><span>{html.escape(d)}</span></a>'
        for h, t, d in cards)
    index = f"""<title>{html.escape(nombre)} Sistema</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
:root{{--bg:#f6f6f4;--card:#fff;--ink:#111;--soft:#5c5c5c;--line:#e2e2df;--acc:#1f4fd1}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121212;--card:#1c1c1c;--ink:#f2f2f2;--soft:#a5a5a5;--line:#2c2c2c;--acc:#7b9bff}}}}
:root[data-theme="dark"]{{--bg:#121212;--card:#1c1c1c;--ink:#f2f2f2;--soft:#a5a5a5;--line:#2c2c2c;--acc:#7b9bff}}
[hidden]{{display:none!important}}
body{{background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,sans-serif;margin:0}}
main{{max-width:760px;margin:0 auto;padding:32px 16px 48px}}
h1{{font-size:28px;line-height:1.15;margin:0 0 6px}} p.lead{{color:var(--soft);margin:0 0 24px}}
.grid{{display:grid;gap:12px}} .card{{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;color:inherit;text-decoration:none}}
.card b{{display:block;font-size:17px;margin-bottom:2px}} .card span{{color:var(--soft);font-size:14px}}
.card:hover{{border-color:var(--acc)}}
</style>
<main>
<h1>Sistema de {html.escape(nombre)}</h1>
<p class="lead">Todo tu sistema en un solo enlace. Entra en cada parte y vuelve con el botón «Índice».</p>
<div class="grid">
{lis}
</div>
</main>
"""
    idx = os.path.join(out, "index.html")
    open(idx, "w", encoding="utf-8").write(index)
    print(json.dumps({"file_path": os.path.abspath(idx),
                      "files": {k: os.path.abspath(v) for k, v in files.items()}}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
