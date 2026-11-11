"""Pasa los carruseles de nicho (estilo oscuro, K..Y) al estilo titular (foto + etiqueta naranja), solo en inglés."""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
# Fotos con luz y encuadre limpio para rellenar las slides que en el estilo oscuro no llevaban foto.
POOL = ["hk-pose", "dubai-piscina-infinita", "safari-atardecer", "tailandia-cabana", "dubai-playa-rosa", "gym-triceps-amarillo",
        "hawaii-playa", "miami-parque", "gym-jalon-amarillo", "la-sentado", "desierto", "comida-coco", "dubai-fruta",
        "gym-disco", "bungalow-sentado", "hk-espaldas", "jeep-hawaii", "gym-mancuernas-rojo", "la-espaldas", "conduciendo-range",
        "gym-muscleworks", "miami-playa", "paracaidas", "escalera-dorada", "gym-remo-cable", "hk-cerca"]


def limpio(txt):
    """Quita el marcado [amarillo] / **negrita** y junta párrafos con un salto simple."""
    txt = re.sub(r"\*\*([^*]+)\*\*", r"\1", txt)
    txt = re.sub(r"\[([^\]]+)\]", r"\1", txt)
    return re.sub(r"\n\n+", "\n", txt)


def en(v):
    return v["en"] if isinstance(v, dict) else (v or "")


def convertir(ruta, desfase):
    cfg = json.loads(ruta.read_text(encoding="utf-8"))
    usadas = {s["foto"] for s in cfg["slides"] if s.get("foto")}
    libres = [f"fotos/{p}.jpg" for p in POOL[desfase:] + POOL[:desfase] if f"fotos/{p}.jpg" not in usadas]
    slides, vistas = [], set()
    for s in cfg["slides"]:
        foto = s.get("foto")
        if not foto or foto in vistas:
            foto = next(f for f in libres if f not in vistas)
            s = {**s, "foco": [0.5, 0.45]}
        vistas.add(foto)
        tipo = s.get("tipo")
        if tipo == "portada":
            etiqueta = (f"{en(s['numero'])} " if s.get("numero") else "") + limpio(en(s["texto"]))
            texto = ""
        elif tipo == "cta":
            etiqueta = limpio(en(s["etiqueta"]))
            texto = limpio(en(s["texto"]))
        else:
            etiqueta = limpio(en(s.get("titulo", "")))
            texto = limpio(en(s.get("texto", "")))
        slides.append({"foto": foto, "foco": s.get("foco", [0.5, 0.45]), "etiqueta": etiqueta, "texto": texto,
                       "tam": 46, "tam_etiqueta": 62 if tipo == "portada" else 56})
    nombre = cfg["nombre"].replace("calentamiento-", "titular-en-")
    out = {"nombre": nombre, "estilo": "titular", "pie_de_post": en(cfg.get("pie_de_post")), "slides": slides}
    (RAIZ / "carruseles" / "titular-en" / (ruta.stem + ".json")).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return nombre


if __name__ == "__main__":
    for i, ruta in enumerate(sorted((RAIZ / "carruseles" / "calentamiento").glob("[K-Y]-*.json"))):
        print(convertir(ruta, (i * 5) % len(POOL)))
