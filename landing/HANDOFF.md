# Landing de la mentoría: traspaso

Todo lo necesario para seguir con la landing en otra sesión.

## Qué es

Landing de la **mentoría 1:1 de AGLEZ Academy** (Alberto González). Público: entrenadores y coaches que quieren vivir de sus asesorías online.

- Archivo: `landing/index.html`. Es una sola página, sin build: HTML y CSS en línea, con un poco de JS al final.
- Recursos: `landing/mentoria.mp4` y `landing/poster.jpg` (vídeo explicativo de 3:20) y `landing/casos/` (prueba social).
- Publicada como artifact privado: https://claude.ai/artifact/Ne3PYaSyaPDJfeVcEw1rws
- Botón principal: Calendly `https://calendly.com/albertoglezfitness/1-1`.
- Instagram: @albertomentor (mentoría), @albertoglez6 (español), @albertoglezcoach (inglés).

### Formato del archivo

No lleva `<!doctype>`, `<html>`, `<head>` ni `<body>` porque el artifact añade ese esqueleto al publicar. Para alojarla fuera (Vercel, Netlify, GitHub Pages), envuélvela con `<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>` … `</body></html>`.

## Posicionamiento (decidido con Alberto)

- **Empresa, no hobby.** Es para quien quiere un negocio sólido: métricas, procesos, oferta clara. No es para quien quiere "un extra".
- **El 1:1 es lo central.** "No vendo cursos. Es un servicio 1:1 conmigo con una academia como apoyo." Lo central es un plan de acción semanal, WhatsApp diario directo con él y una revisión cada domingo con métricas.
- **Academia en paralelo** (formación teórico-práctica) y comunidad como extra.
- **Frente a otras mentorías:** las grupales dan la misma clase a cientos de alumnos. Esta es individual y con un grupo reducido.
- **Solo bloques de 3 meses, a propósito:**
  1. Para comprobar que congenian.
  2. Porque el proyecto es igual de importante para las dos partes.
  3. Porque quiere máxima cercanía.

  Si funciona, siguen a largo plazo, pero nunca más de 3 meses de entrada.
- **Recomienda ver varias horas de su YouTube antes de contratar**, para entender su visión.
- **Garantía, bajo contrato:** si en 3 meses no recuperas la inversión, siguen trabajando juntos; si el servicio no tiene la calidad prometida, devolución.
- **Estilo:** fondo claro y sobrio, con el amarillo AGLEZ `#ffd21f` solo como acento. Tipografías Archivo (texto y titulares condensados) y JetBrains Mono (etiquetas). Nada de relleno que suene a IA.

## Orden de secciones (lo pidió Alberto)

1. Hero, con 4 resultados que se pueden tocar y bajan a `#casos`.
2. `#video`: cómo funciona por dentro, con capítulos.
3. `#tres-meses`: por qué va de 3 en 3.
4. `#diferencia`: 1:1 frente a mentoría grupal, más la captura "esto sí que es un plan".
5. `#casos`: caso destacado de Sergio, foto de grupo, 3 vídeos, muro de casos y botón "Ver todos los resultados".
6. `#garantia`
7. `#como`, `#enfoque` (hobby frente a empresa), `#historia`, `#youtube`, `#para-quien`, `#pasos`, `#faq`, cierre.

Entre secciones hay barras `.jump` con el enlace "Ver todos los resultados ↓" a `#casos`. Alberto quiere uno cada 2 o 3 secciones.

## Cómo añadir un caso

Los casos van dentro de `<div class="wall">` en `#casos`. Se ven los 6 primeros. El resto lleva `hidden class="shot extra"`, y el botón `#showAll` los cuenta y los despliega solo.

Caso con imagen:

```html
<figure hidden class="shot extra">
  <img src="casos/NOMBRE.jpg" alt="Descripción literal de la captura" loading="lazy" width="W" height="H">
  <figcaption><b>Resultado con número</b>Contexto en una o dos frases.</figcaption>
</figure>
```

Caso de solo texto, para citas:

```html
<div hidden class="shot extra text">
  <div class="big">Titular con número</div>
  <blockquote>“Cita literal del alumno.”</blockquote>
  <div class="who"><span class="avatar" aria-hidden="true">X</span><div><b>Nombre</b><span>@usuario · detalle</span></div></div>
</div>
```

Vídeo de testimonio: añade un `<figure class="vid">` dentro de `.vids` (copia uno de los existentes).

**Orden:** primero los casos con número y plazo. Los anónimos o sin cifras, al final.

### Comprimir medios (ffmpeg)

```bash
# Vídeo vertical de testimonio, unos 2–3 MB
ffmpeg -i entrada.mov -c:v libx264 -preset slow -crf 29 -maxrate 700k -bufsize 1400k -vf "scale=480:-2" -c:a aac -b:a 64k -ac 1 -movflags +faststart casos/testimonio-N.mp4
ffmpeg -ss 2 -i entrada.mov -frames:v 1 -vf scale=480:-2 -q:v 4 casos/testimonio-N.jpg
```

