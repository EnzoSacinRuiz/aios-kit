# Personaje recurrente — Doña Meche, la vecina

_Creado para el post 4 (13 oct 2026). Reaparece en el post 10 (30 oct). Reúsalo tal cual: misma
imagen de referencia, misma descripción y misma voz. Si cambias algo, el personaje deja de
ser reconocible._

## Quién es

- **Nombre:** Doña Meche (Mercedes). Todos en el barrio le dicen "Doña Meche".
- **Rol:** la vecina de Iquitos que cocina para toda la familia. Es el personaje, no la marca:
  Amazon Gas aparece al final, en el CTA. El chiste es de ella.
- **Edad aparente:** unos 55 años.

## Descripción física exacta (copiar en cada prompt)

Mujer de Iquitos de unos 55 años, mestiza, piel morena cálida, cara redonda y amable con
líneas de expresión, ojos marrón oscuro muy expresivos. Pelo negro grueso con algunas canas,
recogido en un moño bajo con un colet granate oscuro. Aretes pequeños de aro dorado.

**Ropa (siempre la misma):** blusa de algodón de manga corta con estampado floral pequeño en
crema y granate, mandil crema liso con un bolsillo delantero, falda marrón oscuro hasta la
rodilla y sandalias de jebe.

**Escenario base:** cocina humilde pero ordenada de una casa de Iquitos: paredes de tablas
pintadas de crema, ventana con malla mosquitero verde y plantas tropicales afuera, mostrador
de mayólica con cocina de mesa de dos hornillas, olla grande de aluminio.

## Archivos

| Archivo | Qué es |
|---|---|
| `dona-meche-ref.png` | Imagen de referencia (1792×2400, de la cintura para arriba, en su cocina). **Pásala siempre como `image_input`.** |
| `ref-url.txt` | URL temporal de kie.ai de la referencia. Puede caducar: si falla, sube `dona-meche-ref.png` de nuevo (ver `post-04-humor/scripts/kie.py`, función `upload`). |
| `../post-04-humor/assets/img/a-cocinando.png`, `b-susto.png`, `c-celular.png` | Escenas 9:16 del post 4, ya consistentes con la referencia. Sirven como referencias extra de poses. |

## Cómo se generó (kie.ai)

- **Modelo:** `nano-banana-2` (kie.ai), `aspect_ratio` 3:4, `resolution` 2K, png. Costó 12 créditos.
- **Prompt de la referencia:**

> Waist-up portrait of a friendly 55-year-old woman from Iquitos in the Peruvian Amazon,
> mestiza, warm brown skin, round kind face with laugh lines, expressive dark brown eyes, thick
> black hair with a few grey streaks pulled back in a low bun held by a dark maroon scrunchie,
> small gold hoop earrings. She wears a short-sleeve cotton blouse with a small cream and
> maroon floral print, a plain cream apron with one front pocket, a knee-length dark brown
> skirt and simple rubber sandals. She stands in a humble but tidy home kitchen in Iquitos:
> wooden plank walls painted light cream, a window with green mosquito screen and tropical
> plants outside, a tiled counter with a two-burner tabletop gas stove, a big aluminium pot
> full of juanes (rice parcels wrapped in green bijao leaves tied with string), looking
> straight at the camera with a warm, cheeky neighbourly smile, hands resting on her apron.
> Character reference photo, centered, face clearly visible. Photorealistic, natural warm
> daylight, shot on a smartphone like a TikTok comedy sketch, realistic skin texture, no text,
> no captions, no logos, no brand names, no purple or violet colors anywhere, no gas cylinders
> visible.

- **Para escenas nuevas:** `nano-banana-2` con `image_input: [URL de la referencia]`,
  `aspect_ratio` 9:16, y el prompt empieza con: *"Use the woman from the reference image,
  identical face, hair, earrings and clothes."* Luego el plano y la expresión. Termina con el
  mismo bloque de estilo (photorealistic … no purple … no gas cylinders visible). Ver
  `post-04-humor/scripts/imagenes.py`.
- **Para que hable:** `kling/ai-avatar-standard` (kie.ai) con `image_url` = escena 9:16 y
  `audio_url` = la línea de ElevenLabs. Da sincronía labial. Ver `post-04-humor/scripts/clips.py`.

## Voz (ElevenLabs)

- **Voz:** Lily — femenina, peruana, adulta, cálida y enérgica (librería compartida).
- **voice_id:** `ek0qR5Bu0N3aPdijsdae`
- **Modelo:** `eleven_multilingual_v2`
- **Ajustes:** stability 0.35, similarity_boost 0.8, style 0.5, use_speaker_boost true.
- Terry (`ulJB4yAMefhHYn0FWgGy`) es la voz de narrador de la marca, no la de Meche. No las mezcles.
- Ver `post-04-humor/scripts/voz.py`.

## Rasgos de humor

- **Exagera el drama doméstico**, pero con cariño: cara de susto con las manos en las mejillas,
  pausas largas, "¿justo ahorita?".
- **Le habla a la cámara como si fuera la vecina de al lado** ("ya aprendí, vecina").
- **Aprende la lección al final** y la comparte: ella es la que da el consejo, no la marca.
- **Sabor loretano suave:** diminutivos ("juanecitos"), "ahorita", "vecina". Sin exceso de
  jerga y sin burlarse de la gente de Loreto: el chiste es la situación (quedarse sin gas en
  el peor momento), nunca la persona ni su forma de hablar.
- **Comida y fechas locales** como detonante: juane, almuerzo familiar del domingo, fiestas.
- **Coletilla posible para el post 10:** "¡Ay, no, otra vez no!" (ella ya aprendió en el post 4;
  en el 10 la que se queda sin gas puede ser otra vecina, y Meche le da el consejo).

## Lo que no se hace

- No mostrar balones inventados por IA como si fueran Amazon Gas. Si hace falta un balón, usar
  una foto real de `references/branding/fotos/`.
- Nada morado en la ropa ni en el escenario (el morado es de Llamagas).
- No ponerle uniforme ni logo de Amazon Gas: es una clienta, no una empleada.
