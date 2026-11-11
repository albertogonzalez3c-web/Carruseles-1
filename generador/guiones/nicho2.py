"""Segunda tanda de carruseles de nicho (estilo oscuro). Genera carruseles/calentamiento/U..Y.json."""
import json
from pathlib import Path

from nicho import PERFIL, P, cta, foto

C = {}

C["U-dopamina"] = ("¿Cuál de estas te roba más? Dímelo en comentarios y sígueme.", "Which one steals the most from you? Tell me and follow.", [
    P("portada", "Por qué no tienes ganas de nada [(y no es pereza)]", "Why you can't get motivated [(and it's not laziness)]",
      **foto("dubai-playa-rosa", (0.55, 0.45))),
    P("punto", "Es la molécula de las ganas: la que te empuja a [ir a por algo].\n\nNo es la del placer. Es la de la motivación.",
      "It's the molecule of drive: the one that pushes you to [go after something].\n\nNot pleasure. Motivation.",
      titulo=("¿Qué es la [dopamina]?", "What is [dopamine]?")),
    P("punto", "Scroll infinito, notificaciones, ultraprocesados, series en bucle.\n\nRecompensa inmediata sin esfuerzo. Y entonces [lo difícil se vuelve aburrido].",
      "Endless scrolling, notifications, ultra-processed food, binge-watching.\n\nInstant reward, zero effort. Then [hard things start to feel boring].",
      titulo=("[Dopamina barata]", "[Cheap dopamine]")),
    P("punto", "Entrenar, leer o trabajar en tu negocio se hace cuesta arriba.\n\nNo te falta disciplina: [tu listón de estímulo está demasiado alto].",
      "Training, reading or working on your business feels like an uphill battle.\n\nYou don't lack discipline: [your stimulation bar is set too high].",
      titulo=("El resultado", "The result")),
    P("punto", "Móvil fuera de la habitación. La primera hora del día sin pantallas. Notificaciones apagadas salvo llamadas.\n\n[Pequeños cambios, efecto enorme.]",
      "Phone out of the bedroom. First hour of the day screen-free. Notifications off except calls.\n\n[Small changes, huge effect.]",
      titulo=("Cómo lo reseteo", "How I reset it"), **foto("tailandia-cabana", (0.5, 0.62), 340)),
    P("punto", "Entrenar, el sol por la mañana, terminar una tarea difícil, una conversación de verdad.\n\n[Esfuerzo primero, recompensa después.]",
      "Training, morning sun, finishing a hard task, a real conversation.\n\n[Effort first, reward second.]",
      titulo=("Dopamina que [se gana]", "Dopamine you [earn]"), **foto("gym-mancuernas-rojo", (0.45, 0.55), 340)),
    cta(("Recupera las ganas. [Gánatelas.]", "Get your drive back. [Earn it.]")),
])

C["V-cafeina"] = ("Guárdalo y revisa a qué hora tomas tu último café. Sígueme para más.", "Save it and check when you have your last coffee. Follow for more.", [
    P("portada", "Tu café te está robando [la energía] que crees que te da", "Your coffee is stealing [the energy] you think it gives you",
      **foto("conduciendo-range", (0.4, 0.45))),
    P("punto", "La cafeína bloquea la adenosina, la señal de cansancio de tu cerebro.\n\nNo te da energía: [esconde el cansancio] durante unas horas.",
      "Caffeine blocks adenosine, your brain's tiredness signal.\n\nIt doesn't give you energy: [it hides the fatigue] for a few hours.",
      titulo=("Cómo funciona", "How it works")),
    P("punto", "Su vida media es de unas 5–6 horas.\n\nUn café a las 17h → a las 23h todavía tienes [cerca de la mitad] en el cuerpo.",
      "Its half-life is around 5–6 hours.\n\nA coffee at 5pm → at 11pm you still have [about half of it] in your system.",
      titulo=("La trampa de la [tarde]", "The [afternoon] trap")),
    P("punto", "Te duermes, pero el sueño profundo se resiente.\n\nAl día siguiente, más cansancio → más café. [El círculo vicioso.]",
      "You fall asleep, but your deep sleep suffers.\n\nNext day, more tired → more coffee. [The vicious circle.]",
      titulo=("Duermes peor [sin notarlo]", "You sleep worse [without noticing]")),
    P("punto", "Primer café 60–90 min después de despertar. El último, antes de las 14h. Máximo 2–3 al día.\n\n[Así lo uso yo]: como herramienta, no como muleta.",
      "First coffee 60–90 min after waking up. Last one before 2pm. Max 2–3 a day.\n\n[That's how I use it]: as a tool, not a crutch.",
      titulo=("Mis reglas", "My rules"), **foto("grabando-video", (0.5, 0.45), 340)),
    P("punto", "“Zero sugar” no es cero efecto. Una lata grande puede llevar [150–200 mg de cafeína]: como dos cafés.\n\nCuéntalas en tu total del día.",
      "“Zero sugar” doesn't mean zero effect. A large can can pack [150–200 mg of caffeine]: about two coffees.\n\nCount them in your daily total.",
      titulo=("Ojo con las [bebidas energéticas]", "Watch the [energy drinks]")),
    cta(("Menos café. [Más sueño.]", "Less coffee. [More sleep.]")),
])

