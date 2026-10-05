#!/usr/bin/env python3
"""Round driver for the bone-china-doll project.

Two engines are available on the same ComfyUI server:
  * ``zimage`` - Z-Image-Turbo (fast, stylized); rounds 3-6
  * ``qwen``   - Qwen-Image 2512 (much finer surface detail, real negative prompt); rounds 7-11

Usage:
  python3 run_round.py 7            # generate the round's images
  python3 run_round.py 7 --dry      # print prompts without generating
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_SCRIPTS = os.path.normpath(
    os.path.join(HERE, "..", "..", "skills", "text-to-image-comfyui", "scripts")
)
sys.path.insert(0, SKILL_SCRIPTS)
import comfyui_gen as cg  # noqa: E402
import comfyui_qwen as qw  # noqa: E402

SERVER = os.environ.get("COMFYUI_SERVER", cg.DEFAULT_SERVER)
WORKFLOW = os.path.normpath(
    os.path.join(HERE, "..", "..", "skills", "text-to-image-comfyui", "assets", "z-image-turbo-ui.json")
)

# ---------------------------------------------------------------------------
# z-image bases (rounds 3-6)
# ---------------------------------------------------------------------------
BASE = (
    "Photorealistic photograph of a handcrafted fine bone china princess doll. "
    "Translucent cream-white porcelain with visible subsurface scattering, glossy fired glaze, "
    "crisp specular highlights, faint hairline craquelure, hand-painted eyebrows drawn hair by hair, "
    "glossy glass doll eyes with hazel irises and sharp catchlights, finely sculpted eyelids and lips. "
    "Elegant serene princess face with refined oval features, slender neck, gentle expression, "
    "not a toddler, not cartoonish. Very subtle soft blush. "
    "White lace gown with visible thread structure, hand-sewn pearl beading, pale blue silk sash, "
    "silver filigree tiara set with sapphire and tiny diamonds, real pearl drop earrings. "
    "Museum collector piece, medium format camera, 120mm macro lens, shallow depth of field, "
    "clean seamless studio backdrop, no studio equipment visible, no text, no watermark"
)

BASE4 = (
    "Photorealistic photograph of a handcrafted fine bone china princess doll, museum collector piece. "
    "Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights, faint hairline "
    "craquelure, delicate warm translucency where the porcelain is thin at the rim of the ears and "
    "fingertips. Elegant adult princess proportions, refined oval face, defined jawline, slender tapered "
    "neck, small head relative to the body, serene gentle expression, not a child, not cartoonish. "
    "Hand-painted eyebrows drawn hair by hair, glossy glass doll eyes with hazel irises, deep pupils and "
    "sharp catchlights, finely sculpted eyelids and lips, very subtle soft blush. White lace gown with "
    "clearly visible thread structure, a single strand of pearls at the neckline, hand-sewn beadwork, "
    "pale blue silk sash, silver filigree tiara set with sapphire and small diamonds, real pearl drop "
    "earrings. Soft directional light from the upper left with a gentle rim light, even exposure, clean "
    "seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens, shallow "
    "depth of field, ultra-detailed surface, centered composition, no text, no watermark, no floating "
    "objects, no extra limbs"
)

BASE5 = (
    "Photorealistic photograph of a handcrafted fine bone china figurine of a princess, museum "
    "collector piece. Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights, "
    "faint hairline craquelure, delicate warm translucency where the porcelain is thinnest at the rim of "
    "the ears and fingertips. The face is an elegant young woman in her early twenties: refined oval "
    "face, high cheekbones, defined jawline, straight nose bridge, serene closed lips with a faint smile, "
    "proportionally sized almond eyes with a subtle eyelid crease, glossy glass eyes with warm hazel "
    "irises, deep pupils and sharp catchlights, finely sculpted eyelids. Slender tapered neck, small head "
    "relative to the body, poised posture, not a child, not cartoonish, not a toy. Hand-painted eyebrows "
    "drawn hair by hair, very subtle soft blush. White lace gown with clearly visible thread structure "
    "and soft fabric folds, a single strand of warm ivory pearls at the neckline, hand-sewn beadwork, "
    "pale blue silk sash, silver filigree tiara set with sapphire and small diamonds, pearl drop earrings. "
    "Soft directional light from the upper left with a gentle rim light, even exposure, clean seamless "
    "studio backdrop free of any equipment, medium format camera, 120mm macro lens, shallow depth of "
    "field, ultra-detailed surface, centered composition, no text, no watermark, no floating objects, "
    "no extra limbs, no skin blemishes"
)

BASE6 = (
    "Photorealistic macro photograph of a handcrafted fine bone china figurine of a princess, museum "
    "collector piece, ultra-detailed. Uniform glossy fired glaze over cream-white porcelain with visible "
    "micro glaze texture and fine craquelure lines, crisp specular highlights, delicate warm translucency "
    "where the porcelain is thinnest at the rim of the ears and fingertips. The face is an elegant young "
    "woman in her early twenties: refined oval face, high cheekbones, defined jawline, straight nose "
    "bridge, serene closed lips with a faint smile, individually rendered eyelashes, proportionally sized "
    "almond eyes with a subtle eyelid crease, glossy glass eyes with warm hazel irises, deep pupils and "
    "sharp catchlights. Slender tapered neck, poised posture, not a child, not cartoonish, not a toy. "
    "Hand-painted eyebrows drawn hair by hair, very subtle soft blush. White lace gown with clearly "
    "visible thread structure and soft fabric folds, a hand-painted rose motif on the skirt, tiny "
    "hand-sewn beadwork, a single strand of warm ivory pearls at the neckline, pale blue silk sash, "
    "silver filigree tiara set with sapphire and small diamonds, pearl drop earrings. Soft directional "
    "light from the upper left with a gentle rim light, even exposure, clean seamless studio backdrop "
    "free of any equipment, medium format camera, 120mm macro lens, shallow depth of field, centered "
    "composition, no text, no watermark, no floating objects, no extra limbs, no skin blemishes"
)

# ---------------------------------------------------------------------------
# Qwen-Image base (rounds 7-11): pristine glaze, no cracks on skin, doll joints,
# microscopic material detail; Qwen honors a real negative prompt.
# ---------------------------------------------------------------------------
BASE_Q = (
    "Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess, "
    "photographed like a real physical object under studio light. Pristine flawless ivory porcelain with "
    "a perfectly smooth fired glaze, crisp specular highlights, delicate warm translucency at the thin "
    "porcelain of the ears and fingertips, microscopic surface texture, completely clean and dust-free. "
    "Visible ball-joint seams at the neck and wrists. An elegant princess face with refined adult "
    "proportions: oval face, high cheekbones, straight nose bridge, serene closed lips, almond eyes of "
    "realistic size with a subtle crease, individually painted eyelashes, eyebrows painted hair by hair, "
    "the faintest soft blush. A gown of real white lace with individual visible threads, dense hand "
    "embroidery, seed pearls stitched one by one, a pale blue silk sash, a silver filigree tiara set "
    "with sapphires and small diamonds, pearl drop earrings. Fine art studio lighting from the upper "
    "left, gentle rim light, deep but clean shadows, sharp focus on the face, medium format camera, "
    "120mm macro lens, natural shallow depth of field, seamless neutral backdrop"
)

NEG_Q = (
    "cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl, "
    "waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail, "
    "low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers, deformed "
    "hands, floating objects, text, watermark, signature, logo, busy background"
)

# Round 8 base: Qwen + richer costume craft + sculptural chiaroscuro light.
BASE_Q8 = BASE_Q + (
    ". Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery, dense lace "
    "with individual visible threads, seed pearls stitched one by one, faceted gemstones set in metal "
    "prongs, a pale blue velvet sash, a heavy ceremonial tiara with enamelled details. Sculptural "
    "chiaroscuro studio lighting with one strong key light and deep natural falloff, subtle warm bounce "
    "on the shadow side, museum-vitrine realism, tack-sharp focus on the face, extremely fine texture"
)

# Round 9 base: push microscopic glaze texture and kill the CGI-smooth look.
BASE_Q9 = BASE_Q8 + (
    ". Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks, a few "
    "microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory, the matte "
    "unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness. Photographed with a "
    "100mm macro lens at f/8, focus stacked, ultra high resolution scan quality, natural sensor grain"
)

# Round 10 base: jewellery/metalwork macro, fabric macro, soft window light.
BASE_Q10 = BASE_Q9 + (
    ". Jewellery realism: engraved silver filigree with crisp milled edges, faceted sapphires and "
    "diamonds showing internal refraction and tiny inclusions, seed pearls with subtle orient and "
    "nacre rings, metal prongs and hinges clearly readable. Fabric realism: silk brocade with raised "
    "weft, linen-backed lace, visible individual stitches, slightly irregular handmade quality"
)

# Round 11 base: framing must LEAD the prompt -- round 10 showed that a long
# costume description makes Qwen pull back to a standard waist-up portrait.
BASE_Q11 = (
    "Photorealistic studio photograph of a handcrafted ball-jointed bone china doll of a princess. "
    "Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights, "
    "delicate warm translucency at the thin porcelain of the ears and fingertips, microscopic surface "
    "texture, completely clean and dust-free. Ball-joint seams at the neck and wrists. Fine art studio "
    "lighting, sharp focus, medium format camera, subtle natural sensor grain, no digital sharpening"
)

BASE_Q11_COSTUME = (
    " She wears a gown of real white lace with individual threads and raised gold-thread embroidery, "
    "seed pearls stitched one by one, sapphires set in milled silver prongs, a pale blue silk sash, a "
    "silver filigree tiara with faceted sapphires, pearl drop earrings."
)


# ---------------------------------------------------------------------------
# Rounds 1-2 predate this driver: each was ONE batch request (batch_size=5) with
# a single prompt, recorded here verbatim so the prompt archive is complete.
# ---------------------------------------------------------------------------
LEGACY_ROUNDS: dict[int, dict] = {
    1: {
        "engine": "zimage", "size": (1024, 1024), "steps": 8, "batch": 5, "seed": 100,
        "note": "baseline (single batch of 5)",
        "prompt": (
            "Museum-quality bone china princess doll, collector-grade photorealistic portrait photograph. "
            "Porcelain skin with soft translucency, fine hand-painted rosy blush, delicate hand-painted "
            "arched eyebrows, long curled eyelashes, glossy lips. Intricate white lace gown with woven "
            "silver threads, beaded pearl bodice, soft blue satin sash, tiny pearl buttons. Silver tiara "
            "with small diamonds, pearl drop earrings, a single sapphire pendant. Painted porcelain hands "
            "with slender jointed fingers. Centered head-and-shoulders portrait, soft diffused studio light "
            "with gentle specular highlight on the porcelain cheek, dark blue-black velvet backdrop, "
            "shallow depth of field, 85mm macro lens, ultra-detailed surface glaze, subtle craquelure, "
            "no text"
        ),
    },
    2: {
        "engine": "zimage", "size": (1024, 1360), "steps": 8, "batch": 5, "seed": 200,
        "note": "material realism + glass eyes + 3:4 (single batch of 5)",
        "prompt": (
            "Photorealistic close-up photograph of a handcrafted fine bone china princess doll, genuine "
            "material realism. Translucent cream-white porcelain face with visible subsurface scattering, "
            "glossy fired glaze with crisp specular highlights, faint hairline craquelure, delicate "
            "hand-painted pink blush fading at the edges, hand-painted eyebrows with individual hair "
            "strokes, glossy glass doll eyes with dark brown irises, deep pupils and sharp catchlights, "
            "sculpted eyelids with soft shadow, subtle sculpted lips with glaze pooling. Realistic "
            "miniature ball-jointed porcelain arms. Heavily detailed white lace gown with visible thread "
            "structure, hand-sewn pearl beading, pale blue silk sash, silver filigree tiara set with "
            "sapphire and tiny diamonds, real pearl drop earrings. Soft large softbox key light from upper "
            "left, gentle rim light on porcelain cheek and tiara, dark desaturated teal studio backdrop, "
            "medium format camera, 120mm macro lens, shallow depth of field, visible material texture, "
            "no text, no watermark"
        ),
    },
}

ROUNDS: dict[int, dict] = {
    3: {
        "engine": "zimage", "size": (1024, 1360), "steps": 8,
        "note": "material translucency + elegant proportions + 5 distinct camera setups",
        "shots": [
            {"name": "front", "seed": 300,
             "prompt": BASE + ", centered head-and-shoulders portrait, facing camera, large softbox key light from upper left, soft rim light on the tiara, deep muted teal backdrop"},
            {"name": "three-quarter-fan", "seed": 310,
             "prompt": BASE + ", three-quarter view, holding a white lace fan near her cheek, soft key light from the right, gentle shadow under the jaw, warm grey backdrop"},
            {"name": "profile-translucent", "seed": 320,
             "prompt": BASE + ", strict side profile with the light behind the doll so light glows through the thin porcelain of the ear, cheek and neck, dark backdrop, strong rim light"},
            {"name": "hands-lap", "seed": 330,
             "prompt": BASE + ", waist-up, seated with both porcelain hands resting on her lap, ball-jointed wrist seams visible, balanced soft light, muted blue-grey backdrop"},
            {"name": "full-figure", "seed": 340,
             "prompt": BASE + ", full figure standing on a velvet cushion, complete gown with train visible, low-key museum lighting, distant soft spotlight, dark hall backdrop"},
        ],
    },
    4: {
        "engine": "zimage", "size": (1024, 1360), "steps": 8,
        "note": "no equipment words, adult proportions, single pearl strand, anti-artifact terms",
        "shots": [
            {"name": "beauty-portrait", "seed": 400,
             "prompt": BASE4 + ", tight beauty portrait, eye level, quiet grey-blue backdrop, soft falloff on the shoulders"},
            {"name": "fan-three-quarter", "seed": 410,
             "prompt": BASE4 + ", three-quarter view holding a white lace fan open beside her face, warm neutral backdrop, gentle shadow under the jaw"},
            {"name": "rimlight-profile", "seed": 420,
             "prompt": BASE4 + ", near-profile with warm light travelling along the porcelain rim of the cheek and ear, dark charcoal backdrop"},
            {"name": "seated-hands", "seed": 430,
             "prompt": BASE4 + ", seated waist-up, both porcelain hands folded on her lap with visible ball-joint seams at the wrists, soft even light, muted blue-grey backdrop"},
            {"name": "full-figure-cushion", "seed": 440,
             "prompt": BASE4 + ", full figure standing on a velvet cushion, gown and short train fully visible, low-key museum light, dark hall backdrop, slight low camera angle"},
        ],
    },
    5: {
        "engine": "zimage", "size": (1024, 1360), "steps": 12,
        "note": "figurine + adult princess face, steps 12, ivory pearls, fabric folds",
        "shots": [
            {"name": "portrait", "seed": 500, "prompt": BASE5 + ", tight beauty portrait, eye level, cool grey backdrop"},
            {"name": "bouquet", "seed": 510,
             "prompt": BASE5 + ", three-quarter view holding a small bouquet of white porcelain flowers, warm neutral backdrop, soft shadow under the jaw"},
            {"name": "fan", "seed": 520,
             "prompt": BASE5 + ", three-quarter view with an open white lace fan beside her face, soft even light, muted teal backdrop"},
            {"name": "seated", "seed": 530,
             "prompt": BASE5 + ", seated waist-up with both hands folded on her lap, visible ball-joint seams at the wrists, soft even light, blue-grey backdrop"},
            {"name": "full-figure", "seed": 540,
             "prompt": BASE5 + ", full figure standing on a velvet cushion, complete gown with lace fabric folds and a short train, low-key museum light, dark hall backdrop"},
        ],
    },
    6: {
        "engine": "zimage", "size": (1024, 1360), "steps": 16,
        "note": "final z-image round: steps 16 + micro-detail demands + macro close-up shot",
        "shots": [
            {"name": "macro-face", "seed": 600,
             "prompt": BASE6 + ", extreme macro close-up filling the frame with the face and tiara, razor-sharp focus on the porcelain cheek, individual eyelashes and glaze micro-texture clearly visible, soft grey backdrop"},
            {"name": "bouquet", "seed": 610,
             "prompt": BASE6 + ", three-quarter view holding a small bouquet of white porcelain flowers, warm neutral backdrop, soft shadow under the jaw"},
            {"name": "fan", "seed": 620,
             "prompt": BASE6 + ", three-quarter view with an open white lace fan beside her face, soft even light, muted teal backdrop"},
            {"name": "seated-hands", "seed": 630,
             "prompt": BASE6 + ", seated waist-up with both hands folded on her lap, ball-joint seams at the wrists clearly visible, soft even light, blue-grey backdrop"},
            {"name": "full-figure", "seed": 640,
             "prompt": BASE6 + ", full figure standing on a velvet cushion, complete gown with lace fabric folds and a short train, low-key museum light, dark hall backdrop"},
        ],
    },
    7: {
        "engine": "qwen", "size": (1024, 1360), "steps": 24, "cfg": 3.0, "negative": NEG_Q,
        "note": "engine switch to Qwen-Image 2512; pristine glaze, no cracks, 3 shots",
        "shots": [
            {"name": "macro-upper", "seed": 700,
             "prompt": BASE_Q + ", tight three-quarter upper-body framing filling most of the frame, the tiara and the lace bodice in sharp focus"},
            {"name": "bouquet", "seed": 710,
             "prompt": BASE_Q + ", three-quarter view holding a small bouquet of white porcelain roses, warm neutral backdrop, soft shadow under the jaw"},
            {"name": "seated-hands", "seed": 720,
             "prompt": BASE_Q + ", seated, both hands folded on her lap, the ball-joint seams and painted fingernails clearly visible, soft even light, blue-grey backdrop"},
        ],
    },
    8: {
        "engine": "qwen", "size": (1152, 1536), "steps": 28, "cfg": 3.2, "negative": NEG_Q,
        "note": "higher resolution + more steps + chiaroscuro light + brocade/gold-thread costume",
        "shots": [
            {"name": "rembrandt-portrait", "seed": 800,
             "prompt": BASE_Q8 + ", three-quarter beauty portrait with Rembrandt lighting, the tiara and "
             "the pearl earring catching the key light, simple dark backdrop"},
            {"name": "hands-embroidery", "seed": 810,
             "prompt": BASE_Q8 + ", close-up of the doll's hands folded over the embroidered bodice, "
             "macro detail of the ball-joint seams, the gold thread and the pearl beading, soft light"},
            {"name": "full-figure", "seed": 820,
             "prompt": BASE_Q8 + ", full figure standing on a stone plinth, complete gown with train, "
             "dramatic side light from the left, deep shadows, dark exhibition hall backdrop"},
        ],
    },
    9: {
        "engine": "qwen", "size": (1152, 1536), "steps": 30, "cfg": 3.5, "negative": NEG_Q,
        "note": "microscopic glaze texture, anti-CGI, focus-stacked macro framing",
        "shots": [
            {"name": "face-macro", "seed": 900,
             "prompt": BASE_Q9 + ", the porcelain face and the tiara fill the frame, cropped just below "
             "the collarbone, the glaze micro-texture and the painted eyelashes visible at pixel level, "
             "soft key light from the left"},
            {"name": "fan-portrait", "seed": 910,
             "prompt": BASE_Q9 + ", three-quarter portrait with an open lace fan held near the shoulder, "
             "warm side light, the embroidered sleeve in sharp focus"},
            {"name": "bust-rimlight", "seed": 920,
             "prompt": BASE_Q9 + ", bust portrait with a strong rim light behind her so the thin porcelain "
             "of the ears and neck glows, near-black backdrop, delicate shadow detail"},
        ],
    },
    10: {
        "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_Q,
        "note": "jewellery/weave macro + window light; resolution and steps up again",
        "shots": [
            {"name": "tiara-macro", "seed": 1000,
             "prompt": BASE_Q10 + ", extreme close-up of the tiara and the hair, milled silver filigree "
             "and faceted sapphires filling the upper half of the frame, razor-sharp metal edges"},
            {"name": "embroidery-macro", "seed": 1010,
             "prompt": BASE_Q10 + ", extreme close-up of the embroidered bodice and the doll's hands, "
             "gold thread, seed pearls and the wrist joint seam in sharp macro focus, shallow depth of field"},
            {"name": "window-light", "seed": 1020,
             "prompt": BASE_Q10 + ", three-quarter portrait in soft north window light with a pale rose "
             "brocade gown, gentle shadow gradient across the porcelain cheek, quiet interior backdrop"},
        ],
    },
    11: {
        "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_Q,
        "note": "final round: framing-first prompts, minimal costume text, three deliberately different shots",
        "shots": [
            {"name": "tiara-macro", "seed": 1100,
             "prompt": "Extreme macro photograph: ONLY the silver filigree tiara and the top of the brown "
             "hair fill the entire frame, cropped tight on the crown, nothing else visible. " + BASE_Q11 +
             ". Every milled silver edge, every prong and every facet of the sapphires is razor sharp, "
             "the metal shows tiny polishing marks, the stones show internal refraction. "
             "Dark neutral background, shallow depth of field"},
            {"name": "hand-macro", "seed": 1110,
             "prompt": "Extreme macro photograph: ONLY the doll's porcelain hands and the lace cuff fill "
             "the frame, cropped tight on the hands, no face visible. " + BASE_Q11 +
             ". The ball-joint seam at the wrist, the painted fingernails, the individual lace threads "
             "and a few seed pearls are razor sharp, shallow depth of field".replace("BASE_Q11", ""),
             "prompt_suffix": ""},
            {"name": "portrait-velvet", "seed": 1120,
             "prompt": "Elegant half-body studio portrait, head and shoulders centred in frame. " + BASE_Q11 +
             " She wears a deep royal-blue velvet gown with silver embroidery and a diamond-set tiara, "
             "pearl drop earrings, a single strand of pearls. Soft directional key light from the upper "
             "left, gentle rim light on the porcelain cheek, clean dark grey backdrop, tack-sharp focus",
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# Round 12 base: kill the CGI / wax look.
# Diagnosis of R7-R11: every one of those bases kept the perfection words
# "pristine / flawless / perfectly smooth fired glaze / completely clean" while
# ALSO asking for microscopic texture.  The perfection words won -- the face came
# back airbrushed, with no readable specular highlight, i.e. exactly the "cgi,
# 3d render" the negative prompt was trying to forbid.  A glaze reads as glass
# because of *small sharp highlights*, not because it is smooth.
# R12 therefore: (a) deletes the perfection words, (b) *describes* the physical
# glaze instead (pooled glaze, micro bubbles, polishing marks, warm translucency),
# (c) asks for ONE CRISP KEY LIGHT so every highlight is small and sharp, and
# (d) keeps the full eye description in ALL three shots -- R11 lost the eyes
# because the macro crop had dropped every facial word.
# ---------------------------------------------------------------------------
BASE_Q12 = (
    "Photorealistic studio photograph of a handcrafted ball-jointed bone china doll of a princess, "
    "photographed like a real object on a table. Ivory porcelain covered in a fired glaze that behaves "
    "like real glass: bright crisp specular highlights where the light strikes, faint undulation in the "
    "glaze where it pooled and ran, microscopic air bubbles and the finest polishing marks caught just "
    "under the surface, warm translucency glowing through the thin porcelain of the ears and the "
    "fingertips, small handmade irregularities, but no cracks and no damage. Visible ball-joint seams at "
    "the neck and the wrists. Refined adult doll face: oval face, high cheekbones, straight nose bridge, "
    "serene softly closed lips with glaze pooling on the lower lip. Open glass doll eyes of realistic "
    "size, dark brown iris with a ring of fine radial fibres, clearly defined pupil, one sharp "
    "rectangular window catchlight in each eye, sculpted eyelids, individually painted eyelashes, "
    "eyebrows painted hair by hair. One crisp key light from the upper left so that every highlight is "
    "small and sharp, deep clean falloff, subtle warm bounce on the shadow side, sharp focus, medium "
    "format camera, 120mm macro lens, natural sensor grain, no digital sharpening"
)

# R11 gave us two concrete artefacts to forbid: a macro crop with no eyes at all,
# and a two-hand crop that grew ten-odd fingers finished with rainbow nail art
# (chromatic-aberration smears).  Both are named here.
NEG_Q12 = NEG_Q + (
    ", nail polish, coloured fingernails, painted nail art, rainbow iridescence, chromatic aberration, "
    "duplicated fingers, six fingers, fused fingers, extra knuckles, blank eyes, eyeless, closed "
    "eyelids, empty eye sockets, mannequin, wax figure, airbrushed, matte chalky clay"
)

ROUNDS[12] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_Q12,
    "note": "de-CGI round: drop pristine/flawless, describe the physical glaze, one crisp key light; "
            "keep the eyes in every crop; simplify the hand to ONE hand",
    "shots": [
        {"name": "eyes-tiara", "seed": 1200,
         "prompt": "Close-up beauty photograph framed from the top of the tiara down to the collarbone, "
         "the face centred, the eyes on the upper third line, open and looking just past the lens. "
         + BASE_Q12 +
         " She wears a silver filigree tiara set with faceted diamond-like stones and pearl drop "
         "earrings; bare porcelain neck and shoulders. Dark charcoal backdrop, tack-sharp focus on the "
         "eyes, shallow depth of field"},
        {"name": "hand-single", "seed": 1210,
         "prompt": "Extreme macro photograph cropped tight on ONE porcelain hand. Exactly one hand is in "
         "the frame: a left hand resting palm down and relaxed on white lace, exactly five slender "
         "fingers slightly apart, each finger a single straight segment ending in one clean glossy ivory "
         "fingernail, the ball joint seam clearly visible at the wrist, a lace cuff with seed pearls at "
         "the edge of the frame. " + BASE_Q12 +
         ". Razor-sharp focus on the knuckles, shallow depth of field, dark background"},
        {"name": "portrait-specular", "seed": 1220,
         "prompt": "Elegant half-body studio portrait, head and shoulders centred in frame, the doll "
         "turned a quarter away from the light so one cheek catches it. " + BASE_Q12 +
         " She wears a deep royal-blue velvet gown with silver-thread embroidery and a diamond-set "
         "tiara, pearl drop earrings, a single strand of pearls. The crisp key light leaves a small "
         "bright highlight on the cheekbone, the nose tip and the lower lip, and a warm translucent "
         "glow along the rim of the ear. Clean dark grey backdrop, tack-sharp focus on the eyes"},
    ],
}

# ---------------------------------------------------------------------------
# Round 13: back to the proven baseline.
# R11 and R12 were both regressions.  The user's review of R8-R10 settled it:
# R10 is the quality peak, and R11/R12 lost it by *removing* the material and
# craft vocabulary that R8-R10 had built up.  R13 therefore does NOT invent a
# new base -- it reuses BASE_Q10 verbatim, and only adds back the two things
# that were independently proven to work:
#   * framing-first wording (R11's one good idea) -- but WITHOUT deleting any
#     material vocabulary, which is what actually broke R11;
#   * the "ONE hand / exactly five fingers" hand wording (R12's one good result).
# It also keeps R10's soft window light and never names a light fixture.
#
# Shot 1 is a deliberate control: R10's winning prompt with a NEW seed.  If the
# R10 water level does not reproduce under a different seed, then R10's quality
# was seed luck and the whole baseline needs rethinking.
# ---------------------------------------------------------------------------
BASE_Q13_ROSE = (
    ", three-quarter portrait in soft north window light with a pale rose brocade gown, gentle shadow "
    "gradient across the porcelain cheek, quiet interior backdrop"
)

ROUNDS[13] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_Q,
    "note": "back to the BASE_Q10 baseline; framing-first without deleting material vocabulary; "
            "R10 control shot at a new seed + two true macros",
    "shots": [
        # Control: byte-for-byte the R10 winning prompt, new seed 1300.
        {"name": "window-light-control", "seed": 1300, "prompt": BASE_Q10 + BASE_Q13_ROSE},
        # True macro #1 -- crown only, cropped above the eyebrows so the eyeless-
        # face failure of R11 simply cannot happen (there is no face in frame).
        {"name": "tiara-macro", "seed": 1310,
         "prompt": "Close-up photograph cropped tight on the silver filigree tiara and the top of her "
         "head: the jewelled crown fills the frame edge to edge and is cut off just above the eyebrows, "
         "no face and no eyes are visible. " + BASE_Q10 +
         " Every milled silver edge, every prong and every facet of the sapphires is razor sharp, the "
         "metal shows tiny polishing marks, the stones show internal refraction. Dark neutral "
         "background, shallow depth of field"},
        # True macro #2 -- R12's proven single-hand wording on the R10 base.
        {"name": "hand-macro", "seed": 1320,
         "prompt": "Extreme macro photograph cropped tight on ONE porcelain hand. Exactly one hand is "
         "in the frame: a left hand resting palm down and relaxed on white lace, exactly five slender "
         "fingers slightly apart, each finger a single straight segment ending in one clean glossy "
         "ivory fingernail, the ball joint seam clearly visible at the wrist, a lace cuff with seed "
         "pearls at the edge of the frame. " + BASE_Q10 +
         ". Razor-sharp focus on the knuckles, shallow depth of field, dark background"},
    ],
}

# ---------------------------------------------------------------------------
# Round 14: the resolution ablation.
# R13 locked the baseline: BASE_Q10 reproduces across seeds, and Qwen will not
# give us a true macro while the material vocabulary is present.  So the detail
# bottleneck is now pixel count, not prompt wording.  R14 therefore holds the
# prompt AND the seed fixed and varies only the resolution -- 1.25x, 1.40x and
# 1.50x linear (3.4 / 4.3 / 4.9 MP) -- to find where the RTX 4060 Ti 8 GB runs
# out and whether extra pixels actually buy extra detail.
# Sizes are multiples of 16 to keep the VAE stride happy and the aspect ratio
# within 0.3% of the 1280x1712 baseline.
# ---------------------------------------------------------------------------
_R14_PROMPT = BASE_Q10 + BASE_Q13_ROSE

ROUNDS[14] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_Q,
    "note": "resolution ablation at fixed prompt and fixed seed 1400: 1.25x / 1.40x / 1.50x",
    "shots": [
        {"name": "res-125", "seed": 1400, "size": (1600, 2144), "timeout": 3600,
         "prompt": _R14_PROMPT},
        {"name": "res-140", "seed": 1400, "size": (1792, 2400), "timeout": 4500,
         "prompt": _R14_PROMPT},
        {"name": "res-150", "seed": 1400, "size": (1920, 2560), "timeout": 5400,
         "prompt": _R14_PROMPT},
    ],
}

# ---------------------------------------------------------------------------
# Round 15: composition variety, driven by CANVAS SHAPE.
# R10 and R13 both produced three near-identical half-body portraits -- that is
# the project's one genuinely unaddressed defect.  Prompt wording cannot fix it
# (R10/R13 proved Qwen ignores crop instructions), but R14 turned up a usable
# side effect: changing the canvas re-plans the composition.  So R15 keeps the
# proven BASE_Q10 text and manipulates the ASPECT RATIO instead of the wording:
#   * 1:2 ultra-tall  -> forces a full-length standing figure
#   * 1:1 square      -> forces a seated / mid-shot composition
#   * 3:4 as before   -> a back view, an angle this project has never shot
# Resolution stays at the 1280-wide sweet spot (R14 proved more pixels buy
# nothing but time).
# ---------------------------------------------------------------------------
ROUNDS[15] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_Q,
    "note": "composition variety via canvas aspect ratio: ultra-tall full figure, square "
            "seated, and the first back view of the project",
    "shots": [
        {"name": "full-figure", "seed": 1500, "size": (1024, 2048), "timeout": 3600,
         "prompt": BASE_Q10 + ", full-length standing figure: the entire doll from the top of the tiara "
         "down to the hem of the gown and her porcelain slippers is inside the frame, standing on a low "
         "velvet cushion, the whole gown and its short train clearly visible, low-key museum lighting "
         "with a distant soft spotlight, dark hall backdrop, slight low camera angle"},
        {"name": "back-view", "seed": 1510, "size": (1280, 1712), "timeout": 3600,
         "prompt": BASE_Q10 + ", seen from behind and a little to her left in a three-quarter back view: "
         "the coiled hair and the back of the silver filigree tiara are in sharp focus, the back of the "
         "gown shows the laced bodice, the pearl buttons and the long train, soft north window light, "
         "quiet interior backdrop"},
        {"name": "seated-square", "seed": 1520, "size": (1600, 1600), "timeout": 4200,
         "prompt": BASE_Q10 + ", seated three-quarter view at a small side table, both porcelain hands "
         "resting on her lap with the ball-joint seams at the wrists clearly visible, a white lace fan "
         "lying on the table, soft north window light, pale grey backdrop"},
    ],
}

# ---------------------------------------------------------------------------
# Round 16: the closing round.
# Everything R12-R15 established, applied at once:
#   * BASE_Q10 is the authority (R13); it must not be edited;
#   * composition is chosen with the CANVAS ASPECT RATIO, not with wording (R15);
#   * resolution stays at the proven width (R14: more pixels buy only time);
#   * the last untested sampling lever is the step count -- 32 -> 40.
# The three shots are the three compositions the project now knows how to hit
# reliably, so this round doubles as the final deliverable set.
# ---------------------------------------------------------------------------
ROUNDS[16] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 40, "cfg": 3.5, "negative": NEG_Q,
    "note": "closing round: BASE_Q10 + aspect-driven composition x steps 40; final deliverable set",
    "shots": [
        {"name": "final-portrait", "seed": 1600, "size": (1280, 1712), "steps": 40, "timeout": 3600,
         "prompt": BASE_Q10 + BASE_Q13_ROSE},
        {"name": "final-full-figure", "seed": 1610, "size": (1024, 2048), "steps": 40, "timeout": 3600,
         "prompt": BASE_Q10 + ", full-length standing figure: the entire doll from the top of the tiara "
         "down to the hem of the gown and her porcelain slippers is inside the frame, standing on a low "
         "velvet cushion, the whole gown and its short train clearly visible, low-key museum lighting "
         "with a distant soft spotlight, dark hall backdrop, slight low camera angle"},
        {"name": "final-seated", "seed": 1620, "size": (1600, 1600), "steps": 40, "timeout": 4200,
         "prompt": BASE_Q10 + ", seated three-quarter view at a small side table, both porcelain hands "
         "resting on her lap with the ball-joint seams at the wrists clearly visible, a white lace fan "
         "lying on the table, soft north window light, pale grey backdrop"},
    ],
}

# ===========================================================================
# 第三阶段（R17+）：主题变更 —— 骨瓷国公主 / 东方古典美女
# ===========================================================================
# 方法：R13 已证明"质量来自 BASE_Q10 的材质词汇"。所以本次改主题**只替换文化要素**
# （面容 / 发式 / 服饰 / 珠宝），材质核心（釉面、半透光、球关节、显微质感、镜头与光比
# 语言）**逐字继承**，其余一切不动：同引擎、同 32 steps、同 cfg、同 NEG_Q、
# 同 R15 的画布长宽比构图法、微距仍走裁切。
#
# 刻意保留的两处（有实验依据，不要"顺手优化"）：
#   * "Pristine flawless ... perfectly smooth fired glaze" 等完美词 —— R13 证明它们
#     与 R10/R16 的高质量共存，R12 对它们的归因是错的；
#   * BASE_Q8 的 "one strong key light"（在 chiaroscuro 光比描述内部）—— R13 证明安全。
# 刻意规避的三处（R12/R15 的教训）：
#   * 不单独下"锐利高光"的照明指令；
#   * 不单独强调眼睛大小（眼睛只出现在整体比例句里）；
#   * 不写视角/裁切措辞（构图一律交给画布长宽比）。
# ===========================================================================
BASE_E = (
    "Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical "
    "princess, photographed like a real physical object under studio light. "
    "Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights, "
    "delicate warm translucency at the thin porcelain of the ears and fingertips, microscopic surface "
    "texture, completely clean and dust-free. Visible ball-joint seams at the neck and wrists. "
    # --- 面容：东方古典，全部写进"整体比例"句（R12 教训）---
    "An elegant Eastern classical beauty with refined adult proportions: a delicate oval face with a "
    "softly tapered jaw, fine arched willow-leaf eyebrows, a slender straight nose bridge, a small "
    "rosebud mouth with serene closed lips, almond eyes of realistic size with gently upswept outer "
    "corners and a subtle crease, dark brown irises, individually painted eyelashes, eyebrows painted "
    "hair by hair, the faintest soft blush on the cheeks. "
    # --- 发式 ---
    "Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples, "
    "held by a gold filigree hairpin set with jade and a dangling pearl ornament. "
    # --- 服饰：交领、广袖、织金、云肩、玉带 ---
    "She wears a classical Eastern gown of ivory silk with a crossed collar, wide flowing sleeves and a "
    "broad sash, woven with gold-thread cloud and peony patterns, its edges densely embroidered and "
    "trimmed with hundreds of tiny seed pearls stitched one by one, a jade-inlaid gold filigree belt, "
    "an embroidered cloud collar over the shoulders, and carved jade earrings with gold filigree. "
    "Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows, sharp "
    "focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field, "
    "seamless neutral backdrop. "
    # --- 工艺写实：东方材质（玉 / 金 / 丝）---
    "Extravagant craft: ivory silk brocade with raised gold-thread embroidery, dense silk embroidery "
    "with individual visible threads, seed pearls stitched one by one, carved jade with a soft waxy "
    "lustre and internal veining, gold filigree with milled edges, a heavy ceremonial headdress with "
    "enamelled details. Sculptural chiaroscuro studio lighting with one strong key light and deep "
    "natural falloff, subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus "
    "on the face, extremely fine texture. Extremely fine porcelain surface: microscopic glaze texture "
    "with faint polishing marks, a few microscopic bubbles suspended inside the glaze, gentle colour "
    "variation in the ivory, absolutely no CGI smoothness. Photographed with a 100mm macro lens at "
    "f/8, focus stacked, ultra high resolution scan quality, natural sensor grain. Jewellery realism: "
    "engraved gold filigree with crisp milled edges, carved jade showing internal veining, seed pearls "
    "with subtle orient and nacre rings, metal prongs and hinges clearly readable. Fabric realism: "
    "silk with a visible woven weft, embroidered satin, linen-backed inner layers, visible individual "
    "stitches, slightly irregular handmade quality"
)

ROUNDS[17] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_Q,
    "note": "phase 3 opens: theme switched to Eastern classical (骨瓷国公主); BASE_Q10 material core "
            "kept verbatim, only face/hair/costume/jewellery replaced",
    "shots": [
        {"name": "portrait", "seed": 1700, "size": (1280, 1712), "timeout": 3600,
         "prompt": BASE_E + ", three-quarter portrait in soft north window light, gentle shadow gradient "
         "across the porcelain cheek, quiet neutral interior backdrop"},
        {"name": "full-figure", "seed": 1710, "size": (1024, 2048), "timeout": 3600,
         "prompt": BASE_E + ", full-length standing figure: the entire doll from the top of the hair bun "
         "down to the hem of the gown and her porcelain slippers is inside the frame, standing on a low "
         "carved wooden stand, the whole gown and its train clearly visible, low-key museum lighting "
         "with a distant soft spotlight, dark hall backdrop, slight low camera angle"},
        {"name": "seated", "seed": 1720, "size": (1600, 1600), "timeout": 4200,
         "prompt": BASE_E + ", seated three-quarter view at a small rosewood table, both porcelain hands "
         "resting on her lap with the ball-joint seams at the wrists clearly visible, a round silk fan "
         "lying on the table, a carved wooden folding screen softly out of focus behind her, soft north "
         "window light"},
    ],
}

# ---------------------------------------------------------------------------
# Round 18.  R17 delivered the Eastern theme in one round, with one miss: the
# full-figure shot came back cropped at the waist.  BASE_E is frozen (its text
# is already archived verbatim inside ROUNDS[17]) so R18 adds new constants
# instead of editing it.
#
# Two targeted changes:
#  1. Full-figure: R17 confirmed that R10/R13's rule -- long costume prose pulls
#     the camera in -- is theme-independent.  So for that one shot the costume
#     INVENTORY is removed entirely (only the material/craft nouns survive) and
#     the canvas is pushed taller (880x2048, 1:2.33).  This isolates the cause.
#  2. Jewellery: add the two classical pieces R17 lacked -- 花钿 (a forehead
#     ornament) and 璎珞 (a jade-and-pearl necklace) -- and pin the cloud
#     collar to the ivory/gold palette, since R17's came back grey.
# ---------------------------------------------------------------------------
BASE_E18 = BASE_E + (
    ", a delicate forehead ornament of tiny gold and jade flowers set between the eyebrows, a beaded "
    "necklace of carved jade beads and pearls resting on the collarbone, the cloud collar worked in "
    "ivory silk and gold thread to match the gown"
)

# Slim variant for the wide shots: material core + face + hair + craft nouns only,
# with the whole costume inventory (collars, sleeves, sash, belt, trim) removed.
BASE_E18_SLIM = (
    "Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical "
    "princess, photographed like a real physical object under studio light. "
    "Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights, "
    "delicate warm translucency at the thin porcelain of the ears and fingertips, microscopic surface "
    "texture, completely clean and dust-free. Visible ball-joint seams at the neck and wrists. "
    "An elegant Eastern classical beauty with refined adult proportions: a delicate oval face with a "
    "softly tapered jaw, fine arched willow-leaf eyebrows, a slender straight nose bridge, a small "
    "rosebud mouth with serene closed lips, almond eyes of realistic size with gently upswept outer "
    "corners, dark brown irises, the faintest soft blush on the cheeks. Glossy black hair dressed in a "
    "classical high coiled bun held by a gold filigree hairpin set with jade and a dangling pearl "
    "ornament. Fine art studio lighting from the upper left, deep but clean shadows, sharp focus, "
    "medium format camera, 120mm macro lens, natural sensor grain, no digital sharpening. Ivory silk "
    "with a visible woven weft, raised gold-thread embroidery, carved jade with a soft waxy lustre, "
    "engraved gold filigree with milled edges, seed pearls, extremely fine porcelain surface, "
    "absolutely no CGI smoothness"
)

ROUNDS[18] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_Q,
    "note": "fix the full-figure shot by cutting the costume inventory and pushing the canvas taller; "
            "add 花钿 forehead ornament and 璎珞 jade-pearl necklace",
    "shots": [
        {"name": "portrait", "seed": 1800, "size": (1280, 1712), "timeout": 3600,
         "prompt": BASE_E18 + ", three-quarter portrait in soft north window light, gentle shadow "
         "gradient across the porcelain cheek, quiet neutral interior backdrop"},
        {"name": "full-figure", "seed": 1810, "size": (880, 2048), "timeout": 3600,
         "prompt": "Full-length photograph: the entire doll from the top of the hair bun down to the hem "
         "of the gown and her porcelain slippers is inside the frame, standing upright on a low carved "
         "wooden stand, the whole robe and its train visible, low-key museum lighting with a distant "
         "soft spotlight, dark hall backdrop, slight low camera angle. " + BASE_E18_SLIM},
        {"name": "seated", "seed": 1820, "size": (1600, 1600), "timeout": 4200,
         "prompt": BASE_E18 + ", seated three-quarter view at a small rosewood table, both porcelain "
         "hands resting on her lap with the ball-joint seams at the wrists clearly visible, a round silk "
         "fan lying on the table, a carved wooden folding screen softly out of focus behind her, soft "
         "north window light"},
    ],
}

# ---------------------------------------------------------------------------
# Round 19: a Tang-dynasty variant, so the project gains more than one Eastern
# silhouette.  R17/R18 both produced the same "crossed collar + wide sleeves +
# brocade" look.  R19 swaps ONLY the garment-shape sentence for a Tang one
# (high-waisted ruqun skirt + short jacket + sheer gauze pibo stole) and keeps
# everything else -- material core, craft nouns, face, hair, jewellery.
#
# 花钿 (the forehead ornament) is a Tang fashion, so it is re-stated here in its
# own context: R17/R18 both failed to render it in a generic classical setting,
# and this round tests whether context is what it needs.
#
# The garment sentence is replaced by exact string substitution rather than by
# rewriting the base, so nothing else can drift.  The asserts below make a
# silent no-op substitution impossible.
# ---------------------------------------------------------------------------
_E18_COSTUME = (
    "She wears a classical Eastern gown of ivory silk with a crossed collar, wide flowing sleeves and a "
    "broad sash, woven with gold-thread cloud and peony patterns, its edges densely embroidered and "
    "trimmed with hundreds of tiny seed pearls stitched one by one, a jade-inlaid gold filigree belt, "
    "an embroidered cloud collar over the shoulders, and carved jade earrings with gold filigree."
)
_E19_COSTUME = (
    "She wears a Tang-dynasty style gown: a high-waisted ivory silk skirt tied under the arms with a "
    "gold-thread sash, a short crossed-collar silk jacket, and a long sheer gauze scarf draped over the "
    "shoulders and falling in a wide loop; the silk is woven with gold-thread peony and cloud patterns "
    "and its edges are trimmed with hundreds of tiny seed pearls stitched one by one. A jade-inlaid "
    "gold filigree belt, an embroidered cloud collar, and carved jade earrings with gold filigree."
)
assert _E18_COSTUME in BASE_E18, "R19: costume sentence not found -- substitution would be a no-op"
BASE_E19 = BASE_E18.replace(_E18_COSTUME, _E19_COSTUME) + (
    ", a gilded flower ornament painted on the centre of the forehead between the eyebrows"
)

_E18_SLIM_MATERIALS = (
    "Ivory silk with a visible woven weft, raised gold-thread embroidery, carved jade with a soft waxy "
    "lustre, engraved gold filigree with milled edges, seed pearls, extremely fine porcelain surface, "
    "absolutely no CGI smoothness"
)
_E19_SLIM_MATERIALS = (
    "Ivory silk with a visible woven weft, sheer gauze with a fine open weave, raised gold-thread "
    "embroidery, carved jade with a soft waxy lustre, engraved gold filigree with milled edges, seed "
    "pearls, extremely fine porcelain surface, absolutely no CGI smoothness"
)
assert _E18_SLIM_MATERIALS in BASE_E18_SLIM, "R19: slim materials not found"
BASE_E19_SLIM = BASE_E18_SLIM.replace(_E18_SLIM_MATERIALS, _E19_SLIM_MATERIALS)

ROUNDS[19] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_Q,
    "note": "Tang-dynasty variant: high-waisted ruqun + sheer gauze pibo stole + 花钿 forehead "
            "ornament; only the garment-shape sentence changes",
    "shots": [
        {"name": "portrait", "seed": 1900, "size": (1280, 1712), "timeout": 3600,
         "prompt": BASE_E19 + ", three-quarter portrait in soft north window light, gentle shadow "
         "gradient across the porcelain cheek, quiet neutral interior backdrop"},
        {"name": "full-figure", "seed": 1910, "size": (880, 2048), "timeout": 3600,
         "prompt": "Full-length photograph: the entire doll from the top of the hair bun down to the hem "
         "of the skirt and her porcelain slippers is inside the frame, standing upright on a low carved "
         "wooden stand, the high-waisted skirt, the trailing gauze scarf and the hem are all visible, "
         "low-key museum lighting with a distant soft spotlight, dark hall backdrop, slight low camera "
         "angle. " + BASE_E19_SLIM},
        {"name": "seated", "seed": 1920, "size": (1600, 1600), "timeout": 4200,
         "prompt": BASE_E19 + ", seated three-quarter view at a small rosewood table, both porcelain "
         "hands resting on her lap with the ball-joint seams at the wrists clearly visible, a round silk "
         "fan lying on the table, a carved wooden folding screen softly out of focus behind her, soft "
         "north window light"},
    ],
}

# ---------------------------------------------------------------------------
# Round 20: Eastern craft macros -- by cropping, never by prompt.
# R10/R11/R13 proved Qwen ignores every macro/crop instruction while the material
# prose is present, and R15 solved the same problem for the Western phase by
# cropping a high-resolution render.  R20 does exactly that for the Eastern
# phase: three renders at the 3.43 MP detail sweet spot R14 identified, framed
# only via the canvas aspect ratio, and their crops become the macro set.
# No new wording is invented for this round -- the bases are reused as-is.
# ---------------------------------------------------------------------------
ROUNDS[20] = {
    "engine": "qwen", "size": (1600, 1600), "steps": 32, "cfg": 3.5, "negative": NEG_Q,
    "note": "high-resolution plates for the Eastern macro set (crop source); no new prompt wording",
    "shots": [
        {"name": "plate-portrait", "seed": 2000, "size": (1600, 2144), "timeout": 4200,
         "prompt": BASE_E18 + ", three-quarter portrait in soft north window light, gentle shadow "
         "gradient across the porcelain cheek, quiet neutral interior backdrop"},
        {"name": "plate-seated", "seed": 2010, "size": (1600, 1600), "timeout": 4200,
         "prompt": BASE_E18 + ", seated three-quarter view at a small rosewood table, both porcelain "
         "hands resting on her lap with the ball-joint seams at the wrists clearly visible, a round silk "
         "fan lying on the table, a carved wooden folding screen softly out of focus behind her, soft "
         "north window light"},
        {"name": "plate-figure", "seed": 2020, "size": (1200, 2560), "timeout": 4200,
         "prompt": "Full-length photograph: the entire doll from the top of the hair bun down to the hem "
         "of the skirt and her porcelain slippers is inside the frame, standing upright on a low carved "
         "wooden stand, the high-waisted skirt, the trailing gauze scarf and the hem are all visible, "
         "low-key museum lighting with a distant soft spotlight, dark hall backdrop, slight low camera "
         "angle. " + BASE_E19_SLIM},
    ],
}

# ---------------------------------------------------------------------------
# Round 21: closing round for the Eastern phase.
# R19 left one open question: a wide shot needs the costume inventory gone (or the
# camera pulls back in), but deleting it makes the costume plain -- "wide framing
# vs costume detail, pick one".  R21 tests whether a MIDDLE density exists: the
# garment shape plus the few ornaments that actually read (chest band, jade belt,
# gauze stole) but none of the exhaustive enumeration.  The other two shots are
# the proven BASE_E18 compositions, so the round doubles as the deliverable set.
# ---------------------------------------------------------------------------
BASE_E21_MED = (
    "Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical "
    "princess, photographed like a real physical object under studio light. "
    "Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights, "
    "delicate warm translucency at the thin porcelain of the ears and fingertips, microscopic surface "
    "texture, completely clean and dust-free. Visible ball-joint seams at the neck and wrists. "
    "An elegant Eastern classical beauty with refined adult proportions: a delicate oval face with a "
    "softly tapered jaw, fine arched willow-leaf eyebrows, a slender straight nose bridge, a small "
    "rosebud mouth with serene closed lips, almond eyes of realistic size with gently upswept outer "
    "corners, dark brown irises, the faintest soft blush on the cheeks. Glossy black hair dressed in a "
    "classical high coiled bun held by a gold filigree hairpin set with jade and a dangling pearl "
    "ornament. She wears a high-waisted Tang-style ivory silk gown with a gold-thread sash and a long "
    "sheer gauze scarf, its chest band woven with gold peony patterns and set with carved jade, and a "
    "jade-inlaid gold filigree belt. Fine art studio lighting from the upper left, deep but clean "
    "shadows, sharp focus, medium format camera, 120mm macro lens, natural sensor grain, no digital "
    "sharpening. Extremely fine porcelain surface: microscopic glaze texture with faint polishing "
    "marks, carved jade with a soft waxy lustre, engraved gold filigree with milled edges, silk with a "
    "visible woven weft, seed pearls, absolutely no CGI smoothness"
)

ROUNDS[21] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_Q,
    "note": "closing round: medium-density costume base for the wide shot + the two proven "
            "compositions; Eastern deliverable set",
    "shots": [
        {"name": "final-portrait", "seed": 2100, "size": (1280, 1712), "timeout": 3600,
         "prompt": BASE_E18 + ", three-quarter portrait in soft north window light, gentle shadow "
         "gradient across the porcelain cheek, quiet neutral interior backdrop"},
        {"name": "figure-medium", "seed": 2110, "size": (880, 2048), "timeout": 3600,
         "prompt": "Full-length photograph: the entire doll from the top of the hair bun down to the hem "
         "of the skirt and her porcelain slippers is inside the frame, standing upright on a low carved "
         "wooden stand, the high-waisted skirt, the gold chest band, the trailing gauze scarf and the "
         "hem are all visible, low-key museum lighting with a distant soft spotlight, dark hall "
         "backdrop, slight low camera angle. " + BASE_E21_MED},
        {"name": "final-seated", "seed": 2120, "size": (1600, 1600), "timeout": 4200,
         "prompt": BASE_E18 + ", seated three-quarter view at a small rosewood table, both porcelain "
         "hands resting on her lap with the ball-joint seams at the wrists clearly visible, a round silk "
         "fan lying on the table, soft north window light, quiet interior backdrop"},
    ],
}

# ===========================================================================
# 第四阶段（R22+）：换思路 —— 从"摆件"改为"活人"，改用红楼梦出场笔法（中文直出）
# ===========================================================================
# 用户反馈：前 21 轮"太像个摆件了"，且"公主的皮肤是骨瓷质感的，还不够细致"。
#
# 诊断：前 21 轮的 prompt 一直在强化"她是一件物品"——
#   "handcrafted ball-jointed bone china doll"（人偶）
#   "photographed like a real physical object on a table"（物件）
#   "Visible ball-joint seams at the neck and wrists"（关节缝 = 摆件特征）
#   "museum-vitrine realism"（陈列柜）
#   "porcelain slippers" / "carved wooden stand"（展台与配件）
# 所以越做越像博物馆里的一座人偶。
#
# 本阶段三条改动：
#   1. 正向里彻底删除人偶/关节/展台/陈列柜的一切词，主语改为"一位东方古典公主"；
#   2. **肌肤**单独成层细描：莹润如骨瓷、看不见毛孔却非塑料般平滑、胎薄处透血色与光、
#      极薄的釉光、极细的绒毛——直接回应"还不够细致"；
#   3. prompt **改用中文**，按红楼梦人物出场笔法逐层白描
#      （发式 → 面 → 眉 → 目 → 鼻 → 唇 → 肌肤 → 首饰 → 衣裳 → 神态 → 环境 → 光 → 镜头）。
#      Qwen-Image 的文本编码器是 Qwen2.5-VL，中文语义对齐应当优于英文转译——
#      这是前 21 轮从未试过的杠杆。
# ===========================================================================
BASE_H = (
    "一幅细致入微的东方古典公主写照，写实照片，人在内室之中。"
    # 发式与头面
    "乌油油的青丝绾成飞仙髻，正中一支赤金点翠衔珠凤钗，凤口垂下三串米珠，"
    "鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。"
    # 面
    "鹅蛋脸儿，面若中秋之月，色如春晓之花。"
    # 眉
    "两弯似蹙非蹙的罥烟眉，眉梢淡淡入鬓。"
    # 目
    "一双似喜非喜的含情目，眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，"
    "睫毛根根分明，眼睑薄得透出一线极淡的血色，瞳子里含着一点窗光。"
    # 鼻与唇
    "鼻梁秀挺，鼻头圆润。樱桃小口，唇色如点朱，唇角含着一点未露的笑意。"
    # 肌肤 —— 本阶段的核心，单独成层
    "肌肤莹润如骨瓷：细腻得如同刚出窑的细瓷，看不见毛孔，却绝不是塑料那样的平滑；"
    "面颊覆着一层极薄的釉光，胎薄处——耳缘、鼻翼、指尖——透着温润的血色与光；"
    "颧骨上一抹极淡的绯色，下颌与颈侧有柔和的反射，皮肤上有一层极细的绒毛。"
    # 首饰
    "项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。"
    # 衣裳
    "身上穿着月白织金团花褙子，领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；"
    "腰间一条秋香色宫绦，垂一块双衡比目玉佩；下着藕荷色绣兰裙。"
    # 神态
    "神态端庄沉静，含而不露，眉心一点若有若无的轻愁。"
    # 环境（内室，而非展台）
    "身后一架紫檀绢本屏风，几上博山炉袅袅一缕沉香，窗外疏影横斜。"
    # 光与镜头
    "柔和天光自左侧斜照进来，面上的明暗过渡自然。"
    "真实照片，中画幅相机，120mm 微距镜头，浅景深，自然颗粒，无数字锐化"
)

# 负向：在 NEG_Q 基础上**明确禁掉"摆件"**——人偶、球形关节、关节缝、展台、陈列柜、雕像。
NEG_H = NEG_Q + (
    ", doll, figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, "
    "display stand, pedestal, plinth, museum display case, toy, plastic figure, statue, "
    "人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像"
)

ROUNDS[22] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_H,
    "note": "phase 4 opens: drop every doll/ball-joint/display-stand word, make her a living "
            "princess whose skin is bone-china fine; first Chinese prompt, written in the layered "
            "Dream-of-the-Red-Chamber entrance style",
    "shots": [
        {"name": "portrait", "seed": 2200, "size": (1280, 1712), "timeout": 3600,
         "prompt": BASE_H + "。半身像，取到腰际，人在内室中，身后屏风与几案柔和虚化"},
        {"name": "full-figure", "seed": 2210, "size": (880, 2048), "timeout": 3600,
         "prompt": BASE_H + "。全身像，自飞仙髻直到裙裾与绣鞋尽入画面，"
                            "人立于内室地上，裙裾曳地，身姿挺拔，不倚不靠"},
        {"name": "skin-plate", "seed": 2220, "size": (1600, 2144), "timeout": 4200,
         "prompt": BASE_H + "。近景肖像，面部占据画面大半，肌肤的细腻质感、"
                            "釉光与眼神里的高光清晰可辨，背景完全虚化"},
    ],
}

# ---------------------------------------------------------------------------
# Round 23.  R22 decoupled the wrong pair: it removed the doll framing AND the
# porcelain material along with it, so she came back as an ordinary young woman
# with ordinary skin.  The two goals are independent -- the SUBJECT can be a
# living princess while the MATERIAL is still bone china.
#
# The fix is a bilingual base, because R22 showed exactly where each language
# wins:
#   * Chinese  -> what exists: person, expression, jewellery, costume, interior.
#                 R22 landed the incense burner's curling smoke, the screen
#                 painting, the jade ring and the embroidered lapel in one go.
#   * English  -> what it is made of.  The BASE_Q10 material lines have 21 rounds
#                 of proof behind them, so they are reused nearly verbatim -- but
#                 the subject is now "her skin", never "a doll".
# R22 also drifted into studio-glamour makeup, so the Chinese段 now pins the
# face down: 妆极淡 / 近乎素面 / 唇上只点一点浅胭脂, and the negative forbids
# heavy makeup, red lipstick and the 影楼 look.
# ---------------------------------------------------------------------------
BASE_H2_CN = (
    "一幅细致入微的东方古典公主写照，写实照片，人在内室之中。"
    "乌油油的青丝绾成飞仙髻，正中一支金累丝衔珠凤钗，凤口垂下三串米珠，"
    "鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。"
    "鹅蛋脸儿，面若中秋之月，色如春晓之花。"
    "两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛。"
    "一双似喜非喜的含情目，眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，"
    "睫毛根根分明，眼睑薄得透出一线极淡的血色，瞳子里含着一点窗光。"
    "鼻梁秀挺，鼻头圆润。樱桃小口，唇上只点一点浅胭脂，唇角含着一点未露的笑意。"
    "妆极淡，近乎素面，只在颊上留一抹极淡的绯色。"
    "项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。"
    "身上穿着月白织金团花褙子，领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；"
    "腰间一条秋香色宫绦，垂一块双衡比目玉佩；下着藕荷色绣兰裙。"
    "神态端庄沉静，含而不露，眉心一点若有若无的轻愁。"
    "身后一架紫檀绢本屏风，几上博山炉袅袅一缕沉香，窗外疏影横斜。"
    "柔和天光自左侧斜照进来，面上的明暗过渡自然。"
)

# 材质层（英文，主语是 her skin —— 这正是 R22 丢掉的东西）
BASE_H2_EN = (
    " Her skin is bone china -- the material itself, not a mask: ivory porcelain under a fired "
    "glaze, with crisp specular highlights where the light strikes, delicate warm translucency "
    "glowing through the thin porcelain of the ears, the wings of the nose and the fingertips, "
    "microscopic glaze texture with the faintest polishing marks, a few microscopic bubbles "
    "suspended inside the glaze, gentle variation in the ivory, a soft ivory sheen, and absolutely "
    "no CGI smoothness and no plastic. Fine art studio lighting from the upper left, deep but clean "
    "shadows, sharp focus on the eyes. Photographed on a medium format camera with a 120mm macro "
    "lens at f/2.8, natural sensor grain, no digital sharpening"
)
BASE_H2 = BASE_H2_CN + BASE_H2_EN

# 全身像用精简中文段（长服饰清单会把镜头拉近——R10/R13/R17/R18 四次复现）
BASE_H2_CN_SLIM = (
    "一幅细致入微的东方古典公主写照，写实照片，人在内室之中。"
    "乌油油的青丝绾成飞仙髻，正中一支金累丝衔珠凤钗，鬓边一朵白玉兰。"
    "鹅蛋脸儿，两弯似蹙非蹙的罥烟眉，一双似喜非喜的含情目，樱桃小口，妆极淡，近乎素面。"
    "身上是月白织金团花褙子，腰间一条秋香色宫绦，垂一块双衡比目玉佩。"
    "神态端庄沉静。身后一架紫檀绢本屏风，几上一缕沉香，窗外疏影横斜。"
)
BASE_H2_SLIM = BASE_H2_CN_SLIM + BASE_H2_EN

NEG_H2 = NEG_H + (
    ", heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay, "
    "studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容"
)

ROUNDS[23] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_H2,
    "note": "bilingual base: Chinese for what exists, English for what it is made of -- the subject "
            "stays a living princess while her skin is bone china again; makeup pinned to 素面",
    "shots": [
        {"name": "portrait", "seed": 2300, "size": (1280, 1712), "timeout": 3600,
         "prompt": BASE_H2 + "。半身像，取到腰际，人在内室中，身后屏风与几案柔和虚化"},
        {"name": "full-figure", "seed": 2310, "size": (880, 2048), "timeout": 3600,
         "prompt": BASE_H2_SLIM + "。全身像，自飞仙髻直到裙裾与绣鞋尽入画面，人立于内室地上，"
                                  "裙裾曳地，身姿挺拔，不倚不靠"},
        {"name": "skin-plate", "seed": 2320, "size": (1600, 2144), "timeout": 4200,
         "prompt": BASE_H2 + "。近景肖像，面部占据画面大半，肌肤的细腻质感、"
                            "釉光与眼神里的高光清晰可辨，背景完全虚化"},
    ],
}

# ---------------------------------------------------------------------------
# Round 24.  R23's face-macro crop (out/macro-skin/skin-face-r23.png) is the
# evidence: the eyes are excellent, but the skin is ordinary retouched human
# skin -- no glaze, no translucency, no porcelain micro-texture.  The English
# material block was sitting at the END of a ~450-character Chinese passage and
# got diluted; R11 and R15 already showed that whatever leads the prompt wins.
#
# So R24 changes ONE thing: the material block moves to the FRONT.  cfg, steps,
# size and seed policy are untouched.
# Two supporting tweaks, both aimed at the same target:
#   * the Chinese passage gains an explicit 瓷胎 layer (釉 / 胎薄处透光 / 釉下气泡,
#     不见肉身毛孔) and drops the word 写实照片, which was pulling toward
#     ordinary photographic skin;
#   * the negative now forbids human-skin cues outright (pores, matte skin,
#     retouched skin, 真人皮肤 / 哑光皮肤 / 毛孔).
# ---------------------------------------------------------------------------
BASE_H3_EN = (
    "Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china "
    "-- the material itself, not a mask: ivory porcelain under a fired glaze, with crisp specular "
    "highlights where the light strikes, delicate warm translucency glowing through the thin porcelain "
    "of the ears, the wings of the nose and the fingertips, microscopic glaze texture with the faintest "
    "polishing marks, a few microscopic bubbles suspended inside the glaze, gentle variation in the "
    "ivory, a soft ivory sheen, absolutely no CGI smoothness and no plastic. Her face is human; her "
    "skin is porcelain. "
)

BASE_H3_CN = (
    "一幅细致入微的东方古典公主写照，人在内室之中。"
    "乌油油的青丝绾成飞仙髻，正中一支金累丝衔珠凤钗，凤口垂下三串米珠，"
    "鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。"
    "鹅蛋脸儿，面若中秋之月，色如春晓之花；"
    "两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；"
    "一双似喜非喜的含情目，眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，"
    "睫毛根根分明，眼睑薄得透出一线极淡的血色，瞳子里含着一点窗光。"
    "鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂。妆极淡，近乎素面。"
    "肌肤是骨瓷的胎质：莹润而半透，面颊上覆着一层极薄的釉，"
    "胎薄处——耳缘、鼻翼、指节——透出温润的血色与光，"
    "釉下可见极细的气泡与磨痕，却不见肉身的毛孔。"
    "项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。"
    "身上穿着月白织金团花褙子，领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；"
    "腰间一条秋香色宫绦，垂一块双衡比目玉佩；下着藕荷色绣兰裙。"
    "神态端庄沉静，含而不露，眉心一点若有若无的轻愁。"
    "身后一架紫檀绢本屏风，几上博山炉袅袅一缕沉香，窗外疏影横斜。"
    "柔和天光自左侧斜照进来"
)

BASE_H3 = (
    BASE_H3_EN + BASE_H3_CN
    + "。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化"
)

BASE_H3_CN_SLIM = (
    "一幅细致入微的东方古典公主写照，人在内室之中。"
    "乌油油的青丝绾成飞仙髻，正中一支金累丝衔珠凤钗，鬓边一朵白玉兰。"
    "鹅蛋脸儿，两弯似蹙非蹙的罥烟眉，一双似喜非喜的含情目，樱桃小口，妆极淡，近乎素面。"
    "肌肤是骨瓷的胎质：莹润而半透，面颊上覆着一层极薄的釉。"
    "身上是月白织金团花褙子，腰间一条秋香色宫绦，垂一块双衡比目玉佩。"
    "神态端庄沉静。身后一架紫檀绢本屏风，几上一缕沉香，窗外疏影横斜"
)
BASE_H3_SLIM = (
    BASE_H3_EN + BASE_H3_CN_SLIM
    + "。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化"
)

NEG_H3 = NEG_H2 + (
    ", human skin texture, realistic skin pores, visible pores, matte skin, ordinary human skin, "
    "retouched skin, airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔"
)

ROUNDS[24] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_H3,
    "note": "material block moved to the FRONT of the prompt (R11/R15 position rule); Chinese passage "
            "gains an explicit 瓷胎 layer and drops 写实照片; negative forbids human-skin cues",
    "shots": [
        {"name": "portrait", "seed": 2400, "size": (1280, 1712), "timeout": 3600,
         "prompt": BASE_H3 + "。半身像，取到腰际，身后屏风与几案柔和虚化"},
        {"name": "full-figure", "seed": 2410, "size": (880, 2048), "timeout": 3600,
         "prompt": BASE_H3_SLIM + "。全身像，自飞仙髻直到裙裾与绣鞋尽入画面，"
                                  "人立于内室地上，裙裾曳地，身姿挺拔，不倚不靠"},
        {"name": "skin-plate", "seed": 2420, "size": (1600, 2144), "timeout": 4200,
         "prompt": BASE_H3 + "。近景肖像，面部占据画面大半，肌肤的瓷胎质感、"
                             "釉光与眼神里的高光清晰可辨，背景完全虚化"},
    ],
}

# ---------------------------------------------------------------------------
# Round 25.  R24's face-macro crop proved the glaze finally reads as bone china,
# but exposed three fresh problems:
#   1. the ears came out pointed and glowing orange -- "warm translucency through
#      the thin porcelain of the ears" literally grew elf ears;
#   2. the surface is a perfectly smooth glaze with NO micro-detail at all, which
#      is exactly the user's "还不够细致";
#   3. the face is only ~500 px wide in a 1600x2144 plate, so no crop can show
#      micro-texture even if it were rendered.
# R25 therefore: (a) drops ears from the translucency list and forbids pointed /
# glowing ears outright; (b) NAMES the real defects of a fired glaze -- pinholes
# where the glaze pulled back, trapped bubbles and blisters, polishing drag
# lines, orange-peel ripple, uneven glaze thickness and colour, kiln grit -- plus
# an explicit "never a uniform flat surface"; (c) shoots the skin plate on a
# 2048x2048 square (4.19 MP, still inside R14's proven 4.92 MP ceiling) so the
# head occupies far more pixels and the crop can actually be microscopic.
# ---------------------------------------------------------------------------
BASE_H4_EN = (
    "Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china "
    "-- the material itself, not a mask: ivory porcelain under a fired glaze, with crisp specular "
    "highlights where the light strikes, warm translucency glowing through the thin porcelain of the "
    "fingertips and the temples, and above all a REAL fired surface rather than a smooth render: "
    "microscopic pinholes where the glaze pulled back, tiny trapped bubbles and blisters under the "
    "glaze, faint polishing marks and hairline drag lines, a fine orange-peel ripple, glaze that is "
    "very slightly uneven in thickness and in colour, a few tiny specks of kiln grit, and a soft "
    "blush of warm colour across the cheeks -- real variation everywhere, never a uniform flat "
    "surface, absolutely no CGI smoothness and no plastic. Her face is human; her skin is porcelain. "
)

BASE_H4_CN = (
    "一幅细致入微的东方古典公主写照，人在内室之中。"
    "乌油油的青丝绾成飞仙髻，正中一支金累丝衔珠凤钗，凤口垂下三串米珠，"
    "鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。"
    "鹅蛋脸儿，面若中秋之月，色如春晓之花；"
    "两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；"
    "一双似喜非喜的含情目，眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，"
    "睫毛根根分明，眼睑薄得透出一线极淡的血色，瞳子里含着一点窗光。"
    "鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂。妆极淡，近乎素面。"
    "肌肤是骨瓷的胎质：莹润而半透，面颊上覆着一层极薄的釉，"
    "颞侧与指节这些胎薄处透出温润的血色与光；"
    "釉面并非均匀光滑，而是有极细的缩釉小点、釉下的小气泡与棕眼、"
    "擦拭留下的细磨痕、橘子皮似的细微起伏，釉色深浅也略有不同；"
    "两颊透出温润的血色，却不见肉身的毛孔。"
    "项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。"
    "身上穿着月白织金团花褙子，领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；"
    "腰间一条秋香色宫绦，垂一块双衡比目玉佩；下着藕荷色绣兰裙。"
    "神态端庄沉静，含而不露，眉心一点若有若无的轻愁。"
    "身后一架紫檀绢本屏风，几上博山炉袅袅一缕沉香，窗外疏影横斜。"
    "柔和天光自左侧斜照进来"
)
BASE_H4 = (
    BASE_H4_EN + BASE_H4_CN
    + "。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化"
)

BASE_H4_CN_SLIM = (
    "一幅细致入微的东方古典公主写照，人在内室之中。"
    "乌油油的青丝绾成飞仙髻，正中一支金累丝衔珠凤钗，鬓边一朵白玉兰。"
    "鹅蛋脸儿，两弯似蹙非蹙的罥烟眉，一双似喜非喜的含情目，樱桃小口，妆极淡，近乎素面。"
    "肌肤是骨瓷的胎质：莹润而半透，面颊上覆着一层极薄的釉，釉面有极细的缩釉点与磨痕。"
    "身上是月白织金团花褙子，腰间一条秋香色宫绦，垂一块双衡比目玉佩。"
    "神态端庄沉静。身后一架紫檀绢本屏风，几上一缕沉香，窗外疏影横斜"
)
BASE_H4_SLIM = (
    BASE_H4_EN + BASE_H4_CN_SLIM
    + "。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化"
)

NEG_H4 = NEG_H3 + (
    ", pointed ears, elf ears, long pointed ears, glowing orange ears, animal ears, 尖耳, 精灵耳, "
    "smooth featureless skin, uniform flat surface, completely even skin, waxy flawless surface, "
    "光滑无细节, 死白, 蜡像"
)

ROUNDS[25] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_H4,
    "note": "kill the elf-ear artifact, NAME the real defects of a fired glaze (pinholes, bubbles, "
            "drag lines, orange peel, uneven glaze) so the surface stops being featureless, and shoot "
            "the skin plate on a 2048 square so the face finally occupies enough pixels for a macro",
    "shots": [
        {"name": "portrait", "seed": 2500, "size": (1280, 1712), "timeout": 3600,
         "prompt": BASE_H4 + "。半身像，取到腰际，身后屏风与几案柔和虚化"},
        {"name": "full-figure", "seed": 2510, "size": (880, 2048), "timeout": 3600,
         "prompt": BASE_H4_SLIM + "。全身像，自飞仙髻直到裙裾与绣鞋尽入画面，"
                                  "人立于内室地上，裙裾曳地，身姿挺拔，不倚不靠"},
        {"name": "skin-square", "seed": 2520, "size": (2048, 2048), "timeout": 5400,
         "prompt": BASE_H4 + "。近景肖像，面部占据画面大半，肌肤的瓷胎质感、"
                             "釉面的缩釉点与磨痕、以及眼神里的高光清晰可辨，背景完全虚化"},
    ],
}

# ---------------------------------------------------------------------------
# Round 26.  R25 landed the skin (its 2048 square macro shows fired glaze + real
# human blush + an actual pinhole and orange-peel ripple in the glaze), so the
# skin block is frozen as-is.  The user's remaining note is about the CLOTH:
# it must read as light, airy, "half gauze, half bone china".
#
# R25's costume was heavy -- 织金团花褙子 (gold brocade) reads as thick, stiff
# fabric, which is the opposite of 轻盈.  R26 therefore swaps ONLY the costume
# layer: several layers of cicada-wing gauze over bone-china-white silk, sheer
# enough to show the layers beneath and the light behind, with the crisp fine
# weave and clean cut edge of porcelain rather than the softness of cloth, and
# with the hems and sleeves lifting in still air.  Heavy gold brocade and dense
# peony embroidery are removed; the ornament is reduced to sparse fine silver
# thread, so the fabric stays light.
#
# The skin block, the makeup restraint, the props, the negative list and every
# sampling parameter are untouched -- this round changes one layer.
# ---------------------------------------------------------------------------
BASE_H5_FABRIC_EN = (
    "Her robes are nearly weightless: several layers of fine translucent gauze as thin as cicada "
    "wings, drifting and floating in the still air, the outermost layer so sheer that the layers "
    "beneath it and the light behind them show through, the sleeves and hems lifting as if in a "
    "breath of air; the gauze keeps the crisp fine weave and the cleanly cut edge of porcelain "
    "rather than the softness of ordinary cloth, half gauze and half bone china"
)

BASE_H5_CN = (
    "一幅细致入微的东方古典公主写照，人在内室之中。"
    "乌油油的青丝绾成飞仙髻，正中一支金累丝衔珠凤钗，凤口垂下三串米珠，"
    "鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。"
    "鹅蛋脸儿，面若中秋之月，色如春晓之花；"
    "两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；"
    "一双似喜非喜的含情目，眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，"
    "睫毛根根分明，眼睑薄得透出一线极淡的血色，瞳子里含着一点窗光。"
    "鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂。妆极淡，近乎素面。"
    "肌肤是骨瓷的胎质：莹润而半透，面颊上覆着一层极薄的釉，"
    "颞侧与指节这些胎薄处透出温润的血色与光；"
    "釉面并非均匀光滑，而是有极细的缩釉小点、釉下的小气泡与棕眼、"
    "擦拭留下的细磨痕、橘子皮似的细微起伏，釉色深浅也略有不同；"
    "两颊透出温润的血色，却不见肉身的毛孔。"
    "项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。"
    # 衣裳 —— 本轮的核心：轻盈、半纱半骨瓷
    "身上是数层极轻的纱罗：外层薄如蝉翼的素纱，内层是骨瓷白的细绢，"
    "纱薄得透出里层的光影与轮廓；衣袂与披帛飘飘欲举，裙裾曳地如烟；"
    "纱罗的经纬细密而挺括，边缘清爽利落，有瓷器那样的筋骨，绝不是软塌塌的厚布；"
    "纱上只用极细的银线疏疏绣着几枝兰草，不作繁密织金；"
    "腰间一条秋香色宫绦，垂一块双衡比目玉佩。"
    "神态端庄沉静，含而不露，眉心一点若有若无的轻愁。"
    "身后一架紫檀绢本屏风，几上博山炉袅袅一缕沉香，窗外疏影横斜。"
    "柔和天光自左侧斜照进来，纱罗在光里近乎透亮"
)
BASE_H5 = (
    BASE_H4_EN + BASE_H5_FABRIC_EN + "。 " + BASE_H5_CN
    + "。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化"
)

BASE_H5_CN_SLIM = (
    "一幅细致入微的东方古典公主写照，人在内室之中。"
    "乌油油的青丝绾成飞仙髻，正中一支金累丝衔珠凤钗，鬓边一朵白玉兰。"
    "鹅蛋脸儿，两弯似蹙非蹙的罥烟眉，一双似喜非喜的含情目，樱桃小口，妆极淡，近乎素面。"
    "肌肤是骨瓷的胎质：莹润而半透，面颊上覆着一层极薄的釉，釉面有极细的缩釉点与磨痕。"
    "身上是数层极轻的纱罗，薄如蝉翼，衣袂与裙裾飘飘欲举，纱上疏疏几枝银线兰草。"
    "神态端庄沉静。身后一架紫檀绢本屏风，几上一缕沉香，窗外疏影横斜"
)
BASE_H5_SLIM = (
    BASE_H4_EN + BASE_H5_FABRIC_EN + "。 " + BASE_H5_CN_SLIM
    + "。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化"
)

NEG_H5 = NEG_H4 + (
    ", heavy stiff fabric, thick brocade, heavy gold embroidery, dense embroidery, bulky robe, "
    "cardboard-stiff cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重"
)

ROUNDS[26] = {
    "engine": "qwen", "size": (1280, 1712), "steps": 32, "cfg": 3.5, "negative": NEG_H5,
    "note": "clothing-only change: heavy gold brocade -> several layers of cicada-wing gauze over "
            "bone-china-white silk, sheer and lifting, with porcelain-crisp weave and edges; the "
            "frozen skin block from R25 is reused verbatim",
    "shots": [
        {"name": "portrait", "seed": 2600, "size": (1280, 1712), "timeout": 3600,
         "prompt": BASE_H5 + "。半身像，取到腰际，纱罗的层次与透光清晰可见，身后屏风与几案柔和虚化"},
        {"name": "full-figure", "seed": 2610, "size": (880, 2048), "timeout": 3600,
         "prompt": BASE_H5_SLIM + "。全身像，自飞仙髻直到裙裾与绣鞋尽入画面，"
                                  "人立于内室地上，裙裾曳地如烟，衣袂飘飘，身姿挺拔，不倚不靠"},
        {"name": "airy-turn", "seed": 2620, "size": (1600, 1600), "timeout": 4200,
         "prompt": BASE_H5 + "。侧身回眸的瞬间，衣袂与披帛随动作扬起，"
                             "纱罗在光里近乎透亮，能看见里层的轮廓与光影"},
    ],
}

# ---------------------------------------------------------------------------
# Round 27.  Three notes from the user: the blush is too deliberate and must
# look natural; the shots must be FULL BODY; and the mood should be languid
# everyday life -- sitting, lying on the front, or reclining.
#
# Changes:
#  1. Makeup: R26's prominent round cheek-blush came from a clause the material
#     block carried near the FRONT of the prompt ("a soft blush of warm colour
#     across the cheeks").  R27 replaces it in place -- the colour must read as
#     something welling up from under the skin, explicitly not rouge and not a
#     drawn-on blush -- and the negative forbids blush makeup outright.
#  2. Mood: the passage becomes a moment of ordinary life, not a formal sitting
#     -- hair loosely pinned with strands down, eyes lazy and half-sleepy, mouth
#     relaxed rather than posed, sash tied loosely, cuff slipping, everyday props
#     (tea, a half-read scroll, a bolster, a mat, an open window).
#  3. Full body, three poses, and for the two lying poses a LANDSCAPE canvas --
#     a new use of the R15 aspect-ratio lever, since a reclining body is wide.
#     The seated shot keeps a 3:4 canvas and uses the slim passage so the camera
#     does not pull in (R10/R13/R17/R18 rule).
# ---------------------------------------------------------------------------
_H4_BLUSH = (
    "and a soft blush of warm colour across the cheeks -- real variation everywhere, never a uniform "
    "flat surface"
)
_H6_BLUSH = (
    "and only the faint, uneven flush of real living skin -- colour that wells up from beneath rather "
    "than anything applied, no rouge, no drawn-on blush and no blush patches -- real variation "
    "everywhere, never a uniform flat surface"
)
assert _H4_BLUSH in BASE_H4_EN, "R27: blush clause not found -- substitution would be a no-op"
BASE_H6_EN = BASE_H4_EN.replace(_H4_BLUSH, _H6_BLUSH)

# 全身用精简 CN 段（长服饰清单会把镜头拉近），并且通篇改成"家常日子"的松弛语气：
# 发髻松绾、眼神懒懒半含睡意、嘴角不刻意含笑、衣襟齐整却穿得松泛、血色自然而非胭脂。
BASE_H6_SLIM_CN = (
    "一幅细致入微的东方古典公主写照：家常日子里的一个瞬间，人在内室之中。"
    "青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，鬓边散下几缕碎发。"
    "鹅蛋脸儿，面若中秋之月，色如春晓之花；"
    "两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；"
    "一双似喜非喜的含情目，眸子如秋水，眼神懒懒的，半含睡意；"
    "鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂，嘴角松松的，不刻意含笑。"
    "妆极淡，近乎素面，血色自里透出，深浅不匀，自然得很，绝不是涂上去的胭脂，"
    "也不见肉身的毛孔。"
    "肌肤是骨瓷的胎质：莹润而半透，面颊上覆着一层极薄的釉，"
    "釉面有极细的缩釉点与磨痕，橘子皮似的细微起伏，釉色深浅也略有不同。"
    "身上是数层极轻的纱罗，薄如蝉翼，衣襟齐整却穿得松泛，袖口松松滑落，宫绦松松系着。"
    "神态慵懒闲适，不拘礼数，像在自己屋里歇着。"
    "内室里一架紫檀绢本屏风，几上一缕沉香，窗外疏影横斜"
)
BASE_H6_SLIM = (
    BASE_H6_EN + BASE_H5_FABRIC_EN + "。 " + BASE_H6_SLIM_CN
    + "。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化"
)

NEG_H6 = NEG_H5 + (
    ", blush makeup, rouge, blush patches, circular blush, doll-like blush, heavy blush, "
    "applied cosmetics, stiff formal pose, studio pose, standing to attention, 腮红, 胭脂印, "
    "高原红, 刻意妆容, 端坐, 摆拍"
)

ROUNDS[27] = {
    "engine": "qwen", "size": (1200, 1600), "steps": 32, "cfg": 3.5, "negative": NEG_H6,
    "note": "natural flush instead of applied blush, languid everyday mood, and three FULL-BODY "
            "poses -- seated on a daybed, reclining on one elbow, and lying on the front; the two "
            "lying poses use landscape canvases (a new use of the R15 aspect-ratio lever)",
    "shots": [
        {"name": "seated-daybed", "seed": 2700, "size": (1200, 1600), "timeout": 4200,
         "prompt": BASE_H6_SLIM + "。全身像：她斜坐在一张矮榻上，一条腿屈起，"
                                  "手肘支在隐囊上，一手托腮，懒懒望向窗外，"
                                  "纱罗的衣袂垂落榻沿，榻边几上一盏半凉的茶，姿态松弛"},
        {"name": "recline-side", "seed": 2710, "size": (2048, 1024), "timeout": 4200,
         "prompt": BASE_H6_SLIM + "。全身横构图：她侧卧在榻上，一手支腮，"
                                  "另一手随意搭在身侧，数层纱罗铺散在锦垫上，"
                                  "膝上覆着一条薄毯，榻边摊着一卷未读完的书，午后光斜斜落在榻上"},
        {"name": "prone", "seed": 2720, "size": (1792, 1152), "timeout": 4200,
         "prompt": BASE_H6_SLIM + "。全身横构图：她伏卧在长榻上，两肘撑着上身，"
                                  "下巴搁在手背上，小腿在身后轻轻翘起交错，"
                                  "纱罗拖成长长一尾，脚边一只搁倒的团扇，晨光从窗棂斜进来"},
    ],
}

# ---------------------------------------------------------------------------
# Round 28.  R27 fixed the makeup (the applied blush is gone) but both lying
# poses failed -- Qwen returned head-and-shoulders shots on a wide canvas -- and
# a NEW artifact appeared: the hands glow orange.  That is the same failure mode
# as R24's elf ears: "warm translucency ... of the fingertips" is executed
# literally, so the fingertips become a light source.
#
# Three corrections, all measured against what R27 taught:
#  1. translucency now names NO body part at all ("the thinnest parts of the
#     porcelain"); glowing hands / fingers / skin patches go into the negative.
#  2. a much SHORTER base for the pose shots.  R27's base ran ~1500 characters
#     and the face stayed the subject no matter how wide the canvas was.  The
#     pose clause now leads the prompt and the base is cut to the essentials --
#     subject, skin material, gauze, hair, makeup.  Position is weight (R24).
#  3. a more extreme landscape canvas (2048x768, 2.67:1) for the two lying
#     poses.  R27 showed 2:1 alone does not force a lying subject, so the canvas
#     pushes further while the prose stops fighting it.
# ---------------------------------------------------------------------------
BASE_H7_POSE_EN = (
    "Photorealistic image of a living Eastern classical princess resting in her chamber in the "
    "afternoon. Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half "
    "porcelain, with the faint uneven flush of living skin and fine micro-texture in the glaze. She "
    "wears several layers of weightless translucent gauze, half gauze and half bone china. Her hair is "
    "loosely pinned with a gold filigree hairpin, makeup barely there. "
)
BASE_H7_POSE_CN = (
    "东方古典公主在内室里消磨午后时光的写实画面。"
    "肌肤半真半骨瓷：骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，"
    "釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，薄如蝉翼，半纱半骨瓷，"
    "衣襟齐整却穿得松泛。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，鬓边散下几缕碎发。"
    "妆极淡，近乎素面。神态慵懒闲适，不拘礼数"
)
BASE_H7_POSE = (
    BASE_H7_POSE_EN + BASE_H7_POSE_CN
    + "。中画幅相机，50mm 镜头，f/2.8，浅景深，自然颗粒，无数字锐化"
)

NEG_H7 = NEG_H6 + (
    ", glowing hands, orange glowing fingers, luminous hands, glowing skin patches, glowing "
    "fingertips, orange light on the hands, 发光的手, 橙色透光的手, 透光发亮的手指, "
    "portrait crop, head and shoulders crop, close-up crop, bust shot"
)

ROUNDS[28] = {
    "engine": "qwen", "size": (2048, 768), "steps": 32, "cfg": 3.5, "negative": NEG_H7,
    "note": "lying poses fixed by leading with the pose and cutting the base to essentials, with a "
            "2.67:1 canvas; translucency no longer names a body part (R27 glowed orange hands)",
    "shots": [
        {"name": "recline-side", "seed": 2800, "size": (2048, 768), "timeout": 3600,
         "prompt": "全身横构图，一个人躺满整个画面，从发髻到纱罗裙尾全部在画面里："
                    "她侧卧在一张长榻上，一手支腮，另一手随意搭在身侧，"
                    "数层纱罗铺散在锦垫上，膝上覆着一条薄毯，榻边摊着一卷未读完的书。"
                    + BASE_H7_POSE},
        {"name": "prone", "seed": 2810, "size": (2048, 768), "timeout": 3600,
         "prompt": "全身横构图，一个人伏卧在整张长榻上，从头到脚全部在画面里："
                    "她两肘撑着上身，下巴搁在手背上，小腿在身后轻轻翘起交错，"
                    "纱罗拖成长长一尾，脚边一只搁倒的团扇。"
                    + BASE_H7_POSE},
        {"name": "seated-daybed", "seed": 2820, "size": (1200, 1600), "timeout": 3600,
         "prompt": "全身像，一个人坐在矮榻上，自顶至底全身入画，不裁脚不裁手："
                    "她一条腿屈起，手肘支在隐囊上，一手托腮，懒懒望向窗外，"
                    "纱罗的衣袂垂落榻沿，榻边几上一盏半凉的茶。"
                    + BASE_H7_POSE},
    ],
}

# ---------------------------------------------------------------------------
# Round 29: closing round for the languid-life phase.
# R28's formula worked on all three poses -- lead with the pose, keep the base
# short (~600 chars), let the canvas be the shape the pose needs.  R29 keeps
# that formula exactly and only does two things:
#   1. adds three more ordinary moments (propped on a bolster with tea, sitting
#      on a mat by the window, dozing with her head on her arms);
#   2. puts back the classical costume markers the lying poses had lost -- a
#      crossed-collar silk robe under the gauze, the jade-and-pearl necklace and
#      the jade-inlaid belt -- since a short base no longer needs to shed them.
# ---------------------------------------------------------------------------
BASE_H8_POSE_EN = (
    "Photorealistic image of a living Eastern classical princess at home in her chamber in the "
    "afternoon. Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half "
    "porcelain, with the faint uneven flush of living skin and fine micro-texture in the glaze. She "
    "wears several layers of weightless translucent gauze over an ivory silk robe with a crossed "
    "collar, half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt. Her "
    "hair is loosely pinned with a gold filigree hairpin, makeup barely there. "
)
BASE_H8_POSE = (
    BASE_H8_POSE_EN
    + "东方古典公主在内室里消磨午后时光的写实画面。"
      "肌肤半真半骨瓷：骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，"
      "釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，罩在象牙色交领细绢之上，"
      "薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；"
      "颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。"
      "青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，鬓边散下几缕碎发。"
      "妆极淡，近乎素面。神态慵懒闲适，不拘礼数"
    + "。中画幅相机，50mm 镜头，f/2.8，浅景深，自然颗粒，无数字锐化"
)

ROUNDS[29] = {
    "engine": "qwen", "size": (2048, 768), "steps": 32, "cfg": 3.5, "negative": NEG_H7,
    "note": "closing round: three more languid daily moments on the R28 formula (pose first, short "
            "base, canvas shaped to the pose), with the crossed collar, jade-pearl necklace and jade "
            "belt restored",
    "shots": [
        {"name": "propped-bolster", "seed": 2900, "size": (2048, 768), "timeout": 3600,
         "prompt": "全身横构图，一个人躺满整个画面，从发髻到脚尖全部在画面里："
                    "她半躺在长榻上，背靠着一个大隐囊，两膝屈起，一手端着茶盏，"
                    "纱罗从肩头铺散到榻面，裙裾垂落榻沿。" + BASE_H8_POSE},
        {"name": "mat-by-window", "seed": 2910, "size": (1200, 1600), "timeout": 3600,
         "prompt": "全身像，一个人坐在窗边的席垫上，自顶至底全身入画，不裁脚不裁手："
                    "她抱着膝坐着，下巴搁在膝上，懒懒望着窗外，纱罗堆叠在身侧的地上，"
                    "旁边一只矮几，几上一只香炉。" + BASE_H8_POSE},
        {"name": "doze-on-arms", "seed": 2920, "size": (2048, 768), "timeout": 3600,
         "prompt": "全身横构图，一个人伏在案上打盹，从头到脚全身在画面里："
                    "她坐在案前，上身伏下，头枕在自己的臂弯里，长发散落案面，"
                    "数层纱罗从椅背垂下，案上一卷摊开的书与一只茶盏。" + BASE_H8_POSE},
    ],
}


# ---------------------------------------------------------------------------
# Round 30: recover the bone-china skin that phase 5 lost.
#
# Diagnosis (from re-reading out/final-set-life/ against out/final-set-gauze/):
# phase 5 reads as a living woman photographed in hanfu -- the porcelain is
# gone.  The cause is mechanical, not taste: R28 cut the base from 1802 to 635
# chars to win full-body poses, and the cut took the *named glaze-defect
# inventory* with it.  BASE_H4_EN (phase 4) names eight defects; BASE_H8_POSE
# kept only "fine micro-texture in the glaze".  Same failure mode as R11
# (deleting material vocabulary so framing could dominate), just hidden inside
# a change that was otherwise an improvement.
#
# Hypothesis (single variable): put the defect inventory back, change nothing
# else.  Two of the three shots reuse R29's pose text verbatim, so R29 vs R30
# is a direct A/B on the material sentence alone.  This also tests whether
# *material* density pulls the camera in the way *costume* inventories did
# (R10/R13/R17/R18/R27) -- R21/R29 showed the enemy is long costume lists.
#
# NOT restored, on purpose: BASE_H4_EN's "a soft blush of warm colour across
# the cheeks" -- R27 proved that (front-loaded) clause produced the rouge look.
# ---------------------------------------------------------------------------
_H9_MATERIAL_FROM = (
    "Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half "
    "porcelain, with the faint uneven flush of living skin and fine micro-texture in the glaze."
)
_H9_MATERIAL_TO = (
    "Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half "
    "porcelain, with the faint uneven flush of living skin, and above all a REAL fired surface "
    "rather than a smooth render: microscopic pinholes where the glaze pulled back, tiny trapped "
    "bubbles and blisters under the glaze, faint polishing marks and hairline drag lines, a fine "
    "orange-peel ripple, glaze that is very slightly uneven in thickness and in colour, a few "
    "tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface, "
    "absolutely no CGI smoothness and no plastic."
)

assert _H9_MATERIAL_FROM in BASE_H8_POSE, "R30: material anchor not found in BASE_H8_POSE"
BASE_H9_POSE = BASE_H8_POSE.replace(_H9_MATERIAL_FROM, _H9_MATERIAL_TO)
assert BASE_H9_POSE != BASE_H8_POSE, "R30: replace() was a no-op"
for _needle in ("pinholes", "blisters", "orange-peel", "polishing marks", "kiln grit",
                "never a uniform flat surface", "no CGI smoothness"):
    assert _needle in BASE_H9_POSE, f"R30: restored inventory is missing {_needle!r}"
assert "soft blush of warm colour" not in BASE_H9_POSE, "R30: R27's rouge clause came back"

ROUNDS[30] = {
    "engine": "qwen", "size": (2048, 768), "steps": 32, "cfg": 3.5, "negative": NEG_H7,
    "note": "recover the bone-china skin lost in phase 5: put the phase-4 named glaze-defect "
            "inventory back into the pose-first short base, changing nothing else; shots 1-2 reuse "
            "R29's pose text verbatim for a direct A/B",
    "shots": [
        # verbatim R29 pose text -- the only difference from R29's hero is the material sentence
        {"name": "propped-bolster", "seed": 3000, "size": (2048, 768), "timeout": 3600,
         "prompt": "全身横构图，一个人躺满整个画面，从发髻到脚尖全部在画面里："
                    "她半躺在长榻上，背靠着一个大隐囊，两膝屈起，一手端着茶盏，"
                    "纱罗从肩头铺散到榻面，裙裾垂落榻沿。" + BASE_H9_POSE},
        {"name": "mat-by-window", "seed": 3010, "size": (1200, 1600), "timeout": 3600,
         "prompt": "全身像，一个人坐在窗边的席垫上，自顶至底全身入画，不裁脚不裁手："
                    "她抱着膝坐着，下巴搁在膝上，懒懒望着窗外，纱罗堆叠在身侧的地上，"
                    "旁边一只矮几，几上一只香炉。" + BASE_H9_POSE},
        # square canvas = more pixels on skin (R20/R25 trick); does not fight NEG_H7's crop bans
        {"name": "square-plate", "seed": 3020, "size": (1600, 1600), "timeout": 5400,
         "prompt": "全身像，一个人斜坐在矮榻上，自顶至底全身入画，不裁脚不裁手："
                    "她一腿屈起，一手托腮，另一手搁在膝上端着茶盏，"
                    "纱罗一层层垂落榻沿堆在地上，榻边一只香炉一缕青烟。" + BASE_H9_POSE},
    ],
}


# ---------------------------------------------------------------------------
# Round 31: the clause R30 forgot, plus a verdict plate that can actually see it.
#
# R30 restored the *defect inventory* and the skin moved toward porcelain on the
# hands, but it read "smooth + slightly glossy", not "a fired surface with named
# defects".  Diffing BASE_H9_POSE against the phase-4 base that worked (BASE_H4_EN)
# shows what R30 left out:
#
#     with crisp specular highlights where the light strikes
#
# -- the clause that makes a glaze *read* as glaze.  R30 kept the defect list and
# dropped the highlight.  R31 adds that one clause and nothing else.
#
# R31 also fixes a framing mistake in R30: its "square plate" was a full body at
# 1600², so the face held only ~180 px and no crop could reveal glaze detail.
# R25's winning skin plate was a *tight portrait* at 2048².  A tight portrait
# needs a negative without R28's crop bans ("portrait crop / close-up crop"),
# hence the per-shot negative override added to the driver for this round.
#
# Shot 1 is a strict single-variable ablation: R29's mat-by-window pose text and
# seed 2910, same canvas, same NEG_H7 -- only the material sentence differs.
# ---------------------------------------------------------------------------
_H10_SPECULAR_FROM = "ivory porcelain under a fired glaze, half real skin and half porcelain"
_H10_SPECULAR_TO = (
    "ivory porcelain under a fired glaze, with crisp specular highlights where the light "
    "strikes, half real skin and half porcelain"
)
assert _H10_SPECULAR_FROM in BASE_H9_POSE, "R31: specular anchor not found in BASE_H9_POSE"
BASE_H10_POSE = BASE_H9_POSE.replace(_H10_SPECULAR_FROM, _H10_SPECULAR_TO)
assert BASE_H10_POSE != BASE_H9_POSE, "R31: replace() was a no-op"
assert "crisp specular highlights where the light strikes" in BASE_H10_POSE

# NEG_H7 without the crop bans: a tight skin plate must be allowed to crop.
NEG_H10_PORTRAIT = NEG_H6 + (
    ", glowing hands, orange glowing fingers, luminous hands, glowing skin patches, glowing "
    "fingertips, orange light on the hands, 发光的手, 橙色透光的手, 透光发亮的手指"
)

_ROUND31_POSE_WINDOW = (
    "全身像，一个人坐在窗边的席垫上，自顶至底全身入画，不裁脚不裁手："
    "她抱着膝坐着，下巴搁在膝上，懒懒望着窗外，纱罗堆叠在身侧的地上，"
    "旁边一只矮几，几上一只香炉。"
)
# the same pose text R29/R30 used -- asserted below to be byte-identical
assert _ROUND31_POSE_WINDOW == next(
    s["prompt"] for s in ROUNDS[29]["shots"] if s["name"] == "mat-by-window"
).removesuffix(BASE_H8_POSE), "R31: ablation pose text drifted from R29"

ROUNDS[31] = {
    "engine": "qwen", "size": (2048, 768), "steps": 32, "cfg": 3.5, "negative": NEG_H7,
    "note": "restore the specular-highlight clause R30 left out, and judge it on a tight portrait "
            "plate (R30's square plate was a full body, too few pixels on the face); shot 1 is a "
            "same-seed single-variable ablation against R29 mat-by-window",
    "shots": [
        {"name": "ablation-window", "seed": 2910, "size": (1200, 1600), "timeout": 3600,
         "prompt": _ROUND31_POSE_WINDOW + BASE_H10_POSE},
        {"name": "skin-square", "seed": 2520, "size": (2048, 2048), "timeout": 5400,
         "negative": NEG_H10_PORTRAIT,
         "prompt": "紧肖像，半身近景，自头顶到胸前入画，脸占画面大部分："
                    "她侧过脸来迎着窗光，一只手抬起轻触面颊，纱罗松松搭在肩上，"
                    "背景是虚化的窗棂与屏风。" + BASE_H10_POSE},
        {"name": "portrait", "seed": 3030, "size": (1280, 1712), "timeout": 3600,
         "negative": NEG_H10_PORTRAIT,
         "prompt": "肖像，四分之三身，自头顶到腰际入画："
                    "她端坐在矮榻上，一手搁在膝边的茶盏旁，微微侧头望向窗外，"
                    "纱罗从肩头垂落。" + BASE_H10_POSE},
    ],
}


# ---------------------------------------------------------------------------
# Round 32: the assertion, not the inventory.
#
# R31 added the specular clause and judged it on a proper tight portrait plate.
# Same-seed ablations confirm the material sentence *does* change the skin (R29
# vs R31 are visibly different), but the hard fired glaze of R25 is still absent:
# R31 reads as a human portrait with a satin sheen, R25 reads as glazed ceramic.
#
# Diffing the two bases leaves one candidate: the *assertion strength*.
#   R25 (worked):  "whose skin is MADE OF bone china -- THE MATERIAL ITSELF,
#                   NOT A MASK: ... Her face is human; her skin is porcelain."
#   R30/R31:       "Her skin is bone china -- ivory porcelain under a fired glaze,
#                   HALF REAL SKIN AND HALF PORCELAIN, ..."
# "half real skin and half porcelain" literally keeps her half human -- and NEG_H
# bans human skin texture / pores / 真人皮肤 / 毛孔, so the model lands on
# "retouched human skin with some sheen".  R32 swaps the assertion and appends
# the closer, changing nothing else.
#
# Every shot reuses R31's name/seed/size/negative verbatim, so each is an exact
# same-seed A/B against R31 (and shot 1 also against R29 via R31).
# ---------------------------------------------------------------------------
_H11_ASSERT_FROM = (
    "Her skin is bone china -- ivory porcelain under a fired glaze, with crisp specular "
    "highlights where the light strikes, half real skin and half porcelain, with the faint "
    "uneven flush of living skin,"
)
_H11_ASSERT_TO = (
    "Her skin is made of bone china -- the material itself, not a mask: ivory porcelain under a "
    "fired glaze, with crisp specular highlights where the light strikes, with the faint "
    "uneven flush of living skin,"
)
_H11_CLOSER_FROM = "absolutely no CGI smoothness and no plastic."
_H11_CLOSER_TO = (
    "absolutely no CGI smoothness and no plastic. Her face is human; her skin is porcelain."
)

assert _H11_ASSERT_FROM in BASE_H10_POSE, "R32: assertion anchor not found in BASE_H10_POSE"
assert _H11_CLOSER_FROM in BASE_H10_POSE, "R32: closer anchor not found in BASE_H10_POSE"
BASE_H11_POSE = BASE_H10_POSE.replace(_H11_ASSERT_FROM, _H11_ASSERT_TO).replace(
    _H11_CLOSER_FROM, _H11_CLOSER_TO
)
assert BASE_H11_POSE != BASE_H10_POSE, "R32: replace() was a no-op"
assert "half real skin and half porcelain" not in BASE_H11_POSE
assert "Her face is human; her skin is porcelain." in BASE_H11_POSE

ROUNDS[32] = {
    "engine": "qwen", "size": (2048, 768), "steps": 32, "cfg": 3.5, "negative": NEG_H7,
    "note": "swap the material assertion from 'half real skin and half porcelain' to R25's proven "
            "'made of bone china -- the material itself, not a mask' + 'Her face is human; her skin "
            "is porcelain.'; every shot mirrors R31's name/seed/size/negative for an exact A/B",
    "shots": [
        {"name": "ablation-window", "seed": 2910, "size": (1200, 1600), "timeout": 3600,
         "prompt": _ROUND31_POSE_WINDOW + BASE_H11_POSE},
        {"name": "skin-square", "seed": 2520, "size": (2048, 2048), "timeout": 5400,
         "negative": NEG_H10_PORTRAIT,
         "prompt": "紧肖像，半身近景，自头顶到胸前入画，脸占画面大部分："
                    "她侧过脸来迎着窗光，一只手抬起轻触面颊，纱罗松松搭在肩上，"
                    "背景是虚化的窗棂与屏风。" + BASE_H11_POSE},
        {"name": "portrait", "seed": 3030, "size": (1280, 1712), "timeout": 3600,
         "negative": NEG_H10_PORTRAIT,
         "prompt": "肖像，四分之三身，自头顶到腰际入画："
                    "她端坐在矮榻上，一手搁在膝边的茶盏旁，微微侧头望向窗外，"
                    "纱罗从肩头垂落。" + BASE_H11_POSE},
    ],
}


# ---------------------------------------------------------------------------
# Round 33: the face clause the same cut removed.
#
# User feedback on R32: "没有公主的气质，有点老气" (no princess bearing, reads old).
# Auditing BASE_H11_POSE for facial vocabulary explains it mechanically:
#
#   BASE_Q10 (phase 2, 21 rounds validated) had a full face clause --
#     "An elegant princess face with refined adult proportions: oval face, high
#      cheekbones, straight nose bridge, serene closed lips, almond eyes of
#      realistic size with a subtle crease, individually painted eyelashes,
#      eyebrows painted hair by hair, the faintest soft blush."
#   BASE_H11_POSE has: eyebrow 0, eyelash 0, eye 0, lip 0, nose 0, cheek 0,
#                      blush 0, elegant 0, adult 0, young 0.
#
# R28's 1802->635 cut removed the glaze-defect inventory AND the face clause.
# R30-R32 fixed the first half; this round fixes the second.  With no facial
# words the model free-rides on the token "princess" and lands on a mature,
# bloodless, generic adult face -- exactly the reported read.
#
# One variable: the face/bearing description block.  Two supporting edits inside
# that block, because they belong to it:
#   * restore the proven face clause, with an explicit youth band (the project
#     has needed the age anchored from BOTH sides: R2-R4 "脸型偏幼儿" pushed it
#     adult, this feedback pushes back toward young);
#   * remove the *blanket* blush bans from the negative (R27 added them to kill
#     applied rouge; they would now fight the "faintest soft blush" the face
#     clause asks for).  The heavy / circular / doll-like guards stay.
# Material, costume, pose, canvas, seed are untouched.
# ---------------------------------------------------------------------------
_H12_FACE_FROM = "princess at home in her chamber in the afternoon."
_H12_FACE_TO = (
    "princess at home in her chamber in the afternoon. An elegant princess face with refined "
    "adult proportions: oval face, high cheekbones, straight nose bridge, serene closed lips, "
    "almond eyes of realistic size with a subtle crease, individually painted eyelashes, "
    "eyebrows painted hair by hair, the faintest soft blush -- a young woman, refined and "
    "fresh-faced, never matronly and never severe."
)
_H12_CN_FROM = "东方古典公主在内室里消磨午后时光的写实画面。"
_H12_CN_TO = (
    "东方古典公主在内室里消磨午后时光的写实画面。"
    "虽在闲居，气度仍在：肩背挺秀，下颌微收，目光清亮，一份矜贵自持。"
)
_H12_CN_POSE_FROM = "神态慵懒闲适，不拘礼数"
_H12_CN_POSE_TO = "神态慵懒闲适，不拘礼数，却自带一份矜贵"

for _anchor in (_H12_FACE_FROM, _H12_CN_FROM, _H12_CN_POSE_FROM):
    assert _anchor in BASE_H11_POSE, f"R33: anchor not found: {_anchor[:40]!r}"
BASE_H12_POSE = (
    BASE_H11_POSE.replace(_H12_FACE_FROM, _H12_FACE_TO)
    .replace(_H12_CN_FROM, _H12_CN_TO)
    .replace(_H12_CN_POSE_FROM, _H12_CN_POSE_TO)
)
assert BASE_H12_POSE != BASE_H11_POSE, "R33: replace() was a no-op"
for _needle in ("oval face", "high cheekbones", "almond eyes", "eyebrows painted hair by hair",
                "the faintest soft blush", "never matronly", "肩背挺秀", "目光清亮", "矜贵"):
    assert _needle in BASE_H12_POSE, f"R33: face/bearing block is missing {_needle!r}"

_NEG_BLANKET_BLUSH = "blush makeup, rouge, blush patches, "
_NEG_GENERIC_BLUSH = ", 腮红, 胭脂印, 高原红"
assert _NEG_BLANKET_BLUSH in NEG_H10_PORTRAIT and _NEG_GENERIC_BLUSH in NEG_H10_PORTRAIT
NEG_H12_PORTRAIT = NEG_H10_PORTRAIT.replace(_NEG_BLANKET_BLUSH, "").replace(
    _NEG_GENERIC_BLUSH, ", 胭脂印, 高原红"
)
assert "blush makeup" not in NEG_H12_PORTRAIT and "腮红" not in NEG_H12_PORTRAIT
assert "heavy blush" in NEG_H12_PORTRAIT and "circular blush" in NEG_H12_PORTRAIT

ROUNDS[33] = {
    "engine": "qwen", "size": (2048, 768), "steps": 32, "cfg": 3.5, "negative": NEG_H7,
    "note": "restore the missing face/bearing block (phase-2's proven face clause + an explicit "
            "youth band + Chinese bearing lines) and drop the blanket blush bans so the faintest "
            "soft blush can render; shots mirror R32's seeds/sizes for a direct A/B",
    "shots": [
        # strict ablation: R32's shot 1 with only the face/bearing block added (still NEG_H7)
        {"name": "ablation-window", "seed": 2910, "size": (1200, 1600), "timeout": 3600,
         "prompt": _ROUND31_POSE_WINDOW + BASE_H12_POSE},
        {"name": "skin-square", "seed": 2520, "size": (2048, 2048), "timeout": 5400,
         "negative": NEG_H12_PORTRAIT,
         "prompt": "紧肖像，半身近景，自头顶到胸前入画，脸占画面大部分："
                    "她侧过脸来迎着窗光，一只手抬起轻触面颊，纱罗松松搭在肩上，"
                    "背景是虚化的窗棂与屏风。" + BASE_H12_POSE},
        {"name": "portrait", "seed": 3030, "size": (1280, 1712), "timeout": 3600,
         "negative": NEG_H12_PORTRAIT,
         "prompt": "肖像，四分之三身，自头顶到腰际入画："
                    "她端坐在矮榻上，一手搁在膝边的茶盏旁，微微侧头望向窗外，"
                    "纱罗从肩头垂落。" + BASE_H12_POSE},
    ],
}


# ---------------------------------------------------------------------------
# Round 34: put the age anchor where it has weight.
#
# R33 restored the face clause and fixed a lot (bigger refined eyes, painted
# lashes, drawn brows, colour back in the lips and cheeks) -- but the 2048² tight
# portrait still read as a mature noblewoman.  Direct A/B at seed 2520 shows
# where: fine lines around the eyes, nasolabial folds, a forehead line.  The
# face clause says "refined ADULT proportions" and R33's only youth anchor
# ("a young woman ... never matronly") sits at the END of that clause, mid-prompt.
#
# The project's own rule is position = weight (settled four times: R23/R24,
# R27, R28).  So R34 does one thing: anchor the age early and hard, and stop
# banning youth on the negative side.
#   1. subject line: "a living Eastern classical princess" -> "a YOUNG living ..."
#   2. face clause: "refined ADULT proportions" -> "refined YOUTHFUL proportions"
#   3. the anchor itself: "a young woman, refined and fresh-faced" ->
#      "a young woman in her early twenties, refined and fresh-faced, with dewy
#       clear skin"
#   4. negative: add wrinkles / fine lines / crow's feet / nasolabial folds /
#      aged skin / tired eyes / 皱纹 / 法令纹 / 眼袋 / 老气 / 疲态
#      (Qwen takes a real negative prompt, so this is the right side for it)
# Material, costume, pose, canvas, seed: untouched.
# ---------------------------------------------------------------------------
_H13_EDITS = [
    ("Photorealistic image of a living Eastern classical princess at home in her chamber "
     "in the afternoon.",
     "Photorealistic image of a young living Eastern classical princess at home in her chamber "
     "in the afternoon."),
    ("An elegant princess face with refined adult proportions:",
     "An elegant young princess face with refined youthful proportions:"),
    ("a young woman, refined and fresh-faced, never matronly and never severe.",
     "a young woman in her early twenties, refined and fresh-faced, with dewy clear skin, "
     "never matronly and never severe."),
]
for _from, _to in _H13_EDITS:
    assert _from in BASE_H12_POSE, f"R34: anchor not found: {_from[:50]!r}"
BASE_H13_POSE = BASE_H12_POSE
for _from, _to in _H13_EDITS:
    BASE_H13_POSE = BASE_H13_POSE.replace(_from, _to)
assert BASE_H13_POSE != BASE_H12_POSE, "R34: replace() was a no-op"
assert "young living Eastern classical princess" in BASE_H13_POSE
assert "refined youthful proportions" in BASE_H13_POSE
assert "adult proportions" not in BASE_H13_POSE
assert "in her early twenties" in BASE_H13_POSE

NEG_H13_PORTRAIT = NEG_H12_PORTRAIT + (
    ", wrinkles, fine lines, crow's feet, nasolabial folds, aged skin, mature face, "
    "tired eyes, dark circles, 皱纹, 法令纹, 眼袋, 老气, 疲态"
)
assert "wrinkles" in NEG_H13_PORTRAIT and "法令纹" in NEG_H13_PORTRAIT

ROUNDS[34] = {
    "engine": "qwen", "size": (2048, 768), "steps": 32, "cfg": 3.5, "negative": NEG_H7,
    "note": "anchor the age early and hard (young princess / youthful proportions / early "
            "twenties / dewy skin) and add anti-ageing terms to the negative; shots mirror R33's "
            "seeds/sizes for a direct A/B",
    "shots": [
        {"name": "ablation-window", "seed": 2910, "size": (1200, 1600), "timeout": 3600,
         "prompt": _ROUND31_POSE_WINDOW + BASE_H13_POSE},
        {"name": "skin-square", "seed": 2520, "size": (2048, 2048), "timeout": 5400,
         "negative": NEG_H13_PORTRAIT,
         "prompt": "紧肖像，半身近景，自头顶到胸前入画，脸占画面大部分："
                    "她侧过脸来迎着窗光，一只手抬起轻触面颊，纱罗松松搭在肩上，"
                    "背景是虚化的窗棂与屏风。" + BASE_H13_POSE},
        {"name": "portrait", "seed": 3030, "size": (1280, 1712), "timeout": 3600,
         "negative": NEG_H13_PORTRAIT,
         "prompt": "肖像，四分之三身，自头顶到腰际入画："
                    "她端坐在矮榻上，一手搁在膝边的茶盏旁，微微侧头望向窗外，"
                    "纱罗从肩头垂落。" + BASE_H13_POSE},
    ],
}


# ---------------------------------------------------------------------------
# Round 35: it was never the defects -- it was the word "adult".
#
# R34 attributed the loss of porcelain to the named-defect inventory, on the
# theory that "polishing marks / hairline drag lines / orange-peel" land on a
# face as wrinkles.  Auditing R25 (the phase-4 skin standard) disproves that:
# R25's prompt carries the SAME five defect items verbatim, no face clause and
# no age words at all -- and its plate reads as a *young* face under a hard fired
# glaze, with a visible pinhole on the cheek and a soft porcelain blush.
#
# So: the defects are compatible with a young glazed face.  What made R33 read
# old was "refined ADULT proportions" -- a word restored from phase 2, where it
# had been introduced (R4/R5) to cure "脸型偏幼儿" and was never re-audited.
# R34 fixed that word and added an anti-ageing negative; the porcelain then
# receded, most plausibly because "aged skin / mature face / wrinkles / fine
# lines" suppress exactly the surface variation that reads as glaze.
#
# R35 therefore removes ONLY the anti-ageing negative words.  The positive youth
# anchors (young / youthful / early twenties / dewy clear skin) stay, and so does
# the full defect inventory.  Single variable vs R34: the negative tail.
# ---------------------------------------------------------------------------
assert NEG_H13_PORTRAIT.startswith(NEG_H12_PORTRAIT), "R35: negative lineage changed"
assert NEG_H13_PORTRAIT != NEG_H12_PORTRAIT, "R35: R34 added no anti-ageing terms?"
for _age_word in ("wrinkles", "aged skin", "mature face", "法令纹", "老气"):
    assert _age_word in NEG_H13_PORTRAIT and _age_word not in NEG_H12_PORTRAIT, _age_word

ROUNDS[35] = {
    "engine": "qwen", "size": (2048, 768), "steps": 32, "cfg": 3.5, "negative": NEG_H7,
    "note": "drop the anti-ageing negative words R34 added and change nothing else: test whether "
            "they were suppressing the fired-glaze surface (R25 proves the defect inventory is "
            "compatible with a young glazed face)",
    "shots": [
        {"name": "ablation-window", "seed": 2910, "size": (1200, 1600), "timeout": 3600,
         "prompt": _ROUND31_POSE_WINDOW + BASE_H13_POSE},
        {"name": "skin-square", "seed": 2520, "size": (2048, 2048), "timeout": 5400,
         "negative": NEG_H12_PORTRAIT,
         "prompt": "紧肖像，半身近景，自头顶到胸前入画，脸占画面大部分："
                    "她侧过脸来迎着窗光，一只手抬起轻触面颊，纱罗松松搭在肩上，"
                    "背景是虚化的窗棂与屏风。" + BASE_H13_POSE},
        {"name": "portrait", "seed": 3030, "size": (1280, 1712), "timeout": 3600,
         "negative": NEG_H12_PORTRAIT,
         "prompt": "肖像，四分之三身，自头顶到腰际入画："
                    "她端坐在矮榻上，一手搁在膝边的茶盏旁，微微侧头望向窗外，"
                    "纱罗从肩头垂落。" + BASE_H13_POSE},
    ],
}


# ---------------------------------------------------------------------------
# Readable wrapping for the prompt archive
#
# A "prompt 原文" is one unbroken string (avg 1.8k chars, max 3.5k), which is
# hopeless to read or to diff by eye across rounds.  The archive therefore
# breaks it into clause-level lines.  The breaks are *presentation only* and
# strictly reversible:
#
#   * a break placed where the原文 had an ASCII space drops that space
#   * every other break (after 。！？，；、：, or between two CJK chars) is a
#     pure insertion that removed nothing
#
# so ``unwrap_prompt`` restores the byte-exact string, and the generator
# asserts the round-trip for every prompt it writes.  Breaks are only ever
# placed at positions where that rule is unambiguous -- never at a space that
# is followed by a CJK char, and never between ASCII and CJK.
# ---------------------------------------------------------------------------

ARCHIVE_WIDTH = 100
_ARCHIVE_SEP = re.compile(r"(。|！|？|\. |, |; |: |，|；|、|：)")
_ARCHIVE_STRONG = ("。", "！", "？", ". ")  # 句末：即使没到宽度也断行
_ARCHIVE_PUNCT = ("，", "；", "、", "：")  # 中文子句：断行处原文无空格


def _cols(s: str) -> int:
    """Display width, counting CJK/fullwidth characters as 2 columns."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def _tight(c: str) -> bool:
    """True for a printable ASCII char (the only place a space can sit)."""
    return bool(c) and ord(c) < 128 and not c.isspace()


