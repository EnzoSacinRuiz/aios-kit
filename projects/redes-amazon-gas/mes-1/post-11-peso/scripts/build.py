"""Genera index.html del post 11 (peso verificado) a partir de la alineación de la voz de Terry.

Abre en positivo ("Tu balón llega completo"), explica tara + 10 kg con un gráfico, muestra planta
(pesaje, precinto, etiqueta) y cierra con el WhatsApp y "peso exacto, peso verificado y precio justo" (frase pedida por Enzo el
2026-10-26; papá había dicho no tocar el precio, la revisa al aprobar). Mismo lenguaje visual que el post 7.
Imágenes y clips: kie.ai (Nano Banana 2 + Kling 2.1). El camión es la foto real con paneo: el clip de Kling
(assets/clips/d-camion.mp4) se descartó porque cambiaba el camión y borraba el letrero.
Uso: python3 scripts/build.py         → index.html (9:16, TikTok)
     python3 scripts/build.py 4x5     → ../post-11-peso-4x5/index.html (1080x1350, feed de FB e IG)
"""
import json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VO = 0.30

F45 = len(sys.argv) > 1 and sys.argv[1] == "4x5"
H = 1350 if F45 else 1920
L = dict(card_top=130, f_top=120, cap_top=880, sm=96, md=104, f_big=120, logo=200, end_num=88, end_tag=72, slogan_mt=40,
         wa_mt=30, wa_num=104, wa_ico=100, handle_mt=34) if F45 else \
    dict(card_top=290, f_top=280, cap_top=1220, sm=112, md=124, f_big=150, logo=300, end_num=120, end_tag=96, slogan_mt=70,
         wa_mt=56, wa_num=120, wa_ico=118, handle_mt=60)
OUT = ROOT.parent / "post-11-peso-4x5" if F45 else ROOT
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


T_CADA, T_TARA, T_DIEZ, T_MARCAR = t("Cada"), t("tara"), t("diez"), t("marcar")
T_EN, T_PESAMOS, T_PRECINTO, T_ETIQUETA = t("En"), t("pesamos"), t("precinto"), t("etiqueta")
T_PORQUE, T_PESALO = t("Porque"), t("Cuando")   # "Cuando te llegue, pésalo y revisa el precinto"
T_AMARILLO, T_NOMBRE, T_ROMPER = t("Amarillo,"), t("nombre"), t("sin")
END = round(t("Y", 1) - 0.1, 2)          # el cierre entra en "Y si no te cuadra…"
TOTAL = round(words[-1][2] + 2.6, 1)     # el contacto queda ~2,5 s después de la voz
MUS = min(TOTAL, 40.0)                   # la música dura 40 s: termina con fundido antes del final

# Subtítulos: grupos de hasta 3 palabras / 16 caracteres, cortando en puntuación; solo antes del cierre.
groups, g = [], []
for w in words:
    if w[1] >= END - 0.05:
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
    nxt = groups[i + 1][0][1] if i + 1 < len(groups) else END
    dur = round(min(nxt, END) - start, 2)
    spans = " ".join(f'<span class="w" id="w{i}_{j}">{w[0]}</span>' for j, w in enumerate(g))
    caps_html.append(f'      <div id="cap{i}" class="clip cap" data-start="{start:.2f}" data-duration="{dur:.2f}" '
                     f'data-track-index="4"><div class="cap-in">{spans}</div></div>')
    caps_js.append(f'      tl.fromTo("#cap{i} .cap-in", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {start:.2f});')
    for j, w in enumerate(g):
        caps_js.append(f'      tl.fromTo("#w{i}_{j}", {{ color: "#fbf8f3" }}, {{ color: "#f5dc17", duration: 0.06 }}, {w[1]:.2f});')


def span(a_, b_):
    """Toma de a_ a b_, con 0.4 s extra para el fundido con la siguiente."""
    return (round(a_, 2), round(b_ + 0.25 - a_, 2))


