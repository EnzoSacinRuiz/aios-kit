# Post 2 — "El gas de aquí"

**Idea:** Amazon Gas es la empresa de gas de Loreto. Tu balón se llena aquí, lo llena gente de
aquí y llega a tu barrio en camiones de aquí, y así es desde 1999. El post no compara con la
competencia: habla de origen, pertenencia y trayectoria.

**Formato:** video de 22 a 25 s, en 9:16 (TikTok, Reels) y 4:5 (feed de FB e IG). Voz en off
de Terry a 0.88, como el resto de videos, con música suave de fondo y subtítulos palabra por
palabra.

## Por qué cambió el texto original

El texto del primer borrador era: "Hay gas que viaja días para llegar a Iquitos. El nuestro se
envasa aquí…". Tenía dos problemas:

1. **Se contradice.** Nuestro GLP también viaja días: llega en barcaza por el río, y eso fue
   justo lo que contó el post 1 de octubre. Cualquiera que lo haya visto lo nota.
2. **Es una comparación que no podemos probar.** Insinúa que la competencia trae el gas ya
   envasado de fuera. Si alguna de esas empresas envasa en Iquitos, el post queda mal y le da
   motivo para responder.

La nueva versión reconoce el río y gira hacia lo que de verdad es local: **el gas llega por el
río, pero tu balón se llena aquí.** Así se conecta con el post de octubre sin repetirlo.

Además se quitó "completo y seguro", porque el peso es el tema del post 3 y la seguridad el del
post 5. Este post se queda con una sola idea.

## Guion

| # | Tiempo | Imagen | Voz en off | Texto en pantalla |
|---|---|---|---|---|
| 1 | 0–3 s | `aerea-rio` → `barcaza-real`: el río desde arriba y la barcaza navegando. | "El gas llega por el río…" | — (solo subtítulos) |
| 2 | 3–6 s | Corte seco a `aerea-planta`, con un zoom lento hacia la planta. | "…pero tu balón se llena aquí." | **AQUÍ** en grande, con un pin: *Santa Clara, Iquitos* |
| 3 | 6–10 s | `planta` → `tanque-planta`: tanques y línea de envasado. | "En nuestra planta de Santa Clara, con gente de Loreto." | — |
| 4 | 10–13 s | `equipo-planta` → `tripulacion`: la gente, con zoom lento (*Ken Burns*). | (sigue la frase anterior) | *Gente de aquí* |
| 5 | 13–17 s | `camion-balones` → `reparto`: el camión saliendo y la entrega. | "Sale en camiones que conocen tus calles, hasta tu barrio." | — |
| 6 | 17–20 s | Fondo con la paleta de la marca y un contador que sube de 1999 a 2026. | "Así trabajamos desde 1999." | **Desde 1999** · *27 años en Loreto* |
| 7 | 20–25 s | Logo sobre `aerea-meandro` desenfocada. | "Amazon Gas: el gas de aquí." | **El gas de aquí** · ¿En qué barrio cocinas con Amazon Gas? · WhatsApp 991 511 401 |

**Voz en off completa (unas 45 palabras, entre 20 y 22 s a 0.88):**

> El gas llega por el río… pero tu balón se llena aquí. En nuestra planta de Santa Clara, con
> gente de Loreto. Sale en camiones que conocen tus calles, hasta tu barrio. Así trabajamos
> desde 1999. Amazon Gas: el gas de aquí.

Para ElevenLabs, el año va escrito en letras ("mil novecientos noventa y nueve") para que Terry
no lo lea dígito por dígito.

### Notas de edición

- **Gancho (0–3 s):** el corte seco de la escena 1 a la 2, con "AQUÍ" apareciendo de golpe, es
  el momento que retiene. Hay que caer justo sobre la palabra "aquí".
- **Gente (escena 4):** las fotos de personas solo llevan zoom o paneo. **No se animan con
  kie.ai**, porque la IA deforma caras y manos, y esas personas son trabajadores reales.
  El río, la planta y los camiones sí se pueden animar con Kling, como en `mes-1/post-01-rio/`.
- **Música:** cálida, con un poco de ritmo; nada épico ni corporativo.

## Copies por red

**TikTok:**
> El gas llega por el río, pero tu balón se llena aquí, en Santa Clara 📍 Desde 1999. ¿En qué
> barrio cocinas con Amazon Gas? 👇
> #Iquitos #Loreto #AmazonGas #HechoEnLoreto

**Instagram y Facebook:**
> Nuestro gas viaja por el río, pero tu balón se llena aquí nomás, en nuestra planta de Santa
> Clara, con gente de Loreto. Y de ahí sale a tu barrio en nuestros camiones. Así trabajamos
> desde 1999. 🔥
>
> Cuéntanos: ¿en qué barrio cocinas con Amazon Gas? 👇
>
> 📲 Pedidos al WhatsApp 991 511 401
> #Iquitos #Loreto #AmazonGas #ElGasDeAquí

## Material

Todo sale de fotos reales de `references/branding/fotos/`: `aerea-rio`, `barcaza-real`,
`aerea-planta`, `planta`, `tanque-planta`, `equipo-planta`, `tripulacion`, `camion-balones`,
`reparto` y `aerea-meandro`. No hace falta grabar nada nuevo. Si Enzo puede grabar en planta
un clip real de 3 a 5 s de un balón llenándose, reemplaza con ventaja a la escena 3.

## Por confirmar con papá

- **¿1999 o 2000?** `context/work.md` dice "desde 1999", pero la voz del post 1 de octubre
  (`mes-1/post-01-rio/scripts/voz.py`) dijo "desde el año dos mil". Hay que fijar un año y
  corregirlo en el archivo que esté mal.
- **"Con gente de Loreto":** confirmar que el personal de planta y de reparto es, en su gran
  mayoría, de la zona. Si no, cambiar a "con nuestra gente".
- **"Camiones que conocen tus calles":** confirmar que el reparto es propio y llega a los
  barrios, no solo a distribuidores.
- **`tripulacion`:** confirmar que las personas que salen en la foto están de acuerdo en
  aparecer en redes.

## Relación con otros posts

- Retoma el post 1 de octubre (el río) sin repetirlo: el río ocupa solo la primera frase.
- El post 6 de este mes ("La gente detrás de tu balón") profundiza en el equipo. Este solo lo
  muestra de pasada, así que conviene que salgan separados.
