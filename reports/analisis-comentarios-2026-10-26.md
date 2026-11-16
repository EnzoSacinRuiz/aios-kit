# Análisis de posts y comentarios: TikTok y Facebook (26 set – 26 oct 2026)

_Fuente: Apify, sacado el 2026-10-26. Los datos crudos y el script están en `projects/redes-amazon-gas/analisis-comentarios/`. Costo del scrapeo: unos USD 0,05._
_Instagram no se incluyó._

> **Actualización del 2026-10-26:** papá decidió no tocar el tema del precio en redes. Las ideas sobre el precio de este informe quedan descartadas. Solo se hace el post del peso (post 11). Ver `decisions/log.md`.

## Lo importante primero

- **Casi todos los comentarios son quejas, y todas son del post 1 de Facebook** ("Iquitos no tiene carretera", 9.691 vistas). De sus 18 comentarios, 13 hablan del precio y 3 dicen que el balón llega con menos gas. Solo 1 es positivo.
- **La queja del peso también salió en TikTok:** el único comentario de TikTok del mes, en el post 7, dice "llega incompleto los balones".
- **Las quejas llegaron cuando el post se volvió viral.** El post 1 llegó a gente que no sigue la página, y esa gente respondió con lo que piensa de la marca. Si los próximos posts también funcionan, van a llegar las mismas quejas. Por eso conviene tener lista la respuesta antes.
- **No se ve que la marca haya respondido.** El comentario más largo (Meko L. Caina) tiene 1 respuesta, pero el scrapeo no la trajo. Revisa a mano si alguien le contestó.

## Rendimiento de los posts

| Post | Facebook (vistas / likes / comentarios / compartidos) | TikTok (reproducciones / likes / compartidos) |
|---|---|---|
| 1 · Iquitos no tiene carretera (3–5 oct) | **9.691** / 75 / 20 / 15 | 301 / 12 / 3 |
| 2 · 3 cosas al recibir el balón (6 oct) | 417 / 7 / 0 / 3 | 275 / 8 / 2 |
| 4 · Se acabó el gas en el juane (13 oct) | 413 / 3 / 0 / 1 | 22 / 2 / 2 |
| 3 · Tacacho con cecina (15 oct) | 359 / 8 / 0 / 4 | 21 / 4 / 0 |
| 7 · Parte 2, vaciante (21 oct) | 671 / 7 / 0 / 1 | **2.480** / 75 / 4 |

- Lo que funciona es el río y la logística. El post 1 arrasó en Facebook y la parte 2 es lo mejor de TikTok por lejos.
- La receta y el humor casi no tuvieron reproducciones en TikTok (21 y 22). Esto confirma sacar Cocina, como dice `reports/estrategia-contenido-2026-10-21.md`.
- Facebook también tiene 2 posts del 15 de octubre sin texto, probablemente cambios de foto. No se analizaron.

## Qué dicen los comentarios

### 1. Precio: 14 de 19 comentarios

| Tipo | Ejemplos (textuales) | Cuántos |
|---|---|---|
| "Es caro", sin más | "Demasiado caro", "Costo elevado", "Muy caro su costo", "Deberían bajar sus precios" | 8 |
| Acusan a la empresa de abusar | "Muy caro venden abusivos.", "acá se vienen. ASER ricos", "¿Kien se lleva el mayor margen de utilidad?" | 3 |
| Comparan con otro producto | "Como Backus transporta la cerveza en barcazas y tiene el mismo precio que el Pucallpa" | 1 |
| Acusan a las envasadoras en general | "compran directo en planta a precio barato … lo venden al precio doble … NADIES los controla" | 1 |
| Argumento completo | Meko: "Que el gas llegue en barcazas … explica la logística, pero no justifica por sí solo que el consumidor loretano tenga que pagar un precio tan elevado … sería bueno hablar también de precios, costos reales" | 1 |

**Cómo leerlo:**
- El post 1 explicó la logística y la gente contestó: "¿y entonces por qué es tan caro?". El post despertó esa pregunta y no la respondió.
- Meko y Miguel (el de Backus) dicen lo mismo: que el río no alcanza como excusa. Un post que solo diga "es caro porque viene por río" va a recibir la misma respuesta.
- Ruben pregunta "¿quién se lleva el mayor margen?". Puede ser una pista: hay que saber si la gente reclama por el precio de planta o por el que cobran la bodega y el repartidor. Eso solo lo sabe papá.

### 2. Peso o rendimiento del balón: 4 comentarios

