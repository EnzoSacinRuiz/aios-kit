> 🇬🇧 [Read this in English](README.md)

# aios-kit

Un sistema operativo para el contexto de tu agente de IA — cuatro mecanismos y siete skills para que deje de no encontrar lo que ya sabe.

[![Licencia: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## El problema

Le sigues dando más contexto al agente, y sigue pasando por alto lo que ya tiene.

Más contexto no es la solución. Un montón más grande tarda más en recorrerse y esconde más contradicciones.

El problema casi nunca es cuánto sabe — es que no encuentra lo que ya sabe.

---

## Los cuatro mecanismos

| Mecanismo | Qué resuelve |
|---|---|
| **Precedencia** | Un dato vive en un solo lugar; todo lo demás apunta ahí. |
| **Ruteo** | Una tabla de qué contiene cada carpeta y cuándo ir ahí. |
| **Protocolo de falla** | Cuando el agente no encuentra algo que sí estaba, se nombra el modo de falla y se arregla la causa, no el síntoma. |
| **Ciclo de mantenimiento** | El sistema se audita y se repara solo, o se pudre. |

Los cuatro viven en `CLAUDE.md`, el manual que el agente lee antes que cualquier otra cosa.

**Precedencia** existe porque un número copiado es correcto el día que lo pegas y falso desde el día siguiente. Nadie actualiza la copia, porque nadie recuerda que existe. Seis semanas después se abre una sesión, lee la copia vieja en la capa que se carga siempre, y te afirma con total seguridad algo que no es cierto.

**Ruteo** es una tabla que cubre todas las carpetas de primer nivel — qué guarda cada una y cuándo ir ahí. Una carpeta que el mapa no menciona es una carpeta que el agente no va a encontrar. Si agregas una carpeta, agregas su fila en el mismo commit.

El **protocolo de falla** se corre en el momento en que se confirma que el agente no encontró algo. Toda falla es exactamente uno de cuatro modos, y el kit usa las mismas cuatro palabras en todas partes: `poisoning` (un archivo precargado afirmó algo falso o viejo), `bloat` (la respuesta estaba ahí, enterrada en demasiado), `confusion` (el mapa calla o manda a un lugar irrelevante), `clash` (dos archivos se contradicen y el agente le creyó al equivocado). Nombrar el modo es lo que convierte una disculpa en una reparación — un archivo encontrado a mano y no re-ruteado se vuelve a perder la semana siguiente.

El **ciclo de mantenimiento** es el que todo el mundo se salta. Los manuales, los índices y los archivos de contexto son afirmaciones sobre lo que existe, y nadie vuelve a verificar una afirmación una vez que está escrita. Un workspace que nadie mantiene deja de ser cierto en unos sesenta días, y un sistema que se equivoca con seguridad es peor que no tener sistema. Por eso el kit se revisa a sí mismo: un chequeo de deriva de solo lectura corre al inicio de cada sesión y habla únicamente cuando algo se movió, y dos skills — una de exactitud y otra de estructura — dejan el estado del workspace por escrito cada mes.

---

## Anatomía

```
aios-kit/
├── CLAUDE.md                     El manual operativo. Tabla de precedencia, mapa
│                                 de ruteo, protocolo de falla, automatizaciones.
├── context/                      Se carga en cada sesión. Cuatro archivos cortos.
│   ├── me.md                     Quién es el operador.
│   ├── work.md                   Qué vende el negocio y a quién.
│   ├── team.md                   Quién hace qué, y quién firma.
│   └── priorities.md             Metas del trimestre. El único lugar donde se editan.
├── knowledge/
│   ├── external/                 El mundo de afuera: clientes, prospectos,
│   │                             competencia. Un grafo [[wiki-link]] con su propio
│   │                             index.md y su manual de ingesta.
│   └── playbook/                 Tu método propio: principios y jugadas. Igual forma.
├── decisions/log.md              Append-only. Qué se decidió, por qué, en qué contexto.
├── projects/                     Trabajo por cuenta. Entregables, no contexto — vas
│                                 al proyecto puntual, nunca cargas la carpeta entera.
├── reports/                      Lo que escriben las skills. Generado, no redactado.
├── references/                   voice.md, marcos de trabajo y sops/ — un archivo por
│                                 proceso repetible.
├── templates/                    Puntos de partida que se copian, no se editan encima.
├── archives/                     Acá nada se borra, se archiva.
├── scripts/
│   └── aios-freshness-check.sh   Chequeo de deriva de solo lectura. Corre al inicio de
│                                 cada sesión y no imprime nada si nada se movió.
├── docs/                         Documentación sobre el kit mismo, para humanos.
└── .claude/
    ├── rules/                    Reglas permanentes — la regla, y luego el porqué.
    ├── skills/                   Siete skills, una carpeta cada una.
    └── settings.json             Conecta el hook de sesión.
```

### Viene lleno, no vacío

La mayoría de los repos plantilla están huecos: carpetas con un `.gitkeep` y un README que describe un sistema que nunca contuvo nada. Este llega precargado con un ejemplo trabajado — **Meridian Research**, una consultora ficticia de investigación de mercado de cuatro personas — para que leas un workspace vivo en vez de imaginártelo.

Entra a `knowledge/playbook/` y vas a encontrar un principio de venta escrito como una afirmación por archivo, enlazado a la cuenta de `knowledge/external/` que lo dispara una y otra vez y a la entrada de `decisions/log.md` de donde salió. Entra a `context/priorities.md` y vas a ver las metas del trimestre junto a una advertencia explícita de que el saldo en caja jamás se escribe ahí. Esa es la tesis completa, funcionando, en archivos que puedes abrir ahora mismo.

Todos los archivos del demo abren con la misma línea — `> 🟡 DEMO — /onboard replaces this file with yours.` — y `/onboard` los encuentra por esa línea, no por una lista que quedaría desactualizada, los mueve a `archives/demo/` conservando su ruta, y escribe los tuyos en su lugar. No se borra nada: puedes volver a leer el ejemplo cuando tu propio workspace ya esté andando.

---

## Arranque rápido

```sh
git clone https://github.com/EnzoSacinRuiz/aios-kit.git mi-workspace
cd mi-workspace
claude
```

Y dentro de la sesión:

```
/onboard
```

Te pregunta en qué idioma quieres que trabaje el workspace, te entrevista de a una pregunta por vez, archiva la empresa demo y escribe tus archivos de contexto reales y tu primera regla permanente. Se puede volver a correr sin riesgo: la segunda corrida actualiza sobre lo que ya hay y no archiva el demo dos veces.

Eso es toda la instalación. No hay paquete que instalar ni nada que configurar antes.

---

## El ciclo de vida

| Skill | Rol |
|---|---|
| `/onboard` | **Instalar.** Te entrevista y reemplaza el demo con tu contexto real. |
| `/distill` | **Alimentar.** Convierte un transcript, un documento o un volcado de notas en conocimiento ruteado y enlazado — decisiones al log, hechos del mundo externo a una wiki, tu propio método a la otra, tareas a tu gestor. Nunca un solo archivo volcado. |
| `/route-fix` | **Reparar.** No encontraste algo que sí estaba. Traza qué leíste, nombra el modo de falla, arregla la causa. |
| `/os-audit` | **¿Sigue siendo cierto?** Seis chequeos de solo lectura que contrastan cada afirmación del manual contra lo que hay en disco. Escribe un reporte; no cambia nada. |
| `/blueprint` | **¿Está bien construido?** Puntúa el workspace sobre 100 en ruteo, precedencia, frescura y ciclo, y nombra los tres arreglos de mayor apalancamiento con el comando exacto de cada uno. |
| `/leverage` | **Extender, cada semana.** Encuentra la fricción, corta la parte que no debería existir, y construye la máquina más chica que resuelva lo que quedó. |
| `/skill-builder` | **Extender, cuando haga falta.** Convierte un proceso que repites a mano en una skill, con una entrevista de nueve bloques que pregunta antes de escribir. |

`/os-audit` y `/blueprint` miden cosas distintas y las dos importan. Un workspace puede sacar 95 en estructura y estar lleno de datos vencidos; puede estar perfectamente al día y sacar 40 porque no hay nada que lo sostenga. Corre ambas, una vez al mes.

---

## Qué NO es esto

- **No es un pack de prompts.** No hay prompts ingeniosos que pegar. La unidad de trabajo es dónde vive cada dato y quién es su dueño.
- **No es un framework de agentes.** Acá nada orquesta modelos, maneja estado ni envuelve una API. Es markdown que tu agente lee.
- **Sin suscripción, sin cuenta, sin telemetría.** Licencia MIT. Fork, renómbralo, cobra por lo que construyas encima.
- **Sin dependencias y sin build.** Archivos markdown más un script POSIX que corre en macOS y en Linux sin tocarlo. Pesa menos de un megabyte: se clona al instante y se lee desde el celular.
- **No es una base de conocimiento que llenas y olvidas.** El ciclo es el producto. Sin él, los otros tres mecanismos son ciertos el primer día y silenciosamente falsos a los sesenta.

Hecho para Claude Code, y portable en principio a cualquier agente que lea un manual de proyecto desde la raíz del repositorio.

---

## Más

- [Cómo funciona](docs/how-it-works.es.md) — el ensayo: qué se rompe sin cada mecanismo, y cuánto cuesta mantener cada uno.
- [Créditos](docs/credits.md) — ideas que dieron forma a este kit y que no nacieron acá.
- [Read this in English](README.md)
- Autor: **Enzo Sacin Ruiz** — [LinkedIn](https://www.linkedin.com/in/enzosacin/)

MIT. Issues y pull requests bienvenidos.
