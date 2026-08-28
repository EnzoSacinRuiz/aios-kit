# Cómo funciona

Un agente con buena memoria y mal archivo se comporta exactamente igual que un agente sin
memoria. Busca, no encuentra nada y te dice que eso no existe — mientras el archivo está tres
carpetas más allá, escrito por ti, hace seis semanas.

Este kit son cuatro mecanismos que hacen que esa falla sea rara, y un ciclo que la caza cuando
ocurre igual.

| Mecanismo | Qué es |
|---|---|
| **Precedencia** (Precedence) | Un dato vive en un solo lugar; todo lo demás apunta ahí. |
| **Ruteo** (Routing) | Una tabla de qué guarda cada carpeta y cuándo ir ahí. |
| **Protocolo de falla** (Failure protocol) | Cuando el agente no encuentra algo que sí existe, se nombra el modo de falla y se arregla la causa, no el síntoma. |
| **Ciclo de mantenimiento** (Maintenance loop) | El sistema se audita y se repara solo, o se pudre. |

Cada sección responde tres preguntas en el mismo orden: qué se rompe sin el mecanismo, qué es
el mecanismo, y cuánto cuesta mantenerlo. La tercera es la que casi ningún kit de contexto
contesta. Todo lo de acá tiene una factura de mantenimiento, y conviene verla antes de decidir
si adoptas algo de esto.

---

## 1. Precedencia

### Qué se rompe sin esto

Escribes la meta del trimestre en `context/priorities.md`. Dos semanas después estás armando
el brief de un proyecto y vuelves a tipear el número, porque tipearlo es más rápido que abrir
el archivo. Ahora existe dos veces.

La copia es correcta el día que la pegas y falsa para siempre después. Nadie la actualiza,
porque nadie se acuerda de que está ahí. Dos meses más tarde se abre una sesión, lee la copia
y te dice algo falso con voz de certeza. No hay error. No se ve nada roto.

Multiplica eso por cada número, estado, fecha y headcount que alguna vez mencionaste dos
veces, y el workspace deja de ser fuente de verdad para convertirse en una pila de
afirmaciones de antigüedad desconocida.

### Qué es el mecanismo

`CLAUDE.md` abre con una tabla de precedencia. Cada fila nombra una clase de dato y el único
lugar que lo posee:

| Sobre… | El dueño |
|---|---|
| Metas del trimestre | `context/priorities.md` |
| Estado de tareas y proyectos | tu herramienta de tareas |
| Qué skills existen | el disco — `ls .claude/skills/` |
| Plata y runway | tu banco y tu contabilidad |
| Qué se decidió y por qué | `decisions/log.md` |

Todo lo que está fuera del dueño apunta hacia él y nunca lo repite. `context/work.md` no dice
cuál es la meta de propuestas del trimestre; dice que esa meta vive en
`context/priorities.md`. Ningún archivo enumera las skills, porque `ls .claude/skills/` no se
puede desactualizar.

La regla se generaliza más allá de la tabla: si te encuentras copiando un número o un estado a
un segundo archivo, no lo copies — escribe dónde vive.

### Qué te cuesta

- **Es más lento en el momento.** Pegar el número toma dos segundos. Abrir el archivo dueño,
  confirmar que sigue siendo el dueño y escribir un puntero toma treinta. Ese impuesto lo
  pagas cada vez, y el retorno llega meses después en forma de un error que no ocurrió.
- **Tienes que decidir un dueño antes de poder escribir.** Para una clase nueva de dato — quién
  posee los precios, quién posee el headcount — esa es una decisión real, y saltearla hace que
  el dato caiga en dos archivos por defecto.
- **La tabla necesita una fila por cada clase disputada.** Una tabla de precedencia con tres
  filas en un workspace con diez datos disputados es peor que ninguna, porque insinúa una
  cobertura que no tiene.
- **Los punteros se leen peor para un humano.** "Ver `context/priorities.md`" le sirve menos a
  una persona que hojea que el número directo. Estás cambiando comodidad humana por verdad
  para la máquina. El canje es el correcto, y sigue siendo un canje.

---

## 2. Ruteo

### Qué se rompe sin esto

El agente necesita la nota que escribiste sobre cómo negocia un cliente. Busca en `projects/`.
Busca en `reports/`. No busca en `knowledge/external/`, porque nada le dijo que esa carpeta
guarda inteligencia de cuentas. Responde que esa nota no existe.

Le pegas la ruta. El trabajo sigue. La semana que viene pasa otra vez con otro archivo.

Un workspace sin mapa no es buscable, es adivinable — y el agente adivina con los nombres de
carpeta que tú elegiste, que significan algo para ti y nada para él.

### Qué es el mecanismo

