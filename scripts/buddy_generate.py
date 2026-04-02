#!/usr/bin/env python3
"""Generate stickers for any Claude Code buddy/companion via Gemini (Nano Banana).

Reads buddy species, stats, rarity from ~/.claude.json (recomputed bones + stored soul).
Generates emotion presets tailored to the buddy's type and personality.
"""

import argparse
import asyncio
import base64
import json
import os
import sys
import tempfile
from pathlib import Path

try:
    import httpx
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx", "-q"])
    import httpx

# --- Config ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-exp-image-generation")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Reads from plugin userConfig env vars (CLAUDE_PLUGIN_OPTION_*) or direct env
OPENROUTER_API_KEY = os.environ.get("CLAUDE_PLUGIN_OPTION_OPENROUTER_API_KEY", os.environ.get("OPENROUTER_API_KEY", ""))
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemini-2.5-flash-image")

TELEGRAM_BOT_TOKEN = os.environ.get("CLAUDE_PLUGIN_OPTION_TELEGRAM_BOT_TOKEN", os.environ.get("TELEGRAM_BOT_TOKEN", ""))

TELEGRAM_SESSION = os.path.expanduser("~/.claude/scripts/telegram-mcp/session")
TELEGRAM_ENV = os.path.expanduser("~/.claude/scripts/telegram-mcp/.env")
CLAUDE_JSON = os.path.expanduser("~/.claude.json")

# Use plugin data dir if available, otherwise fallback
PLUGIN_DATA = os.environ.get("CLAUDE_PLUGIN_DATA", "")
OUTPUT_DIR = Path(PLUGIN_DATA) / "stickers" if PLUGIN_DATA else Path(os.environ.get("BUDDY_OUTPUT_DIR", os.path.expanduser("~/.claude/buddy-stickers")))

# ============================================================
# Species visual descriptions → consistent image generation
# ============================================================
SPECIES_VISUALS = {
    "duck":      "small cute yellow rubber duck character, round body, tiny orange beak, beady eyes",
    "goose":     "small mischievous white goose character, long neck, orange beak, chaotic energy",
    "cat":       "small cute round cat character, pointy ears, whiskers, soft fur texture",
    "rabbit":    "small cute round bunny character, long floppy ears, fluffy tail, soft",
    "owl":       "small wise round owl character, large eyes, tiny beak, feathery texture",
    "penguin":   "small cool round penguin character, tuxedo pattern, tiny flippers",
    "turtle":    "small chill round turtle character, green shell, sleepy eyes, relaxed",
    "snail":     "small round snail character, spiral shell, two eye stalks, glistening",
    "dragon":    "small cute round baby dragon character, tiny wings, small flame, scales",
    "octopus":   "small cute round octopus character, eight tiny tentacles, big eyes, squishy",
    "axolotl":   "small cute round pink axolotl character, feathery gills, permanent smile, kawaii",
    "ghost":     "small cute round ghost character, translucent white, floating, playful expression",
    "robot":     "small cute round robot character, antenna, LED eyes, metallic body, boxy-round",
    "blob":      "small cute round amorphous blob character, gelatinous, semi-transparent, jiggly",
    "cactus":    "small cute round cactus character, tiny spines, flower on top, green",
    "mushroom":  "small cute round mushroom character, spotted cap, tiny stem, forest vibes",
    "chonk":     "small absurdly chubby round mochi blob character in soft warm peach-pink color (like a blushing mochi), impossibly soft and squishy, tiny stubby limbs too small for its body, maximum roundness, derpy half-closed eyes with Buddhist acceptance expression, slightly vibrating, goofy and endearing, BOLD THICK BLACK OUTLINE around entire body",
    "capybara":  "small cute round capybara character, chill expression, brown fur, tiny ears, zen master vibes",
}

