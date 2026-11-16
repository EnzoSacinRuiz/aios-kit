"""Genera index.html del post 7 (vaciante) a partir de la alineación de la voz de Terry.

Parte 2 de "Iquitos no tiene carretera" (post 1). Abre con el video real de la barcaza (WhatsApp,
upscale en kie.ai) y cierra con "energía que mueve a Loreto", sin cantidad de embarcaciones.
Mismo lenguaje visual que post-01-rio (Barlow Condensed, granate/crema, subtítulos palabra a palabra
en amarillo llama). La versión anterior está en versiones/build-v1.py.
Uso: python3 scripts/build.py         → index.html (9:16, TikTok)
     python3 scripts/build.py 4x5     → ../post-07-vaciante-4x5/index.html (1080x1350, feed de FB e IG)
"""
import json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VO = 0.30          # la voz entra 0.3 s después del inicio
TOTAL = 18.8       # el contacto queda ~3 s en pantalla después de la voz

# Medidas por formato. El feed de FB e IG rechaza el 9:16, por eso existe la versión 4:5.
F45 = len(sys.argv) > 1 and sys.argv[1] == "4x5"
H = 1350 if F45 else 1920
L = dict(card_top=150, nivel_top=640, cap_top=850, sm=100, md=110, logo=250, end_num=100, end_tag=72,
         wa_mt=36, wa_num=108, wa_ico=104, handle_mt=36) if F45 else \
    dict(card_top=290, nivel_top=900, cap_top=1180, sm=112, md=124, logo=360, end_num=120, end_tag=84,
         wa_mt=56, wa_num=120, wa_ico=118, handle_mt=64)
OUT = ROOT.parent / "post-07-vaciante-4x5" if F45 else ROOT
if F45:
    OUT.mkdir(exist_ok=True)
    for f in ("hyperframes.json", "package.json"):
        shutil.copyfile(ROOT / f, OUT / f)
    shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)

# Video real: el upscale si existe; si no, la versión a 30 fps constantes del original.
REAL = "assets/clips/real-barcaza-upscale.mp4"
if not (ROOT / REAL).exists():
    REAL = "assets/clips/real-barcaza-cfr.mp4"
REAL_W = round(H * 854 / 480)   # ancho mostrado del video 16:9 a la altura del formato


def real_x(cx):
    """Desplazamiento horizontal para centrar la fracción cx (0..1) del video real en 1080 px."""
    return round(-(cx * REAL_W - 540))


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


def t(word):
    return round(words[W.index(word)][1], 2)


T_Y, T_COMO, T_DESDE, T_PORQUE = t("Y"), t("¿Cómo"), t("Desde"), t("Porque")
END = round(t("Amazon") - 0.1, 2)   # entra el cierre justo antes de "Amazon Gas"

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

