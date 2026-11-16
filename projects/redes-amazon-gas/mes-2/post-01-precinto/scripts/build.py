"""Genera index.html del post 1 del mes 2 (precinto) a partir de la alineación de la voz de Terry.

Gancho con la entrega en la puerta ("¿Cómo sabes que tu balón es Amazon Gas?"), primer plano del precinto,
planta real con los dos checks (amarillo, dice Amazon Gas), las tres señales de alerta (no es amarillo, no
dice Amazon Gas, viene roto), "No lo recibas" y cierre con el WhatsApp. Mismo lenguaje visual que el post 11.

⚠️ BORRADOR: los primeros planos del precinto (b-precinto, c-revisa) son IA y llevan la marca "TOMA
TEMPORAL". Antes de publicar se reemplazan por la grabación real del precinto (cambiar SRC_PRECINTO /
SRC_REVISA y poner TEMPORAL = False).

Uso: python3 scripts/build.py         → index.html (9:16, TikTok)
     python3 scripts/build.py 4x5     → ../post-01-precinto-4x5/index.html (1080x1350, feed de FB e IG)
"""
import json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VO = 0.30
TEMPORAL = False
SRC_ENTREGA = "assets/img/balones-marca-grupo-v2.jpg"   # foto real: balones con la marca
SRC_PRECINTO = "assets/img/precinto-1.jpg"   # foto real del precinto (image copy 8), centrado; ver scripts/precintos.py
SRC_REVISA = "assets/clips/c-revisa.mp4"
SRC_FIJO = "assets/img/precinto-3.jpg"       # foto real del precinto (image copy 7)

F45 = len(sys.argv) > 1 and sys.argv[1] == "4x5"
H = 1350 if F45 else 1920
L = dict(card_top=130, cap_top=880, md=104, big=130, logo=200, end_q=72, wa_mt=30, wa_num=104, wa_ico=100,
         handle_mt=34, chk=56, chk_top=360, no_size=170, prod_h=860, prod_r=30, prod_b=50, ok_top=990) if F45 else \
    dict(card_top=290, cap_top=1220, md=124, big=160, logo=300, end_q=96, wa_mt=56, wa_num=120, wa_ico=118,
         handle_mt=60, chk=64, chk_top=560, no_size=220, prod_h=1180, prod_r=20, prod_b=110, ok_top=1400)
OUT = ROOT.parent / "post-01-precinto-4x5" if F45 else ROOT
if F45:
    OUT.mkdir(exist_ok=True)
    for f in ("hyperframes.json", "package.json"):
        shutil.copyfile(ROOT / f, OUT / f)
    shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)

a = json.loads((ROOT / "assets/audio/voz-alignment.json").read_text())
words, cur, st, en = [], "", None, None
for ch, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
    if ch == " ":
        if cur:
            words.append([cur, st + VO, en + VO])
        cur = ""
        continue
    if not cur:
        st = s
    cur += ch
    en = e
if cur:
    words.append([cur, st + VO, en + VO])
VOZ_DUR = round(words[-1][2] - VO, 2)
W = [w[0] for w in words]


def t(word, nth=0):
    """Inicio de la palabra (la n-ésima vez que aparece)."""
    idx = [i for i, x in enumerate(W) if x == word][nth]
    return round(words[idx][1], 2)


T_MIRALO, T_TODOS = t("fíjate"), t("Todos")
T_AMARILLO1, T_NOMBRE = t("amarillo"), t("nombre")
T_SI, T_AMARILLO2, T_DICE, T_ROTO, T_ESE = t("Si"), t("amarillo,"), t("dice"), t("roto,"), t("ese")
T_NO = t("Te")   # "Te recomendamos no recibirlo" (en pantalla sigue "No lo recibas")
END = round(t("Si", 1) - 0.1, 2)   # "Si tienes dudas…"
TOTAL = round(words[-1][2] + 2.6, 1)
MUS = min(TOTAL, 30.0)

