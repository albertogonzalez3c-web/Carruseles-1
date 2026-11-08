# Pendiente de publicar (límite diario de 200 publicaciones; se reinicia a medianoche UTC)

DECISIÓN DE ALBERTO: a partir de ahora, UNA sola página por cliente.
Cómo: `python3 tools/hub.py clientes/<cliente> "Nombre"` → genera clientes/<cliente>/_hub/ e imprime file_path + mapa files.
Publicar con Artifact: file_path = _hub/index.html, files = el mapa impreso, capabilities {db:{}} (para CRM y reporte), icon.

PRUEBA PRIMERO con Juanmi: abrir el artifact, entrar en 7 · CRM y comprobar que guarda (no sale "modo prueba").
- Si el CRM/reporte NO acceden a la base de datos dentro del hub: publicar crm.html y 7-reportes.html como artifacts propios (con db) y que el hub enlace a esas URLs (editar las tarjetas del índice) → 3 publicaciones por cliente.

Clientes nuevos a publicar como hub: juanmi-baron, carlos-santos, gerard-pavon, zent-jorge-gabriel, jorge-sanchez, xavier-garcia (cuando sus agentes terminen).

Clientes antiguos (ya publicados en 8 enlaces sueltos): republicar las 2 páginas pendientes de Seguí en sus URLs:
- clientes/fran-segui/partes/crm.html → https://claude.ai/artifact/TMfVbQ1ENMxA3xvZzQq1iq
- clientes/fran-segui/partes/7-reportes.html → https://claude.ai/artifact/4RYs2SMvqgbtbaGNrksYDe
(Opcional, preguntar a Alberto: pasar también los antiguos a hub; cambia sus enlaces.)

## AL FINAL (petición de Alberto): página maestra con los 17 clientes
Una sola página "Clientes Mentoría" con los 17: para cada cliente, nombre, nicho en una línea, método, precio de entrada, estado (publicado / qué falta confirmar) y su enlace (hub para los nuevos; para los 11 antiguos, sus 8 enlaces en desplegable o su landing/perfil). URLs de los antiguos: buscar en el historial de commits / resumen de la sesión o con Artifact action "list".
Datos de la página maestra (17 clientes, URLs antiguas e info): clientes/_maestra/datos.json. Rellenar la URL hub de los 6 nuevos al publicarlos.
