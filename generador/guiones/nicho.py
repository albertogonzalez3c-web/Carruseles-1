"""Guiones de los carruseles de nicho (estilo oscuro). Genera carruseles/calentamiento/M..T.json."""
import json
from pathlib import Path

PERFIL = {"nombre": "Alberto González", "usuario": {"es": "@albertoglez6", "en": "@albertoglezcoach"},
          "foto": "fotos/perfil.png", "caja": [0, 0, 1, 1], "verificado": True}
CTA = ("Cada semana publico cómo optimizar tus hormonas pasados los 30, [sin vivir en el gimnasio].\n\n**Sígueme** para no perderte el siguiente.",
       "Every week I share how to optimize your hormones after 30, [without living in the gym].\n\n**Follow me** so you don't miss the next one.")


def P(tipo, es=None, en=None, **kw):
    d = {"tipo": tipo}
    for k, v in kw.items():
        d[k] = {"es": v[0], "en": v[1]} if isinstance(v, tuple) else v
    if es is not None:
        d["texto"] = {"es": es, "en": en}
    return d


def foto(nombre, foco=(0.5, 0.45), alto=None):
    d = {"foto": f"fotos/{nombre}.jpg", "foco": list(foco)}
    if alto:
        d["alto_foto"] = alto
    return d


def cta(etiqueta):
    return P("cta", *CTA, etiqueta=etiqueta)


C = {}

C["M-estres-senales"] = ("¿Te reconoces en 3? Guárdalo y sígueme para más.", "Recognize 3 of these? Save it and follow for more.", [
    P("portada", "señales de que el [estrés crónico] te está robando la energía", "signs [chronic stress] is draining your energy",
      numero="5", **foto("laptop-negro", (0.5, 0.35))),
    P("punto", "Te acuestas reventado y te despiertas a las 3–4 de la mañana con la cabeza a mil.\n\nEl estrés sostenido [altera tu ritmo de cortisol] y rompe el sueño profundo.",
      "You go to bed exhausted and wake up at 3–4am with your mind racing.\n\nOngoing stress [disrupts your cortisol rhythm] and breaks deep sleep.",
      titulo=("[1.] Cansado pero sin dormir", "[1.] Tired but can't sleep")),
    P("punto", "Entrenas y comes bien, pero la cintura no baja.\n\nEl cortisol alto de forma crónica [se asocia con más grasa abdominal].",
      "You train and eat well, but your waist won't shrink.\n\nChronically high cortisol [is linked to more belly fat].",
      titulo=("[2.] Barriga que no se va", "[2.] Belly fat that won't budge"), **foto("hawaii-playa", (0.55, 0.55), 340)),
    P("punto", "A las 22h te comerías la nevera.\n\nNo es falta de voluntad: el estrés y el mal sueño [disparan el hambre] de lo rápido y dulce.",
      "At 10pm you'd eat the whole fridge.\n\nIt's not willpower: stress and poor sleep [drive cravings] for fast, sweet food.",
      titulo=("[3.] Antojos por la noche", "[3.] Late-night cravings")),
    P("punto", "Menos ganas, menos chispa.\n\nCuando el cuerpo vive en modo supervivencia, [la reproducción pasa a segundo plano]. Tu testosterona lo nota.",
      "Less drive, less spark.\n\nWhen your body lives in survival mode, [reproduction takes a back seat]. Your testosterone feels it.",
      titulo=("[4.] Libido por los suelos", "[4.] Low libido")),
    P("punto", "Agujetas que duran días y estancado en los pesos.\n\nNo necesitas entrenar más. [Necesitas recuperarte mejor.]",
      "Soreness that lasts for days and stuck on your lifts.\n\nYou don't need to train more. [You need to recover better.]",
      titulo=("[5.] No te recuperas", "[5.] You don't recover"), **foto("gym-remo", (0.5, 0.35), 340)),
    cta(("El estrés no se elimina. [Se gestiona.]", "You can't eliminate stress. [You manage it.]")),
])