# Subtítulos: grupos de hasta 3 palabras / 16 caracteres, cortando en puntuación; solo antes del cierre.
groups, g = [], []
for w in words:
    if w[1] >= T_NO - 0.05:   # "No lo recibas" ya va como titular grande
        break
    g.append(w)
    txt = " ".join(x[0] for x in g)
    if w[0][-1] in ".,:?" or len(g) >= 3 or len(txt) >= 16:
        groups.append(g)
        g = []
if g:
    groups.append(g)

caps_html, caps_js = [], []
for i, g in enumerate(groups):
    start = g[0][1]
    nxt = groups[i + 1][0][1] if i + 1 < len(groups) else T_NO
    dur = round(min(nxt, T_NO) - start, 2)
    spans = " ".join(f'<span class="w" id="w{i}_{j}">{w[0]}</span>' for j, w in enumerate(g))
    caps_html.append(f'      <div id="cap{i}" class="clip cap" data-start="{start:.2f}" data-duration="{dur:.2f}" '
                     f'data-track-index="4"><div class="cap-in">{spans}</div></div>')
    caps_js.append(f'      tl.fromTo("#cap{i} .cap-in", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {start:.2f});')
    for j, w in enumerate(g):
        caps_js.append(f'      tl.fromTo("#w{i}_{j}", {{ color: "#fbf8f3" }}, {{ color: "#f5dc17", duration: 0.06 }}, {w[1]:.2f});')


def span(a_, b_):
    """Toma de a_ a b_, con 0.25 s extra para el fundido con la siguiente."""
    return (round(a_, 2), round(b_ + 0.25 - a_, 2))


S1 = span(0.0, T_MIRALO)                 # foto real: balones con la marca (gancho)
S2 = span(T_MIRALO - 0.15, T_TODOS)      # foto real: precinto amarillo
T_CON = t("con")
S3 = span(T_TODOS - 0.15, T_CON)         # foto real: balones en planta con los trabajadores (paneo)
S3B = span(T_CON - 0.15, T_SI)          # foto real: precinto de cerca (image copy 9), con los checks debajo
S4 = span(T_SI - 0.15, T_NO)             # foto real: balón Amazon Gas de estudio sobre fondo de marca
S5 = span(T_NO - 0.15, END + 0.15)       # fijo del precinto, oscurecido, con "No lo recibas"

WIDE_W = round(H * 1600 / 900)


def wide_x(cx):
    """Desplazamiento para centrar cx (0–1) de la foto ancha, sin salirse de sus bordes."""
    return max(min(round(-(cx * WIDE_W - 540)), 0), 1080 - WIDE_W)


TAG = "TOMA TEMPORAL (IA) · reemplazar por precinto real"
temp_tag = (f'<div id="temp2" class="clip temp" data-start="{S5[0]}" data-duration="{round(END - S5[0], 2)}" data-track-index="7">{TAG}</div>'
            ) if TEMPORAL else ""

