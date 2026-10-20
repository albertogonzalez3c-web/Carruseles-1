# Sistema de Carruseles

Tres tipos de carrusel, cada uno con un trabajo distinto dentro del embudo.
Si un carrusel intenta hacer los tres trabajos a la vez, no hace ninguno.

| Tipo | Trabajo | Temperatura de la audiencia | Métrica que importa | CTA |
|---|---|---|---|---|
| [Conexión](carruseles/01-conexion.md) | Que te conozcan y confíen en ti como persona | Fría / tibia | Guardados, compartidos, DMs espontáneos, follows | Blando (comenta, comparte, sígueme) |
| [Calentamiento](carruseles/02-calentamiento.md) | Que entiendan el problema, tu método y que tú sabes resolverlo | Tibia | Guardados, respuestas a la keyword, tiempo en el carrusel | Medio (comenta PALABRA → lead magnet / DM) |
| [Venta / Servicio](carruseles/03-venta.md) | Que levanten la mano para comprar | Caliente | DMs con intención, llamadas agendadas, ventas | Duro (escríbeme X / agenda / plazas limitadas) |

## Reglas comunes a los tres

1. **Slide 1 = 80% del resultado.** Si la portada no para el scroll, el resto no existe.
2. **Una idea por carrusel.** Una por slide. Si sobra texto, sobra slide.
3. **7–10 slides** en calentamiento y venta. En conexión (estilo subtítulo) se puede ir a 10–18, porque cada slide es una frase.
4. **Slide 2 justifica el swipe.** Promete lo que viene o abre un bucle.
5. **Último slide = una sola acción.** Nunca "comenta, guarda, comparte y sígueme" juntos.
6. **Lenguaje del cliente, no del experto.** Escribe con las palabras que usa tu cliente en los DMs y llamadas.
7. **Prueba > opinión.** Números, capturas, casos, antes/después siempre que existan.

## Mezcla semanal recomendada

Ver [plan-semanal.md](carruseles/plan-semanal.md).

## Cómo usarlo

1. Rellena [brief.md](carruseles/brief.md) una vez (nicho, avatar, oferta, pruebas). Sin esto, todo lo demás es genérico.
2. Elige tipo según el día del plan.
3. Copia la plantilla del tipo y rellena slide por slide.
4. Pasa el checklist del final de cada plantilla antes de publicar.

## Generador de slides con tus fotos

```bash
pip install pillow
python3 generador/carrusel.py ejemplos/conexion.json      # o ejemplos/*.json
```

1. Mete tus fotos en `fotos/` (ver `fotos/README.md`).
2. Copia un JSON de `ejemplos/`, cambia textos y rutas de foto.
3. Las slides salen en `salida/<nombre>/01.png, 02.png...` a 1080x1350, listas para subir.

| Tipo | Estilo | Ejemplo |
|---|---|---|
| Conexión | `subtitulo` | `ejemplos/conexion.json` |
| Calentamiento | `titular` | `ejemplos/calentamiento.json` |
| Venta | `tarjeta` | `ejemplos/venta.json` |