Capturas: recorta solo el contenido, quitando la interfaz de Instagram. Máximo 900 px de ancho y JPG con calidad 80.

### Publicar el artifact

Publica `landing/index.html` en la URL de arriba. En `files` pasa cada recurso nuevo con su ruta (`casos/archivo.jpg`). El límite es 16 MB por página y 15 MB por archivo.

## Prueba social ya incluida (fuente: capturas y vídeos de Alberto)

| Caso | Dato | Archivo |
|---|---|---|
| Sergio | 11.300 € en un mes, empezando desde cero (lo dijo Alberto; **falta la captura**) | bloque `.star` |
| Alumno anónimo | De 2–3k €/mes a 7.000 € y luego 8.000 € en sus 2 primeros meses | `ingresos-7k-8k.jpg` |
| Alumno anónimo (Polonia) | 9.000 € en un mes; le compró un coche a su padre | cita de texto |
| Adrián Domínguez | Supera su récord de 3k en 24 h; cierre de 4.670 € | `adrian-4670.jpg` |
| Alumno anónimo | 4.500 € en octubre; deja los presenciales; "cumplí el contrato en un mes" | `chat-4500.jpg` |
| Car @fitconcar / Lukas @polacotrainer | De 211 a 159K y de 2.524 a 293K seguidores | `seguidores.jpg` |
| Alumno anónimo | 1.350 € en 24 h (seguimiento por WhatsApp) | `adrian-1350.jpg` (no está confirmado que sea Adrián; el pie no lo dice) |
| Alumno anónimo | Empezó con 1 cliente y llegó a 3k; dejó su trabajo | cita de texto |
| Alumno anónimo | Pagos de Stripe y venta a 24 meses | `stripe-24-meses.jpg` |
| Alumno anónimo | Recupera la inversión con un solo cliente | `chat-310.jpg` |
| Pablo Suero @pablosphysique | Testimonio de inicio, sin cifras | cita de texto |
| Venía de otra mentoría | "Nada que ver, esto sí que es un plan" | `esto-si-es-un-plan.jpg` (en `#diferencia`) |
| 3 vídeos | Testimonios sin nombre todavía | `testimonio-1..3.mp4` |
| Alberto | Fisioterapia en 2020 → +33.000 € en 23 días; su mujer y su mejor amigo viven de esto | `historia-*.jpg` |

## Pendiente

1. **Zip con unos 30 testimonios** (`Duro.zip`, 1,7 GB, en el Drive de Alberto). Hay que comprimirlos y añadirlos con la plantilla de arriba.
2. **Nombres y resultados de los 3 vídeos y de los casos anónimos.** No inventar nada: si falta un dato, preguntar.
3. **Sergio:** falta la captura, su @, el mes concreto y su permiso.
4. **Títulos de dos vídeos de YouTube** (`FhWKW4vhyFg`, `3nnf2uBxCYI`): ahora pone "Ver vídeo".
5. **Comprobar los enlaces de Instagram en "Más casos".** Se copiaron de capturas y pueden tener una "l" donde va una "I" o al revés.
6. **"Grupo reducido":** mejor poner la cifra real ("máximo X alumnos").
7. **Garantía:** definir "calidad" en el contrato con criterios medibles (revisión cada domingo, respuesta en menos de 24 h, plan entregado cada semana). Alinear el texto de Instagram, que dice "o lo logramos o te devolvemos la inversión", con el de la landing.
8. **"WhatsApp directo a diario"** es una promesa: confirmar que se puede mantener cuando crezca el número de alumnos.
9. **Revisar el renderizado en móvil y en escritorio** antes de compartir la página. No se ha hecho una revisión visual completa.

## Cómo trabajar con Alberto

Directo y sin adular. Hay que señalar los riesgos (promesas, cifras sin prueba, contradicciones) y estar de su lado. No se inventan cifras, nombres ni plazos.

---

# Landing de asesoría de salud (`landing-salud/`)

## Archivos y enlaces
- `landing-salud/index.html`: versión en español (@albertoglez6). Artifact: https://claude.ai/artifact/N7RS1e83EmYXnMNJ1vLXHq
- `landing-salud/en.html`: traducción literal al inglés (@albertoglezcoach). Artifact: https://claude.ai/artifact/MVfHeanGfCnykuABiz195e
- Los dos archivos tienen la misma estructura. **Cualquier cambio se hace en los dos.**

## Oferta y enfoque (decidido con Alberto)
- Asesoría 1:1 de salud con WhatsApp diario, revisión semanal y una visión global de la persona.
- **Lo primero, y lo que se remarca:** lo básico bien hecho. Una rutina de alimentación y entrenamiento hecha para el cliente, que desde la primera semana hace que todo mejore.
- **Después**, la visión global:
  - Fisioterapia y readaptación de lesiones. Alberto es fisioterapeuta y este es su gran diferencial.
  - Digestiones.
  - Hormonas.
  - Metabolismo y energía.
