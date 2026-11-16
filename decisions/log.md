# Registro de decisiones

Solo se agregan entradas, nunca se editan. Formato: `[AAAA-MM-DD] DECISION: … | REASONING: … | CONTEXT: …`

---

[2026-09-28] DECISION: workspace initialized via /onboard | REASONING: replaced demo content with the operator's real context | CONTEXT: operator said the agent must never "publicar sin aprobacion de mi papa".

[2026-09-28] DECISION: El tono cercano de `references/voice.md` también rige para lo publicado en redes. Se ajusta `.claude/rules/communication-style.md`, que pedía un tono formal para todo lo externo | REASONING: El operador pidió un tono "cercano y loretano, sin jerga excesiva" para las redes, y la regla formal lo contradecía | CONTEXT: Ya se había detectado esta contradicción en una auditoría anterior (19 de septiembre).

[2026-10-26] DECISION: Las redes no hablan del precio. A los comentarios de que el balón llega incompleto se responde con un post de peso verificado (post 11), y papá lo revisa antes de que se suba | REASONING: Papá: "Creo que eso mejor no tocarlo. La única forma de tocarlo es bajando el precio". Defender el precio a gente que lo siente caro reabre la discusión | CONTEXT: Análisis de comentarios del 2026-10-26 (`reports/analisis-comentarios-2026-10-26.md`): 14 de 19 comentarios se quejan del precio y 4 del peso, casi todos en el post 1 de Facebook.

[2026-10-26] DECISION: El dashboard de comentarios se despliega en Railway con `railway up` desde `projects/redes-amazon-gas/analisis-comentarios/`, sin repo nuevo ni auto-deploy desde GitHub, y los datos scrapeados viven solo en el volumen de Railway | REASONING: Railway permite un cron de varios minutos esperando a Apify y uso comercial por ~USD 5/mes. Vercel Hobby prohíbe uso comercial y corta funciones largas, y Coolify exige mantener un VPS. El repo `aios-kit` es público y los comentarios traen nombres de personas reales, así que no pasan por git | CONTEXT: El operador quería que el cliente viera el análisis en vivo. Protegido con contraseña (`DASHBOARD_PASSWORD` en Railway) y se actualiza cada 12 h.
