# Claude Buddy Stickers

> Turn your Claude Code buddy into a Telegram sticker pack. Every species. Every emotion. Automatically.

<p align="center">
  <img src="examples/zen.png" width="120" />
  <img src="examples/chaos.png" width="120" />
  <img src="examples/facepalm.png" width="120" />
  <img src="examples/sleep.png" width="120" />
  <img src="examples/itworks.png" width="120" />
  <img src="examples/hug.png" width="120" />
</p>

## What is this?

Claude Code has a companion system — a tiny ASCII pet called a **buddy** that lives in your terminal. This skill reads your buddy's species, personality, rarity, and stats from `~/.claude.json`, then:

1. Generates **12 unique emotion stickers** tailored to your buddy's species
2. Removes backgrounds automatically
3. Creates a **Telegram sticker pack** you can use in any chat

**18 species supported**: Duck, Goose, Cat, Rabbit, Owl, Penguin, Turtle, Snail, Dragon, Octopus, Axolotl, Ghost, Robot, Blob, Cactus, Mushroom, Chonk, Capybara.

Each species has its own emotions. A Goose gets `honk`, `steal`, `chase`. A Cat gets `loaf`, `zoomies`, `knock`. A Chonk gets `zen`, `vibrate`, `meditate`.

## Quick Start

### 1. Install as Claude Code Plugin

```bash
# One command — installs the plugin with skill, scripts, and hooks
/plugin add Voronik1801/claude-buddy-stickers
```

Or install from marketplace:
```bash
/plugin marketplace add Voronik1801/claude-buddy-stickers
```

On first enable, Claude Code will prompt you for:
- **OpenRouter API key** — for image generation ([openrouter.ai](https://openrouter.ai), free $5 credit)
- **Telegram Bot token** — for creating sticker packs (optional, from [@BotFather](https://t.me/BotFather))
- **Telegram chat** — where to send stickers (optional)

### 2. Generate your sticker pack

Just say:
```
/buddy stickers
```

Or use the script directly:
```bash
# See your buddy
python3 buddy_generate.py --info

# Generate all emotions
OPENROUTER_API_KEY="..." python3 buddy_generate.py --all --no-send

# Create Telegram sticker pack
OPENROUTER_API_KEY="..." TELEGRAM_BOT_TOKEN="..." python3 buddy_generate.py --all --sticker-pack
```

## Buddy Reactions in Telegram

Want your buddy to **react with stickers** when you work with Claude Code via Telegram? The skill can modify your other skills to send buddy stickers as reactions:

- Task completed? Buddy sends `approve` sticker
- Build failed? Buddy sends `facepalm` sticker
- Deploying to prod? Buddy sends `chaos` sticker
- Long session? Buddy sends `coffee` sticker

To enable, add to your Claude Code hooks in `settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "python3 .claude/scripts/buddy_react.py",
          "timeout": 10
        }]
      }
    ]
  }
}
```

The `buddy_react.py` script analyzes tool output and sends the appropriate buddy sticker to your Telegram chat.

## Prerequisites

| Requirement | What | How to get |
|------------|------|-----------|
| **OpenRouter API** | Image generation | [openrouter.ai](https://openrouter.ai) — free $5 signup credit |
| **Telegram Bot** | Sticker pack creation | [@BotFather](https://t.me/BotFather) |
| **Telegram MTProto** | Sending stickers to chat | [my.telegram.org](https://my.telegram.org) + Telethon session |
| **Python 3.10+** | Runtime | `python3 --version` |
| **httpx, telethon, Pillow** | Dependencies | `pip install httpx telethon Pillow` |

## Species & Emotions

<details>
<summary>Click to see all 18 species and their emotions</summary>

| Species | Emotions |
|---------|----------|
| Chonk | zen, bug, sarcasm, chaos, approve, vibrate, meditate, deadline, facepalm, sleep, itworks, hug |
| Duck | quack, swim, debug, rage, bath, follow, rain, bread, nap, fly, approve, hug |
| Goose | honk, steal, chase, innocent, judge, chaos, peace, plan, victory, hiss, nap, hug |
| Cat | loaf, zoomies, knock, purr, judge, box, hunt, yawn, gift, ignore, belly, hug |
| Rabbit | binky, flop, thump, munch, zoom, nose, stand, dig, groom, hide, sleep, hug |
| Owl | wise, rotate, hoot, swoop, pellet, blink, read, sleep, ruffle, hunt, approve, hug |
| Penguin | slide, waddle, fish, huddle, dive, cold, tux, egg, dance, judge, sleep, hug |
| Dragon | flame, hoard, fly, roar, curl, egg, treasure, sneeze, grow, read, protect, hug |
| Octopus | multitask, ink, wave, hide, squeeze, smart, dance, tangle, garden, tool, sleep, hug |
| Axolotl | smile, regenerate, swim, curious, bubble, wave, blush, crown, eat, glow, sleep, hug |
| Ghost | boo, phase, float, spook, vanish, chain, read, haunt, glow, cold, sleep, hug |
| Robot | compute, spark, upgrade, beep, error, charge, scan, dance, rust, build, sleep, hug |
| Blob | jiggle, split, absorb, morph, bounce, puddle, grow, color, drip, mirror, sleep, hug |
| Cactus | bloom, poke, thirst, sun, hug, grow, tough, rain, pot, friend, sleep, dance |
| Mushroom | sprout, spore, glow, rain, grow, forest, fairy, bounce, cook, toxic, sleep, hug |
| Turtle | retreat, race, stack, sun, swim, carry, munch, old, hide, patient, sleep, hug |
| Snail | trail, shell, rain, slow, climb, garden, mail, bubble, leaf, friend, sleep, hug |
| Capybara | soak, friend, munch, chill, swim, stack, squad, rain, sun, bird, sleep, hug |

</details>

## How It Works

```
~/.claude.json          buddy_generate.py           Telegram
┌──────────┐     ┌─────────────────────┐     ┌──────────────┐
│companion:│     │ 1. Detect species   │     │ Sticker Pack │
│  name    │────>│ 2. Pick emotions    │────>│ 12 stickers  │
│  personality   │ 3. Generate via AI  │     │ with emojis  │
│          │     │ 4. Remove bg        │     │              │
└──────────┘     │ 5. Resize to 512px  │     │ t.me/add...  │
                 └─────────────────────┘     └──────────────┘
```

## Made with

- [Claude Code](https://claude.ai/code) — AI coding assistant with companion system
- [OpenRouter](https://openrouter.ai) — unified API for AI models (Gemini image generation)
- [Telethon](https://github.com/LonamiWebs/Telethon) — Telegram MTProto client
- [Telegram Bot API](https://core.telegram.org/stickers) — sticker pack management

## Author

**Voronik1801** — [GitHub](https://github.com/Voronik1801)

---

*Your buddy is watching. It probably has opinions about your code. Now it can express them as stickers.*