S1 = span(0.0, T_CADA)                       # clip: balón en la balanza (gancho)
S2 = span(T_CADA - 0.15, T_EN)               # foto de la balanza con zoom lento + gráfico tara + 10 kg
S3 = span(T_EN - 0.15, T_PRECINTO)           # clip: línea de llenado
S4 = span(T_PRECINTO - 0.15, T_PORQUE)       # clip: precinto
S5 = span(T_PORQUE - 0.15, T_PESALO)         # foto real del camión de reparto con paneo (el clip de Kling borraba la marca)
S6 = span(T_PESALO - 0.15, END + 0.15)       # vuelve el balón en la balanza

WIDE_W = round(H * 1600 / 900)   # ancho mostrado de la foto 16:9 a la altura del formato


def wide_x(cx):
    """Desplazamiento para centrar la fracción cx (0..1) de la foto en 1080 px."""
    return round(-(cx * WIDE_W - 540))


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

      #veil {{
        position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(27,21,18,0.72) 0%, rgba(27,21,18,0.15) 38%, rgba(27,21,18,0.05) 55%, rgba(27,21,18,0.66) 100%);
      }}

      .card {{ position: absolute; left: 80px; right: 140px; top: {L["card_top"]}px; }}
      .kicker {{
        display: inline-block; font-family: "Barlow Condensed", sans-serif; font-weight: 700;
        font-size: 44px; letter-spacing: 0.08em; text-transform: uppercase;
        color: var(--crema); background: var(--granate); padding: 8px 22px 6px;
      }}
      .headline {{
        font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase;
        color: var(--crema); font-size: 150px; line-height: 0.9; letter-spacing: -0.01em;
        text-shadow: 0 4px 24px rgba(27,21,18,0.6); margin-top: 18px;
      }}
      .headline.md {{ font-size: {L["md"]}px; }}
      .headline.sm {{ font-size: {L["sm"]}px; }}
      .headline em {{ font-style: normal; color: var(--llama); }}
      .headline.box {{ display: inline; background: var(--granate); padding: 4px 22px 0; text-shadow: none;
        -webkit-box-decoration-break: clone; box-decoration-break: clone; line-height: 1.08; }}
      .bar {{ display: block; width: 140px; height: 12px; background: var(--granate); margin-top: 26px; }}

      /* Fórmula del peso: tara + 10 kg = lo que marca la balanza */
      #formula {{ position: absolute; left: 80px; right: 80px; top: {L["f_top"]}px; }}
      #formula .row {{ display: flex; align-items: baseline; gap: 22px; margin-bottom: 14px; }}
      #formula .op {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: {L["f_big"]}px; line-height: 0.9;
        color: var(--llama); text-shadow: 0 4px 24px rgba(27,21,18,0.7); width: 90px; text-align: center; }}
      #formula .big {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: {L["f_big"]}px; line-height: 0.9;
        text-transform: uppercase; color: var(--crema); text-shadow: 0 4px 24px rgba(27,21,18,0.7); }}
      #formula .sub {{ font-family: "Barlow Condensed", sans-serif; font-weight: 700; font-size: 40px; letter-spacing: 0.04em;
        text-transform: uppercase; color: var(--crema); background: var(--granate); padding: 6px 16px 4px; align-self: center; }}
      #formula .res {{ display: inline-block; font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 64px;
        line-height: 1; text-transform: uppercase; color: var(--marron); background: var(--llama); padding: 10px 22px 6px; }}

      /* Checklist de planta */
      #checks, #checks2 {{ position: absolute; left: 80px; top: {L["card_top"] + (250 if not F45 else 210)}px; display: flex; flex-direction: column; gap: 16px; }}
      #checks2 {{ top: {L["card_top"] + (330 if not F45 else 280)}px; }}  /* el titular de t4 ocupa dos líneas */
      .chk {{ display: inline-flex; align-items: center; gap: 18px; font-family: "Barlow Condensed", sans-serif; font-weight: 800;
        font-size: 64px; line-height: 1; text-transform: uppercase; color: var(--marron); background: var(--crema); padding: 10px 26px 6px 16px; }}
      .tick {{ display: inline-flex; align-items: center; justify-content: center; width: 54px; height: 54px; border-radius: 50%;
        background: var(--granate); color: var(--crema); font-size: 40px; }}

      .cap {{ position: absolute; left: 70px; right: 150px; top: {L["cap_top"]}px; }}
      .cap-in {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 84px; line-height: 1.02;
        text-transform: uppercase; color: var(--crema); text-align: left;
        text-shadow: 0 3px 0 rgba(27,21,18,0.9), 0 0 22px rgba(27,21,18,0.85); }}
      .cap-in .w {{ display: inline-block; }}

      #end {{ position: absolute; inset: 0; background: var(--crema); display: flex; flex-direction: column; align-items: center; justify-content: center; }}
      #end-logo {{ width: {L["logo"]}px; height: auto; display: block; }}
      #end-num {{ margin-top: {L["slogan_mt"]}px; font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: {L["end_num"]}px; line-height: 0.9;
        text-transform: uppercase; color: var(--granate); text-align: center; }}
      #end-tag, .end-tag {{
        margin-top: 10px; font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase;
        font-size: {L["end_tag"]}px; line-height: 0.95; color: var(--marron); text-align: center; max-width: 900px;
      }}
      #end-tag em, .end-tag em {{ font-style: normal; color: var(--granate); }}
      /* Contacto: ícono oficial de WhatsApp (Simple Icons) y número grande en negro, igual que el post 7 */
      #end-wa {{ margin-top: {L["wa_mt"]}px; display: flex; flex-direction: column; align-items: center; }}
      #end-wa .wa-lbl {{ font-weight: 700; font-size: 42px; color: var(--marron); letter-spacing: 0.01em; }}
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
    <!-- Generado por scripts/build.py. Balanza, llenado y precinto: imágenes de kie.ai (Nano Banana 2) animadas con
         Kling 2.1, con el balón real de 10 kg como referencia. Camión: foto real con paneo, sin IA. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="{H}">
      <div id="s1-vis" class="shot-wrap"><video id="s1" class="clip shot" src="assets/clips/a-balanza.mp4" data-start="{S1[0]}" data-duration="{S1[1]}" data-media-start="0" data-track-index="0" muted playsinline></video></div>
      <div id="s2-vis" class="shot-wrap"><img id="s2" class="clip shot" src="assets/clips/a-balanza.png" data-start="{S2[0]}" data-duration="{S2[1]}" data-track-index="1" alt="" /></div>
      <div id="s3-vis" class="shot-wrap"><video id="s3" class="clip shot" src="assets/clips/c-llenado.mp4" data-start="{S3[0]}" data-duration="{S3[1]}" data-media-start="0" data-track-index="0" muted playsinline></video></div>
      <div id="s4-vis" class="shot-wrap"><video id="s4" class="clip shot" src="assets/clips/b-precinto.mp4" data-start="{S4[0]}" data-duration="{S4[1]}" data-media-start="0" data-track-index="1" muted playsinline></video></div>
      <div id="s5-vis" class="shot-wrap"><img id="s5" class="clip wide" src="assets/img/camion-real.webp" data-start="{S5[0]}" data-duration="{S5[1]}" data-track-index="0" alt="" /></div>
      <div id="s6-vis" class="shot-wrap"><video id="s6" class="clip shot" src="assets/clips/a-balanza.mp4" data-start="{S6[0]}" data-duration="{S6[1]}" data-media-start="0" data-track-index="1" muted playsinline></video></div>

      <div id="veil" class="clip" data-start="0" data-duration="{END + 0.4}" data-track-index="2"></div>

      <div id="t1" class="clip card" data-start="0.1" data-duration="{round(T_CADA - 0.1, 2)}" data-track-index="3">
        <div class="t1-in">
          <span class="kicker">Peso verificado</span>
          <div class="headline">Tu balón llega <em>completo</em></div>
        </div>
      </div>

      <div id="formula" class="clip" data-start="{T_CADA}" data-duration="{round(T_EN - T_CADA, 2)}" data-track-index="3">
        <div class="row r1"><span class="op"></span><span class="big">Tara</span><span class="sub">peso del balón vacío</span></div>
        <div class="row r2"><span class="op">+</span><span class="big">10 kg</span><span class="sub">de gas</span></div>
        <div class="row r3"><span class="op">=</span><span class="res">Lo que marca la balanza</span></div>
      </div>

      <div id="t2" class="clip card" data-start="{T_EN}" data-duration="{round(T_PORQUE - T_EN, 2)}" data-track-index="3">
        <div class="t2-in">
          <span class="kicker">En planta</span>
          <div class="headline md">Uno por <em>uno</em></div>
        </div>
      </div>
      <div id="checks" class="clip" data-start="{T_PESAMOS}" data-duration="{round(T_PORQUE - T_PESAMOS, 2)}" data-track-index="5">
        <div class="chk c1"><span class="tick">✓</span>Pesado</div>
        <div class="chk c2"><span class="tick">✓</span>Precinto</div>
        <div class="chk c3"><span class="tick">✓</span>Etiqueta</div>
      </div>

      <div id="t3" class="clip card" data-start="{T_PORQUE}" data-duration="{round(T_PESALO - T_PORQUE, 2)}" data-track-index="3">
        <div class="t3-in">
          <div class="headline md box">Peso <em>verificado</em></div>
          <span class="bar"></span>
        </div>
      </div>

      <div id="t4" class="clip card" data-start="{T_PESALO}" data-duration="{round(END - T_PESALO, 2)}" data-track-index="3">
        <div class="t4-in">
          <div class="headline md box">Pésalo y revisa <em>el precinto</em></div>
        </div>
      </div>
      <!-- Cómo es un precinto correcto (sin primer plano: no hay foto real del precinto) -->
      <div id="checks2" class="clip" data-start="{T_AMARILLO}" data-duration="{round(END - T_AMARILLO, 2)}" data-track-index="5">
        <div class="chk c1"><span class="tick">✓</span>Amarillo</div>
        <div class="chk c2"><span class="tick">✓</span>Con el nombre Amazon Gas</div>
        <div class="chk c3"><span class="tick">✓</span>Sin romper</div>
      </div>

