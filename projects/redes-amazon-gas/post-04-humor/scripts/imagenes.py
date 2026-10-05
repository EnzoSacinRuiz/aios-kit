"""Personaje recurrente (Doña Meche) y escenas del post 4 con kie.ai (Nano Banana 2).

Paso 1 (`ref`): genera la imagen de referencia del personaje y la guarda en
`projects/redes-amazon-gas/personaje/`.
Paso 2 (`escenas`): genera las escenas 9:16 usando la referencia como image_input, para que la
cara y la ropa se mantengan entre planos.

Uso: python3 imagenes.py ref | escenas [nombre ...]
"""
import json, sys
from pathlib import Path
import kie

ROOT = kie.ROOT
PERSONAJE = ROOT.parent / "personaje"
OUT = ROOT / "assets/img"
PERSONAJE.mkdir(exist_ok=True)
LOG = ROOT / "assets/img/credits.json"

DESC = (
    "a friendly 55-year-old woman from Iquitos in the Peruvian Amazon, mestiza, warm brown skin, round kind face "
    "with laugh lines, expressive dark brown eyes, thick black hair with a few grey streaks pulled back in a low bun "
    "held by a dark maroon scrunchie, small gold hoop earrings. She wears a short-sleeve cotton blouse with a small "
    "cream and maroon floral print, a plain cream apron with one front pocket, a knee-length dark brown skirt and "
    "simple rubber sandals"
)
KITCHEN = (
    "a humble but tidy home kitchen in Iquitos: wooden plank walls painted light cream, a window with green "
    "mosquito screen and tropical plants outside, a tiled counter with a two-burner tabletop gas stove, a big "
    "aluminium pot full of juanes (rice parcels wrapped in green bijao leaves tied with string)"
)
STYLE = ("Photorealistic, natural warm daylight, shot on a smartphone like a TikTok comedy sketch, realistic skin "
         "texture, no text, no captions, no logos, no brand names, no purple or violet colors anywhere, no gas "
         "cylinders visible")

REF_PROMPT = (f"Waist-up portrait of {DESC}. She stands in {KITCHEN}, looking straight at the camera with a warm, "
              f"cheeky neighbourly smile, hands resting on her apron. Character reference photo, centered, "
              f"face clearly visible. {STYLE}.")

SCENES = {
    "a-cocinando": (f"Use the woman from the reference image, identical face, hair, earrings and clothes. Vertical "
                    f"medium shot from the waist up: she stands at the stove in {KITCHEN}, stirring the pot of "
                    f"juanes with a big wooden spoon, steam rising, a small blue gas flame under the pot. She looks "
                    f"at the camera, proud and happy, mouth closed in a smile. Face in the upper half of the frame. "
                    f"{STYLE}."),
    "b-susto": (f"Use the woman from the reference image, identical face, hair, earrings and clothes. Vertical "
                f"close-up from the chest up in the same kitchen: comedic shocked expression, eyebrows raised, eyes "
                f"wide, both hands on her cheeks, looking straight at the camera, lips closed. Behind her the pot "
                f"of juanes on the stove, no flame and no steam. Face centered in the upper half. {STYLE}."),
    "c-celular": (f"Use the woman from the reference image, identical face, hair, earrings and clothes. Vertical "
                  f"medium shot from the waist up in the same kitchen: she holds a smartphone in one hand at chest "
                  f"height, screen facing herself, and raises the index finger of the other hand as if giving "
                  f"wise advice, knowing confident smile, looking straight at the camera, mouth relaxed and "
                  f"closed. Face clearly visible in the upper half. {STYLE}."),
    "d-hornilla": ("Vertical close-up of a two-burner tabletop gas stove on a tiled counter in a humble Iquitos "
                   "home kitchen, a big aluminium pot full of juanes wrapped in green bijao leaves sitting on the "
                   "front burner, a small weak blue gas flame flickering under the pot, light steam. Shallow depth "
                   "of field, warm daylight. Photorealistic, no text, no logos, no people, no gas cylinders, no "
                   "purple."),
}
# Variante del inserto: misma hornilla con la llama apagada (se edita sobre d-hornilla).
APAGADA = ("Edit this exact image: the gas burner flame under the pot is now completely OFF, no flame at all, no "
           "steam. Keep everything else identical: same pot, juanes, stove, counter, framing and light. "
           "Photorealistic, no text, no purple.")


def log_write(key, val):
    data = json.loads(LOG.read_text()) if LOG.exists() else {}
    data[key] = val
    LOG.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    step = sys.argv[1]
    before = kie.credits()
    if step == "ref":
        tid = kie.create("nano-banana-2", {"prompt": REF_PROMPT, "image_input": [], "aspect_ratio": "3:4",
                                          "resolution": "2K", "output_format": "png"})
        res = kie.wait_all({"ref": tid}, every=10)
        r = res["ref"]
        if r["state"] == "success":
            kie.download(r["urls"][0], PERSONAJE / "dona-meche-ref.png")
            (PERSONAJE / "ref-url.txt").write_text(r["urls"][0] + "\n")
        log_write("ref", {**r, "prompt": REF_PROMPT, "credits_before": before, "credits_after": kie.credits()})
        print(json.dumps(r))
    elif step == "apagada":
        src = json.loads(LOG.read_text())["d-hornilla"]["urls"][0]
        tid = kie.create("nano-banana-2", {"prompt": APAGADA, "image_input": [src], "aspect_ratio": "9:16",
                                          "resolution": "2K", "output_format": "png"})
        r = kie.wait_all({"e-hornilla-apagada": tid}, every=10)["e-hornilla-apagada"]
        if r["state"] == "success":
            kie.download(r["urls"][0], OUT / "e-hornilla-apagada.png")
        log_write("e-hornilla-apagada", {**r, "prompt": APAGADA})
        print(json.dumps(r))
    elif step == "escenas":
        ref_url = (PERSONAJE / "ref-url.txt").read_text().strip()
        only = set(sys.argv[2:])
        tasks = {}
        for name, prompt in SCENES.items():
            if only and name not in only:
                continue
            imgs = [] if name == "d-hornilla" else [ref_url]
            tasks[name] = kie.create("nano-banana-2", {"prompt": prompt, "image_input": imgs, "aspect_ratio": "9:16",
                                                      "resolution": "2K", "output_format": "png"})
            print(name, tasks[name], flush=True)
        res = kie.wait_all(tasks, every=10)
        for name, r in res.items():
            if r["state"] == "success":
                kie.download(r["urls"][0], OUT / f"{name}.png")
            log_write(name, {**r, "prompt": SCENES[name]})
        log_write("escenas_credits", {"before": before, "after": kie.credits()})
        print(json.dumps(res))


if __name__ == "__main__":
    main()