C["N-estres-habitos"] = ("Guárdalo y empieza mañana. Sígueme para más.", "Save it and start tomorrow. Follow for more.", [
    P("portada", "Cómo bajo el [estrés crónico] con 20 minutos al día (aunque trabaje 10 horas)",
      "How I lower [chronic stress] in 20 minutes a day (even working 10 hours)", **foto("miami-parque", (0.5, 0.5))),
    P("punto", "10 minutos de luz natural al despertar.\n\nAyuda a [poner en hora tu reloj interno]: más energía por la mañana y mejor sueño por la noche.",
      "10 minutes of daylight after waking up.\n\nIt helps [set your internal clock]: more energy in the morning, better sleep at night.",
      titulo=("[1.] Sol antes que móvil", "[1.] Sunlight before your phone"), **foto("hawaii-playa", (0.55, 0.5), 340)),
    P("punto", "10 minutos andando después de comer y cenar.\n\nBaja el pico de glucosa y [desconecta la cabeza]. Llamadas incluidas.",
      "A 10-minute walk after lunch and dinner.\n\nIt blunts the glucose spike and [clears your head]. Take your calls on the go.",
      titulo=("[2.] Caminar tras comer", "[2.] Walk after meals")),
    P("punto", "5 minutos: inhala 4 segundos, exhala 6.\n\nLa exhalación larga [activa tu sistema de calma]. Entre reunión y reunión.",
      "5 minutes: breathe in for 4 seconds, out for 6.\n\nLong exhales [switch on your calm system]. Between meetings.",
      titulo=("[3.] Respiración 4–6", "[3.] 4–6 breathing")),
    P("punto", "45 minutos de fuerza, no 2 horas de castigo.\n\nEl entreno es estrés bueno [si te recuperas de él]. Más no siempre es mejor.",
      "45 minutes of strength, not 2 hours of punishment.\n\nTraining is good stress [if you recover from it]. More isn't always better.",
      titulo=("[4.] Entreno corto e intenso", "[4.] Short, intense training"), **foto("gym-curl", (0.5, 0.35), 340)),
    P("punto", "Pantallas fuera 1 hora antes de dormir y a la cama a la misma hora.\n\nDormir es [la herramienta antiestrés más barata] que existe.",
      "Screens off 1 hour before bed and the same bedtime every night.\n\nSleep is [the cheapest anti-stress tool] there is.",
      titulo=("[5.] Apagar para recargar", "[5.] Switch off to recharge")),
    cta(("20 minutos. [Sin excusas.]", "20 minutes. [No excuses.]")),
])

C["O-grasa-visceral"] = ("Mídete hoy y dime tu número en comentarios. Sígueme para más.", "Measure yourself today and tell me your number. Follow for more.", [
    P("portada", "La grasa que no ves es [la que más te debería preocupar]", "The fat you can't see is [the one you should worry about most]",
      **foto("miami-playa", (0.5, 0.45))),
    P("punto", "Es la grasa que se acumula [dentro del abdomen], alrededor de tus órganos.\n\nNo es la que pellizcas. Es la que empuja la barriga hacia fuera, dura como un balón.",
      "It's the fat stored [inside your abdomen], around your organs.\n\nNot the fat you can pinch. It's what pushes your belly out, hard like a ball.",
      titulo=("¿Qué es la [grasa visceral]?", "What is [visceral fat]?")),
    P("punto", "Se asocia con [resistencia a la insulina], inflamación y más riesgo cardiovascular.\n\nY con [menos testosterona]: un círculo vicioso.",
      "It's linked to [insulin resistance], inflammation and higher cardiovascular risk.\n\nAnd to [lower testosterone]: a vicious circle.",
      titulo=("Por qué importa", "Why it matters")),
    P("punto", "Cinta métrica a la altura del ombligo.\n\nSi tu cintura mide [más de la mitad de tu altura], es una señal de alerta.\n\nEjemplo: mides 1,80 m → cintura por debajo de 90 cm.",
      "Tape measure at belly-button height.\n\nIf your waist is [more than half your height], that's a warning sign.\n\nExample: 6 ft tall → waist under 36 in.",
      titulo=("Mídela en casa en [10 segundos]", "Measure it at home in [10 seconds]")),
    P("punto", "Fuerza 3 días, 8–10k pasos, 7–8 h de sueño, menos alcohol y un déficit moderado.\n\nLa visceral suele ser [de la primera en irse] cuando haces las cosas bien.",
      "Strength 3 days, 8–10k steps, 7–8 hours of sleep, less alcohol and a moderate deficit.\n\nVisceral fat is often [among the first to go] when you do things right.",
      titulo=("Qué la baja", "What brings it down"), **foto("lobby-movil", (0.5, 0.4), 340)),
    P("punto", "Los abdominales no queman la grasa de la barriga.\n\n[No se puede quemar grasa localizada.] Se baja con el conjunto, no con 100 crunches.",
      "Crunches don't burn belly fat.\n\n[You can't spot-reduce fat.] It comes off with the whole system, not 100 crunches.",
      titulo=("Qué [no] la baja", "What [doesn't] work")),
    cta(("Tu cintura dice más que [tu báscula].", "Your waist says more than [your scale].")),
])

