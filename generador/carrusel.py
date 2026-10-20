#!/usr/bin/env python3
"""Genera carruseles de Instagram (1080x1350) a partir de tus fotos y un guion JSON.

Uso:
    python3 generador/carrusel.py ejemplos/conexion.json
    python3 generador/carrusel.py ejemplos/*.json

Cada JSON define un carrusel:
    {
      "nombre": "conexion-origen",
      "estilo": "doble" | "cierre" | "subtitulo" | "tarjeta" | "titular",
      "contador": true,
      "slides": [
        {"foto": "fotos/01.jpg", "texto": "Frase de la slide"},
        ...
      ]
    }

Estilos (calcados de las referencias). Cada slide puede sobrescribir el estilo con "estilo":
  doble     -> CONEXIÓN "reflejo". Dos fotos apiladas, frase centrada en cada una.
               slide: {"arriba": {"foto", "texto"}, "abajo": {"foto", "texto"}}
  cierre    -> Una foto oscurecida con el mensaje final centrado.
  subtitulo -> CONEXIÓN. Foto a pantalla completa + una frase tipo subtítulo abajo.
  tarjeta   -> VENTA / PRUEBA. Fondo blanco, titular arriba, foto centrada, remate abajo.
  titular   -> CALENTAMIENTO / VALOR. Foto oscurecida + etiqueta de color + titular grande arriba.

Las fotos se recortan solas al centro (4:5). Las rutas de foto son relativas a la raíz del repo.
Salida: salida/<nombre>/01.png, 02.png, ...
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

IDIOMA = None  # idioma activo cuando los textos vienen como {"es": ..., "en": ...}


def t(valor):
    """Devuelve el texto en el idioma activo si el valor es un diccionario de idiomas."""
    if isinstance(valor, dict):
        return valor.get(IDIOMA) or next(iter(valor.values()))
    return valor or ""


RAIZ = Path(__file__).resolve().parent.parent
FUENTES = Path(__file__).resolve().parent / "fuentes"
W, H = 1080, 1350
BLANCO = (255, 255, 255)
NEGRO = (17, 17, 17)


def fuente(peso, tam):
    return ImageFont.truetype(str(FUENTES / f"Inter-{peso}.otf"), tam)


def abrir_foto(ruta, w=W, h=H, foco=None, zoom=1):
    p = RAIZ / ruta
    if not p.exists():
        # Marcador gris para poder maquetar antes de tener la foto.
        img = Image.new("RGB", (w, h), (60, 60, 60))
        d = ImageDraw.Draw(img)
        d.text((w // 2, h // 2), f"FALTA FOTO\n{ruta}", font=fuente("Bold", 40),
               fill=BLANCO, anchor="mm", align="center")
        return img
    img = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    if zoom > 1:
        # Recorta alrededor del foco para acercar al sujeto cuando sale pequeño en la foto.
        fx, fy = foco or (0.5, 0.4)
        cw, ch = img.width / zoom, img.height / zoom
        x0 = min(max(fx * img.width - cw / 2, 0), img.width - cw)
        y0 = min(max(fy * img.height - ch / 2, 0), img.height - ch)
        img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
        foco = (0.5, 0.3)
    # foco = [x, y] de 0 a 1: qué punto de la foto se queda en el centro del recorte.
    return ImageOps.fit(img, (w, h), Image.LANCZOS, centering=tuple(foco or (0.5, 0.4)))


def partir(texto, f, ancho_max, draw):
    """Ajusta el texto al ancho respetando saltos de línea manuales."""
    lineas = []
    for parrafo in texto.split("\n"):
        actual = ""
        for palabra in parrafo.split():
            prueba = f"{actual} {palabra}".strip()
            if draw.textlength(prueba, font=f) <= ancho_max:
                actual = prueba
            else:
                if actual:
                    lineas.append(actual)
                actual = palabra
        lineas.append(actual)
    return lineas


def bloque(draw, texto, f, x, y, ancho_max, color, ancla="ma", interlineado=1.18, sombra=False):
    """Dibuja un bloque de texto. ancla 'ma' = centrado, 'la' = izquierda. Devuelve la y final."""
    alto = int(f.size * interlineado)
    for linea in partir(texto, f, ancho_max, draw):
        if sombra:
            draw.text((x + 2, y + 3), linea, font=f, fill=(0, 0, 0, 200), anchor=ancla)
        draw.text((x, y), linea, font=f, fill=color, anchor=ancla)
        y += alto
    return y


def degradado(img, desde, hasta, opacidad_max):
    """Oscurece verticalmente entre dos alturas (para que el texto se lea)."""
    capa = Image.new("L", (1, H), 0)
    for yy in range(H):
        if desde < hasta:
            t = (yy - desde) / (hasta - desde)
        else:
            t = (desde - yy) / (desde - hasta)
        capa.putpixel((0, yy), int(max(0, min(1, t)) * opacidad_max))
    capa = capa.resize((W, H))
    negro = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(negro, img, capa)


def contador(draw, i, n, oscuro=False):
    f = fuente("SemiBold", 26)
    txt = f"{i}/{n}"
    caja = draw.textbbox((0, 0), txt, font=f)
    cw, ch = caja[2] - caja[0] + 28, caja[3] - caja[1] + 18
    x0, y0 = W - cw - 36, 36
    fondo = (0, 0, 0, 110) if not oscuro else (0, 0, 0, 25)
    draw.rounded_rectangle((x0, y0, x0 + cw, y0 + ch), radius=ch // 2, fill=fondo)
    draw.text((x0 + cw // 2, y0 + ch // 2), txt, font=f, fill=NEGRO if oscuro else BLANCO, anchor="mm")


# ---------- estilos ----------

def slide_subtitulo(s):
    img = degradado(abrir_foto(s["foto"], foco=s.get("foco")), int(H * 0.55), H, 190)
    d = ImageDraw.Draw(img, "RGBA")
    f = fuente("Bold", s.get("tam", 56))
    lineas = partir(t(s.get("texto", "")), f, W - 160, d)
    y = int(H * 0.80) - len(lineas) * int(f.size * 1.18) // 2
    bloque(d, t(s.get("texto", "")), f, W // 2, y, W - 160, BLANCO, sombra=True)
    return img


def caras(img):
    """Cajas (x0, y0, x1, y1) de caras detectadas (frontal y de perfil). Lista vacía si no hay OpenCV."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return []
    gris = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    cajas = []
    for modelo, espejo in (("haarcascade_frontalface_default.xml", False),
                           ("haarcascade_profileface.xml", False),
                           ("haarcascade_profileface.xml", True)):
        cascada = cv2.CascadeClassifier(cv2.data.haarcascades + modelo)
        g = cv2.flip(gris, 1) if espejo else gris
        for x, y, w, h in cascada.detectMultiScale(g, 1.1, 6, minSize=(40, 40)):
            if espejo:
                x = g.shape[1] - x - w
            # Margen para no rozar frente ni barbilla.
            cajas.append((x - w * 0.2, y - h * 0.35, x + w * 1.2, y + h * 1.3))
    return cajas