html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Barlow Condensed"; font-weight: 600; src: url("assets/fonts/BarlowCondensed-SemiBold.ttf") format("truetype"); }}
      @font-face {{ font-family: "Barlow Condensed"; font-weight: 700; src: url("assets/fonts/BarlowCondensed-Bold.ttf") format("truetype"); }}
      @font-face {{ font-family: "Barlow Condensed"; font-weight: 800; src: url("assets/fonts/BarlowCondensed-ExtraBold.ttf") format("truetype"); }}
      @font-face {{ font-family: "Inter"; font-weight: 100 900; src: url("assets/fonts/Inter.ttf") format("truetype"); }}

      :root {{
        --granate: #8e4149;
        --granate-oscuro: #6e2f35;
        --marron: #1b1512;
        --crema: #fbf8f3;
        --arena: #c9bdb0;
        --llama: #f5dc17;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: {H}px; overflow: hidden; background: var(--marron); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Inter", sans-serif; }}

      .shot-wrap {{ position: absolute; inset: 0; overflow: hidden; }}
      video.shot, img.shot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      img.wide {{ position: absolute; top: 0; left: 0; height: 100%; width: {WIDE_W}px; max-width: none; }}

      .prod-bg {{ background: radial-gradient(ellipse 70% 55% at 72% 62%, #8e4149 0%, #6e2f35 38%, #1b1512 100%); }}
      img.prod {{ position: absolute; right: {L["prod_r"]}px; bottom: {L["prod_b"]}px; height: {L["prod_h"]}px; width: auto; max-width: none; }}
      #ok {{ top: {L["ok_top"]}px; }}  /* checks bajo el precinto, para no taparlo */
      #veil {{
        position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(27,21,18,0.72) 0%, rgba(27,21,18,0.15) 38%, rgba(27,21,18,0.05) 55%, rgba(27,21,18,0.66) 100%);
      }}
      #dim {{ position: absolute; inset: 0; background: rgba(27,21,18,0.62); }}

      .card {{ position: absolute; left: 80px; right: 140px; top: {L["card_top"]}px; }}
      .kicker {{
        display: inline-block; font-family: "Barlow Condensed", sans-serif; font-weight: 700;
        font-size: 44px; letter-spacing: 0.08em; text-transform: uppercase;
        color: var(--crema); background: var(--granate); padding: 8px 22px 6px;
      }}
      .headline {{
        font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase;
        color: var(--crema); font-size: {L["big"]}px; line-height: 0.9; letter-spacing: -0.01em;
        text-shadow: 0 4px 24px rgba(27,21,18,0.6); margin-top: 18px;
      }}
      .headline.md {{ font-size: {L["md"]}px; }}
      .headline em {{ font-style: normal; color: var(--llama); }}
      .headline.box {{ display: inline; background: var(--granate); padding: 4px 22px 0; text-shadow: none;
        -webkit-box-decoration-break: clone; box-decoration-break: clone; line-height: 1.08; }}
      .bar {{ display: block; width: 140px; height: 12px; background: var(--granate); margin-top: 26px; }}

      /* Checks: lo correcto (✓ crema) y las alertas (✗ marrón sobre amarillo llama) */
      .checks {{ position: absolute; left: 80px; top: {L["chk_top"]}px; display: flex; flex-direction: column; align-items: flex-start; gap: 16px; }}
      .chk {{ display: inline-flex; align-items: center; gap: 18px; font-family: "Barlow Condensed", sans-serif; font-weight: 800;
        font-size: {L["chk"]}px; line-height: 1; text-transform: uppercase; color: var(--marron); background: var(--crema); padding: 10px 26px 6px 16px; }}
      .chk.bad {{ background: var(--llama); }}
      .tick {{ display: inline-flex; align-items: center; justify-content: center; width: 54px; height: 54px; border-radius: 50%;
        background: var(--granate); color: var(--crema); font-size: 40px; }}
      .chk.bad .tick {{ background: var(--marron); color: var(--llama); }}

      /* No lo recibas */
      #nolo {{ position: absolute; left: 80px; right: 80px; top: 0; bottom: 0; display: flex; flex-direction: column; justify-content: center; }}
      #nolo .big {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase; font-size: {L["no_size"]}px;
        line-height: 0.86; color: var(--crema); }}
      #nolo .big em {{ font-style: normal; color: var(--llama); }}

      .temp {{ position: absolute; left: 50%; transform: translateX(-50%); bottom: 40px; font-family: "Inter", sans-serif; font-weight: 700;
        font-size: 30px; color: #ffffff; background: rgba(200,30,30,0.85); padding: 10px 22px; border-radius: 8px; white-space: nowrap; }}

      .cap {{ position: absolute; left: 70px; right: 150px; top: {L["cap_top"]}px; }}
      .cap-in {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 84px; line-height: 1.02;
        text-transform: uppercase; color: var(--crema); text-align: left;
        text-shadow: 0 3px 0 rgba(27,21,18,0.9), 0 0 22px rgba(27,21,18,0.85); }}
      .cap-in .w {{ display: inline-block; }}

      #end {{ position: absolute; inset: 0; background: var(--crema); display: flex; flex-direction: column; align-items: center; justify-content: center; }}
      #end-logo {{ width: {L["logo"]}px; height: auto; display: block; }}
      #end-q {{ margin-top: 40px; font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: {L["end_q"]}px; line-height: 0.95;
        text-transform: uppercase; color: var(--marron); text-align: center; max-width: 900px; }}
      #end-q em {{ font-style: normal; color: var(--granate); }}
      #end-wa {{ margin-top: {L["wa_mt"]}px; display: flex; flex-direction: column; align-items: center; }}
      #end-wa .wa-lbl {{ font-weight: 700; font-size: 42px; color: var(--marron); letter-spacing: 0.01em; text-align: center; }}
      #end-wa .wa-row {{ margin-top: 18px; display: flex; align-items: center; gap: 26px; background: #ffffff;
        border: 5px solid #25D366; border-radius: 999px; padding: 18px 48px 18px 30px; }}
      #end-wa .wa-ico {{ width: {L["wa_ico"]}px; height: {L["wa_ico"]}px; display: block; }}
      #end-wa .wa-num {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: {L["wa_num"]}px; line-height: 1;
        color: #000000; letter-spacing: 0.01em; }}
      #end-handle {{
        margin-top: {L["handle_mt"]}px; font-family: "Barlow Condensed", sans-serif; font-weight: 700; font-size: 44px;
        color: var(--crema); background: var(--granate); padding: 10px 28px 8px;
      }}
      #end-rule {{ position: absolute; left: 0; right: 0; bottom: 0; height: 22px; background: var(--granate); }}
      #end-wave {{ position: absolute; left: 0; right: 0; top: 0; height: 22px; background: var(--granate); }}
    </style>
  </head>
  <body>
    <!-- Generado por scripts/build.py. Entrega, precinto y revisión: kie.ai (Nano Banana 2 + Kling 2.1).
         Planta: dos fotos reales de balones en planta (paneo y zoom), sin IA. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="{H}">
      <div id="s1-vis" class="shot-wrap"><img id="s1" class="clip wide" src="{SRC_ENTREGA}" data-start="{S1[0]}" data-duration="{S1[1]}" data-track-index="0" alt="" /></div>
      <div id="s2-vis" class="shot-wrap"><img id="s2" class="clip shot" src="{SRC_PRECINTO}" data-start="{S2[0]}" data-duration="{S2[1]}" data-track-index="1" alt="" /></div>
      <div id="s3-vis" class="shot-wrap"><img id="s3" class="clip wide" src="assets/img/planta-balones-wide.jpg" data-start="{S3[0]}" data-duration="{S3[1]}" data-track-index="0" alt="" /></div>
      <div id="s3b-vis" class="shot-wrap"><img id="s3b" class="clip shot" src="assets/img/precinto-2.jpg" data-start="{S3B[0]}" data-duration="{S3B[1]}" data-track-index="8" alt="" /></div>
      <div id="s4-vis" class="shot-wrap prod-bg"><img id="s4" class="clip prod" src="assets/img/balon-producto.png" data-start="{S4[0]}" data-duration="{S4[1]}" data-track-index="1" alt="" /></div>
      <div id="s5-vis" class="shot-wrap"><img id="s5" class="clip shot" src="{SRC_FIJO}" data-start="{S5[0]}" data-duration="{S5[1]}" data-track-index="0" alt="" /></div>

      <div id="veil" class="clip" data-start="0" data-duration="{round(T_NO, 2)}" data-track-index="2"></div>
      <div id="dim" class="clip" data-start="{S5[0]}" data-duration="{S5[1]}" data-track-index="2"></div>

      <div id="t1" class="clip card" data-start="0.1" data-duration="{round(T_MIRALO - 0.1, 2)}" data-track-index="3">
        <div class="t1-in">
          <span class="kicker">Balón seguro</span>
          <div class="headline md">¿Tu balón es <em>Amazon Gas</em>?</div>
        </div>
      </div>

      <div id="t2" class="clip card" data-start="{T_MIRALO}" data-duration="{round(T_TODOS - T_MIRALO, 2)}" data-track-index="3">
        <div class="t2-in">
          <span class="kicker">Míralo en</span>
          <div class="headline">el <em>precinto</em></div>
        </div>
      </div>

      <div id="t3" class="clip card" data-start="{T_TODOS}" data-duration="{round(T_SI - T_TODOS, 2)}" data-track-index="3">
        <div class="t3-in">
          <span class="kicker">Así sale de planta</span>
        </div>
      </div>
      <div id="ok" class="clip checks" data-start="{T_AMARILLO1}" data-duration="{round(T_SI - T_AMARILLO1, 2)}" data-track-index="5">
        <div class="chk c1"><span class="tick">✓</span>Amarillo</div>
        <div class="chk c2"><span class="tick">✓</span>Dice Amazon Gas</div>
        <div class="chk c3"><span class="tick">✓</span>Sin romper</div>
      </div>

      <div id="t4" class="clip card" data-start="{T_SI}" data-duration="{round(T_NO - T_SI, 2)}" data-track-index="3">
        <div class="t4-in">
          <div class="headline md box">Si ves <em>esto</em></div>
        </div>
      </div>
      <div id="bad" class="clip checks" data-start="{T_AMARILLO2}" data-duration="{round(T_NO - T_AMARILLO2, 2)}" data-track-index="5">
        <div class="chk bad c1"><span class="tick">✗</span>No es amarillo</div>
        <div class="chk bad c2"><span class="tick">✗</span>No dice Amazon Gas</div>
        <div class="chk bad c3"><span class="tick">✗</span>Viene roto</div>
      </div>

      <div id="nolo" class="clip" data-start="{T_NO}" data-duration="{round(END - T_NO, 2)}" data-track-index="3">
        <div class="big">No lo<br /><em>recibas</em></div>
        <span class="bar"></span>
      </div>

      {temp_tag}