# Tomas: (inicio, duración). Las que se cruzan con fundido empiezan 0.4 s antes del corte.
S1 = (0.0, round(T_COMO + 0.25, 2))                                   # video real: la barcaza navegando (gancho)
S2 = (round(T_COMO - 0.15, 2), round(T_DESDE + 0.25 - (T_COMO - 0.15), 2))   # aérea: el cauce entre la selva
S3 = (round(T_DESDE - 0.15, 2), round(T_PORQUE + 0.25 - (T_DESDE - 0.15), 2))  # vuelve el video real
S3_MEDIA = round(S1[1] + 0.3, 2)                                      # sigue donde quedó la toma 1
S4 = (round(T_PORQUE - 0.15, 2), round(END + 0.4 - (T_PORQUE - 0.15), 2))     # barcaza real en la orilla

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
      video.shot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      video.real {{ position: absolute; top: 0; left: 0; height: 100%; width: {REAL_W}px; max-width: none; }}

      #veil {{
        position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(27,21,18,0.7) 0%, rgba(27,21,18,0.12) 40%, rgba(27,21,18,0.05) 55%, rgba(27,21,18,0.62) 100%);
      }}

      .card {{ position: absolute; left: 80px; right: 160px; top: {L["card_top"]}px; }}
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

      /* Nivel del río: una línea que baja (la vaciante) */
      #nivel {{ position: absolute; left: 80px; top: {L["nivel_top"]}px; width: 260px; }}
      #nivel .ln {{ height: 6px; background: var(--crema); opacity: 0.9; }}
      #nivel .lbl {{ margin-top: 12px; font-family: "Barlow Condensed", sans-serif; font-weight: 700; font-size: 34px;
        letter-spacing: 0.08em; text-transform: uppercase; color: var(--crema); text-shadow: 0 2px 12px rgba(27,21,18,0.8); }}

      .cap {{ position: absolute; left: 70px; right: 150px; top: {L["cap_top"]}px; }}
      .cap-in {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 84px; line-height: 1.02;
        text-transform: uppercase; color: var(--crema); text-align: left;
        text-shadow: 0 3px 0 rgba(27,21,18,0.9), 0 0 22px rgba(27,21,18,0.85); }}
      .cap-in .w {{ display: inline-block; }}

      #end {{ position: absolute; inset: 0; background: var(--crema); display: flex; flex-direction: column; align-items: center; justify-content: center; }}
      #end-logo {{ width: {L["logo"]}px; height: auto; display: block; }}
      #end-num {{ margin-top: 70px; font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: {L["end_num"]}px; line-height: 0.9;
        text-transform: uppercase; color: var(--granate); text-align: center; }}
      #end-tag {{
        margin-top: 10px; font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase;
        font-size: {L["end_tag"]}px; line-height: 0.95; color: var(--marron); text-align: center; max-width: 860px;
      }}
      #end-tag em {{ font-style: normal; color: var(--granate); }}
      /* Contacto: ícono oficial de WhatsApp (Simple Icons) y número grande en negro, a pedido de papá */
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
    <!-- Generado por scripts/build.py. Tomas 1 y 3: video real de la barcaza (upscale, sin IA generativa).
         Tomas 2 y 4: fotos reales animadas con kie.ai (Kling 2.1). -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="{H}">
      <div id="s1-vis" class="shot-wrap"><video id="s1" class="clip real" src="{REAL}" data-start="{S1[0]}" data-duration="{S1[1]}" data-media-start="0" data-track-index="0" muted playsinline></video></div>
      <div id="s2-vis" class="shot-wrap"><video id="s2" class="clip shot" src="assets/clips/v2-meandro.mp4" data-start="{S2[0]}" data-duration="{S2[1]}" data-track-index="1" muted playsinline></video></div>
      <div id="s3-vis" class="shot-wrap"><video id="s3" class="clip real" src="{REAL}" data-start="{S3[0]}" data-duration="{S3[1]}" data-media-start="{S3_MEDIA}" data-track-index="0" muted playsinline></video></div>
      <div id="s4-vis" class="shot-wrap"><video id="s4" class="clip shot" src="assets/clips/v3-barcaza.mp4" data-start="{S4[0]}" data-duration="{S4[1]}" data-track-index="1" muted playsinline></video></div>

      <div id="veil" class="clip" data-start="0" data-duration="{END + 0.4}" data-track-index="2"></div>

      <div id="t1" class="clip card" data-start="0.1" data-duration="{round(T_Y - 0.1, 2)}" data-track-index="3">
        <div class="t1-in">
          <span class="kicker">Parte 2</span>
          <div class="headline sm">Iquitos no tiene <em>carretera</em></div>
        </div>
      </div>
      <div id="t1b" class="clip card" data-start="{T_Y}" data-duration="{round(T_DESDE - 0.2 - T_Y, 2)}" data-track-index="3">
        <div class="t1b-in">
          <span class="kicker">Vaciante en Loreto</span>
          <div class="headline md">¿Y cuando el río baja?</div>
        </div>
      </div>
      <div id="nivel" class="clip" data-start="{T_Y}" data-duration="{round(T_DESDE - 0.2 - T_Y, 2)}" data-track-index="5">
        <div class="ln"></div><div class="lbl">Nivel del río</div>
      </div>
      <div id="t2" class="clip card" data-start="{T_DESDE}" data-duration="{round(END - T_DESDE, 2)}" data-track-index="3">
        <div class="t2-in">
          <div class="headline md box">El gas sigue <em>llegando</em></div>
          <span class="bar"></span>
        </div>
      </div>

