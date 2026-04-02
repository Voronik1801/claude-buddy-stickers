---
description: Generate personalized Telegram sticker packs for your Claude Code buddy. Reads your companion from ~/.claude.json, picks species-specific emotions (18 species x 12 emotions), generates images via AI, removes background, creates a Telegram sticker pack automatically. Trigger — "/buddy stickers", "generate buddy stickers", "sticker pack for my buddy".
allowed-tools: Bash, Read, Write
tags: [creative, telegram, companion, stickers, fun]
---

# Buddy Sticker Generator

Generate a **personalized Telegram sticker pack** for your Claude Code buddy/companion. Each of the 18 species gets 12 unique emotions that match their vibe.

`$ARGUMENTS` — emotion (preset), custom description, `all`, `info`, or `list`.

---

## Prerequisites

Before using this skill, you need:

### 1. OpenRouter API Key (image generation)

Sign up at [openrouter.ai](https://openrouter.ai) (free $5 credit on signup).

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

Or add to your Claude Code project settings:
```json
{ "env": { "OPENROUTER_API_KEY": "sk-or-v1-..." } }
```

### 2. Telegram MTProto Session (for sending stickers)

The script uses [Telethon](https://github.com/LonamiWebs/Telethon) to send images to Telegram. You need:

1. Get API credentials at [my.telegram.org](https://my.telegram.org)
2. Create `.env` file at `~/.claude/scripts/telegram-mcp/.env`:
   ```
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   ```
3. Run auth once:
   ```python
   from telethon import TelegramClient
   client = TelegramClient('~/.claude/scripts/telegram-mcp/session', API_ID, API_HASH)
   client.start()  # will ask for phone + code
   ```

### 3. Telegram Bot Token (for creating sticker packs)

Create a bot via [@BotFather](https://t.me/BotFather), get the token:

```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-your-token"
```

**Important:** You must `/start` your bot before it can create sticker packs for you.

### 4. Python Dependencies

```bash
pip install httpx telethon Pillow
```

---

## 18 Species x Unique Emotions

| Species | Category | Example Emotions |
|---------|----------|-----------------|
| **Chonk** | Meme | zen, bug, sarcasm, chaos, vibrate, meditate |
| **Duck** | Classic | quack, swim, debug, bath, bread, fly |
| **Goose** | Classic | honk, steal, chase, innocent, judge, plan |
| **Cat** | Classic | loaf, zoomies, knock, purr, judge, box |
| **Rabbit** | Classic | binky, flop, thump, munch, zoom, nose |
| **Owl** | Wise | wise, rotate, hoot, read, blink, ruffle |
| **Penguin** | Cool | slide, waddle, fish, tux, dance, egg |
| **Dragon** | Mythical | flame, hoard, roar, sneeze, egg, treasure |
| **Octopus** | Aquatic | multitask, ink, wave, squeeze, tangle, tool |
| **Axolotl** | Exotic | smile, regenerate, swim, glow, crown, blush |
| **Ghost** | Spooky | boo, phase, vanish, haunt, glow, cold |
| **Robot** | Tech | compute, spark, upgrade, error, charge, scan |
| **Blob** | Abstract | jiggle, split, absorb, morph, bounce, puddle |
| **Cactus** | Plant | bloom, poke, thirst, sun, tough, rain |
| **Mushroom** | Fungi | sprout, spore, glow, fairy, toxic, bounce |
| **Turtle** | Chill | retreat, race, stack, sun, carry, patient |
| **Snail** | Chill | trail, shell, rain, slow, mail, leaf |
| **Capybara** | Special | soak, friend, munch, chill, stack, rain |

---

## Usage

### See your buddy info
```bash
python3 buddy_generate.py --info
```

### List available emotions for your buddy
```bash
python3 buddy_generate.py --list
```

### Generate one sticker
```bash
OPENROUTER_API_KEY="..." python3 buddy_generate.py zen --no-send
```

### Generate all 12 + send to Telegram
```bash
OPENROUTER_API_KEY="..." python3 buddy_generate.py --all --chat @your_bot
```

### Generate all + create Telegram sticker pack
```bash
OPENROUTER_API_KEY="..." TELEGRAM_BOT_TOKEN="..." python3 buddy_generate.py --all --sticker-pack
```

### Custom pose
```bash
OPENROUTER_API_KEY="..." python3 buddy_generate.py "wearing a tiny pirate hat, standing on treasure chest"
```

---

## How It Works

1. Reads `~/.claude.json` -> `companion` (name, personality)
2. Detects species from personality text (chonk, duck, goose, cat...)
3. Picks 12 unique emotions for that species
4. Applies visual modifiers based on rarity, stats >70, hat, shiny status
5. Generates PNG via OpenRouter (Gemini image model) or Gemini direct
6. Removes white background automatically (transparent PNG)
7. Resizes to 512px for Telegram
8. Creates sticker pack via Telegram Bot API

---

## Visual Modifiers

### By Rarity
- **Common** — no effects
- **Uncommon** — subtle sparkle aura
- **Rare** — glowing aura
- **Epic** — purple shimmer
- **Legendary** — golden celestial aura

### By Stats (>70)
- **Debugging** — detective hat / magnifying glass
- **Patience** — extra zen lines, serene energy
- **Chaos** — glitch particles
- **Wisdom** — halo / book nearby
- **Snark** — raised eyebrow, smug expression

### Bonuses
- **Hat** — rendered on character (crown, wizard, beanie, tiny duck...)
- **Shiny** — rainbow shimmer + sparkle particles
