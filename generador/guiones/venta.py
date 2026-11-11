"""Carruseles de venta: casos reales de clientes (estilo caso). Genera carruseles/venta/*.json."""
import json
from pathlib import Path

from nicho import PERFIL


def T(es, en):
    return {"es": es, "en": en}


def caso(nombre, semanas, foto, portada, problemas, proceso, clave, ficha, logros):
    """Estructura fija: portada → punto de partida → proceso → clave → resultado → CTA."""
    fotos = {"antes": f"fotos/caso-{foto}-antes.jpg", "despues": f"fotos/caso-{foto}-despues.jpg"}
    sem_total = T(f"SEM 0 → {semanas}", f"WK 0 → {semanas}")
    return [
        {"tipo": "portada", "semana": sem_total, "titulo": portada, "alto_fotos": 640, **fotos,
         "texto": T(f"**{nombre}** · {semanas} semanas", f"**{nombre}** · {semanas} weeks"), "centrado": True,
         "pie": T("Desliza para ver cómo →", "Swipe to see how →")},
        {"tipo": "punto", "semana": T("SEM 0", "WK 0"), "titulo": T("[El punto de partida]", "[Where he started]"),
         "lista": problemas, "marca": "no"},
        {"tipo": "punto", "semana": T(f"SEM 1–{semanas}", f"WK 1–{semanas}"), **proceso},
        {"tipo": "punto", "titulo": T("[La clave]", "[The key]"), "texto": clave},
        {"tipo": "punto", "semana": T(f"SEM {semanas}", f"WK {semanas}"), "titulo": T("[Cómo terminó]", "[How it ended]"),
         "alto_fotos": 330, **fotos, "ficha": ficha, "logros": logros},
        {"tipo": "cta", "etiqueta": T("¿Te suena [su historia]?", "Does [his story] sound familiar?"),
         "texto": T("Trabajo con hombres de +30 que quieren recuperar su físico y su energía [sin vivir en el gimnasio].\n\nEscríbeme **INFO** por DM y vemos si encajas.",
                    "I work with men over 30 who want their body and energy back [without living in the gym].\n\nDM me **INFO** and let's see if you're a fit."),
         "boton": T("Escríbeme INFO", "DM me INFO")},
    ]


C = {}

C["V1-javi"] = (T("Javi no tenía tiempo. Tenía un plan que encajaba con su vida. Escríbeme INFO.",
                  "Javi didn't have time. He had a plan that fit his life. DM me INFO."), caso(
    "Javi", 16, "javi",
    T("Un trabajo exigente, casi sin días libres… [y aun así quería volver a estar en forma.]",
      "A demanding job, almost no days off… [and he still wanted to get back in shape.]"),
    [T("Trabajo con casi ningún día libre", "Work schedule with almost no days off"),
     T("Ciclismo + gimnasio imposible de cuadrar", "Cycling + gym were hard to balance"),
     T("Ningún plan que encajara con su vida", "No structure that actually fit his life")],
    {"titulo": T("Cómo fue [por dentro]", "How it went [from the inside]"),
     "pasos": [(T("Semana 1", "Week 1"), T("Analítica y punto de partida", "Bloodwork and starting point")),
               (T("Semana 3", "Week 3"), T("Primera semana completa sin fallar", "First complete week without a miss")),
               (T("Semana 6", "Week 6"), T("La cintura se mueve por primera vez", "The waist moves for the first time")),
               (T("Semana 12", "Week 12"), T("Récord de fuerza y medidas bajando", "Strength record and measurements down"))]},
    T("Construimos el plan [alrededor de su trabajo y su bici], no al revés.\n\nCon 1 día libre cada 10, pudo ser constante igualmente.",
      "We built the plan [around his work and his cycling], not the other way around.\n\nWith 1 day off every 10, he could still stay consistent."),
    [(T("Peso", "Weight"), "−10", "kg"), (T("Tiempo", "Time"), "16", T("sem", "wks"))],
    [T("Trabajo, bici y entreno: por fin en equilibrio", "Work, cycling and training: finally balanced")],
))