| Comentario | Red | Qué dice en realidad |
|---|---|---|
| "llega incompleto los balones." | TikTok, post 7 | Que el balón llega con menos gas |
| "La mitad te dan" | Facebook, post 1 | Que el balón llega con menos gas |
| "Por eso no llega ni a los 10 kilos" | Facebook, post 1 | Que el balón llega con menos gas, y dice la cifra |
| "Solo dura 20 días" | Facebook, post 1 | Que dura poco. Puede ser peso o puede ser consumo. |

Hay uno ambiguo: "Pero lo embasan completo" (Jjair Plaza). Puede estar defendiendo a la marca o ser sarcasmo.

**Cómo leerlo:**
- Es menos frecuente que el precio, pero es más grave, porque es una acusación concreta y se puede comprobar o desmentir con una balanza.
- Aquí sí hay algo que mostrar: el pesaje en planta, la tara impresa en el balón y el derecho a pesarlo frente al repartidor, que respalda Osinergmin.
- No sabemos si quienes se quejan compraron Amazon Gas o un balón recargado de forma informal. El contenido no puede acusar a nadie. Lo que sí puede hacer es enseñar a la gente a comprobar lo que recibe.

### 3. Positivos: 1

- "Excelente! 👍🏻" (Jahel Panduro).

## Qué significa para el contenido que quieres hacer

**Peso, "el balón está bien pesado": se puede hacer, y es lo más fácil de probar.**
- Formato: video real en planta, con un balón en la balanza y el número en pantalla. Se explica qué es la tara y cómo pesarlo en casa o frente al repartidor.
- Remate: "si no te cuadra, escríbenos al 991 511 401". Así la queja va al WhatsApp y no a los comentarios.
- Es material real, y eso es lo que mejor funcionó este mes.
- Requiere: que papá autorice grabar en planta y que esté seguro del control de peso. Si aparece un video de un cliente pesando un balón de Amazon Gas que no cuadra, el post se cae.

**Precio, "es el precio justo": cuidado, así como está puede salir mal.**
- Decir "precio justo" a gente que siente que es caro suena a que no los escuchamos. Además, Meko ya respondió por adelantado al argumento de la logística.
- Lo que sí puede funcionar es la transparencia: mostrar desde dónde viene el gas, cuántos días navega la barcaza, qué cuesta (combustible, tripulación, seguros, envasado, reparto) y qué parte del precio no depende de nosotros (impuestos, precio internacional y el margen de quien te lo vende). Algo como "¿Por qué el gas cuesta lo que cuesta en Iquitos? Te lo contamos".
- Requiere datos que no tenemos y que solo papá puede dar y aprobar: la estructura de costos que se puede mostrar en público, el precio de venta al distribuidor y el precio sugerido al público, y la comparación con los precios de "Facilito Balón de Gas" de Osinergmin, solo si nos favorece.
- Hay que decidir con él si conviene responder a lo de Backus. La cerveza y el GLP no se transportan igual (el GLP va en barcaza presurizada y está regulado), pero explicarlo puede sonar a excusa.

**Otras ideas que salen de los comentarios:**
- **Responder un comentario con un video.** Se toma el de Meko o el de "llega incompleto" y se contesta con un video. Es un formato nativo de TikTok, y quien comentó suele compartirlo.
- **"Cómo saber si te están dando un balón completo".** Es un video de seguridad útil: precinto, etiqueta de peso y pesaje. No defiende a la marca, educa, y por eso genera menos rechazo.
- **"¿Por qué se te acaba el gas en 20 días?".** Explica el consumo real según la familia y la cocina, y da tips para que rinda. Responde a Lucas sin discutirle.
- **Responder ya los comentarios del post 1** con un mensaje corto que lleve al WhatsApp. Estas respuestas también son publicaciones, así que necesitan la aprobación de papá.

## Preguntas para papá antes de producir

1. ¿Podemos grabar el pesaje en planta? ¿Qué margen de error tiene el llenado?
2. ¿Qué parte del precio final controla Amazon Gas y qué parte cobra el distribuidor o la bodega?
3. ¿Qué datos de costos se pueden decir en público?
4. ¿Cómo está nuestro precio frente a Facilito Balón de Gas (Osinergmin) en Iquitos?
5. ¿Alguien respondió los comentarios del post 1? ¿Quiere que respondamos?

## Notas

- El post 7 ya aparece publicado en Facebook y TikTok el 21 de octubre.
- Faltan Instagram y las respuestas anidadas de Facebook. Si los quieres, se agregan al script.
