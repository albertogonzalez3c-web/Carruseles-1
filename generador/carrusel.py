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
  dibujo    -> CONEXIÓN humor. Dos viñetas con efecto cómic + frase gruesa con contorno negro abajo.
  caja      -> CONEXIÓN "Te juzgan". Dos fotos + texto a la izquierda en caja oscura translúcida arriba.
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


def dibujo(img):
    """Efecto ilustración suave: piel y superficies lisas, color vivo y contornos finos y discretos."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return img
    a = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    base = a.copy()
    for _ in range(3):
        base = cv2.bilateralFilter(base, 9, 35, 7)
    pintado = cv2.stylization(base, sigma_s=30, sigma_r=0.25)
    res = pintado.astype("float32") * 0.6 + base.astype("float32") * 0.4
    gris = cv2.GaussianBlur(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), (5, 5), 0)
    bordes = cv2.GaussianBlur(cv2.Canny(gris, 70, 160), (3, 3), 0).astype("float32")[..., None] / 255 * 0.35
    res = res * (1 - bordes) + 30 * bordes
    hsv = cv2.cvtColor(np.clip(res, 0, 255).astype("uint8"), cv2.COLOR_BGR2HSV).astype("float32")
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.15, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * 1.06 + 6, 0, 255)
    return Image.fromarray(cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2RGB))


def slide_dibujo(s):
    """Dos viñetas tipo cómic con frase gruesa y contorno negro abajo: 'Pintura de $200: supervisa.'"""
    img = Image.new("RGB", (W, H), NEGRO)
    mitad = H // 2
    for i, parte in enumerate((s["arriba"], s["abajo"])):
        foto = dibujo(abrir_foto(parte["foto"], W, mitad - 3, parte.get("foco"), parte.get("zoom", 1)))
        img.paste(foto, (0, i * (mitad + 3)))
        d = ImageDraw.Draw(img)
        f = fuente("Black", parte.get("tam", 58))
        texto = t(parte.get("texto", ""))
        lineas = partir(texto, f, W - 100, d)
        alto = len(lineas) * int(f.size * 1.1)
        y0 = i * (mitad + 3)
        y = y0 + int((mitad - 3) * parte.get("texto_pos", 0.8)) - alto // 2
        for linea in lineas:
            d.text((W // 2, y), linea, font=f, fill=BLANCO, anchor="ma", stroke_width=7, stroke_fill=NEGRO)
            y += int(f.size * 1.1)
    return img


def slide_caja(s):
    """Dos fotos apiladas con texto alineado a la izquierda en una caja oscura translúcida (estilo 'Te juzgan.')."""
    img = Image.new("RGB", (W, H))
    mitad = H // 2
    for i, parte in enumerate((s["arriba"], s["abajo"])):
        foto = abrir_foto(parte["foto"], W, mitad, parte.get("foco"), parte.get("zoom", 1))
        img.paste(foto, (0, i * mitad))
        d = ImageDraw.Draw(img, "RGBA")
        f = fuente("DisplayBold", parte.get("tam", 64))
        texto = t(parte.get("texto", ""))
        ancho = int(W * 0.58)
        lineas = partir(texto, f, ancho, d)
        paso = int(f.size * 1.02)
        tw = max(d.textlength(l, font=f) for l in lineas)
        th = len(lineas) * paso
        pad = 22
        y0 = i * mitad + 95 if parte.get("vertical", "arriba") == "arriba" else (i + 1) * mitad - 50 - th - 2 * pad
        # Lado: el que no tape caras (por defecto derecha, como la referencia).
        lados = {"derecha": W - 40 - tw - 2 * pad, "izquierda": 40}
        lado = parte.get("lado")
        if not lado:
            lado = "derecha"
            for nombre, x in lados.items():
                caja = (x, y0, x + tw + 2 * pad, y0 + th + 2 * pad)
                if not any(c[0] < caja[2] and c[2] > caja[0] and c[1] + i * mitad < caja[3] and c[3] + i * mitad > caja[1]
                           for c in caras(foto)):
                    lado = nombre
                    break
        x = lados[lado]
        d.rounded_rectangle((x, y0, x + tw + 2 * pad, y0 + th + 2 * pad), radius=14, fill=(20, 30, 40, 130))
        yy = y0 + pad - 4
        for linea in lineas:
            d.text((x + pad, yy), linea, font=f, fill=BLANCO)
            yy += paso
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
    """Etiqueta de color + titular blanco alineados a la izquierda, arriba o abajo según dónde no haya caras."""
    foto = abrir_foto(s["foto"], foco=s.get("foco"), zoom=s.get("zoom", 1))
    d = ImageDraw.Draw(foto, "RGBA")
    f_et = fuente("ExtraBold", s.get("tam_etiqueta", 70))
    f_tx = fuente("Bold", s.get("tam", 62))
    et = t(s.get("etiqueta", "")).upper()
    tx = t(s.get("texto", ""))
    alto = (len(partir(et, f_et, W - 160, d)) * int(f_et.size * 1.18) + 10 if et else 0) + \
        len(partir(tx, f_tx, W - 180, d)) * int(f_tx.size * 1.18)
    pos = s.get("texto_pos")
    if pos not in ("arriba", "abajo"):
        arriba = (0, 110, W, 110 + alto)
        tapa = any(c[1] < arriba[3] and c[3] > arriba[1] for c in caras(foto))
        pos = "abajo" if tapa else "arriba"
    if pos == "arriba":
        img = degradado(foto, int(H * 0.55), 0, 200)
        y = 110
    else:
        img = degradado(foto, int(H * 0.40), H, 215)
        y = H - 110 - alto
    d = ImageDraw.Draw(img, "RGBA")
    x = 80
    if et:
        color = tuple(int(s.get("color", "#FF8A1F").lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        y = bloque(d, et, f_et, x, y, W - 160, color, ancla="la", sombra=True) + 10
    bloque(d, tx, f_tx, x, y, W - 180, BLANCO, ancla="la", sombra=True)
    return img


# ---------- estilo "oscuro" (fondo negro texturizado + cabecera de perfil + acentos amarillos) ----------
#
# Marcado en los textos:  [palabras] = amarillo en negrita · **palabras** = blanco en negrita
# Párrafos separados con \n\n. Cada slide lleva "tipo": portada | punto | cta.

AMARILLO = (247, 230, 50)
PERFIL = {}  # se rellena desde el JSON: {"nombre", "usuario", "foto", "foco"}


def fondo_oscuro():
    import random
    rnd = random.Random(7)
    img = Image.new("RGB", (W, H), (8, 8, 8))
    # Haz de luz diagonal suave.
    luz = Image.new("L", (W, H), 0)
    ImageDraw.Draw(luz).polygon([(W * 0.15, -50), (W * 0.55, -50), (W * 0.95, H * 0.75), (W * 0.45, H * 0.75)], fill=70)
    luz = luz.filter(ImageFilter.GaussianBlur(160))
    img = Image.composite(Image.new("RGB", (W, H), (60, 60, 60)), img, luz)
    # Viñeta.
    vin = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vin).ellipse((-W * 0.3, -H * 0.2, W * 1.3, H * 1.1), fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(220))
    img = Image.composite(img, Image.new("RGB", (W, H), (0, 0, 0)), vin)
    # Grano fino.
    ruido = Image.effect_noise((W, H), 18).convert("RGB")
    return Image.blend(img, ruido, 0.06)


def recorte_cara(ruta, lado):
    """Recorte cuadrado centrado en la cara más grande de la foto (para la foto de perfil)."""
    img = ImageOps.exif_transpose(Image.open(RAIZ / ruta)).convert("RGB")
    escala = 900 / max(img.size)
    peq = img.resize((int(img.width * escala), int(img.height * escala)))
    cs = caras(peq)
    if not cs:
        return ImageOps.fit(img, (lado, lado), Image.LANCZOS, centering=(0.5, 0.3))
    x0, y0, x1, y1 = max(cs, key=lambda c: (c[2] - c[0]) * (c[3] - c[1]))
    cx, cy, tam = (x0 + x1) / 2 / escala, (y0 + y1) / 2 / escala, (x1 - x0) / escala * 1.5
    caja = (max(0, cx - tam / 2), max(0, cy - tam / 2), min(img.width, cx + tam / 2), min(img.height, cy + tam / 2))
    return ImageOps.fit(img.crop(tuple(int(v) for v in caja)), (lado, lado), Image.LANCZOS)


def avatar(diam, aro=8):
    """Foto de perfil circular con aro degradado tipo historia de Instagram."""
    base = recorte_cara(PERFIL["foto"], diam) if PERFIL.get("foto") else Image.new("RGB", (diam, diam), (80, 80, 80))
    total = diam + 2 * aro
    anillo = Image.new("RGB", (total, total))
    da = ImageDraw.Draw(anillo)
    for i in range(total):
        t_ = i / total
        c = (int(250 - 40 * t_), int(180 - 150 * t_), int(40 + 160 * t_))
        da.line([(0, i), (total, i)], fill=c)
    capa = Image.new("RGBA", (total, total), (0, 0, 0, 0))
    m = Image.new("L", (total, total), 0)
    ImageDraw.Draw(m).ellipse((0, 0, total - 1, total - 1), fill=255)
    capa.paste(anillo, (0, 0), m)
    hueco = Image.new("L", (total, total), 0)
    ImageDraw.Draw(hueco).ellipse((aro - 3, aro - 3, total - aro + 2, total - aro + 2), fill=255)
    capa.paste(Image.new("RGB", (total, total), (10, 10, 10)), (0, 0), hueco)
    mf = Image.new("L", (diam, diam), 0)
    ImageDraw.Draw(mf).ellipse((3, 3, diam - 4, diam - 4), fill=255)
    capa.paste(base, (aro, aro), mf)
    return capa


def cabecera(img, centrada=False, y=70):
    d = ImageDraw.Draw(img)
    av = avatar(120 if not centrada else 150)
    nombre, usuario = PERFIL.get("nombre", ""), PERFIL.get("usuario", "")
    fn, fu = fuente("SemiBold", 40 if not centrada else 44), fuente("Regular", 30 if not centrada else 32)
    if centrada:
        img.paste(av, ((W - av.width) // 2, y), av)
        yy = y + av.height + 18
        d.text((W // 2, yy), nombre, font=fn, fill=BLANCO, anchor="ma")
        if usuario:
            d.text((W // 2, yy + 50), usuario, font=fu, fill=(200, 200, 200), anchor="ma")
        return yy + (100 if usuario else 55)
    img.paste(av, (70, y), av)
    tx = 70 + av.width + 22
    cy = y + av.height // 2
    if usuario:
        d.text((tx, cy - 4), nombre, font=fn, fill=BLANCO, anchor="ls")
        d.text((tx, cy + 6), usuario, font=fu, fill=(200, 200, 200), anchor="lt")
    else:
        d.text((tx, cy), nombre, font=fn, fill=BLANCO, anchor="lm")
    return y + av.height


def trozos(texto, peso_base="Regular"):
    """Convierte '[amarillo] y **negrita**' en palabras con estilo: (palabra, peso, color, pegada_a_la_anterior)."""
    import re
    salida = []
    for bruto in re.split(r"(\[[^\]]+\]|\*\*[^*]+\*\*)", texto):
        if not bruto:
            continue
        if bruto.startswith("["):
            peso, color, parte = "Bold", AMARILLO, bruto[1:-1]
        elif bruto.startswith("**"):
            peso, color, parte = "Bold", BLANCO, bruto[2:-2]
        else:
            peso, color, parte = peso_base, BLANCO, bruto
        # Pegada si no hay espacio entre este trozo y el anterior (ej. "[testosterona].").
        pegada = bool(salida) and not parte[:1].isspace() and not ultimo_espacio
        for i, pal in enumerate(parte.split()):
            salida.append((pal, peso, color, pegada and i == 0))
        ultimo_espacio = parte[-1:].isspace()
    return salida


def parrafo(d, texto, x, y, ancho, tam, peso_base="Regular", centrado=False, interlineado=1.12):
    """Texto con estilos mezclados, con salto de línea automático. Devuelve la y final."""
    palabras = trozos(texto, peso_base)
    esp = fuente(peso_base, tam).getlength(" ")
    lineas, actual, ancho_act = [], [], 0
    for pal, peso, color, pegado in palabras:
        f = fuente(peso, tam)
        w = f.getlength(pal)
        sep = 0 if (pegado or not actual) else esp
        if actual and ancho_act + sep + w > ancho and not pegado:
            lineas.append((actual, ancho_act))
            actual, ancho_act, sep = [], 0, 0
        actual.append((pal, f, color, sep))
        ancho_act += sep + w
    if actual:
        lineas.append((actual, ancho_act))
    for linea, lw in lineas:
        xx = x + (ancho - lw) / 2 if centrado else x
        for pal, f, color, sep in linea:
            xx += sep
            d.text((xx, y), pal, font=f, fill=color)
            xx += f.getlength(pal)
        y += int(tam * interlineado)
    return y


def tarjeta_foto(img, ruta, caja, foco=None, zoom=1):
    x0, y0, x1, y1 = caja
    w, h = x1 - x0, y1 - y0
    foto = abrir_foto(ruta, w, h, foco, zoom)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=255)
    borde = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    ImageDraw.Draw(borde).rounded_rectangle((0, 0, w + 7, h + 7), radius=38, fill=(120, 120, 120, 150))
    img.paste(borde, (x0 - 4, y0 - 4), borde)
    img.paste(foto, (x0, y0), m)


def pie_desliza(d, texto):
    d.text((W // 2, H - 120), texto, font=fuente("Regular", 34), fill=(225, 225, 225), anchor="ma")


def slide_oscuro(s):
    img = fondo_oscuro()
    d = ImageDraw.Draw(img)
    tipo = s.get("tipo", "punto")
    if tipo == "cta":
        y = cabecera(img, centrada=True, y=230) + 80
        if s.get("etiqueta"):
            y = parrafo(d, t(s["etiqueta"]), 110, y, W - 220, 64, "Bold", centrado=True) + 36
        for p_ in t(s.get("texto", "")).split("\n\n"):
            y = parrafo(d, p_, 110, y, W - 220, 48, centrado=True, interlineado=1.2) + 26
        boton = t(s.get("boton", {"es": "Sígueme", "en": "Follow me"}))
        fb = fuente("Bold", 50)
        bw = int(fb.getlength(boton)) + 140
        y += 40
        d.rounded_rectangle(((W - bw) // 2, y, (W + bw) // 2, y + 110), radius=55, fill=AMARILLO)
        d.text((W // 2, y + 55), boton, font=fb, fill=NEGRO, anchor="mm")
        return img
    y = cabecera(img) + 60
    if tipo == "portada":
        if s.get("numero"):
            d.text((W // 2, y - 10), t(s["numero"]), font=fuente("Black", 280), fill=AMARILLO, anchor="ma")
            y += 290
        y = parrafo(d, t(s.get("texto", "")), 90, y, W - 180, 66, "SemiBold", centrado=True, interlineado=1.08)
        if s.get("subtexto"):
            y = parrafo(d, t(s["subtexto"]), 90, y + 4, W - 180, 40, centrado=True)
        if s.get("foto"):
            alto = H - 200 - (y + 40)
            ancho = min(W - 180, int(alto * 1.5))
            tarjeta_foto(img, s["foto"], ((W - ancho) // 2, y + 40, (W + ancho) // 2, y + 40 + alto), s.get("foco"), s.get("zoom", 1))
        pie_desliza(d, t(s.get("pie", {"es": "Desliza para explicarte →", "en": "Swipe to learn more →"})))
        return img
    # punto: titular amarillo + foto opcional + cuerpo
    cuerpo = t(s.get("texto", ""))
    if s.get("foto"):
        y = parrafo(d, t(s.get("titulo", "")), 110, y + 30, W - 220, 64, "Bold", interlineado=1.05) + 50
        alto_foto = s.get("alto_foto", 430)
        tarjeta_foto(img, s["foto"], (110, y, W - 110, y + alto_foto), s.get("foco"), s.get("zoom", 1))
        y += alto_foto + 50
        for p_ in cuerpo.split("\n\n"):
            if p_:
                y = parrafo(d, p_, 110, y, W - 220, 44) + 20
    else:
        # Centrado vertical del bloque de texto, como en la referencia.
        prueba = Image.new("RGB", (W, H))
        dp = ImageDraw.Draw(prueba)
        yy = parrafo(dp, t(s.get("titulo", "")), 110, 0, W - 220, 70, "Bold", interlineado=1.05) + 50
        for p_ in cuerpo.split("\n\n"):
            yy = parrafo(dp, p_, 110, yy, W - 220, 50) + 30
        y = max(y + 40, (H - yy) // 2 + 40)
        y = parrafo(d, t(s.get("titulo", "")), 110, y, W - 220, 70, "Bold", interlineado=1.05) + 50
        for p_ in cuerpo.split("\n\n"):
            y = parrafo(d, p_, 110, y, W - 220, 50) + 30
    pie_desliza(d, t(s.get("pie", {"es": "Desliza para ver más →", "en": "Swipe for more →"})))
    return img


ESTILOS = {"oscuro": slide_oscuro, "dibujo": slide_dibujo, "caja": slide_caja, "doble": slide_doble, "cierre": slide_cierre, "subtitulo": slide_subtitulo, "tarjeta": slide_tarjeta, "titular": slide_titular}


def generar(ruta_json):
    """Si el JSON trae "idiomas": ["es", "en"], genera una carpeta por idioma (<nombre>-es, <nombre>-en)."""
    global IDIOMA
    cfg = json.loads(Path(ruta_json).read_text(encoding="utf-8"))
    for idioma in cfg.get("idiomas", [None]):
        IDIOMA = idioma
        generar_idioma(cfg, ruta_json, idioma)


def generar_idioma(cfg, ruta_json, idioma):
    PERFIL.clear()
    PERFIL.update(cfg.get("perfil", {}))
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