Una sola tabla en `CLAUDE.md`, con una fila por carpeta de primer nivel y tres columnas: la
carpeta, qué guarda, y **cuándo ir ahí**.

La tercera columna es la que hace el trabajo. "Entregables, no contexto" describe `projects/`.
"Un pedazo específico de trabajo de cliente o de proyecto — ve al proyecto puntual, nunca
cargues la carpeta entera" le dice al agente cuándo abrirla y cuándo no meterse. El mapa está indexado por la
pregunta que se hace, no por el contenido de la carpeta.

Tres propiedades lo mantienen honesto:

- **Cubre todas las carpetas de primer nivel.** Incluida `.claude/`. La única excepción
  deliberada es `.git/`, y el mapa lo dice explícitamente, para que la auditoría no la marque
  todos los meses.
- **Las wikis llevan su propio índice.** `knowledge/external/` y `knowledge/playbook/` tienen
  cada una un `index.md` que lista todos sus nodos, y un `CLAUDE.md` de carpeta con el formato
  de nodo. Un nodo que no está en el índice es invisible para cualquiera que siga el grafo,
  aunque el archivo esté ahí.
- **Lleva una fecha de `Last verified`.** Que significa algo solo si la mueves cuando
  verificaste, y nunca en otro caso.

### Qué te cuesta

- **La tabla se actualiza en el mismo commit que la carpeta.** No el mismo día, no la misma
  semana — el mismo commit. Una carpeta creada un martes y mapeada un viernes es inencontrable
  durante tres días, y la costumbre de postergarlo es como mueren los mapas.
- **Renombrar ahora toca dos archivos.** Mover `reports/` a `output/` implica editar el mapa, y
  probablemente una o dos skills que escriben ahí.
- **Tienes que resistir la tentación de engordarlo.** Cada búsqueda fallida da ganas de agregar
  una fila. Un mapa de cuarenta filas no es más preciso que uno de doce; es un mapa que nadie
  lee. Cuando un archivo está en un lugar que el manual no describe, mover el archivo suele
  salir más barato que agregarle una fila.
- **La fecha de `Last verified` es una promesa que hay que cumplir.** Moverla en una pasada que
  no verificó nada convierte al mapa entero en una afirmación sin evidencia detrás.

---

## 3. Protocolo de falla

### Qué se rompe sin esto

Este es el intercambio que destruye sistemas de contexto en silencio:

> **Agente:** No encontré nada sobre eso.
> **Tú:** Está ahí — `knowledge/playbook/hold-the-fee-negotiate-scope.md`.
> **Agente:** Tienes razón, disculpa. Lo leo ahora.

El trabajo sigue. Nada del sistema cambió, así que la misma falla se repite la semana que
viene, y la siguiente. La disculpa es el problema: se siente como una resolución y no repara
nada.

En unos meses aprendes a no confiar en que el agente encuentre las cosas y empiezas a pegar
rutas a mano. En ese punto el índice eres tú, y el workspace es decoración.

### Qué es el mecanismo

Una falla confirmada dispara un procedimiento fijo de cuatro pasos, que `/route-fix` recorre:

1. **Traza, no te disculpes.** Cada ruta leída, en orden, incluidas las que no devolvieron
   nada. Cada búsqueda corrida y qué matcheó. Qué fila del mapa de ruteo mandó al agente al
   lugar equivocado, citada. Y después una pregunta contestada por escrito: ¿por qué el mapa
   apuntaba lejos del archivo?
2. **Nombra el modo de falla.** Exactamente uno de cuatro. Nunca dos, nunca uno nuevo.
3. **Arregla la causa, según el modo.** Una falla de `confusion` no se arregla nunca podando un
   archivo.
4. **Muestra el diff y detente.** No se escribe nada sin aprobación, y el arreglo tiene que
   señalar la línea que evita que esta falla específica vuelva a pasar. Si no puedes trazar esa
   línea, el arreglo es decorativo.

### Los cuatro modos de falla

Siempre estos cuatro, siempre en minúscula, siempre en este orden.

**`poisoning`** — un archivo precargado o indexado afirma algo falso o vencido, y el agente le
creyó. *Ejemplo:* `context/team.md` todavía lista a alguien que se fue en junio. Todas las
sesiones del trimestre planificaron trabajo alrededor de una persona que no está, y ninguna
sesión tenía cómo saberlo.

**`bloat`** — la respuesta estaba en un archivo que el agente abrió, enterrada bajo demasiado.
*Ejemplo:* se pegó una transcripción de cuatro mil palabras entera en un archivo de
conocimiento. La única decisión que importaba está en la página tres. El agente leyó el
archivo, no vio la línea, y la mayoría de las sesiones directamente no lo abren porque cuesta
demasiado.

