# Post 1 — "¿Tu balón es Amazon Gas? Míralo en el precinto"

Abre el mes 2. Enseña a reconocer un balón de Amazon Gas por su precinto: **amarillo y con el
nombre de la marca** (dato de Enzo, 2026-11-15).

**Visual:** primer plano de un balón real. Una mano señala el precinto, zoom al color y al nombre
impreso. Tres checks en pantalla, uno por vez:

1. ✓ Amarillo
2. ✓ Dice Amazon Gas
3. ✓ Sin romper

**Texto (voz en off), versión B del 2026-11-16, más informativa y neutral:** "Para saber si tu balón es Amazon
Gas, fíjate en el precinto. Todos nuestros balones salen de planta con su precinto amarillo y nuestro nombre
impreso. Si el precinto no es amarillo, no dice Amazon Gas o está roto, ese balón no salió así de nuestra planta.
Te recomendamos no recibirlo. Si tienes dudas, mándanos una foto del precinto por WhatsApp." Los textos en pantalla
no cambian ("¿Tu balón es Amazon Gas?", "No lo recibas", "¿Dudas con tu balón?").

**Cierre:** "¿Dudas con tu balón? Mándanos una foto del precinto al WhatsApp 991 511 401."

**Formato:** video 15–20 s (TikTok, Reels, Facebook). Opcional: carrusel de 4 láminas con los
mismos tres checks.

## Material

Foto o video **real** de un precinto en un balón. No hay ninguno en `references/branding/fotos/`,
así que hay que grabarlo. No se genera con IA: el post consiste justo en reconocer el precinto
verdadero, y la IA deforma el texto impreso.

## Por confirmar con papá

- El texto exacto del precinto: "Amazon Gas" o "Energeo". Es la misma duda que quedó abierta en
  `mes-1/export/copies-post-11.txt`.
- Si el precinto tiene algo más que sirva para identificarlo (código, número, holograma).
- La frase "No lo recibas": es firme a propósito; confirmar que papá la quiere así.

## Relación con otros posts

- El post 11 de octubre (`mes-1/post-11-peso/`) ya menciona los tres checks del precinto de pasada.
  Este post lo convierte en el tema central.
- El post 5 de este mes ("5 señales de un balón seguro") repite "precinto intacto" como señal 1.
  Está bien que lo refuerce, pero conviene que salgan separados por al menos una semana.

## Producción (borrador del 2026-11-15)

- Videos: `../export/post-01-precinto-borrador.mp4` (9:16) y `../export/post-01-precinto-4x5-borrador.mp4` (4:5), 22 s.
- Voz: Terry a 0.95 con `style 0` y `stability 0.65`, para que suene neutral y no como profesor ni alarmista. Dura 19,1 s. Las pruebas A/B están en `pruebas-voz/`. Música de ElevenLabs. Todo se regenera con `scripts/voz.py` y `scripts/build.py`.
- kie.ai: 187,5 créditos del primer borrador (3 imágenes Nano Banana 2 + 3 clips Kling 2.1). Ninguno de esos
  clips queda ya en el video. El upscale con Topaz falló dos veces (kie no pudo descargar las fotos) y no cobró.
- **Ya no queda ninguna toma hecha con IA** (`TEMPORAL = False`). Todas son fotos reales de Enzo; los
  originales `image*.png` siguen en esta carpeta:
  - **1, gancho:** `assets/img/balones-marca-grupo-v2.jpg`, balones con la marca, con paneo. La foto está aclarada
    (sin el velo blanco) y el velo oscuro del video baja al 45 % en esta toma para que no se vea opaca.
  - **2, "Míralo en el precinto":** `assets/img/precinto-1.jpg` (`image copy 8`).
  - **3a, planta:** `assets/img/planta-balones-wide.jpg`, con un paneo que termina en el equipo.
  - **3b, checks:** `assets/img/precinto-2.jpg` (`image copy 9`). Los checks bajan para no tapar el precinto.
  - **4, "Si ves esto":** `assets/img/balon-producto.png`, el balón de estudio (`image copy 4.png`) sin el
    fondo negro, sobre un degradado granate.
  - **5, "No lo recibas":** `assets/img/precinto-3.jpg` (`image copy 7`), oscurecido.
  - Las fotos del precinto salen de `scripts/precintos.py`: recorte 9:16 con el precinto al centro y upscale
    local (lanczos + nitidez).
  - Sin usar: `balones-marca-fila-v2.jpg`, `precinto-balanza.jpg`, `planta-balones-vertical.jpg` y
    `planta-balones-cerca.jpg`. La foto completa de la balanza le sirve al post 3.