# ============================================================
# Species-specific emotion presets
# Each species gets 12 unique emotions that match their vibe
# ============================================================
SPECIES_PRESETS = {
    "chonk": {
        "zen":       "sitting peacefully, eyes half-closed in zen calm, tiny sparkle above head",
        "bug":       "slightly vibrating with motion lines, tiny sweat drop, maintaining perfect composure",
        "sarcasm":   "one eye slightly twitching, mouth a thin pressed line, suppressed energy",
        "chaos":     "watching small cartoon flames around him with cup of tea, completely serene",
        "approve":   "both eyes fully open wide (rare!), tiny nod, golden sparkle",
        "vibrate":   "vibrating intensely with motion blur, eyes still perfectly calm",
        "meditate":  "floating above ground, eyes closed, faint golden halo glow",
        "deadline":  "surrounded by flying clocks and papers, expression completely unchanged",
        "facepalm":  "tiny stub arm covering face, one eye peeking through",
        "sleep":     "lying on side like melted puddle, zzz bubbles, shapeless from relaxation",
        "itworks":   "both eyes wide open in shock, levitating, sparkles everywhere",
        "hug":       "two of them hugging, merging slightly like soft mochi, warm glow",
    },
    "duck": {
        "quack":     "mouth wide open quacking loudly, sound waves visible",
        "swim":      "floating in tiny puddle, content expression, ripples around",
        "debug":     "wearing tiny detective hat, magnifying glass, inspecting code",
        "rage":      "flapping wings rapidly, tiny anger symbols, still adorable",
        "bath":      "in tiny bathtub with bubbles, rubber duck inception, relaxed",
        "follow":    "waddling in a line, determined expression, tiny footprints behind",
        "rain":      "standing in rain with tiny umbrella, happy expression",
        "bread":     "excitedly looking at piece of bread, sparkle eyes",
        "nap":       "tucked into wing, sleeping peacefully, zzz bubbles",
        "fly":       "attempting to fly with tiny wings spread, determined face",
        "approve":   "giving thumbs up with wing tip, confident wink",
        "hug":       "two ducks nuzzling beaks together, tiny hearts",
    },
    "goose": {
        "honk":      "aggressive honking, mouth wide open, chaos energy radiating",
        "steal":     "running away with stolen keyboard key in beak, mischievous grin",
        "chase":     "wings spread menacingly, running forward, pure chaos",
        "innocent":  "sitting angelically, halo above head, obviously guilty",
        "judge":     "staring directly with intense disapproval, one eyebrow raised",
        "chaos":     "surrounded by overturned objects and flames, looking satisfied",
        "peace":     "rare moment of calm, sitting by lake, serene (suspicious)",
        "plan":      "scheming face, tiny thought bubble with evil plan",
        "victory":   "standing on pile of stolen items, triumphant pose",
        "hiss":      "neck extended, hissing, defensive posture",
        "nap":       "sleeping with one eye secretly open, never fully trusts",
        "hug":       "reluctantly allowing hug, stiff body, secretly enjoying it",
    },
    "cat": {
        "loaf":      "in perfect bread loaf position, eyes half-closed, content",
        "zoomies":   "running at top speed, motion blur, wild eyes, midnight energy",
        "knock":     "pushing object off table edge, direct eye contact, no remorse",
        "purr":      "curled up, vibration lines, eyes fully closed, happy",
        "judge":     "sitting upright, looking down with maximum disdain",
        "box":       "squeezed into tiny box too small, happy despite physics",
        "hunt":      "butt wiggle, focused eyes, about to pounce on cursor",
        "yawn":      "huge dramatic yawn showing tiny fangs",
        "gift":      "proudly presenting dead bug, expecting praise",
        "ignore":    "facing away, tail up, deliberately ignoring",
        "belly":     "showing belly (trap!), innocent eyes, claws slightly visible",
        "hug":       "headbutting affectionately, eyes closed, purr lines",
    },
    "rabbit": {
        "binky":     "jumping with twist mid-air, pure joy, ears flopping",
        "flop":      "dramatically flopping onto side, maximum relaxation",
        "thump":     "back foot thumping, annoyed expression, something is wrong",
        "munch":     "tiny carrot, cheeks puffed, happy munching",
        "zoom":      "running in circles, speed lines, ears back",
        "nose":      "nose twitching rapidly, investigating something suspicious",
        "stand":     "standing on hind legs, ears up, alert and curious",
        "dig":       "digging frantically, dirt flying behind, focused",
        "groom":     "washing face with tiny paws, meticulous",
        "hide":      "peeking out from behind object, only ears and eyes visible",
        "sleep":     "curled in ball, ears folded down, peaceful",
        "hug":       "two bunnies grooming each other, gentle and sweet",
    },
    "owl": {
        "wise":      "perched on stack of books, glasses on, thoughtful expression",
        "rotate":    "head turned 180 degrees, unsettling but cute",
        "hoot":      "hooting at moon, sound waves visible, majestic",
        "swoop":     "wings spread wide, diving down gracefully",
        "pellet":    "looking slightly embarrassed, tiny pellet nearby",
        "blink":     "slow deliberate blink, conveying deep judgment",
        "read":      "tiny book open, reading intently, cup of tea nearby",
        "sleep":     "one eye closed one open, half-sleeping, still watching",
        "ruffle":    "feathers puffed up, looking twice as big, offended",
        "hunt":      "silent flight pose, focused piercing eyes",
        "approve":   "slow sage nod, eyes half-closed, ancient wisdom energy",
        "hug":       "wrapping wing around smaller creature, protective",
    },
    "penguin": {
        "slide":     "sliding on belly, wheee expression, ice trail",
        "waddle":    "waddling with swagger, sunglasses, cool vibes",
        "fish":      "catching fish mid-air, triumphant expression",
        "huddle":    "standing in group for warmth, cozy, snowflakes",
        "dive":      "diving into water splash, graceful",
        "cold":      "shivering in tropical setting, confused, out of element",
        "tux":       "adjusting invisible bow tie, looking fancy",
        "egg":       "balancing egg on feet, careful focused expression",
        "dance":     "happy feet dance, musical notes around",
        "judge":     "arms crossed (flippers), unimpressed stare",
        "sleep":     "standing sleep, head tucked, balanced perfectly",
        "hug":       "two penguins touching beaks, heart shape between them",
    },
    "dragon": {
        "flame":     "breathing tiny flame, surprised by own fire, cute",
        "hoard":     "sitting on pile of golden coins, protective, tiny",
        "fly":       "first flight attempt, wobbly wings, determined",
        "roar":      "tiny roar with small flame puff, trying to be scary",
        "curl":      "curled around own tail, sleeping, smoke from nostril",
        "egg":       "just hatched, eggshell on head, blinking at world",
        "treasure":  "hugging single gold coin, mine, possessive eyes",
        "sneeze":    "sneezing fire accidentally, oops expression",
        "grow":      "flexing tiny arms, trying to look big and fierce",
        "read":      "reading ancient scroll, scholarly glasses, wise",
        "protect":   "standing guard pose, wings spread, fierce but smol",
        "hug":       "wrapping tail around friend, sharing warmth, tiny flames as hearts",
    },
    "octopus": {
        "multitask": "each tentacle doing different task, typing+drinking+reading+coding",
        "ink":       "startled, tiny ink cloud, embarrassed expression",
        "wave":      "waving with all 8 tentacles at once, enthusiastic",
        "hide":      "camouflaged against background, only eyes visible",
        "squeeze":   "fitting through impossibly small space, determined",
        "smart":     "wearing monocle, three tentacles holding books",
        "dance":     "tentacles flowing in rhythm, graceful underwater dance",
        "tangle":    "tentacles knotted up, confused expression, help",
        "garden":    "arranging tiny underwater garden, peaceful",
        "tool":      "each tentacle holding different tool, ready for anything",
        "sleep":     "all tentacles curled inward, eyes closed, peaceful ball",
        "hug":       "wrapping all tentacles around friend, maximum embrace",
    },
    "axolotl": {
        "smile":     "permanent adorable smile, gills waving gently, pink glow",
        "regenerate":"sparkle effect around body, healing energy, magical",
        "swim":      "floating gracefully, feathery gills spread, ethereal",
        "curious":   "head tilted, gills perked up, investigating something",
        "bubble":    "blowing tiny bubbles, playful, underwater joy",
        "wave":      "waving tiny hand, gills bouncing, friendly",
        "blush":     "turning deeper pink, shy expression, gills down",
        "crown":     "gills forming natural crown shape, majestic, regal",
        "eat":       "vacuum-sucking food, cheeks puffed, happy",
        "glow":      "bioluminescent glow, magical night scene, ethereal",
        "sleep":     "resting on plant leaf, gills relaxed, gentle breathing",
        "hug":       "two axolotls tangled together, gills intertwined, cute",
    },
    "ghost": {
        "boo":       "popping out, tiny boo text, not actually scary, cute",
        "phase":     "halfway through wall, stuck, embarrassed expression",
        "float":     "drifting peacefully upward, serene, translucent",
        "spook":     "trying very hard to be scary, failing adorably",
        "vanish":    "partially invisible, fading in/out, mysterious",
        "chain":     "dragging tiny chain, dramatic, theatrical ghost",
        "read":      "floating through library, reading, glasses on",
        "haunt":     "following someone, helpful haunting, carrying their coffee",
        "glow":      "glowing warmly in darkness, comforting nightlight",
        "cold":      "shivering despite being dead, existential confusion",
        "sleep":     "sleeping upside down like a bat, zzz floating up",
        "hug":       "trying to hug but phasing through, sad, eventually succeeds",
    },
    "robot": {
        "compute":   "eyes showing loading bar, processing, steam from head",
        "spark":     "tiny electrical sparks, malfunction, still cute",
        "upgrade":   "installing update, progress bar above head, waiting",
        "beep":      "beeping happily, musical notes as binary, dancing",
        "error":     "screen showing 404, confused tilt, question marks",
        "charge":    "plugged into wall, battery icon filling, sleepy",
        "scan":      "laser eyes scanning code, detective mode",
        "dance":     "robot dance, stiff but enthusiastic movements",
        "rust":      "tiny rust spot, looking at it with concern",
        "build":     "welding something tiny, sparks flying, focused",
        "sleep":     "standing, screen showing screensaver, powered down",
        "hug":       "extending extendable arms for hug, warm LED heart on chest",
    },
    "blob": {
        "jiggle":    "wobbling back and forth, jelly physics, content",
        "split":     "temporarily splitting into two, both halves confused",
        "absorb":    "absorbing tiny object into body, visible inside, oops",
        "morph":     "shape-shifting between forms, identity crisis, fun",
        "bounce":    "bouncing like a ball, happy trail of sparkles",
        "puddle":    "melted flat into puddle, relaxation maximum",
        "grow":      "inflating larger, surprised at own size",
        "color":     "cycling through rainbow colors, mood ring energy",
        "drip":      "tiny drip falling off, looking at it sadly",
        "mirror":    "perfectly mimicking another character shape",
        "sleep":     "completely flat pancake, barely visible, ultimate relax",
        "hug":       "engulfing friend in warm blob hug, cozy",
    },
    "cactus": {
        "bloom":     "tiny flower blooming on top, proud, beautiful moment",
        "poke":      "accidentally poking someone, apologetic expression",
        "thirst":    "in desert, single water drop, hopeful eyes",
        "sun":       "basking in sunlight, happy face, glowing",
        "hug":       "wanting hug, arms out, but spines prevent it, sad then finds way with oven mitts",
        "grow":      "tiny new arm sprouting, surprised and excited",
        "tough":     "flexing, showing off spines like muscles, fierce",
        "rain":      "standing in rain, ecstatic expression, absorbing",
        "pot":       "in cute decorated pot, cozy home vibes",
        "friend":    "tiny bird sitting on top, both happy, symbiosis",
        "sleep":     "nighttime desert, stars above, peaceful sway",
        "dance":     "swaying in wind, maracas nearby, fiesta vibes",
    },
    "mushroom": {
        "sprout":    "emerging from ground, tiny, cap still wet, newborn",
        "spore":     "releasing cloud of sparkly spores, magical",
        "glow":      "bioluminescent in dark forest, ethereal, magical",
        "rain":      "acting as umbrella for tiny bug, helpful, cozy",
        "grow":      "growing rapidly, time-lapse effect, expanding cap",
        "forest":    "among other tiny mushrooms, community, mycelium visible",
        "fairy":     "fairy ring formation, magical sparkles, enchanted",
        "bounce":    "using cap as trampoline for tiny creature, fun",
        "cook":      "in tiny chef hat, cooking (not self), wholesome",
        "toxic":     "warning sign, purple glow, dont eat me expression",
        "sleep":     "cap drooped over like nightcap, snoring, cozy",
        "hug":       "two mushrooms leaning together, caps touching, sweet",
    },
    "turtle": {
        "retreat":   "pulled into shell, only eyes peeking out, safe",
        "race":      "moving surprisingly fast, determined, speed lines (for a turtle)",
        "stack":     "turtles stacked on each other, tower, balanced",
        "sun":       "basking on rock, sunbeam, ultimate relaxation",
        "swim":      "graceful underwater, flippers spread, majestic",
        "carry":     "tiny world on back, atlas pose, philosophical",
        "munch":     "eating lettuce leaf, slow deliberate bites, content",
        "old":       "wearing tiny glasses, wise old expression, seen it all",
        "hide":      "fully in shell, pretending to be a rock",
        "patient":   "waiting calmly, infinite patience embodied",
        "sleep":     "in shell, tiny zzz coming from opening, cozy",
        "hug":       "two turtles touching shells, gentle bump, affection",
    },
    "snail": {
        "trail":     "leaving sparkly trail behind, proud of it, artistic",
        "shell":     "retreated in shell, spiral visible, cozy inside",
        "rain":      "dancing in rain drops, each drop huge relative to size, joy",
        "slow":      "racing with turtle, both in slow motion, dramatic",
        "climb":     "scaling vertical surface, determined, defying gravity",
        "garden":    "among giant flowers, tiny explorer, wonder",
        "mail":      "carrying tiny letter on shell, snail mail, cute",
        "bubble":    "making tiny bubbles, entertained by simple things",
        "leaf":      "riding a leaf like a boat, sailing, adventure",
        "friend":    "with tiny ladybug friend, having picnic on mushroom",
        "sleep":     "in shell, sealed entrance, deep hibernation, cozy",
        "hug":       "two snails with intertwined eye stalks, slow tender hug",
    },
    "capybara": {
        "soak":      "sitting in hot spring, eyes closed, peak relaxation, steam",
        "friend":    "surrounded by different animals sitting on/around it, unbothered",
        "munch":     "eating grass slowly, zen munching, no thoughts",
        "chill":     "lying flat, zero stress energy, everything is fine",
        "swim":      "nose barely above water, cruising, effortless",
        "stack":     "orange/tangerine balanced on head, perfectly still, unbothered",
        "squad":     "group of capybaras in formation, squad goals",
        "rain":      "sitting in rain, doesn't care, transcended weather",
        "sun":       "sunbathing, belly up, maximum vulnerability = maximum trust",
        "bird":      "bird on head, both sleeping, interspecies harmony",
        "sleep":     "sleeping in pile with other animals, ultimate peace",
        "hug":       "leaning against friend, weight of the world gone, warm",
    },
}

