# GLP Amazónico SAC — Amazon Gas

## Qué vende y a quién

- **Producto:** GLP (gas licuado de petróleo), tanto envasado en cilindros (marca "Energeo") como
  a granel.
- **Clientes:** hogares, restaurantes y pequeña industria de Iquitos y Loreto. Vende al por
  mayor y al por menor.
- **Operación:** desde 1999, con cadena propia: planta envasadora, terminal portuario, barcazas
  que transportan GLP por los ríos amazónicos y reparto terrestre.
- **Diferenciador:** es la única empresa peruana que transporta GLP por río en alto tonelaje.
  El mensaje de marca es "energía que mueve a Loreto".

El análisis completo de la empresa (riesgo social, reputación y estado de sus redes) no va en
este archivo. Su lugar es `knowledge/external/`.

## Dónde vive la verdad

- **Tareas, estado de cada post y costos:** `projects/redes-amazon-gas/calendario-contenido.xlsx`.
  Tiene una fila por post e incluye los tokens y créditos consumidos. Sus números nunca se
  copian aquí; se consultan en el Excel.
- **Producción:** kie.ai (video e imagen) y ElevenLabs (audio). Las credenciales están en
  `.env`, que nunca se commitea.
- **ClickUp:** no se usa, aunque su clave figure en `.env`.
- **Branding:** el kit de marca vive en `references/`. Se extrae de https://amazongas.com.pe.

## Fricción recurrente

Todo el pipeline de generación de contenido (idea, copy, imagen o video, audio y adaptación a
cada red) se hace a mano. Primero hay que documentarlo como SOP en `references/sops/` y,
después, automatizarlo.
