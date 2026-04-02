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

Claude Code has a companion system — a tiny ASCII pet called a **buddy** that lives in your terminal. This plugin reads your buddy's species, personality, rarity, and stats from `~/.claude.json`, then:

1. Generates **12 unique emotion stickers** tailored to your buddy's species
2. Removes backgrounds automatically (transparent PNG)
3. Creates a **Telegram sticker pack** you can use in any chat

**18 species supported**: Duck, Goose, Cat, Rabbit, Owl, Penguin, Turtle, Snail, Dragon, Octopus, Axolotl, Ghost, Robot, Blob, Cactus, Mushroom, Chonk, Capybara.

Each species has its own emotions. A Goose gets `honk`, `steal`, `chase`. A Cat gets `loaf`, `zoomies`, `knock`. A Chonk gets `zen`, `vibrate`, `meditate`.

## Install

### As Claude Code Plugin

```
claude plugin add github:Voronik1801/claude-buddy-stickers
```

On first enable, Claude Code will prompt you for:
- **OpenRouter API key** — for image generation ([openrouter.ai](https://openrouter.ai), free $5 credit on signup)
- **Telegram Bot token** — optional, for creating sticker packs (from [@BotFather](https://t.me/BotFather))
- **Telegram chat** — optional, where to send stickers

### Manual install

```bash
git clone https://github.com/Voronik1801/claude-buddy-stickers.git
pip install httpx telethon Pillow
```

## Usage

### Via Claude Code skill

```
/buddy-stickers:sticker-pack
```

Or just ask Claude: "generate stickers for my buddy"

### Via CLI

```bash
# See your buddy's species, stats, and available emotions
python3 scripts/buddy_generate.py --info

# List all emotions for your buddy's species
python3 scripts/buddy_generate.py --list

# Generate one sticker (saves to ~/.claude/buddy-stickers/<name>/)
OPENROUTER_API_KEY="..." python3 scripts/buddy_generate.py zen --no-send

# Generate all 12 emotions
OPENROUTER_API_KEY="..." python3 scripts/buddy_generate.py --all --no-send

# Generate all + create Telegram sticker pack
OPENROUTER_API_KEY="..." TELEGRAM_BOT_TOKEN="..." python3 scripts/buddy_generate.py --all --sticker-pack

# Custom pose (not a preset)
OPENROUTER_API_KEY="..." python3 scripts/buddy_generate.py "wearing a pirate hat on a treasure chest" --no-send
```

## Buddy Reactions

Your buddy can **react with stickers** in Telegram when things happen in your coding session. This is enabled automatically via the plugin's `hooks.json`:

| Event | Sticker |
|-------|---------|
| Tests passed | approve 👍 |
| Build failed | facepalm 🤦 |
| Error/exception | bug 🐛 |
| Deploy to prod | chaos 🔥 |
| Installing deps | meditate ✨ |
| Timeout | deadline ⏰ |

Requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in env.

## Prerequisites

| Requirement | What | How to get |
|------------|------|-----------|
| **OpenRouter API** | Image generation | [openrouter.ai](https://openrouter.ai) — free $5 signup credit |
| **Telegram Bot** | Sticker pack creation | [@BotFather](https://t.me/BotFather) — optional |
| **Telegram MTProto** | Sending stickers to chat | [my.telegram.org](https://my.telegram.org) + Telethon session — optional |
| **Python 3.10+** | Runtime | `python3 --version` |
| **httpx, telethon, Pillow** | Dependencies | `pip install httpx telethon Pillow` |

## Species & Emotions

<details>
<summary>All 18 species and their 12 unique emotions</summary>

| Species | Emotions |
|---------|----------|
| **Chonk** | zen, bug, sarcasm, chaos, approve, vibrate, meditate, deadline, facepalm, sleep, itworks, hug |
| **Duck** | quack, swim, debug, rage, bath, follow, rain, bread, nap, fly, approve, hug |
| **Goose** | honk, steal, chase, innocent, judge, chaos, peace, plan, victory, hiss, nap, hug |
| **Cat** | loaf, zoomies, knock, purr, judge, box, hunt, yawn, gift, ignore, belly, hug |
| **Rabbit** | binky, flop, thump, munch, zoom, nose, stand, dig, groom, hide, sleep, hug |
| **Owl** | wise, rotate, hoot, swoop, pellet, blink, read, sleep, ruffle, hunt, approve, hug |
| **Penguin** | slide, waddle, fish, huddle, dive, cold, tux, egg, dance, judge, sleep, hug |
| **Dragon** | flame, hoard, fly, roar, curl, egg, treasure, sneeze, grow, read, protect, hug |
| **Octopus** | multitask, ink, wave, hide, squeeze, smart, dance, tangle, garden, tool, sleep, hug |
| **Axolotl** | smile, regenerate, swim, curious, bubble, wave, blush, crown, eat, glow, sleep, hug |
| **Ghost** | boo, phase, float, spook, vanish, chain, read, haunt, glow, cold, sleep, hug |
| **Robot** | compute, spark, upgrade, beep, error, charge, scan, dance, rust, build, sleep, hug |
| **Blob** | jiggle, split, absorb, morph, bounce, puddle, grow, color, drip, mirror, sleep, hug |
| **Cactus** | bloom, poke, thirst, sun, hug, grow, tough, rain, pot, friend, sleep, dance |
| **Mushroom** | sprout, spore, glow, rain, grow, forest, fairy, bounce, cook, toxic, sleep, hug |
| **Turtle** | retreat, race, stack, sun, swim, carry, munch, old, hide, patient, sleep, hug |
| **Snail** | trail, shell, rain, slow, climb, garden, mail, bubble, leaf, friend, sleep, hug |
| **Capybara** | soak, friend, munch, chill, swim, stack, squad, rain, sun, bird, sleep, hug |

</details>

## Visual Modifiers

Sticker style adapts to your buddy's rarity and stats:

| Rarity | Visual |
|--------|--------|
| Common | Clean, no effects |
| Uncommon | Subtle sparkle aura |
| Rare | Glowing aura |
| Epic | Purple shimmer |
| Legendary | Golden celestial aura |

Stats above 70 add visual bonuses: Debugging (detective hat), Patience (zen lines), Chaos (glitch particles), Wisdom (halo), Snark (raised eyebrow).

Shiny buddies get rainbow shimmer. Hats are rendered on the character.

## How It Works

```
~/.claude.json           scripts/                    Telegram
┌──────────┐     ┌─────────────────────┐     ┌──────────────┐
│companion:│     │ 1. Detect species   │     │ Sticker Pack │
│  name    │────>│ 2. Pick 12 emotions │────>│ 12 stickers  │
│  personality   │ 3. Generate via AI  │     │ with emojis  │
│  stats   │     │ 4. Remove bg        │     │              │
│  rarity  │     │ 5. Resize to 512px  │     │ t.me/add...  │
└──────────┘     └─────────────────────┘     └──────────────┘
```

## Plugin Structure

```
claude-buddy-stickers/
├── .claude-plugin/
│   ├── plugin.json            # Plugin manifest with userConfig
│   └── marketplace.json       # Marketplace metadata
├── skills/
│   └── sticker-pack/
│       └── SKILL.md           # Skill: /buddy-stickers:sticker-pack
├── scripts/
│   ├── buddy_generate.py      # Image generation + sticker pack creation
│   └── buddy_react.py         # Sticker reactions on code events
├── hooks/
│   └── hooks.json             # PostToolUse hook for buddy reactions
├── examples/                  # Sample stickers (Chonk species)
├── LICENSE                    # MIT
└── README.md
```

## Made with

- [Claude Code](https://claude.ai/code) — AI coding assistant with companion system
- [OpenRouter](https://openrouter.ai) — unified API for AI models (Gemini image generation)
- [Telethon](https://github.com/LonamiWebs/Telethon) — Telegram MTProto client
- [Telegram Bot API](https://core.telegram.org/stickers) — sticker pack management

## License

MIT

---

*Your buddy is watching. It probably has opinions about your code. Now it can express them as stickers.*