# ============================================================
# Rarity-specific visual modifiers
# ============================================================
RARITY_MODIFIERS = {
    "common":    "",
    "uncommon":  "slightly sparkly aura, ",
    "rare":      "glowing subtle aura, rare specimen energy, ",
    "epic":      "strong magical aura, purple shimmer, epic energy, ",
    "legendary": "intense golden aura, legendary radiance, celestial sparkles, ",
}

# ============================================================
# Stat-driven style modifiers (applied when stat > 70)
# ============================================================
STAT_MODIFIERS = {
    "debugging":  "wearing tiny detective hat or magnifying glass, ",
    "patience":   "extra serene expression, zen lines, peaceful energy, ",
    "chaos":      "tiny chaos particles around, slightly glitchy energy, ",
    "wisdom":     "tiny halo or book nearby, sage-like presence, ",
    "snark":      "slightly smug expression, one eyebrow raised, ",
}


def load_buddy() -> dict:
    """Load buddy/companion info from ~/.claude.json."""
    if not os.path.exists(CLAUDE_JSON):
        print(f"ERROR: {CLAUDE_JSON} not found.", file=sys.stderr)
        sys.exit(1)

    with open(CLAUDE_JSON) as f:
        data = json.load(f)

    companion = data.get("companion", {})
    if not companion:
        print("ERROR: No companion in ~/.claude.json. Run /buddy first.", file=sys.stderr)
        sys.exit(1)

    return companion