- **Historia de Alberto:**
  - En la adolescencia pesaba casi 100 kg sin haber pisado un gimnasio, con sobrepeso y sin capacidades físicas básicas.
  - De niño compraba ropa de tallas especiales.
  - Estudió Fisioterapia, empezó Medicina y lo dejó.
  - 12 años entrenando, casi 10 asesorando y +1.800 personas.
  - 11 competiciones al natural, con 1º y 2º puesto.
  - Pasó por ansiedad con la comida.
- **Garantía, bajo contrato:** devolución si el cliente hace su parte y no hay resultados, o si no se le atiende como se prometió.
- **Orden de la página:** hero → lo que me hace diferente → casos → historia → problema → oferta → comparativa → garantía → para quién → pasos → preguntas frecuentes → formulario → cierre.

## Contacto (ya puesto)
- **WhatsApp:** +34 722 731 303, con `data-wa="34722731303"` en `<div id="contact">`. Todos los botones `.js-contact` abren WhatsApp con un mensaje ya escrito.
- **Jotform:** https://form.jotform.com/260062853529055, con utm por idioma.
  - Los botones "Rellenar el formulario" lo abren directamente.
  - La sección `#formulario` / `#form` lo incrusta en un iframe solo si la página no está dentro de otro marco, es decir, cuando está alojada en su dominio. En el visor de Claude queda el botón.
  - **Pendiente:** versión del formulario en inglés.

## Casos actuales
Son 12 tarjetas de texto (en `.wall` dentro de `#casos` / `#cases`), sacadas de los captions de @albertoglez6. Cada una enlaza a su publicación. **No tienen ni foto ni vídeo.**

| Permalink | Caso |
|---|---|
| `reel/Dc1mvYLAsVD` | David, −20 kg en 10 meses, padre y muy ocupado |
| `reel/Dc1iHnNgZ7d` | Carlos, 7 años en la asesoría |
| `reel/Dc3fHTRNOyw` | Cliente con 5 años progresando (cambios de trabajo y ciudad) |
| `p/DMvKXMetoAY` | Sergio @sergio_camsfit, competidor; su físico no respondía con calorías bajas |
| `p/C_qzQ4qNY6d` | @sergiopg96, 12 semanas de preparación |
| `reel/Dc3cErNNJmd` | Enrique |
| `reel/Dc3a3vgNIrf` | "Aprendió a comer" |
| `reel/DasdAZstlSh` | Gonzalo |
| `reel/DavMZErtmnd` | David, los detalles |
| `reel/DbEDAdqtdHa` | Sergio |
| `reel/Dc31_JkACta` | Sergio Caro |
| `p/DcgW8WkDXOe` | Jordi |
| `p/DTF496JDcCH` | Transformaciones de clientes |
| Carruseles del 04-09-2025 | Caption "Comenta INFO para optar a tu plaza"; probablemente antes y después |

## Cómo sacar el material de Instagram
Herramienta MCP de Meta Ads `ads_get_ig_media`. Es de solo lectura: no crees ni promociones nada.
- `ad_account_id`: `1057957433816789` (cuenta "AGLEZ US")
- `ig_account_id`: `17841401214324388` (@albertoglez6)
- `filters`: `[{"field":"product_type","operator":"in","value":["FEED","REELS"]}]`
- Paginar con `next_cursor`. Hay unas 500 publicaciones o más.
- Cada elemento trae `media_url` (se descarga con curl), `caption`, `permalink` y `timestamp`.

Limitaciones:
- Las **destacadas no salen por la API**. Alberto tiene que subirlas.
- @albertomentor y @albertoglezcoach no están vinculadas a esa cuenta de anuncios.

## Pendiente
1. Descargar y meter vídeos e imágenes de los casos:
   - Convertir las tarjetas en tarjetas con `<video controls playsinline preload="none" poster>` o `<img>`.
   - Se ven 6; el resto lleva `hidden class="case extra"`.
   - Los casos con cifra y plazo van primero.
   - Hacerlo en los dos idiomas.
   - Hay que tener permiso de cada cliente.
2. Fotos de Alberto en `#historia` / `#story`:
   - Antes, con casi 100 kg.
   - Físico actual.
   - Entrenando.
   - Están en su carpeta local `fotos/`, que está excluida del repo por `.gitignore`.
3. Vídeo VSL para arriba del todo.
4. Jotform en inglés.
5. Comprimir: vídeos a 480 px con CRF 29 (ver la sección de la mentoría) y fotos a 900 px y calidad 80, en `landing-salud/casos/`.
6. Volver a publicar los dos artifacts, pasando los medios en `files`.