C["P-visceral-habitos"] = ("¿Cuál es el tuyo? Dímelo en comentarios y sígueme.", "Which one is yours? Tell me in the comments and follow.", [
    P("portada", "hábitos que alimentan tu [grasa visceral] sin que te des cuenta", "habits feeding your [visceral fat] without you noticing",
      numero="4", **foto("espejo-naranja", (0.5, 0.4))),
    P("punto", "Cervezas, copas, vino “para relajarte”.\n\nEl alcohol frecuente [favorece la grasa abdominal] y empeora tu sueño. Doble golpe.",
      "Beers, drinks, wine “to unwind”.\n\nRegular drinking [promotes belly fat] and wrecks your sleep. A double hit.",
      titulo=("[1.] El alcohol de cada finde", "[1.] Every-weekend drinking")),
    P("punto", "Refrescos, zumos, cafés con sirope.\n\nCalorías que [no te quitan el hambre] y van directas a la cintura.",
      "Soda, juice, syrupy coffees.\n\nCalories that [don't fill you up] and go straight to your waist.",
      titulo=("[2.] El azúcar que bebes", "[2.] The sugar you drink")),
    P("punto", "Con 5–6 horas comes más, te mueves menos y [tu metabolismo de la glucosa empeora].\n\nEl sueño también es dieta.",
      "On 5–6 hours you eat more, move less and [your glucose metabolism gets worse].\n\nSleep is part of your diet.",
      titulo=("[3.] Dormir poco", "[3.] Not sleeping enough"), **foto("sofa-cenital", (0.55, 0.45), 340)),
    P("punto", "Coche, oficina, sofá.\n\nUna hora de gimnasio [no compensa] 10 horas sentado. Levántate cada hora, aunque sean 3 minutos.",
      "Car, office, couch.\n\nOne hour at the gym [doesn't cancel out] 10 hours of sitting. Get up every hour, even for 3 minutes.",
      titulo=("[4.] Estar sentado 10 horas", "[4.] Sitting 10 hours a day")),
    P("punto", "No necesitas cambiarlo todo mañana.\n\nElige [uno] de los cuatro y arréglalo esta semana. La semana que viene, el siguiente.",
      "You don't need to change everything tomorrow.\n\nPick [one] of the four and fix it this week. Next week, the next one.",
      titulo=("Por dónde empezar", "Where to start"), **foto("miami-parque", (0.5, 0.5), 340)),
    cta(("Pequeños hábitos, [grandes cambios].", "Small habits, [big changes].")),
])

C["Q-sin-tiempo"] = ("Mándaselo a ese amigo que siempre dice que no tiene tiempo.", "Send this to that friend who always says he has no time.", [
    P("portada", "“[No tengo tiempo]”: la excusa que te está costando tu salud",
      "“[I don't have time]”: the excuse that's costing you your health", **foto("laptop-negro", (0.5, 0.35))),
    P("punto", "Una semana tiene 168 horas.\n\n3 entrenos de 45 minutos son [2,25 horas]. El 1,3 % de tu semana.\n\nNo es falta de tiempo. [Es falta de prioridad.]",
      "A week has 168 hours.\n\n3 workouts of 45 minutes is [2.25 hours]. 1.3% of your week.\n\nIt's not a lack of time. [It's a lack of priority.]",
      titulo=("Haz las cuentas", "Do the math")),
    P("punto", "Lunes, miércoles y viernes. 45 minutos. Básicos pesados.\n\nSi está en el calendario, [se hace]. Si no, no existe.",
      "Monday, Wednesday, Friday. 45 minutes. Heavy basics.\n\nIf it's on the calendar, [it happens]. If not, it doesn't exist.",
      titulo=("Agenda el entreno como una [reunión]", "Book training like a [meeting]"), **foto("gym-amarillo", (0.45, 0.3), 340)),
    P("punto", "Llamadas andando. Escaleras. Aparcar lejos.\n\nNo necesitas una hora extra: [necesitas moverte en la que ya tienes].",
      "Walking calls. Stairs. Park farther away.\n\nYou don't need an extra hour: [you need to move in the hours you already have].",
      titulo=("Los pasos se esconden en tu día", "Steps hide in your day")),
    P("punto", "Cocina proteína para 3 días de una vez. Repite desayunos.\n\nDecidir menos = [cumplir más].",
      "Cook protein for 3 days at once. Repeat breakfasts.\n\nFewer decisions = [more consistency].",
      titulo=("Comida en piloto automático", "Food on autopilot"), **foto("sushi", (0.5, 0.5), 340)),
    P("punto", "Los que más trabajan [son los que más necesitan] energía, foco y cabeza fría.\n\nCuidarte no te quita tiempo. [Te lo multiplica.]",
      "The people who work the most [need energy, focus and a clear head the most].\n\nTaking care of yourself doesn't cost time. [It multiplies it.]",
      titulo=("La verdad incómoda", "The uncomfortable truth")),
    cta(("Sin tiempo no. [Sin sistema.]", "Not no time. [No system.]")),
])