def detect_species(companion: dict) -> str:
    """Detect species from companion data. Falls back to personality-based heuristic."""
    # Direct field (if bones are stored)
    species = companion.get("species", "").lower()
    if species in SPECIES_VISUALS:
        return species

    # Heuristic from personality text
    personality = companion.get("personality", "").lower()
    for sp in SPECIES_VISUALS:
        if sp in personality:
            return sp

    # Known keywords
    keyword_map = {
        "chonk": "chonk", "serene": "chonk", "mochi": "chonk",
        "honk": "goose", "steal": "goose",
        "quack": "duck", "waddle": "duck",
        "purr": "cat", "loaf": "cat",
        "hoot": "owl", "wise": "owl",
        "tentacle": "octopus",
        "gills": "axolotl", "axolotl": "axolotl",
        "ghost": "ghost", "boo": "ghost",
        "robot": "robot", "beep": "robot",
        "capybara": "capybara", "chill": "capybara",
        "flame": "dragon", "dragon": "dragon",
        "shell": "turtle",
        "mushroom": "mushroom", "spore": "mushroom",
        "cactus": "cactus", "spine": "cactus",
        "blob": "blob", "jelly": "blob",
        "snail": "snail", "trail": "snail",
        "penguin": "penguin", "tux": "penguin",
        "bunny": "rabbit", "rabbit": "rabbit",
    }

    for keyword, sp in keyword_map.items():
        if keyword in personality:
            return sp

    return "blob"  # safe fallback