{chr(10).join(caps_html)}

      <div id="end" class="clip" data-start="{END}" data-duration="{round(TOTAL - END, 2)}" data-track-index="6">
        <div id="end-wave"></div>
        <img id="end-logo" src="assets/img/logo.png" alt="Amazon Gas" />
        <div id="end-q">¿Dudas con <em>tu balón</em>?</div>
        <div id="end-wa">
          <div class="wa-lbl">Mándanos una foto del precinto</div>
          <div class="wa-row"><img class="wa-ico" src="assets/img/whatsapp.svg" alt="WhatsApp" /><span class="wa-num">991 511 401</span></div>
        </div>
        <div id="end-handle">@amazongasperu</div>
        <div id="end-rule"></div>
      </div>

      <audio id="musica" src="assets/audio/musica.mp3" data-start="0" data-duration="{MUS}" data-track-index="11" data-volume="0.45"
        data-automation='{{"version":1,"lanes":[{{"target":"volume","points":[{{"t":0,"v":0}},{{"t":0.5,"v":1}},{{"t":{round(MUS - 1.8, 2)},"v":1}},{{"t":{MUS},"v":0}}]}}]}}' data-fx-carve="{{&quot;enabled&quot;:true,&quot;sources&quot;:[&quot;voz&quot;],&quot;strength&quot;:0.8}}"></audio>
      <audio id="voz" src="assets/audio/voz.mp3" data-start="{VO}" data-duration="{VOZ_DUR}" data-track-index="10" data-volume="1"></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const E = "power3.out";

      // Gancho
      tl.fromTo("#t1 .kicker", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: E }}, 0.1);
      tl.fromTo("#t1 .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, 0.2);
      tl.to("#t1 .t1-in", {{ opacity: 0, duration: 0.2 }}, {round(T_MIRALO - 0.2, 2)});

      // Míralo en el precinto
      tl.fromTo("#t2 .kicker", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: E }}, {T_MIRALO});
      tl.fromTo("#t2 .headline", {{ opacity: 0, y: 60, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }}, {round(T_MIRALO + 0.35, 2)});
      tl.to("#t2 .t2-in", {{ opacity: 0, duration: 0.2 }}, {round(T_TODOS - 0.2, 2)});

      // Así sale de planta: amarillo, dice Amazon Gas, sin romper
      tl.fromTo("#t3 .kicker", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: E }}, {T_TODOS});
      tl.fromTo("#ok .c1", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_AMARILLO1});
      tl.fromTo("#ok .c2", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_NOMBRE});
      tl.fromTo("#ok .c3", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {round(T_NOMBRE + 0.6, 2)});
      tl.to(["#t3 .t3-in", "#ok"], {{ opacity: 0, duration: 0.2 }}, {round(T_SI - 0.2, 2)});
      tl.fromTo("#s3", {{ x: {wide_x(0.45)}, scale: 1.0 }}, {{ x: {wide_x(0.9)}, scale: 1.0, duration: {S3[1]}, ease: "sine.inOut" }}, {S3[0]});
      tl.fromTo("#s3b", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {S3B[1]}, ease: "none", transformOrigin: "50% 50%" }}, {S3B[0]});
      // Velo más suave en la toma 1 (con el velo completo la foto se veía opaca); vuelve al 100 % en la toma 2.
      tl.fromTo("#veil", {{ opacity: 0.45 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S2[0]});
      tl.fromTo("#s1", {{ x: {wide_x(0.4)}, scale: 1.0 }}, {{ x: {wide_x(0.58)}, scale: 1.0, duration: {S1[1]}, ease: "sine.inOut" }}, {S1[0]});
      tl.fromTo("#s2", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {S2[1]}, ease: "none", transformOrigin: "50% 45%" }}, {S2[0]});

      // Si ves esto: las tres alertas
      tl.fromTo("#t4 .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {T_SI});
      tl.fromTo("#bad .c1", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_AMARILLO2});
      tl.fromTo("#bad .c2", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_DICE});
      tl.fromTo("#bad .c3", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_ROTO});
      tl.fromTo("#s4", {{ x: 120, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: E }}, {S4[0]});
      tl.fromTo("#s4", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {S4[1]}, ease: "none", transformOrigin: "50% 10%" }}, {S4[0]});

      // No lo recibas
      tl.fromTo("#nolo .big", {{ opacity: 0, scale: 1.15 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: E, transformOrigin: "0% 50%" }}, {T_NO});
      tl.fromTo("#nolo .bar", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.35, ease: E }}, {round(T_NO + 0.3, 2)});
      tl.fromTo("#s5", {{ scale: 1.15 }}, {{ scale: 1.25, duration: {S5[1]}, ease: "none", transformOrigin: "50% 40%" }}, {S5[0]});

      // Fundidos entre tomas
      tl.fromTo("#s2-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S2[0]});
      tl.fromTo("#s3-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S3[0]});
      tl.fromTo("#s3b-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S3B[0]});
      tl.fromTo("#s4-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S4[0]});
      tl.fromTo("#s5-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.inOut" }}, {S5[0]});

      // Cierre
      tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {END});
      tl.fromTo("#end-logo", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, {round(END + 0.05, 2)});
      tl.fromTo("#end-wave", {{ scaleX: 0, transformOrigin: "100% 50%" }}, {{ scaleX: 1, duration: 0.8, ease: E }}, {round(END + 0.2, 2)});
      tl.fromTo("#end-rule", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.8, ease: E }}, {round(END + 0.2, 2)});
      tl.fromTo("#end-q", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {round(END + 0.2, 2)});
      tl.fromTo("#end-wa", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {round(t("mándanos") - 0.1, 2)});
      tl.fromTo("#end-wa .wa-ico", {{ scale: 0.6 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {round(t("WhatsApp."), 2)});
      tl.fromTo("#end-handle", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, {round(words[-1][2] + 0.3, 2)});

      // Subtítulos: la palabra que se dice se enciende en amarillo llama
{chr(10).join(caps_js)}

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
(OUT / "index.html").write_text(html)
print("ok", OUT.name, {"S1": S1, "S2": S2, "S3": S3, "S4": S4, "S5": S5, "END": END, "TOTAL": TOTAL,
                       "groups": len(groups), "voz": VOZ_DUR})
