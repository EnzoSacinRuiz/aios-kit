<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <!-- GENERADO: editar scripts/template.html.tpl y correr `python3 scripts/build.py` (rellena subtítulos desde la alineación de la voz) -->
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Barlow Condensed"; font-weight: 600; src: url("assets/fonts/BarlowCondensed-SemiBold.ttf") format("truetype"); }
      @font-face { font-family: "Barlow Condensed"; font-weight: 700; src: url("assets/fonts/BarlowCondensed-Bold.ttf") format("truetype"); }
      @font-face { font-family: "Barlow Condensed"; font-weight: 800; src: url("assets/fonts/BarlowCondensed-ExtraBold.ttf") format("truetype"); }
      @font-face { font-family: "Inter"; font-weight: 100 900; src: url("assets/fonts/Inter.ttf") format("truetype"); }

      :root {
        --granate: #8e4149;
        --granate-oscuro: #6e2f35;
        --marron: #1b1512;
        --crema: #fbf8f3;
        --arena: #c9bdb0;
        --llama: #f5dc17;
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--marron); }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Inter", sans-serif; }

      .shot-wrap { position: absolute; inset: 0; overflow: hidden; }
      video.shot, img.shot { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }

      /* Plano del balón: fondo de cocina generado + foto REAL del balón compuesta encima */
      #balon-scene { position: absolute; inset: 0; }
      #balon-shadow { position: absolute; left: 30px; top: 1820px; width: 470px; height: 80px; border-radius: 50%;
        background: radial-gradient(ellipse at center, rgba(27,21,18,0.55) 0%, rgba(27,21,18,0) 70%); }
      #balon { position: absolute; left: 50px; top: 1080px; height: 780px; width: auto;
        filter: sepia(0.12) saturate(0.95) brightness(0.97) drop-shadow(18px 10px 26px rgba(27,21,18,0.35)); }

      #veil {
        position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(27,21,18,0.7) 0%, rgba(27,21,18,0.15) 36%, rgba(27,21,18,0.05) 55%, rgba(27,21,18,0.55) 100%);
      }

      .card { position: absolute; left: 80px; right: 150px; top: 250px; }
      .kicker {
        display: inline-block; font-family: "Barlow Condensed", sans-serif; font-weight: 700;
        font-size: 44px; letter-spacing: 0.08em; text-transform: uppercase;
        color: var(--crema); background: var(--granate); padding: 6px 18px 4px;
      }
      .headline {
        font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase;
        color: var(--crema); font-size: 140px; line-height: 0.9; letter-spacing: -0.01em;
        text-shadow: 0 4px 24px rgba(27,21,18,0.6); margin-top: 18px;
      }
      .headline.md { font-size: 104px; }
      .sub {
        margin-top: 26px; max-width: 780px; font-weight: 600; font-size: 46px; line-height: 1.2;
        color: var(--crema); text-shadow: 0 2px 14px rgba(27,21,18,0.8);
      }
      .bar { display: block; width: 140px; height: 12px; background: var(--granate); margin-top: 26px; }

      /* Pasos de la receta */
      .step { display: flex; align-items: flex-start; gap: 28px; }
      .num { flex: 0 0 auto; width: 132px; height: 132px; background: var(--granate); color: var(--crema);
        font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 112px; line-height: 132px;
        text-align: center; border-radius: 3px; box-shadow: 0 6px 22px rgba(27,21,18,0.4); }
      .step-txt { font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase;
        color: var(--crema); font-size: 92px; line-height: 0.92; text-shadow: 0 4px 22px rgba(27,21,18,0.7); }
      .step-label { font-family: "Barlow Condensed", sans-serif; font-weight: 700; font-size: 38px; letter-spacing: 0.1em;
        text-transform: uppercase; color: var(--llama); margin-bottom: 8px; text-shadow: 0 2px 0 rgba(27,21,18,0.9), 0 0 14px rgba(27,21,18,0.9); }

      .pill { display: inline-block; margin-top: 34px; font-family: "Barlow Condensed", sans-serif; font-weight: 800;
        font-size: 64px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--marron);
        background: var(--crema); padding: 10px 34px 6px; border-radius: 3px; }

      /* Subtítulos */
      .cap { position: absolute; left: 70px; right: 150px; top: 1270px; }
      .cap-in { font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 74px; line-height: 1.02;
        text-transform: uppercase; color: var(--crema); text-align: left;
        text-shadow: 0 3px 0 rgba(27,21,18,0.9), 0 0 22px rgba(27,21,18,0.85); }
      .cap-in .w { display: inline-block; }

      /* Cierre */
      #end { position: absolute; inset: 0; background: var(--crema); display: flex; flex-direction: column; align-items: center; justify-content: center; }
      #end-logo { width: 360px; height: auto; display: block; }
      #end-tag {
        margin-top: 60px; font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase;
        font-size: 96px; line-height: 0.95; color: var(--marron); text-align: center; max-width: 860px;
      }
      #end-tag em { font-style: normal; color: var(--granate); }
      #end-q { margin-top: 44px; font-weight: 600; font-size: 42px; color: #6b5d51; text-align: center; max-width: 820px; line-height: 1.25; }
      #end-handle {
        margin-top: 60px; font-family: "Barlow Condensed", sans-serif; font-weight: 700; font-size: 44px;
        color: var(--crema); background: var(--granate); padding: 10px 28px 8px;
      }
      #end-rule { position: absolute; left: 0; right: 0; bottom: 0; height: 22px; background: var(--granate); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="38" data-width="1080" data-height="1920">
      <!-- Escenas de cocina generadas con kie.ai (Nano Banana + Kling 2.1); fundidos de 0.3 s -->
      <div id="vA-vis" class="shot-wrap"><video id="vA" class="clip shot" src="assets/clips/s6-plato.mp4" data-start="0" data-duration="4.65" data-track-index="0" muted playsinline></video></div>
      <div id="vB-vis" class="shot-wrap"><video id="vB" class="clip shot" src="assets/clips/s1-platano.mp4" data-start="4.35" data-duration="3.7" data-track-index="1" muted playsinline></video></div>
      <div id="vC-vis" class="shot-wrap"><video id="vC" class="clip shot" src="assets/clips/s2-fritura.mp4" data-start="7.75" data-duration="5.0" data-track-index="0" muted playsinline></video></div>
      <div id="vD-vis" class="shot-wrap"><video id="vD" class="clip shot" src="assets/clips/s3-machacar.mp4" data-start="12.45" data-duration="4.8" data-track-index="1" muted playsinline></video></div>
      <div id="vE-vis" class="shot-wrap"><video id="vE" class="clip shot" src="assets/clips/s4-bolitas.mp4" data-start="16.95" data-duration="3.0" data-track-index="0" muted playsinline></video></div>
      <div id="vF-vis" class="shot-wrap"><video id="vF" class="clip shot" src="assets/clips/s5-cecina.mp4" data-start="19.65" data-duration="4.6" data-track-index="1" muted playsinline></video></div>
      <div id="vG-vis" class="shot-wrap clip" data-start="23.95" data-duration="4.05" data-track-index="0">
        <div id="balon-scene">
          <img class="shot" src="assets/clips/bg-cocina.png" alt="" />
          <div id="balon-shadow"></div>
          <img id="balon" src="assets/img/balon-15kg.png" alt="Balón Amazon Gas" />
        </div>
      </div>
      <div id="vH-vis" class="shot-wrap clip" data-start="27.7" data-duration="5.9" data-track-index="1">
        <img id="vH" class="shot" src="assets/clips/s6-plato.png" alt="" />
      </div>

      <div id="veil" class="clip" data-start="0" data-duration="33.6" data-track-index="2"></div>

      <!-- Textos -->
      <div id="t0" class="clip card" data-start="0.1" data-duration="4.3" data-track-index="3">
        <div class="t0-in">
          <span class="kicker">Cocina loretana</span>
          <div class="headline">Tacacho con cecina</div>
          <div class="sub t0-sub">a fuego parejo</div>
        </div>
      </div>
      <div id="t1" class="clip card" data-start="4.5" data-duration="3.2" data-track-index="3">
        <div class="step"><div class="num">1</div><div><div class="step-label">Paso 1</div><div class="step-txt">Pela y trocea el plátano verde</div></div></div>
      </div>
      <div id="t2" class="clip card" data-start="7.85" data-duration="4.45" data-track-index="3">
        <div class="step"><div class="num">2</div><div><div class="step-label">Paso 2</div><div class="step-txt">Fríelo a fuego parejo hasta que dore</div></div></div>
      </div>
      <div id="t3" class="clip card" data-start="12.5" data-duration="4.3" data-track-index="3">
        <div class="step"><div class="num">3</div><div><div class="step-label">Paso 3</div><div class="step-txt">Machácalo con manteca, chicharrón y sal</div></div></div>
      </div>
      <div id="t4" class="clip card" data-start="17.0" data-duration="2.5" data-track-index="3">
        <div class="step"><div class="num">4</div><div><div class="step-label">Paso 4</div><div class="step-txt">Forma tus bolitas</div></div></div>
      </div>
      <div id="t5" class="clip card" data-start="19.7" data-duration="4.1" data-track-index="3">
        <div class="step"><div class="num">5</div><div><div class="step-label">Paso 5</div><div class="step-txt">Dora la cecina, vuelta y vuelta</div></div></div>
      </div>
      <div id="t6" class="clip card" data-start="24.0" data-duration="3.55" data-track-index="3">
        <div class="t6-in">
          <div class="headline">¡Listo!</div>
          <div class="sub t6-sub">El desayuno loretano de siempre.</div>
          <span class="bar"></span>
        </div>
      </div>
      <div id="t7" class="clip card" data-start="27.75" data-duration="5.7" data-track-index="3">
        <div class="t7-in">
          <div class="headline md">¿Cuál es tu plato loretano favorito?</div>
          <span class="pill">Comenta</span>
        </div>
      </div>

      <!-- Subtítulos (alineación de la voz de Terry) -->