C["W-proteina"] = ("Guárdalo y calcula tu cifra. Sígueme para más.", "Save it and work out your number. Follow for more.", [
    P("portada", "Cuánta [proteína] necesitas de verdad pasados los 30", "How much [protein] you really need after 30",
      **foto("comida-coco", (0.5, 0.4))),
    P("punto", "Si entrenas fuerza: [1,6–2,2 g por kg] de peso al día.\n\nEjemplo: pesas 80 kg → unos 130–175 g diarios.",
      "If you strength train: [1.6–2.2 g per kg] of bodyweight a day.\n\nExample: 80 kg (176 lb) → about 130–175 g daily.",
      titulo=("La cifra", "The number")),
    P("punto", "Con los años, el músculo responde peor a la proteína.\n\nPasados los 30 no necesitas menos. [Necesitas más, y mejor repartida.]",
      "As you age, muscle responds less to protein.\n\nAfter 30 you don't need less. [You need more, and better spread out.]",
      titulo=("Por qué importa [más] con la edad", "Why it matters [more] with age")),
    P("punto", "3–4 comidas con 30–40 g cada una.\n\nFunciona mejor que meterlo todo en una cena enorme.",
      "3–4 meals with 30–40 g each.\n\nIt works better than cramming it all into one huge dinner.",
      titulo=("[Repártela]", "[Spread it out]"), **foto("dubai-fruta", (0.55, 0.6), 340)),
    P("punto", "~130 g de pechuga de pollo (en crudo).\n\n2 huevos + 5 claras.\n\n1 lata y media de atún.\n\n[Más fácil de lo que parece.]",
      "~130 g (4.5 oz) of raw chicken breast.\n\n2 eggs + 5 egg whites.\n\nA can and a half of tuna.\n\n[Easier than it looks.]",
      titulo=("Cómo son [30 gramos]", "What [30 grams] looks like")),
    P("punto", "Desayunas café y una tostada. A la hora de cenar llevas 50 g.\n\nEmpieza el día con [30 g de proteína] y todo lo demás se ordena.",
      "Breakfast is coffee and toast. By dinner you're at 50 g.\n\nStart your day with [30 g of protein] and everything else falls into place.",
      titulo=("El error típico", "The classic mistake"), **foto("gym-jalon-amarillo", (0.45, 0.4), 340)),
    cta(("Sin proteína [no hay músculo].", "No protein, [no muscle].")),
])