C["R-familia-trabajo"] = ("¿Cuál te has dicho alguna vez? Sé sincero en comentarios.", "Which one have you told yourself? Be honest in the comments.", [
    P("portada", "excusas que te dices por tu [familia y tu trabajo] (y cómo las desmonto)",
      "excuses you make because of your [family and work] (and how I break them down)", numero="5", **foto("escalera-dorada", (0.5, 0.35))),
    P("punto", "Te ven. Y aprenden más de lo que haces que de lo que dices.\n\nCuidarte es [el mejor ejemplo] que les puedes dar.",
      "They're watching. And they learn more from what you do than from what you say.\n\nTaking care of yourself is [the best example] you can give them.",
      titulo=("“Tengo [hijos].”", "“I have [kids].”")),
    P("punto", "30 minutos en el gimnasio del hotel o con tu peso corporal en la habitación.\n\n[Algo] siempre gana a [nada].",
      "30 minutes in the hotel gym or bodyweight in your room.\n\n[Something] always beats [nothing].",
      titulo=("“[Viajo] mucho.”", "“I [travel] a lot.”"), **foto("jeep-hawaii", (0.55, 0.45), 340)),
    P("punto", "Regla simple: proteína + verdura, el pan fuera y una copa como máximo.\n\nPuedes comer fuera [y seguir avanzando].",
      "Simple rule: protein + vegetables, skip the bread, one drink max.\n\nYou can eat out [and still make progress].",
      titulo=("“Como fuera por [trabajo].”", "“I eat out for [work].”")),
    P("punto", "Es al revés: entrenar fuerza y moverte [te da energía], no te la quita.\n\nEl cansancio de no hacer nada es el peor.",
      "It's the opposite: strength training and moving [give you energy], they don't drain it.\n\nThe tiredness of doing nothing is the worst kind.",
      titulo=("“Llego [reventado].”", "“I get home [exhausted].”")),
    P("punto", "Has probado dietas. No un sistema adaptado a tu agenda, tu familia y [tus hormonas].\n\nNo has fallado tú. [Ha fallado el plan.]",
      "You've tried diets. Not a system built around your schedule, your family and [your hormones].\n\nYou didn't fail. [The plan did.]",
      titulo=("“Ya lo he [probado todo].”", "“I've [tried everything].”"), **foto("formacion-sentado", (0.6, 0.6), 340)),
    cta(("Tu familia te necesita [con energía].", "Your family needs you [with energy].")),
])