def texto_centrado(img, texto, tam, caja, pos=None, evitar=None):
    """Texto blanco centrado en horizontal dentro de caja=(x0, y0, x1, y1).

    pos: None = automático (centro si no tapa ninguna cara, si no, el hueco libre más cercano),
         "arriba" | "centro" | "abajo", o un número de 0 a 1 (altura relativa del centro del texto).
    evitar: cajas de caras en coordenadas de img.
    """
    d = ImageDraw.Draw(img, "RGBA")
    f = fuente("Bold", tam)
    x0, y0, x1, y1 = caja
    lineas = partir(texto, f, (x1 - x0) - 160, d)
    alto = len(lineas) * int(tam * 1.12)
    margen = 50 if y1 - y0 < H else 120
    arriba, abajo = y0 + margen, y1 - margen - alto
    centro = (y0 + y1 - alto) // 2
    if pos in ("arriba", "centro", "abajo"):
        y = {"arriba": arriba, "centro": centro, "abajo": abajo}[pos]
    elif isinstance(pos, (int, float)):
        y = int(y0 + pos * (y1 - y0) - alto / 2)
    else:
        def solape(yy):
            return sum(max(0, min(yy + alto, c[3]) - max(yy, c[1])) for c in evitar or []
                       if c[1] < y1 and c[3] > y0)
        candidatos = sorted(range(arriba, abajo + 1, 10), key=lambda yy: (solape(yy) > 0, abs(yy - centro)))
        y = candidatos[0] if candidatos else centro
    bloque(d, texto, f, (x0 + x1) // 2, y, (x1 - x0) - 160, BLANCO, interlineado=1.12, sombra=True)


def oscurecer(img, opacidad):
    return Image.blend(img, Image.new("RGB", img.size, (0, 0, 0)), opacidad)


def slide_doble(s):
    """Dos fotos apiladas, cada una con su frase centrada: 'Tu X,' / 'es el reflejo de...'."""
    img = Image.new("RGB", (W, H))
    mitad = H // 2
    for i, parte in enumerate((s["arriba"], s["abajo"])):
        foto = oscurecer(abrir_foto(parte["foto"], W, mitad, parte.get("foco"), parte.get("zoom", 1)), s.get("oscuro", 0.28))
        img.paste(foto, (0, i * mitad))
        evitar = [(a, b + i * mitad, c, e + i * mitad) for a, b, c, e in caras(foto)]
        texto_centrado(img, t(parte.get("texto", "")), parte.get("tam", 66), (0, i * mitad, W, (i + 1) * mitad),
                       parte.get("texto_pos"), evitar)
    return img


def slide_cierre(s):
    """Una foto entera oscurecida con el mensaje final en el centro (párrafos con \\n\\n)."""
    img = oscurecer(abrir_foto(s["foto"], foco=s.get("foco")), s.get("oscuro", 0.35))
    texto_centrado(img, t(s.get("texto", "")), s.get("tam", 54), (0, 0, W, H), s.get("texto_pos"), caras(img))
    return img


def slide_tarjeta(s):
    img = Image.new("RGB", (W, H), BLANCO)
    d = ImageDraw.Draw(img, "RGBA")
    y = 110
    if s.get("titulo"):
        y = bloque(d, t(s["titulo"]).upper(), fuente("ExtraBold", 74), W // 2, y, W - 140, NEGRO)
    if s.get("subtitulo"):
        y = bloque(d, t(s["subtitulo"]), fuente("SemiBold", 44), W // 2, y + 10, W - 160, NEGRO)
    pie = t(s.get("texto", ""))
    f_pie = fuente("ExtraBold", 62)
    alto_pie = len(partir(pie, f_pie, W - 160, d)) * int(62 * 1.18) if pie else 0
    hueco_arriba = y + 40
    hueco_abajo = H - 110 - alto_pie - 40
    fh = max(300, hueco_abajo - hueco_arriba)
    fw = min(W - 220, int(fh * 0.8))
    foto = abrir_foto(s["foto"], fw, fh)
    mascara = Image.new("L", (fw, fh), 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0, fw, fh), radius=36, fill=255)
    sombra = Image.new("RGBA", (fw + 60, fh + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((30, 38, fw + 30, fh + 38), radius=36, fill=(0, 0, 0, 70))
    sombra = sombra.filter(ImageFilter.GaussianBlur(16))
    fx = (W - fw) // 2
    img.paste(sombra, (fx - 30, hueco_arriba - 30), sombra)
    img.paste(foto, (fx, hueco_arriba), mascara)
    if pie:
        bloque(d, pie, f_pie, W // 2, hueco_arriba + fh + 40, W - 160, NEGRO)
    return img


def slide_titular(s):
    img = degradado(abrir_foto(s["foto"]), int(H * 0.55), 0, 200)
    d = ImageDraw.Draw(img, "RGBA")
    x, y = 80, 110
    if s.get("etiqueta"):
        color = tuple(int(s.get("color", "#FF8A1F").lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        y = bloque(d, t(s["etiqueta"]).upper(), fuente("ExtraBold", 70), x, y, W - 160, color,
                   ancla="la", sombra=True)
        y += 10
    bloque(d, t(s.get("texto", "")), fuente("Bold", s.get("tam", 66)), x, y, W - 180, BLANCO,
           ancla="la", sombra=True)
    return img


ESTILOS = {"doble": slide_doble, "cierre": slide_cierre, "subtitulo": slide_subtitulo, "tarjeta": slide_tarjeta, "titular": slide_titular}


def generar(ruta_json):
    """Si el JSON trae "idiomas": ["es", "en"], genera una carpeta por idioma (<nombre>-es, <nombre>-en)."""
    global IDIOMA
    cfg = json.loads(Path(ruta_json).read_text(encoding="utf-8"))
    for idioma in cfg.get("idiomas", [None]):
        IDIOMA = idioma
        generar_idioma(cfg, ruta_json, idioma)


def generar_idioma(cfg, ruta_json, idioma):
    estilo_base = cfg.get("estilo", "subtitulo")
    slides = cfg["slides"]
    nombre = cfg.get("nombre", Path(ruta_json).stem) + (f"-{idioma}" if idioma else "")
    destino = RAIZ / "salida" / nombre
    destino.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(slides, 1):
        estilo = s.get("estilo", estilo_base)
        img = ESTILOS[estilo](s)
        if cfg.get("contador", True):
            contador(ImageDraw.Draw(img, "RGBA"), i, len(slides), oscuro=estilo == "tarjeta")
        img.save(destino / f"{i:02d}.png", optimize=True)
    print(f"{len(slides)} slides -> {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for r in sys.argv[1:]:
        generar(r)