{chr(10).join(caps_html)}

      <div id="end" class="clip" data-start="{END}" data-duration="{round(TOTAL - END, 2)}" data-track-index="6">
        <div id="end-wave"></div>
        <img id="end-logo" src="assets/img/logo.png" alt="Amazon Gas" />
        <div id="end-num">Energía que mueve</div>
        <div id="end-tag">a <em>Loreto</em></div>
        <div id="end-wa">
          <div class="wa-lbl">Pide tu balón por WhatsApp</div>
          <div class="wa-row"><img class="wa-ico" src="assets/img/whatsapp.svg" alt="WhatsApp" /><span class="wa-num">991 511 401</span></div>
        </div>
        <div id="end-handle">@amazongasperu</div>
        <div id="end-rule"></div>
      </div>

      <audio id="musica" src="assets/audio/musica.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-volume="0.5"
        data-automation='{{"version":1,"lanes":[{{"target":"volume","points":[{{"t":0,"v":0}},{{"t":0.5,"v":1}},{{"t":{round(TOTAL - 1.8, 2)},"v":1}},{{"t":{TOTAL},"v":0}}]}}]}}' data-fx-carve="{{&quot;enabled&quot;:true,&quot;sources&quot;:[&quot;voz&quot;],&quot;strength&quot;:0.8}}"></audio>
      <audio id="voz" src="assets/audio/voz.mp3" data-start="{VO}" data-duration="{VOZ_DUR}" data-track-index="10" data-volume="1"></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const E = "power3.out";

      // Gancho: Iquitos no tiene carretera (parte 2)
      tl.fromTo("#t1 .kicker", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: E }}, 0.1);
      tl.fromTo("#t1 .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, 0.2);
      tl.to("#t1 .t1-in", {{ opacity: 0, duration: 0.2 }}, {round(T_Y - 0.2, 2)});

      // ¿Y cuando el río baja? La línea del nivel baja lentamente
      tl.fromTo("#t1b .kicker", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: E }}, {T_Y});
      tl.fromTo("#t1b .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, {round(T_Y + 0.1, 2)});
      tl.to("#t1b .t1b-in", {{ opacity: 0, duration: 0.2 }}, {round(T_DESDE - 0.4, 2)});
      tl.fromTo("#nivel", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {T_Y});
      tl.fromTo("#nivel", {{ y: -60 }}, {{ y: 120, duration: {round(T_DESDE - 0.6 - T_Y, 2)}, ease: "sine.inOut" }}, {T_Y});
      tl.to("#nivel", {{ opacity: 0, duration: 0.2 }}, {round(T_DESDE - 0.4, 2)});

      // El gas sigue llegando
      tl.fromTo("#t2 .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {T_DESDE});
      tl.fromTo("#t2 .bar", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.35, ease: E }}, {round(T_DESDE + 0.3, 2)});

      // Video real 16:9 recortado a 9:16: paneo lento del remolcador hacia la barcaza con los tanques
      tl.fromTo("#s1", {{ x: {real_x(0.64)} }}, {{ x: {real_x(0.36)}, duration: {S1[1]}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#s3", {{ x: {real_x(0.64)}, scale: 1.0 }}, {{ x: {real_x(0.58)}, scale: 1.04, duration: {S3[1]}, ease: "none" }}, {S3[0]});

      // Fundidos entre tomas
      tl.fromTo("#s2-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S2[0]});
      tl.fromTo("#s3-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S3[0]});
      tl.fromTo("#s4-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S4[0]});

      // Cierre
      tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {END});
      tl.fromTo("#end-logo", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, {round(END + 0.05, 2)});
      tl.fromTo("#end-wave", {{ scaleX: 0, transformOrigin: "100% 50%" }}, {{ scaleX: 1, duration: 0.8, ease: E }}, {round(END + 0.2, 2)});
      tl.fromTo("#end-rule", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.8, ease: E }}, {round(END + 0.2, 2)});
      tl.fromTo("#end-num", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: E }}, {round(t("energía") - 0.05, 2)});
      tl.fromTo("#end-tag", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {round(t("Loreto.") - 0.05, 2)});
      tl.fromTo("#end-wa", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {round(words[-1][2] + 0.1, 2)});
      tl.fromTo("#end-wa .wa-ico", {{ scale: 0.6 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)" }}, {round(words[-1][2] + 0.2, 2)});
      tl.fromTo("#end-handle", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, {round(words[-1][2] + 0.5, 2)});

      // Subtítulos: la palabra que se dice se enciende en amarillo llama
{chr(10).join(caps_js)}

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
(OUT / "index.html").write_text(html)
print("ok", OUT.name, {"real": REAL, "S1": S1, "S2": S2, "S3": S3, "S3_media": S3_MEDIA, "S4": S4, "END": END,
             "groups": len(groups), "voz": VOZ_DUR})