def build_visual_prompt(companion: dict) -> str:
    """Build a complete visual prompt from buddy metadata."""
    species = detect_species(companion)
    name = companion.get("name", "Buddy")
    rarity = companion.get("rarity", "common").lower()
    stats = companion.get("stats", {})

    # Base species visual
    visual = SPECIES_VISUALS.get(species, SPECIES_VISUALS["blob"])

    # Rarity modifier
    rarity_mod = RARITY_MODIFIERS.get(rarity, "")

    # Stat modifiers (for high stats)
    stat_mods = ""
    for stat_name, modifier in STAT_MODIFIERS.items():
        val = stats.get(stat_name, stats.get(stat_name.upper(), 0))
        if isinstance(val, (int, float)) and val > 70:
            stat_mods += modifier

    # Hat
    hat = companion.get("hat", "")
    hat_mod = f"wearing a tiny {hat}, " if hat else ""

    # Shiny
    shiny_mod = "rainbow shimmer effect, sparkle particles, " if companion.get("shiny") else ""

    prompt = (
        f"Character: {name}. {rarity_mod}{shiny_mod}{hat_mod}{stat_mods}"
        f"{visual}. "
        f"BOLD THICK BLACK OUTLINE around entire character (like a coloring book), "
        f"TRANSPARENT BACKGROUND, NO background at all, sticker design, "
        f"kawaii minimal style, flat colors, clean vector look, "
        f"strong black border around every shape, isolated character only."
    )
    return prompt, species


def get_presets(species: str) -> dict:
    """Get emotion presets for a species."""
    return SPECIES_PRESETS.get(species, SPECIES_PRESETS.get("blob"))


def load_telegram_creds():
    creds = {}
    with open(TELEGRAM_ENV) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                creds[k.strip()] = v.strip()
    return int(creds["TELEGRAM_API_ID"]), creds["TELEGRAM_API_HASH"]