C["S-insulina"] = ("Guárdalo para tu próxima analítica. Sígueme para más.", "Save it for your next blood test. Follow for more.", [
    P("portada", "[Sensibilidad a la insulina]: lo que nadie te explica pasados los 30",
      "[Insulin sensitivity]: what nobody explains to you after 30", **foto("gym-curl", (0.5, 0.35))),
    P("punto", "La insulina mete la glucosa en tus células.\n\nSi tus células [dejan de hacerle caso], el cuerpo fabrica más y más insulina. Eso es la resistencia a la insulina.",
      "Insulin moves glucose into your cells.\n\nWhen your cells [stop responding], your body pumps out more and more insulin. That's insulin resistance.",
      titulo=("¿Qué es?", "What is it?")),
    P("punto", "Barriga que crece, sueño después de comer, hambre cada 2 horas y bajones de energía por la tarde.\n\nNo es la edad. [Puede ser tu metabolismo.]",
      "Growing belly, sleepy after meals, hungry every 2 hours and afternoon crashes.\n\nIt's not your age. [It may be your metabolism.]",
      titulo=("Señales de alerta", "Warning signs")),
    P("punto", "Se diagnostica con 3 de estos 5: [cintura grande], glucosa alta, triglicéridos altos, tensión alta y HDL bajo.\n\nMuchos hombres de +30 lo tienen [y no lo saben].",
      "It's diagnosed with 3 of these 5: [large waist], high glucose, high triglycerides, high blood pressure and low HDL.\n\nMany men over 30 have it [and don't know].",
      titulo=("[Síndrome metabólico]", "[Metabolic syndrome]")),
    P("punto", "El músculo es tu mayor almacén de glucosa.\n\n[Más músculo y más movimiento] = mejor sensibilidad a la insulina. Fuerza + caminar tras comer + dormir bien.",
      "Muscle is your biggest glucose storage.\n\n[More muscle and more movement] = better insulin sensitivity. Strength + walking after meals + good sleep.",
      titulo=("Qué la mejora", "What improves it"), **foto("pasillo-sin", (0.5, 0.4), 340)),
    P("punto", "Pídele a tu médico: glucosa en ayunas, HbA1c, insulina en ayunas, triglicéridos y HDL.\n\nY mídete la cintura. [Lo que no se mide, no se mejora.]",
      "Ask your doctor for: fasting glucose, HbA1c, fasting insulin, triglycerides and HDL.\n\nAnd measure your waist. [What isn't measured isn't improved.]",
      titulo=("Qué mirar en tu [analítica]", "What to check in your [bloodwork]")),
    cta(("Tu músculo es [tu mejor medicina].", "Your muscle is [your best medicine].")),
])

C["T-mitos-sedentarismo"] = ("¿Cuál te creías? Dímelo en comentarios y sígueme.", "Which one did you believe? Tell me in the comments and follow.", [
    P("portada", "mitos que te mantienen [sedentario] (y con barriga)", "myths keeping you [sedentary] (and with a belly)",
      numero="5", **foto("paracaidas", (0.6, 0.45))),
    P("punto", "Ayuda mucho, pero estar sentado 10 horas [sigue pasando factura].\n\nMuévete durante el día: pasos, escaleras, pausas activas.",
      "It helps a lot, but sitting 10 hours [still takes its toll].\n\nMove through the day: steps, stairs, active breaks.",
      titulo=("[MITO 1:] “Si entreno 1 hora, ya compenso.”", "[MYTH 1:] “One hour of training makes up for it.”")),
    P("punto", "Engorda el exceso de calorías y la falta de actividad.\n\nLos carbohidratos de calidad [alimentan tu entreno].",
      "A calorie surplus and inactivity make you gain fat.\n\nQuality carbs [fuel your training].",
      titulo=("[MITO 2:] “Los carbohidratos engordan.”", "[MYTH 2:] “Carbs make you fat.”")),
    P("punto", "Cuenta [el total del día], no la hora.\n\nEso sí: una cena copiosa justo antes de dormir [empeora tu sueño].",
      "What counts is [your daily total], not the clock.\n\nBut a huge dinner right before bed [hurts your sleep].",
      titulo=("[MITO 3:] “Comer de noche engorda.”", "[MYTH 3:] “Eating at night makes you fat.”"), **foto("sushi", (0.5, 0.5), 340)),
    P("punto", "El sudor es agua, no grasa.\n\nLo que cambia tu cuerpo es [la constancia], no lo empapado que salgas.",
      "Sweat is water, not fat.\n\nWhat changes your body is [consistency], not how soaked you get.",
      titulo=("[MITO 4:] “Si sudo, quemo más grasa.”", "[MYTH 4:] “More sweat, more fat burned.”")),
    P("punto", "Se gana músculo a cualquier edad con entrenamiento de fuerza y proteína suficiente.\n\nY pasados los 40 [es cuando más lo necesitas].",
      "You can build muscle at any age with strength training and enough protein.\n\nAnd after 40 is [when you need it most].",
      titulo=("[MITO 5:] “A los 40 ya no se gana músculo.”", "[MYTH 5:] “You can't build muscle at 40.”"), **foto("gym-amarillo", (0.45, 0.3), 340)),
    cta(("Muévete más. [Vive más.]", "Move more. [Live more.]")),
])

if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent.parent.parent / "carruseles" / "calentamiento"
    for clave, (pie_es, pie_en, slides) in C.items():
        cfg = {"nombre": f"calentamiento-{clave}", "estilo": "oscuro", "idiomas": ["es", "en"], "perfil": PERFIL,
               "pie_de_post": {"es": pie_es, "en": pie_en}, "slides": slides}
        (raiz / f"{clave}.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        print(clave)
