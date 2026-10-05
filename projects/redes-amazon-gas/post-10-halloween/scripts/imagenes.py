"""Escenas del post 10 (Doña Meche, Halloween + Día de la Canción Criolla) con kie.ai Nano Banana 2.

Usa la referencia del personaje (`personaje/dona-meche-ref.png`, URL en `ref-url.txt`) como
image_input para mantener cara, pelo, aretes y ropa. La descripción y el bloque de estilo son
los mismos del post 4; solo cambia el escenario (cocina de noche, decorada para la jarana).

Uso: python3 imagenes.py escenas [nombre ...] | apagada
"""
import json, sys
from pathlib import Path
import kie

ROOT = kie.ROOT
PERSONAJE = ROOT.parent / "personaje"
OUT = ROOT / "assets/img"
LOG = OUT / "credits.json"

KITCHEN = (
    "her humble but tidy home kitchen in Iquitos at night, decorated for a Saturday party: wooden plank walls "
    "painted light cream, a window with green mosquito screen and dark night outside, warm yellow light bulb, a "
    "simple paper garland of orange and black paper bats hanging on the wall, a small carved pumpkin with a candle "
    "inside on the shelf, a wooden Peruvian cajon drum and a guitar leaning in the corner, a tiled counter with a "
    "two-burner tabletop gas stove and a big aluminium pot of arroz con pollo (green coriander rice with chicken)"
)
STYLE = ("Photorealistic, warm cozy evening light, shot on a smartphone like a TikTok comedy sketch, realistic skin "
         "texture, family-friendly, nothing scary or gory, no text, no captions, no logos, no brand names, no purple "
         "or violet colors anywhere, no gas cylinders visible")
SAME = "Use the woman from the reference image, identical face, hair, earrings and clothes (same floral blouse and cream apron)."

SCENES = {
    "a-fiesta": (f"{SAME} Vertical medium shot from the waist up: she stands at the stove in {KITCHEN}, stirring the "
                 f"pot with a big wooden spoon, steam rising, a small calm blue gas flame under the pot. She looks at "
                 f"the camera with a cheeky, brave, confident smile, mouth closed, as if saying nothing scares her. "
                 f"Face in the upper half of the frame. {STYLE}."),
    "b-susto": (f"{SAME} Vertical close-up from the chest up in the same decorated kitchen at night: comedic "
                f"terrified expression, eyebrows raised, eyes wide, both hands on her cheeks, looking straight at "
                f"the camera, lips closed. Behind her the pot on the stove, no flame and no steam, the paper bats "
                f"garland visible. Face centered in the upper half. {STYLE}."),
    "c-celular": (f"{SAME} Vertical medium shot from the waist up in the same decorated kitchen at night: she holds a "
                  f"smartphone in one hand at chest height, screen facing herself, and raises the index finger of "
                  f"the other hand as if giving wise advice, knowing confident smile, looking straight at the camera, "
                  f"mouth relaxed and closed. Face clearly visible in the upper half. {STYLE}."),
    "d-hornilla": ("Vertical close-up of a two-burner tabletop gas stove on a tiled counter in a humble Iquitos home "
                   "kitchen at night, a big aluminium pot of arroz con pollo on the front burner, a small calm blue gas "
                   "flame under the pot, light steam, a small carved pumpkin with a candle softly out of focus in the "
                   "background, warm yellow light. Shallow depth of field. Photorealistic, family-friendly, no text, "
                   "no logos, no people, no gas cylinders, no purple."),
}
APAGADA = ("Edit this exact image: the gas burner flame under the pot is now completely OFF, no flame at all, no "
           "steam. Keep everything else identical: same pot, stove, counter, pumpkin, framing and light. "
           "Photorealistic, no text, no purple.")


def log_write(key, val):
    data = json.loads(LOG.read_text()) if LOG.exists() else {}
    data[key] = val
    LOG.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def gen(name, prompt, imgs):
    return kie.create("nano-banana-2", {"prompt": prompt, "image_input": imgs, "aspect_ratio": "9:16",
                                        "resolution": "2K", "output_format": "png"})


def main():
    step = sys.argv[1]
    before = kie.credits()
    if step == "escenas":
        ref_url = (PERSONAJE / "ref-url.txt").read_text().strip()
        only = set(sys.argv[2:])
        tasks = {}
        for name, prompt in SCENES.items():
            if only and name not in only:
                continue
            tasks[name] = gen(name, prompt, [] if name == "d-hornilla" else [ref_url])
            print(name, tasks[name], flush=True)
        res = kie.wait_all(tasks, every=10)
        for name, r in res.items():
            if r["state"] == "success":
                kie.download(r["urls"][0], OUT / f"{name}.png")
            log_write(name, {**r, "prompt": SCENES[name]})
    elif step == "apagada":
        src = json.loads(LOG.read_text())["d-hornilla"]["urls"][0]
        tid = gen("e-hornilla-apagada", APAGADA, [src])
        res = kie.wait_all({"e-hornilla-apagada": tid}, every=10)
        r = res["e-hornilla-apagada"]
        if r["state"] == "success":
            kie.download(r["urls"][0], OUT / "e-hornilla-apagada.png")
        log_write("e-hornilla-apagada", {**r, "prompt": APAGADA})
    log_write(f"{step}_credits", {"before": before, "after": kie.credits()})
    print(json.dumps(res, default=str)[:2000])


if __name__ == "__main__":
    main()