def _generate_via_openrouter(prompt: str) -> bytes | None:
    """Try generating image via OpenRouter API."""
    if not OPENROUTER_API_KEY:
        return None

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        with httpx.Client(timeout=180) as client:
            resp = client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()

        choices = data.get("choices", [])
        if not choices:
            print(f"OpenRouter: no choices in response", file=sys.stderr)
            return None

        message = choices[0].get("message", {})
        content = message.get("content", "")
        images = message.get("images", [])

        # Check images array first (OpenRouter native format)
        for img in images:
            url_data = ""
            if isinstance(img, dict):
                url_data = img.get("image_url", {}).get("url", "") or img.get("url", "")
            if url_data.startswith("data:image"):
                b64 = url_data.split(",", 1)[1]
                return base64.b64decode(b64)

        # Check content for inline images
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict):
                    inline = part.get("inline_data") or part.get("inlineData")
                    if inline and "data" in inline:
                        return base64.b64decode(inline["data"])
                    url_data = part.get("image_url", {}).get("url", "")
                    if url_data.startswith("data:image"):
                        b64 = url_data.split(",", 1)[1]
                        return base64.b64decode(b64)

        if isinstance(content, str) and "data:image" in content:
            import re
            match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=\n]+)', content)
            if match:
                return base64.b64decode(match.group(1))

        print(f"OpenRouter: no image found (content_len={len(str(content))}, images={len(images)})", file=sys.stderr)
        return None

    except httpx.HTTPStatusError as e:
        print(f"OpenRouter error: {e.response.status_code} {e.response.text[:200]}", file=sys.stderr)
        return None


def _generate_via_gemini(prompt: str) -> bytes | None:
    """Try generating image via Gemini API directly."""
    if not GEMINI_API_KEY:
        return None

    models = [
        GEMINI_MODEL,
        "gemini-2.0-flash-preview-image-generation",
        "gemini-2.0-flash-exp-image-generation",
    ]

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": "1:1"},
        },
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        try:
            with httpx.Client(timeout=120) as client:
                resp = client.post(url, headers={"Content-Type": "application/json"}, json=payload)
                resp.raise_for_status()
                data = resp.json()

            for candidate in data.get("candidates", []):
                for part in candidate.get("content", {}).get("parts", []):
                    inline = part.get("inlineData") or part.get("inline_data")
                    if inline:
                        return base64.b64decode(inline["data"])
        except httpx.HTTPStatusError:
            continue

    return None


def _remove_background(image_bytes: bytes) -> bytes:
    """Remove white/light background, make it transparent."""
    from PIL import Image
    from io import BytesIO

    img = Image.open(BytesIO(image_bytes)).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # Make white and near-white pixels transparent
            if r > 230 and g > 230 and b > 230:
                pixels[x, y] = (r, g, b, 0)
            # Also handle light gray
            elif r > 210 and g > 210 and b > 210:
                # Semi-transparent for anti-aliasing
                alpha = int((255 - max(r, g, b)) * 255 / 45)
                pixels[x, y] = (r, g, b, min(alpha, a))

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_image(base_style: str, emotion_prompt: str) -> bytes:
    """Generate image trying OpenRouter first, then Gemini direct. Removes background."""
    full_prompt = f"{base_style} Pose/emotion: {emotion_prompt}"

    # Try OpenRouter first (no geo-restrictions)
    result = _generate_via_openrouter(full_prompt)
    if not result:
        # Fallback to Gemini direct
        result = _generate_via_gemini(full_prompt)

    if not result:
        print("ERROR: All providers failed. Set OPENROUTER_API_KEY or GEMINI_API_KEY.", file=sys.stderr)
        sys.exit(1)

    # Remove background automatically
    result = _remove_background(result)
    return result


async def send_to_telegram(image_bytes: bytes, caption: str, chat: str):
    from telethon import TelegramClient
    api_id, api_hash = load_telegram_creds()
    client = TelegramClient(TELEGRAM_SESSION, api_id, api_hash)
    await client.start()
    entity = await client.get_entity(chat)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(image_bytes)
        tmp_path = f.name
    try:
        await client.send_file(entity, tmp_path, caption=caption)
        print(f"Sent to {chat}")
    finally:
        os.unlink(tmp_path)
        await client.disconnect()


# ============================================================
# Telegram Sticker Pack creation via Bot API
# https://core.telegram.org/stickers
# ============================================================