<!--CAPTIONS-->

      <!-- Cierre -->
      <div id="end" class="clip" data-start="33.3" data-duration="4.7" data-track-index="5">
        <img id="end-logo" src="assets/img/logo.png" alt="Amazon Gas" />
        <div id="end-tag">La energía que mueve a <em>Loreto</em></div>
        <div id="end-q">¿Cuál es tu plato loretano favorito? Cuéntanos en los comentarios.</div>
        <div id="end-handle">@amazongasperu</div>
        <div id="end-rule"></div>
      </div>

      <audio id="musica" src="assets/audio/musica.mp3" data-start="0" data-duration="38" data-track-index="11" data-volume="0.4"
        data-automation='{"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":0},{"t":0.6,"v":1},{"t":33.3,"v":1},{"t":33.8,"v":1.6},{"t":36.3,"v":1.6},{"t":38,"v":0}]}]}' data-fx-carve="{&quot;enabled&quot;:true,&quot;sources&quot;:[&quot;voz&quot;],&quot;strength&quot;:0.8}"></audio>
      <audio id="voz" src="assets/audio/voz.mp3" data-start="__OFF__" data-duration="__VOZDUR__" data-track-index="10" data-volume="1"></audio>
    </div>

    <script>
      const tl = gsap.timeline({ paused: true });
      const E = "power3.out";

      // Gancho
      tl.fromTo("#t0 .kicker", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: E }, 0.1);
      tl.fromTo("#t0 .headline", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: E }, 0.18);
      tl.fromTo("#t0 .t0-sub", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, ease: E }, 0.6);
      tl.to("#t0 .t0-in", { opacity: 0, duration: 0.2 }, 4.2);

      // Pasos
      [["#t1", 4.5, 7.5], ["#t2", 7.85, 12.1], ["#t3", 12.5, 16.6], ["#t4", 17.0, 19.3], ["#t5", 19.7, 23.6]].forEach(([id, a, b]) => {
        tl.fromTo(id + " .num", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, a);
        tl.fromTo(id + " .step-label", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.3, ease: E }, a + 0.08);
        tl.fromTo(id + " .step-txt", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: E }, a + 0.12);
        tl.to(id + " .step", { opacity: 0, duration: 0.2 }, b);
      });

      // Listo + balón
      tl.fromTo("#t6 .headline", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: E }, 24.0);
      tl.fromTo("#t6 .t6-sub", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, ease: E }, 25.0);
      tl.fromTo("#t6 .bar", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.35, ease: E }, 25.2);
      tl.to("#t6 .t6-in", { opacity: 0, duration: 0.2 }, 27.35);
      tl.fromTo("#balon-scene", { scale: 1.0, transformOrigin: "30% 80%" }, { scale: 1.07, duration: 4.05, ease: "none" }, 23.95);

      // CTA
      tl.fromTo("#t7 .headline", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: E }, 27.75);
      tl.fromTo("#t7 .pill", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }, 29.6);
      tl.to("#t7 .t7-in", { opacity: 0, duration: 0.2 }, 33.2);
      tl.fromTo("#vH", { scale: 1.0 }, { scale: 1.1, duration: 5.9, ease: "none" }, 27.7);

      // Cierre
      tl.fromTo("#end", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power1.inOut" }, 33.3);
      tl.fromTo("#end-logo", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }, 33.35);
      tl.fromTo("#end-rule", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.8, ease: E }, 33.5);
      tl.fromTo("#end-tag", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: E }, 33.9);
      tl.fromTo("#end-q", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: E }, 34.6);
      tl.fromTo("#end-handle", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: E }, 35.0);

      // Fundidos entre tomas
      [["#vB-vis", 4.35], ["#vC-vis", 7.75], ["#vD-vis", 12.45], ["#vE-vis", 16.95], ["#vF-vis", 19.65], ["#vG-vis", 23.95], ["#vH-vis", 27.7]].forEach(([id, t]) => {
        tl.fromTo(id, { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power1.inOut" }, t);
      });

      // Subtítulos: la palabra que se dice se enciende en amarillo llama
//CAPTIONS_JS

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