**`confusion`** — el mapa de ruteo calla, o apunta a algo irrelevante, así que el archivo
correcto nunca se abrió. *Ejemplo:* agregaste una carpeta `assets/` y nunca agregaste su fila.
El agente no tiene motivo para creer que existe, y no mira.

**`clash`** — dos archivos se contradicen y el agente le creyó al equivocado. *Ejemplo:* la
meta del trimestre es `6 propuestas por mes` en `context/priorities.md` y `10 por mes` en el
README de un proyecto escrito antes de que la meta se revisara. Los dos están precargados. El
agente elige uno.

La distinción que más importa en la práctica es `bloat` contra `confusion`: bloat es un archivo
demasiado gordo para leer, confusion es un mapa que nunca nombró el archivo. Cuando las dos
son ciertas, el modo es la **primera** vuelta equivocada, no la última.

### Qué te cuesta

- **Interrumpe el trabajo que estabas haciendo.** La falla pasa en medio de una tarea. El
  protocolo dice detente, traza, diagnostica y propón — justo cuando menos ganas tienes.
  Correrlo más tarde no funciona: la traza depende de lo que el agente todavía recuerda haber
  leído.
- **Exige una pasada de aprobación cada vez.** El protocolo se niega a escribir sin
  supervisión, porque una reparación que edita mal el mapa es peor que la falla original.
- **Algunas fallas son del agente, y el resultado honesto es no editar nada.** Si el agente
  nunca consultó el mapa de ruteo, el mapa no está roto — el procedimiento se salteó. Editar
  el mapa para parecer diligente agrega filas que nadie necesita, y así es como un mapa se
  vuelve ilegible.
- **Algunas fallas son tuyas.** Nada rutea a un dato que nunca se escribió. Eso no es un
  defecto de ruteo; es material que falta, y le corresponde a `/distill`.

---

## 4. Ciclo de mantenimiento

### Qué se rompe sin esto

Todo lo anterior se degrada, en silencio, y nada de eso avisa que se está degradando.

La precedencia se degrada la primera vez que alguien pega un número en vez de un puntero. El
ruteo se degrada la primera vez que se crea una carpeta a las once de la noche. La capa
precargada se degrada de manera continua, porque los negocios cambian y los archivos no. Los
índices de las wikis se degradan cada vez que un nodo se escribe apurado.

Nada de eso tira un error. Un workspace degradándose se ve exactamente igual que uno sano
desde afuera — las mismas carpetas, los mismos archivos, las mismas respuestas seguras. El
único síntoma observable es que las respuestas se vuelven sutilmente incorrectas, que es
justo el síntoma que peor puedes detectar, porque la pregunta la hiciste tú.

### Qué es el mecanismo

Cuatro capas, corriendo en relojes distintos.

**Cada sesión — el hook.** `.claude/settings.json` engancha `SessionStart` a
`scripts/aios-freshness-check.sh`. Es `sh` POSIX, siempre sale con 0, y no imprime nada cuando
nada se movió. Chequea cinco cosas: `context/` sin tocar hace 60 días, ningún reporte de
auditoría en 30 días, material en `projects/` más nuevo que la última entrada de
`decisions/log.md`, el banner `🟡 DEMO` todavía sentado en `context/me.md`, y archivos
trackeados que parecen secretos. No arregla nada. El silencio es el estado de éxito, y eso es
lo que evita que se convierta en ruido que aprendes a scrollear.

El hook se eligió por encima de un cron a propósito: un hook vive en el repo y corre en esta
máquina, todas las sesiones, para siempre. Un cron de sesión muere cuando cierras la sesión.

**Mensual — las dos auditorías.** Hacen preguntas distintas y necesitas las dos.

- `/os-audit` pregunta *¿esto sigue siendo cierto?* Seis chequeos de solo lectura: integridad
  de rutas, verdad de los índices, frescura, duplicación y bloat, fallas silenciosas (secretos
  trackeados, skills cuya descripción nunca va a disparar, automatizaciones listadas pero no
  cableadas) y ubicación del contexto. Cada hallazgo se etiqueta con uno de los cuatro modos
  de falla. El único archivo que escribe es su propio reporte, que termina en una lista
  numerada de arreglos — por lotes, ordenada de más barato a más caro, y que nadie aplica
  hasta que tú la apruebas.
- `/blueprint` pregunta *¿está bien construido?* Puntúa cuatro ejes sobre 25 — ruteo,
  precedencia, frescura y ciclo — con valores en bandas, y la banda la fija el hallazgo más
  grave, nunca la cantidad de hallazgos. Nombra el hallazgo que fijó cada banda, así dos
  corridas con un mes de diferencia son comparables, y ordena los tres arreglos de mayor
  palanca: puntos recuperados sobre esfuerzo, cada uno con el comando exacto.