C["X-viajes"] = ("¿A dónde viajas pronto? Guárdalo para ese viaje y sígueme.", "Where are you traveling next? Save this for that trip and follow.", [
    P("portada", "Viajo mucho y [no pierdo el físico]: este es mi protocolo", "I travel a lot and [never lose my physique]: here's my protocol",
      **foto("safari-atardecer", (0.45, 0.6))),
    P("punto", "3 sesiones de 30–45 minutos: hotel, gimnasio local o peso corporal.\n\n[Mantener cuesta mucho menos que construir.]",
      "3 sessions of 30–45 minutes: hotel, local gym or bodyweight.\n\n[Maintaining costs far less than building.]",
      titulo=("[1.] Entreno mínimo", "[1.] Minimum training"), **foto("gym-triceps-amarillo", (0.45, 0.45), 340)),
    P("punto", "En cada comida, primero la proteína y la verdura. Después, lo demás.\n\nEn el buffet: [primer plato de proteína], siempre.",
      "At every meal, protein and vegetables first. Then everything else.\n\nAt the buffet: [first plate is protein], always.",
      titulo=("[2.] Proteína primero", "[2.] Protein first")),
    P("punto", "Explora andando. Sin darte cuenta haces 10–15k pasos al día.\n\nLa mejor forma de conocer una ciudad [y de no ganar grasa].",
      "Explore on foot. You'll hit 10–15k steps a day without noticing.\n\nThe best way to see a city [and not gain fat].",
      titulo=("[3.] Camina la ciudad", "[3.] Walk the city"), **foto("dubai-playa-rosa", (0.55, 0.5), 340)),
    P("punto", "Luz solar por la mañana en destino, comidas en horario local y nada de siestas largas el primer día.\n\n[Tu reloj interno se ajusta antes.]",
      "Morning sunlight at your destination, meals on local time and no long naps on day one.\n\n[Your body clock adjusts faster.]",
      titulo=("[4.] Gana al jet lag", "[4.] Beat jet lag"), **foto("dubai-piscina-infinita", (0.5, 0.55), 340)),
    P("punto", "2–3 comidas libres por semana, sin culpa.\n\n[Un viaje no te arruina. Un año sin sistema, sí.]",
      "2–3 free meals a week, guilt-free.\n\n[One trip won't ruin you. A year without a system will.]",
      titulo=("[5.] Disfruta", "[5.] Enjoy it")),
    cta(("Vive. Viaja. [Sin perder lo construido.]", "Live. Travel. [Keep what you built.]")),
])

C["Y-musculo-longevidad"] = ("Mándaselo a alguien que dice que ya es tarde para empezar. Sígueme.", "Send this to someone who thinks it's too late to start. Follow.", [
    P("portada", "El músculo es [tu plan de pensiones]", "Muscle is [your retirement plan]",
      **foto("gym-disco", (0.45, 0.4))),
    P("punto", "Si no lo entrenas, a partir de los 30–40 empiezas a perder músculo poco a poco.\n\nA los 70, esa diferencia es [independencia o dependencia].",
      "If you don't train it, from your 30s–40s you slowly start losing muscle.\n\nAt 70, that difference means [independence or dependence].",
      titulo=("Lo que pasa si [no haces nada]", "What happens if you [do nothing]")),
    P("punto", "El músculo [consume glucosa], protege articulaciones y huesos, y se asocia con vivir más años y con mejor calidad de vida.",
      "Muscle [burns glucose], protects your joints and bones, and is linked to living longer and better.",
      titulo=("Es mucho más que [estética]", "It's much more than [looks]"), **foto("gym-muscleworks", (0.55, 0.45), 340)),
    P("punto", "En los estudios, una de las medidas más asociadas con la mortalidad es la [fuerza de agarre].\n\nPrueba: cuélgate de una barra. ¿Cuánto aguantas?",
      "In research, one of the measures most linked to mortality is [grip strength].\n\nTest it: hang from a bar. How long can you last?",
      titulo=("El test de [la barra]", "The [hang test]")),
    P("punto", "2–3 días de fuerza a la semana, ejercicios básicos y subir el peso poco a poco.\n\n[No hace falta más para empezar.]",
      "2–3 strength days a week, basic lifts and adding weight little by little.\n\n[That's all you need to start.]",
      titulo=("Lo [mínimo] que funciona", "The [minimum] that works"), **foto("gym-remo-cable", (0.6, 0.55), 340)),
    P("punto", "El mejor momento para empezar fue hace 10 años.\n\nEl segundo mejor es [hoy].",
      "The best time to start was 10 years ago.\n\nThe second best is [today].",
      titulo=("La verdad", "The truth")),
    cta(("Entrena hoy para [tu yo de 70 años].", "Train today for [your 70-year-old self].")),
])

if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent.parent.parent / "carruseles" / "calentamiento"
    for clave, (pie_es, pie_en, slides) in C.items():
        cfg = {"nombre": f"calentamiento-{clave}", "estilo": "oscuro", "idiomas": ["es", "en"], "perfil": PERFIL,
               "pie_de_post": {"es": pie_es, "en": pie_en}, "slides": slides}
        (raiz / f"{clave}.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        print(clave)