def _bot_api(method: str, data: dict = None, files: dict = None) -> dict:
    """Call Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}"
    with httpx.Client(timeout=30) as client:
        if files:
            resp = client.post(url, data=data or {}, files=files)
        else:
            resp = client.post(url, json=data or {})
        resp.raise_for_status()
        result = resp.json()
        if not result.get("ok"):
            print(f"Bot API error: {result}", file=sys.stderr)
        return result


def _prepare_sticker_png(image_bytes: bytes) -> bytes:
    """Resize image to 512x512 PNG for Telegram stickers.
    Uses PIL if available, otherwise returns as-is (Gemini usually outputs correct size).
    """
    try:
        from PIL import Image
        from io import BytesIO
        img = Image.open(BytesIO(image_bytes))
        # Telegram requires one side exactly 512px
        img = img.resize((512, 512), Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except ImportError:
        return image_bytes  # hope for the best


def get_telegram_user_id() -> int:
    """Get user ID from Telethon session (the account owner)."""
    import sqlite3
    db_path = TELEGRAM_SESSION + ".session"
    if not os.path.exists(db_path):
        db_path = TELEGRAM_SESSION
    conn = sqlite3.connect(db_path)
    try:
        # Telethon stores sessions in SQLite
        row = conn.execute("SELECT * FROM sessions LIMIT 1").fetchone()
        # user_id is typically at index 3 or we get it from entities
        # Safer: read from the 'self' entity
        me = conn.execute("SELECT id FROM entities WHERE id > 0 ORDER BY id LIMIT 1").fetchone()
        if me:
            return me[0]
        # Fallback: session table
        if row and len(row) > 3:
            return row[3] if row[3] else row[2]
    finally:
        conn.close()
    print("ERROR: Cannot determine Telegram user ID from session", file=sys.stderr)
    sys.exit(1)


def create_sticker_pack(buddy_name: str, stickers: list[tuple[str, bytes]]):
    """Create or add to a Telegram sticker pack.

    Args:
        buddy_name: Name of the buddy (used in pack name)
        stickers: List of (emotion_name, png_bytes) tuples
    """
    if not TELEGRAM_BOT_TOKEN:
        print("WARN: TELEGRAM_BOT_TOKEN not set, skipping sticker pack creation", file=sys.stderr)
        return

    user_id = get_telegram_user_id()
    bot_info = _bot_api("getMe")
    bot_username = bot_info["result"]["username"]

    # Pack name must be alphanumeric + underscores, ending with _by_<bot_username>
    safe_name = buddy_name.lower().replace(" ", "_").replace("-", "_")
    pack_name = f"{safe_name}_buddy_by_{bot_username}"
    pack_title = f"{buddy_name} Sticker Pack"

    print(f"Creating sticker pack: {pack_title} ({pack_name})")

    # Check if pack exists
    existing = _bot_api("getStickerSet", {"name": pack_name})
    pack_exists = existing.get("ok", False)

    for i, (emotion, png_bytes) in enumerate(stickers):
        png_bytes = _prepare_sticker_png(png_bytes)
        emoji = _emotion_to_emoji(emotion)

        sticker_data = {
            "user_id": user_id,
            "sticker": ("sticker.png", png_bytes, "image/png"),
            "sticker_format": "static",
        }

        if not pack_exists and i == 0:
            # Create new pack with first sticker
            files = {"png_sticker": ("sticker.png", png_bytes, "image/png")}
            input_sticker = json.dumps({
                "sticker": "attach://png_sticker",
                "emoji_list": [emoji],
                "format": "static",
            })
            result = _bot_api("createNewStickerSet", {
                "user_id": user_id,
                "name": pack_name,
                "title": pack_title,
                "stickers": f"[{input_sticker}]",
            }, files=files)

            if result.get("ok"):
                pack_exists = True
                print(f"  Created pack + added {emotion} {emoji}")
            else:
                print(f"  ERROR creating pack: {result}", file=sys.stderr)
                return
        else:
            # Add sticker to existing pack
            files = {"png_sticker": ("sticker.png", png_bytes, "image/png")}
            input_sticker = json.dumps({
                "sticker": "attach://png_sticker",
                "emoji_list": [emoji],
                "format": "static",
            })
            result = _bot_api("addStickerToSet", {
                "user_id": user_id,
                "name": pack_name,
                "sticker": input_sticker,
            }, files=files)

            if result.get("ok"):
                print(f"  Added {emotion} {emoji}")
            else:
                print(f"  ERROR adding {emotion}: {result}", file=sys.stderr)

    print(f"\nSticker pack ready: https://t.me/addstickers/{pack_name}")


def _emotion_to_emoji(emotion: str) -> str:
    """Map emotion name to a fitting emoji for the sticker."""
    mapping = {
        # Chonk
        "zen": "\U0001f9d8", "bug": "\U0001f41b", "sarcasm": "\U0001f612",
        "chaos": "\U0001f525", "approve": "\U0001f44d", "vibrate": "\U0001f4f3",
        "meditate": "\U0001f9d8", "deadline": "\u23f0", "facepalm": "\U0001f926",
        "sleep": "\U0001f634", "itworks": "\U0001f389", "hug": "\U0001f917",
        # Duck
        "quack": "\U0001f986", "swim": "\U0001f30a", "debug": "\U0001f50d",
        "bath": "\U0001f6c1", "bread": "\U0001f35e", "fly": "\U0001f4a8",
        # Goose
        "honk": "\U0001f4e2", "steal": "\U0001f3c3", "chase": "\U0001f4a8",
        "innocent": "\U0001f607", "judge": "\U0001f9d0", "plan": "\U0001f608",
        "peace": "\U0001f54a", "victory": "\U0001f3c6", "hiss": "\U0001f620",
        # Cat
        "loaf": "\U0001f35e", "zoomies": "\U0001f4a8", "knock": "\U0001f612",
        "purr": "\U0001f63b", "box": "\U0001f4e6", "hunt": "\U0001f440",
        "yawn": "\U0001f971", "gift": "\U0001f381", "ignore": "\U0001f644",
        "belly": "\u26a0\ufe0f",
        # Common
        "hello": "\U0001f44b", "think": "\U0001f914", "celebrate": "\U0001f389",
        "angry": "\U0001f624", "love": "\u2764\ufe0f", "coffee": "\u2615",
        "nap": "\U0001f634", "rain": "\U0001f327\ufe0f", "friend": "\U0001f91d",
        # More
        "slide": "\U0001f3bf", "waddle": "\U0001f60e", "fish": "\U0001f3a3",
        "flame": "\U0001f525", "hoard": "\U0001f4b0", "roar": "\U0001f432",
        "multitask": "\U0001f9d1\u200d\U0001f4bb", "ink": "\U0001f4a6",
        "smile": "\U0001f60a", "regenerate": "\u2728", "boo": "\U0001f47b",
        "compute": "\U0001f4bb", "spark": "\u26a1", "jiggle": "\U0001f3b6",
        "bloom": "\U0001f33a", "sprout": "\U0001f331", "retreat": "\U0001f422",
        "trail": "\U0001f40c", "soak": "\u2668\ufe0f", "munch": "\U0001f96c",
        "chill": "\U0001f60c", "stack": "\U0001f34a",
    }
    return mapping.get(emotion, "\U0001f600")


def save_local(image_bytes: bytes, buddy_name: str, emotion: str) -> Path:
    buddy_dir = OUTPUT_DIR / buddy_name.lower()
    buddy_dir.mkdir(parents=True, exist_ok=True)
    path = buddy_dir / f"{emotion}.png"
    path.write_bytes(image_bytes)
    print(f"Saved: {path}")
    return path


def main():
    parser = argparse.ArgumentParser(description="Generate buddy stickers from ~/.claude.json")
    parser.add_argument("emotion", nargs="?", default=None,
                        help="Preset emotion, custom prompt, or 'all'")
    parser.add_argument("--chat", default="@claris_voronka_bot", help="Telegram chat")
    parser.add_argument("--no-send", action="store_true", help="Only save locally")
    parser.add_argument("--all", action="store_true", help="Generate all presets")
    parser.add_argument("--info", action="store_true", help="Print buddy info and exit")
    parser.add_argument("--list", action="store_true", help="List available emotions for this buddy")
    parser.add_argument("--sticker-pack", action="store_true",
                        help="Create Telegram sticker pack from generated images (requires TELEGRAM_BOT_TOKEN)")
    args = parser.parse_args()

    companion = load_buddy()
    base_style, species = build_visual_prompt(companion)
    buddy_name = companion.get("name", "Buddy")
    presets = get_presets(species)

    if args.info:
        print(f"Name: {buddy_name}")
        print(f"Species: {species}")
        print(f"Rarity: {companion.get('rarity', 'unknown')}")
        print(f"Stats: {companion.get('stats', {})}")
        print(f"Personality: {companion.get('personality', 'N/A')}")
        print(f"Visual prompt: {base_style}")
        print(f"Emotions ({len(presets)}): {', '.join(presets.keys())}")
        return

    if args.list:
        print(f"🎨 {buddy_name} ({species}) — {len(presets)} emotions:")
        for k, v in presets.items():
            print(f"  {k:12s} — {v}")
        return

    if args.all:
        emotions = list(presets.keys())
    elif args.emotion:
        emotions = [args.emotion]
    else:
        print(f"Usage: buddy-generate.py <emotion>")
        print(f"Available for {buddy_name} ({species}): {', '.join(presets.keys())}")
        return

    generated = []  # collect (emotion, bytes) for sticker pack

    for emotion in emotions:
        prompt = presets.get(emotion, emotion)
        tag = emotion if emotion in presets else "custom"
        print(f"Generating {buddy_name} ({species}) — {emotion}...")

        image_bytes = generate_image(base_style, prompt)
        save_local(image_bytes, buddy_name, tag)
        generated.append((tag, image_bytes))

        if not args.no_send:
            caption = f"🎨 {buddy_name} — {emotion}"
            asyncio.run(send_to_telegram(image_bytes, caption, args.chat))

    # Create Telegram sticker pack if requested
    if args.sticker_pack and generated:
        create_sticker_pack(buddy_name, generated)


if __name__ == "__main__":
    main()