C["V2-carl"] = (T("El segundo capítulo empezó donde estaba él. Escríbeme INFO.",
                  "Chapter two started where he was. DM me INFO."), caso(
    "Carl", 12, "carl",
    T("“Nunca volveré a mi nivel.” [Hoy está por encima del que tenía.]",
      "“I'll never get my level back.” [Today he's above where he was.]"),
    [T("Un parón largo que no eligió", "A long break he didn't choose"),
     T("Un duelo de por medio, todo por reconstruir", "Grief included, everything to rebuild"),
     T("Su miedo no era empezar: era no volver a su nivel", "His fear wasn't starting: it was never getting his level back")],
    {"titulo": T("[Protocolo] de 12 semanas", "12-week [protocol]"),
     "pasos": [(T("Sem 1–4 · Reparar", "Wk 1–4 · Repair"), T("Sueño, digestión y comer lo suficiente", "Sleep, digestion and eating enough")),
               (T("Sem 5–8 · Construir", "Wk 5–8 · Build"), T("Fuerza progresiva y proteína", "Progressive strength and protein")),
               (T("Sem 9–12 · Ajustar", "Wk 9–12 · Adjust"), T("Déficit controlado y medidas", "Controlled deficit and measurements"))]},
    T("El segundo capítulo no empezó donde acabó el primero: [empezó donde estaba ÉL].\n\nEsta vez con todo el motor revisado: sueño, digestión y recuperación.",
      "Chapter two didn't start where chapter one ended: [it started where HE was].\n\nThis time with the whole engine checked: sleep, digestion and recovery."),
    [(T("Cintura", "Waist"), "−8", "cm"), (T("Tiempo", "Time"), "12", T("sem", "wks"))],
    [T("Más fuerte que antes del parón", "Stronger than before the break"),
     T("Y con mucho mejor criterio", "And with far better judgement")],
))

C["V3-raul"] = (T("Perdió comiendo más que nunca. Si te suena, escríbeme INFO.",
                  "He lost it eating more than ever. Sound familiar? DM me INFO."), caso(
    "Raúl", 12, "raul",
    T("“Si no paso hambre, no estoy perdiendo.” [Perdió comiendo más que nunca.]",
      "“If I'm not hungry, I'm not losing.” [He lost it eating more than ever.]"),
    [T("Asociaba resultados con sufrimiento", "He equated results with suffering"),
     T("Comía muy poco y luego atracón los viernes", "Eating far too little, then bingeing on Fridays"),
     T("Nunca había terminado un plan", "He'd never finished a plan")],
    {"titulo": T("Sus [innegociables]", "His [non-negotiables]"), "marca": "si",
     "lista": [T("Nunca dos sesiones seguidas sin hacer", "Never two sessions missed in a row"),
               T("Proteína en cada comida principal", "Protein at every main meal"),
               T("La revisión se manda, semana buena o mala", "The check-in gets sent, good week or bad"),
               T("El fin de semana es parte del plan", "The weekend is part of the plan")]},
    T("El primer mes [subimos comida y bajamos sufrimiento].\n\nSolo después abrimos un déficit pequeño. Por primera vez, llegó al final.",
      "In month one we [raised food and lowered suffering].\n\nOnly then did we open a small deficit. For the first time, he made it to the end."),
    [(T("Peso", "Weight"), "−17", "kg"), (T("Tiempo", "Time"), "12", T("sem", "wks"))],
    [T("Su primer plan completo", "His first complete plan"),
     T("Ni un atracón en todo el proceso", "Not one binge the whole way")],
))

if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent.parent.parent / "carruseles" / "venta"
    for clave, (pie, slides) in C.items():
        cfg = {"nombre": f"venta-{clave}", "estilo": "caso", "idiomas": ["es", "en"], "perfil": PERFIL,
               "pie_de_post": pie, "slides": slides}
        (raiz / f"{clave}.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        print(clave)