def _hard_wrap(line: str, width: int) -> list[str]:
    """Fallback split for a single clause that is itself wider than ``width``."""
    out: list[str] = []
    rest = line
    while _cols(rest) > width:
        space_cut = cjk_cut = -1
        for i, ch in enumerate(rest):
            if _cols(rest[:i + 1]) > width:
                break
            nxt = rest[i + 1] if i + 1 < len(rest) else ""
            if ch == " " and _tight(nxt):
                space_cut = i
            elif nxt and not _tight(ch) and not _tight(nxt):
                cjk_cut = i + 1
        if space_cut > 0:
            out.append(rest[:space_cut])
            rest = rest[space_cut + 1:]
        elif cjk_cut > 0:
            out.append(rest[:cjk_cut])
            rest = rest[cjk_cut:]
        else:
            return out + [rest]  # nothing safe to split on: leave it long
    if rest:
        out.append(rest)
    return out


def wrap_prompt(text: str, width: int = ARCHIVE_WIDTH) -> str:
    """Break a prompt string into clause-level lines for reading/comparison."""
    parts = _ARCHIVE_SEP.split(text)
    # split() with one capture group yields [text, sep, text, sep, ..., text];
    # pair each text with the separator that follows it.
    units = [(parts[i], parts[i + 1] if i + 1 < len(parts) else "")
             for i in range(0, len(parts), 2)]
    if not units[-1][0] and not units[-1][1]:
        units.pop()

    def breakable(i: int) -> bool:
        """May a line break be placed immediately after unit ``i``?"""
        if i < 0 or i >= len(units) - 1:
            return False
        sep = units[i][1]
        nxt = units[i + 1][0][:1]
        if sep in _ARCHIVE_PUNCT:
            return True  # 中文标点后断开是纯插入，与下一字符无关
        # 英文 ", " / ". " 断开 = 用换行替代那个空格，只有下一字符是 ASCII
        # 时才能被 unwrap_prompt 无歧义地还原。
        return _tight(nxt)

    lines: list[str] = []
    cur = ""
    for i, (txt, sep) in enumerate(units):
        if cur and breakable(i - 1) and (
            units[i - 1][1] in _ARCHIVE_STRONG or _cols(cur + txt + sep) > width
        ):
            lines.append(cur)
            cur = ""
        cur += txt + sep
    if cur:
        lines.append(cur)

    out: list[str] = []
    for line in lines:
        out.extend(_hard_wrap(line, width) if _cols(line) > width else [line])
    # Drop the space a break replaced; safe because breakable() guarantees the
    # next line starts with an ASCII char whenever the break ate a space.
    return "\n".join(
        ln[:-1] if ln.endswith(" ") and i + 1 < len(out) else ln
        for i, ln in enumerate(out)
    )