{chr(10).join(caps_html)}

      <div id="end" class="clip" data-start="{END}" data-duration="{round(TOTAL - END, 2)}" data-track-index="6">
        <div id="end-wave"></div>
        <img id="end-logo" src="assets/img/logo.png" alt="Amazon Gas" />
        <div id="end-wa">
          <div class="wa-lbl">¿No te cuadra? Escríbenos</div>
          <div class="wa-row"><img class="wa-ico" src="assets/img/whatsapp.svg" alt="WhatsApp" /><span class="wa-num">991 511 401</span></div>
        </div>
        <!-- Frase final pedida por Enzo, después del WhatsApp -->
        <div id="end-num">Peso exacto,</div>
        <div id="end-tag">peso <em>verificado</em></div>
        <div id="end-tag2" class="end-tag">y precio <em>justo</em></div>
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

      // Gancho: Tu balón llega completo
      tl.fromTo("#t1 .kicker", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: E }}, 0.1);
      tl.fromTo("#t1 .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, 0.2);
      tl.to("#t1 .t1-in", {{ opacity: 0, duration: 0.2 }}, {round(T_CADA - 0.2, 2)});

      // Tara + 10 kg = lo que marca la balanza, cada parte cuando la voz la dice
      tl.fromTo("#formula .r1", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: E }}, {round(T_TARA - 0.1, 2)});
      tl.fromTo("#formula .r2", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: E }}, {round(T_DIEZ - 0.1, 2)});
      tl.fromTo("#formula .r3", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, {round(T_MARCAR - 0.1, 2)});
      tl.to("#formula", {{ opacity: 0, duration: 0.2 }}, {round(T_EN - 0.2, 2)});
      tl.fromTo("#s2", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {S2[1]}, ease: "none", transformOrigin: "40% 70%" }}, {S2[0]});

      // En planta, uno por uno: pesado, precinto, etiqueta
      tl.fromTo("#t2 .kicker", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: E }}, {T_EN});
      tl.fromTo("#t2 .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, {round(T_EN + 0.1, 2)});
      tl.fromTo("#checks .c1", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_PESAMOS});
      tl.fromTo("#checks .c2", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_PRECINTO});
      tl.fromTo("#checks .c3", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_ETIQUETA});
      tl.to(["#t2 .t2-in", "#checks"], {{ opacity: 0, duration: 0.2 }}, {round(T_PORQUE - 0.2, 2)});

      // Peso verificado
      tl.fromTo("#t3 .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {T_PORQUE});
      tl.fromTo("#t3 .bar", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.35, ease: E }}, {round(T_PORQUE + 0.3, 2)});
      tl.to("#t3 .t3-in", {{ opacity: 0, duration: 0.2 }}, {round(T_PESALO - 0.2, 2)});

      // Pésalo cuando te llegue
      tl.fromTo("#t4 .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {T_PESALO});
      tl.fromTo("#checks2 .c1", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_AMARILLO});
      tl.fromTo("#checks2 .c2", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_NOMBRE});
      tl.fromTo("#checks2 .c3", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, {T_ROMPER});

      // Foto real del camión (16:9) en formato vertical: paneo de la carga hacia la cabina y el letrero
      tl.fromTo("#s5", {{ x: {wide_x(0.30)}, scale: 1.0 }}, {{ x: {wide_x(0.62)}, scale: 1.03, duration: {S5[1]}, ease: "sine.inOut" }}, {S5[0]});

      // La toma 6 dura más que el clip (5 s): zoom lento para que el último fotograma no se vea congelado
      tl.fromTo("#s6", {{ scale: 1.0 }}, {{ scale: 1.1, duration: {S6[1]}, ease: "none", transformOrigin: "50% 60%" }}, {S6[0]});

      // Fundidos entre tomas
      tl.fromTo("#s2-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S2[0]});
      tl.fromTo("#s3-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S3[0]});
      tl.fromTo("#s4-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S4[0]});
      tl.fromTo("#s5-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S5[0]});
      tl.fromTo("#s6-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S6[0]});

      // Cierre
      tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {END});
      tl.fromTo("#end-logo", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, {round(END + 0.05, 2)});
      tl.fromTo("#end-wave", {{ scaleX: 0, transformOrigin: "100% 50%" }}, {{ scaleX: 1, duration: 0.8, ease: E }}, {round(END + 0.2, 2)});
      tl.fromTo("#end-rule", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.8, ease: E }}, {round(END + 0.2, 2)});
      tl.fromTo("#end-num", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {round(t("Peso") - 0.05, 2)});
      tl.fromTo("#end-tag", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, {round(t("peso") - 0.05, 2)});
      tl.fromTo("#end-tag2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, {round(t("precio") - 0.05, 2)});
      tl.fromTo("#end-wa", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {round(t("escríbenos") - 0.1, 2)});
      tl.fromTo("#end-wa .wa-ico", {{ scale: 0.6 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {round(t("escríbenos"), 2)});
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
print("ok", OUT.name, {"S1": S1, "S2": S2, "S3": S3, "S4": S4, "S5": S5, "S6": S6, "END": END, "TOTAL": TOTAL,
                       "groups": len(groups), "voz": VOZ_DUR})