Un workspace puede sacar 95 en `/blueprint` y estar lleno de datos vencidos. Puede estar
perfectamente al día y sacar 40 porque nada lo sostiene. Las dos fallas son independientes.

**Al entrar material — `/distill`.** El material crudo se parte en vez de archivarse:
decisiones a `decisions/log.md`, hechos durables sobre el mundo externo a
`knowledge/external/`, método reutilizable a `knowledge/playbook/`, tareas a tu herramienta de
tareas, y todo lo demás se descarta en voz alta. Cada nodo de conocimiento es una afirmación,
no un tema, y el `index.md` de la carpeta se actualiza en la misma pasada. Las contradicciones
con nodos existentes se levantan en vez de pisarse, porque pisar en silencio destruye la
versión que era correcta sin dejar rastro de que alguna vez hubo una duda.

**Semanal — `/leverage`, y `/skill-builder` cuando hace falta.** `/leverage` encuentra una
fricción recurrente, corta la parte que no debería existir, y construye la máquina más chica
para lo que sobrevive — un checklist antes que un script, un script antes que una skill, una
skill antes que un agente programado. La corrida no termina hasta que existe en disco un
archivo que antes no existía. `/skill-builder` corre la entrevista de nueve bloques que
convierte un proceso repetido en una skill real, y si esa skill escribe en una carpeta de la
que el mapa de ruteo nunca oyó hablar, le agrega su fila de ruteo en la misma pasada — así la
carpeta nueva es encontrable desde que termina la sesión que la creó.

### Qué te cuesta

Este es el mecanismo caro, y el que la gente abandona sin decirlo.

- **Las auditorías rinden solo si alguien las corre.** El hook te va a avisar que hay una
  auditoría vencida. No la puede correr. Un mes de avisos vencidos que nadie atiende te
  entrena a ignorar el hook, y eso es peor que no haberlo instalado.
- **Una auditoría produce una lista de arreglos, no arreglos.** Las dos auditorías son de solo
  lectura a propósito — una auditoría que edita en silencio lo que mide nunca se puede volver
  a correr con honestidad. Eso implica una segunda sentada para aprobar y aplicar, y una lista
  de arreglos que nadie aplica es un documento sobre problemas que ahora sabes que tienes.
- **`/distill` es más lento que pegar.** Pegar una transcripción en un archivo es una tecla.
  Partirla en cuatro destinos — decisiones, hechos durables del mundo externo, tu propio
  método, tareas — chequear contradicciones y actualizar un índice son quince minutos. La décima vez, con una entrega encima, vas a querer pegar.
- **Un ritual semanal se va a caer.** `/leverage` está diseñada para sobrevivir eso — si no se
  repitió nada esta semana, te dice que registres el salto en vez de fabricar un candidato.
  Pero una skill que corre cuatro veces al año no es un ciclo.
- **Todo esto es disciplina, no automatización.** El kit automatiza la *detección*. No
  automatiza la *reparación*, y no lo va a hacer, porque un sistema que repara su propio
  contexto sin supervisión puede equivocarse con seguridad de una manera nueva cada sesión.

---

## Por qué el ciclo es lo que más importa

La precedencia, el ruteo y el protocolo de falla son mecanismos reales, y los tres se degradan.

La precedencia se degrada hacia números duplicados. El ruteo se degrada hacia filas que
apuntan a carpetas renombradas. El protocolo de falla se degrada hacia disculpas, porque solo
corre cuando alguien se acuerda de correrlo. Cada uno de los tres se deteriora sin producir un
error, sin una advertencia, y sin ninguna diferencia visible en cómo se ve el workspace.

El ciclo es el único mecanismo que se da cuenta. El hook se da cuenta de que hace un mes que
nadie audita. `/os-audit` se da cuenta de que una fila apunta a nada y de que dos archivos se
contradicen. `/blueprint` se da cuenta de que los mecanismos mismos nunca se terminaron de
construir. Sin ellos, los otros tres mecanismos son una buena idea que tuviste una vez.

Un workspace que nadie mantiene deja de ser cierto en unos sesenta días. No es un umbral duro,
es la vida media aproximada de un conjunto de datos sobre un negocio que sigue moviéndose — y
el peligro específico no es que el workspace quede vacío. Es que sigue lleno. Sigue
respondiendo. Suena exactamente igual de seguro con los datos vencidos que con los vigentes,
porque nada dentro de un archivo markdown lleva su propia fecha de vencimiento.

Un sistema que se equivoca con seguridad es peor que no tener sistema. Sin sistema, verificas.
Con uno equivocado, no.

El ciclo es lo que lo mantiene honesto.

---

**Sigue:** [`anatomy.md`](anatomy.md) — el árbol completo de carpetas, qué mecanismo sirve cada
una y qué skill escribe ahí.