def unwrap_prompt(wrapped: str) -> str:
    """Inverse of :func:`wrap_prompt`: restore the byte-exact one-line string."""
    ls = wrapped.split("\n")
    text = ls[0]
    for prev, cur in zip(ls, ls[1:]):
        text += (" " if _tight(prev[-1:]) and _tight(cur[:1]) else "") + cur
    return text


def _wrap_checked(text: str, label: str) -> str:
    """Wrap ``text``, asserting the wrap is lossless (otherwise fail loudly)."""
    wrapped = wrap_prompt(text)
    if unwrap_prompt(wrapped) != text:
        raise SystemExit(f"FATAL: prompt wrapping is not lossless for {label}")
    return wrapped


def emit_prompt_archive(out_path: str) -> int:
    """Write every round's prompt text, wrapped for reading (losslessly)."""
    lines: list[str] = [
        "# 全部轮次原始 Prompt 存档",
        "",
        "> 本文件由 `python3 run_round.py --prompts` 自动生成，内容 = **实际提交给 ComfyUI 的字符串**。",
        "> 为便于查阅与逐轮对照，代码块内已按分句换行；**换行符不属于 prompt，仅排版**。",
        "> 还原规则：行尾是 ASCII 字符时，该换行等于一个空格；否则换行处原本没有字符。",
        "> `run_round.py` 的 `unwrap_prompt()` 就是这条规则，生成时会逐条断言「还原 == 原文」。",
        "> 逐字原文（单行）另见 `run_round.py` 的 `BASE*` 常量（`python3 run_round.py <N> --dry` 可直接打印）",
        "> 与 `out/rN/round.json`（R7 起）；最终依据是服务器 `GET /history/{prompt_id}`。",
        "> 修改 prompt 请改 `run_round.py`，然后重新生成本文件。",
        "> 返回[项目首页](../README.md)",
        "",
        "## 记录在哪（三层）",
        "",
        "| 层 | 位置 | 内容 |",
        "|----|------|------|",
        "| 权威源 | `run_round.py`（`BASE*` + `ROUNDS` / `LEGACY_ROUNDS`） | 逐字 prompt（真正发出去的，单行） |",
        "| 可读文档 | 本文件 / `docs/rN.md` | 分句换行的 prompt 全文；每轮改动说明与自检 |",
        "| 机器记录 | `out/rN/round.json` | 文件名 / seed / prompt_id / 引擎 / 参数 / **prompt 原文**（R7 起） |",
        "| 服务器侧 | `GET /history/{prompt_id}` | ComfyUI 实际执行的完整图（最终依据） |",
        "",
    ]
    for n in sorted(set(LEGACY_ROUNDS) | set(ROUNDS)):
        if n in LEGACY_ROUNDS:
            spec = LEGACY_ROUNDS[n]
            lines += [
                f"## R{n} · {spec['note']}",
                "",
                f"- 引擎：`{spec['engine']}`　尺寸：{spec['size'][0]}×{spec['size'][1]}　steps：{spec['steps']}",
                f"- 方式：**单次请求 batch={spec['batch']}**（5 张共用同一段 prompt，batch 内 seed 递增，起始 seed={spec['seed']}）",
                f"- 产物：`out/r{n}/bc-r{n}_0000{{1..5}}_.png`",
                "",
                "```text",
                _wrap_checked(spec["prompt"], f"R{n}"),
                "```",
                "",
            ]
            continue
        spec = ROUNDS[n]
        lines += [
            f"## R{n} · {spec['note']}",
            "",
            f"- 引擎：`{spec.get('engine', 'zimage')}`　尺寸：{spec['size'][0]}×{spec['size'][1]}　"
            f"steps：{spec['steps']}" + (f"　cfg：{spec['cfg']}" if spec.get("cfg") else ""),
            f"- 张数：{len(spec['shots'])}（每张独立请求，seed 各自独立）",
            "",
        ]
        if spec.get("negative"):
            lines += ["**负向 prompt（全轮共用）**", "",
                      "```text", _wrap_checked(spec["negative"], f"R{n} negative"), "```", ""]
        for shot in spec["shots"]:
            # Surface any per-shot overrides so the archive always states the
            # parameters that were actually submitted.
            over = []
            if "size" in shot:
                over.append(f"{shot['size'][0]}×{shot['size'][1]}")
            if "steps" in shot:
                over.append(f"steps {shot['steps']}")
            if "cfg" in shot:
                over.append(f"cfg {shot['cfg']}")
            override = f"　（本轮覆盖：{' · '.join(over)}）" if over else ""
            lines += [
                f"### {shot['name']}　seed={shot['seed']}{override}",
                "",
                f"产物：`out/r{n}/bc-r{n}-{shot['name']}_00001_.png`",
                "",
                "```text",
                _wrap_checked(shot["prompt"], f"R{n}/{shot['name']}"),
                "```",
                "",
            ]
    text = "\n".join(lines) + "\n"
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"wrote {out_path} ({len(text)} chars, rounds {sorted(set(LEGACY_ROUNDS) | set(ROUNDS))})")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("round", type=int, nargs="?", help="round number (omit when using --prompts)")
    ap.add_argument("--server", default=SERVER)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--prompts", nargs="?", const="docs/prompts-all.md", metavar="OUT.md",
                    help="write every round's full prompt text to Markdown (default docs/prompts-all.md)")
    args = ap.parse_args(argv)

    if args.prompts:
        return emit_prompt_archive(args.prompts)
    if args.round is None:
        ap.error("a round number is required (or use --prompts)")

    # --dry prints the byte-exact single-line prompt, for every round including
    # the legacy batch rounds (which have no per-shot structure).
    if args.dry and args.round in LEGACY_ROUNDS:
        leg = LEGACY_ROUNDS[args.round]
        print(f"--- R{args.round} (batch={leg['batch']}, seed {leg['seed']}) ---\n{leg['prompt']}\n")
        return 0

    if args.round not in ROUNDS:
        ap.error(f"round {args.round} is not defined yet (have: {sorted(ROUNDS)})")
    spec = ROUNDS[args.round]
    engine = spec.get("engine", "zimage")
    shots = spec["shots"]
    out_dir = os.path.join(HERE, "out", f"r{args.round}")
    os.makedirs(out_dir, exist_ok=True)

    if args.dry:
        for shot in shots:
            print(f"--- {shot['name']} (seed {shot['seed']}) ---\n{shot['prompt']}\n")
        return 0

    log = []
    for i, shot in enumerate(shots, start=1):
        prefix = f"bc-r{args.round}-{shot['name']}"
        # Per-shot overrides: a shot may carry its own size / steps / cfg / timeout,
        # which lets one round run a resolution or step-count ablation.
        size = tuple(shot.get("size", spec["size"]))
        steps = shot.get("steps", spec["steps"])
        cfg = shot.get("cfg", spec.get("cfg", 3.0))
        timeout = shot.get("timeout", 2400)
        # Per-shot negative: a round-level negative may ban crops (R28 added
        # "portrait crop / close-up crop" to force full bodies), which would
        # fight a deliberately tight skin plate.  Same override pattern as
        # size / steps / cfg / timeout.
        negative = shot.get("negative", spec.get("negative", ""))
        print(f"[{i}/{len(shots)}] {prefix} seed={shot['seed']} engine={engine} "
              f"{size[0]}x{size[1]} steps={steps}", flush=True)
        common = dict(
            server=args.server,
            prompt=shot["prompt"],
            width=size[0],
            height=size[1],
            steps=steps,
            seed=shot["seed"],
            filename_prefix=prefix,
            out_dir=out_dir,
            timeout=timeout,
            quiet=True,
        )
        if engine == "qwen":
            result = qw.generate(negative=negative, cfg=cfg, **common)
        else:
            result = cg.generate(workflow=WORKFLOW, **common)
        log.append({
            "file": result["local_paths"][0] if result["local_paths"] else None,
            "seed": shot["seed"],
            "name": shot["name"],
            "engine": engine,
            "prompt_id": result["prompt_id"],
            "status": result["status"],
            "prompt": shot["prompt"],
            "negative": negative,
            "width": size[0],
            "height": size[1],
            "steps": steps,
            "cfg": cfg,
        })
        print(f"      -> {log[-1]['file']}", flush=True)

    with open(os.path.join(out_dir, "round.json"), "w", encoding="utf-8") as fh:
        json.dump({"round": args.round, "engine": engine, "note": spec["note"], "shots": log},
                  fh, ensure_ascii=False, indent=2)
    print(json.dumps(log, ensure_ascii=False, indent=2))
    return 0 if all(item["file"] for item in log) else 1


if __name__ == "__main__":
    sys.exit(main())
