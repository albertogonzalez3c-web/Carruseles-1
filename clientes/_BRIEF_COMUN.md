# Brief común para construir el sistema de un cliente de mentoría (Alberto González)

Cada cliente tiene una carpeta `clientes/<cliente>/` con:
- `historia.md` (resumen de su historia: datos, historia, casos, cliente ideal, frases literales, mensaje, sensibles a no publicar, contradicciones)
- `index.html` (landing; a veces "boceto") + `casos/*.jpg` (recortes de capturas)
- `partes/1-perfil.html`, `2-oferta.html`, `3-contenido.html`, `4-embudo.html`, `6-guion-cierre.html`, `crm.html` (db), `7-reportes.html` (db)

## Plantillas a copiar (estructura, estilos, JS, db)
- Cliente España con anuncios y landing: `clientes/holyfield/` (todas las páginas).
- Cliente EE. UU./USD, multicanal, francotirador, sin landing: `clientes/sebastian-palacios/partes/`.
- Cliente EE. UU. latino, sin anuncios: `clientes/jony-garcia/partes/`.
Lee al menos el perfil, contenido, CRM y reporte de la plantilla más cercana antes de escribir. Adapta TODO el texto al cliente nuevo; no dejes restos del cliente plantilla (nombres, cifras, palabra clave).

## Contrato de página (obligatorio)
- Sin `<!doctype>`, `<html>`, `<head>` ni `<body>`: el archivo empieza por `<title>Nombre Parte</title>` (2–4 palabras), luego `<meta name="claude:viewport-fit-sides" content="cover">`, `<style>` y el contenido.
- `[hidden]{display:none!important}`. Colores como tokens en `:root` con modo oscuro si la plantilla lo tiene.
- Móvil 390 px sin scroll horizontal; también 1280 px.
- CRM y reporte: patrón db de la plantilla (`window.claude.use("db")`, onSnapshot, `set()` con debounce, temporizador de 10 s, mensajes de error invalid_argument/quota_exceeded/revoked, `config/precios {nivel, ventasDesdeSubida}` con escalera +20 % por venta). Moneda con céntimos correctos (0,60 € no 1,60 €).
- Español de España salvo clientes latinos de EE. UU. (español neutro, USD).

## Reglas de contenido de Alberto (para todos)
- Nicho: una única frase exacta, idéntica en todas las páginas; método con nombre propio, 3 pilares, 3 fases, 3 no negociables, cada pilar ligado a su historia real. Ángulos afilados y específicos del cliente (nada genérico), calidad sobre cantidad (50–70).
- Carruseles mínimo 3/semana alternando CONEXIÓN y VALOR (bloque con 10–12 ideas de cada tipo con estructura de slides; filtros "Carrusel conexión"/"Carrusel valor" en el banco).
- Mucho rol entrenador y casos; stories por bloques; Estados de WhatsApp; voz en off con trial reels (3 variantes de gancho).
- Pestaña "Claude Code editor" (copia la de la plantilla y adáptala): instalar Claude Code (Mac/Linux `curl -fsSL https://claude.ai/install.sh | bash`, Windows `irm https://claude.ai/install.ps1 | iex`, o app de escritorio pestaña Code), ffmpeg, carpeta `Contenido-<Nombre>` con 1-sin-editar/2-editados/3-recursos/4-referencias, skills de Alberto en `~/.claude/skills/` (comprobar con /skills), CLAUDE.md copiable adaptado, rutina para educar a Claude, 8 órdenes copiables. Regla: no inventar cifras ni testimonios.
- Embudo: 100 conversaciones/día en 2 rondas de 50, WhatsApp, CRM, llamada, proceso de cierre paso a paso con mensajes copiables, seguimiento días 2/7/14.
- Anuncios (salvo que el cliente no ponga): promocionar Reels con objetivo visitas al perfil, 5–10 €/día, valorar a los 2 días: <1 €/seguidor mantener y escalar; 1–1,5 € cambiar gancho; >1,5 € cortar. Público España +25 (EE. UU.: hispanohablantes EE. UU., USD). Piezas voz en off "sígueme" tocando un ángulo, 3 guiones completos. Normas Meta: nunca "¿tienes…?" ni atribuir rasgos personales/salud al espectador; primera persona o "la mayoría".
- Guion de cierre basado en el "Guion de Cierre Escuela Aglez" mejorado (copia la estructura de la plantilla), con su historia, casos y objeciones del nicho.
- Precios siempre marcados "propuesta, confirmar".
- Nada sensible en público (salud, familia, terceros); huecos [confirmar] cuando falte un dato; nunca inventar casos.

## Pruebas
Playwright con Chromium en `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` (python: `p.chromium.launch(executable_path=...)`). Páginas con db: inyecta el mock de `/tmp/claude-0/-home-user-Carruseles-1/84eb04a3-ddae-53cb-914f-f909d54e0bc5/scratchpad/adrian/mock.js` con `add_init_script`. Comprueba a 390 y 1280: sin errores de JS, sin scroll horizontal, filtros y botones de copiar funcionan, CRM/reporte guardan y recargan.

No publiques ni hagas commit: devuelve la lista de archivos e imágenes referenciadas y lo que hay que confirmar con el cliente.
