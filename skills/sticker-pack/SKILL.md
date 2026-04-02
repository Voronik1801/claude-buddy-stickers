---
description: Generate personalized Telegram sticker packs for your Claude Code buddy. Reads companion from ~/.claude.json, picks species-specific emotions (18 species x 12 emotions), generates images via AI, removes background, creates a Telegram sticker pack. Trigger — "generate stickers", "sticker pack", "buddy stickers".
allowed-tools: Bash, Read, Write
tags: [creative, telegram, companion, stickers, fun]
---

# Buddy Sticker Pack Generator

Generate a **personalized Telegram sticker pack** for your Claude Code buddy/companion. Each of the 18 species gets 12 unique emotions that match their vibe.

`$ARGUMENTS` — emotion (preset), custom description, `all`, `info`, or `list`.

---

## Algorithm

### 1. Check buddy info

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/buddy_generate.py --info
```

### 2. Show available emotions for this buddy's species

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/buddy_generate.py --list
```

### 3. Determine what to generate from `$ARGUMENTS`

- **Preset** (`zen`, `chaos`, `sleep`...) — use that emotion
- **Custom text** ("wearing a pirate hat") — pass as custom prompt
- **`all`** — generate all 12 presets for this species
- **`info`** — show buddy profile
- **`list`** — show available emotions
- **Empty** — ask user which emotion they want, show the list

### 4. Generate

Single emotion:
```bash
OPENROUTER_API_KEY="${user_config.openrouter_api_key}" python3 ${CLAUDE_PLUGIN_ROOT}/scripts/buddy_generate.py <emotion> --no-send
```

All emotions:
```bash
OPENROUTER_API_KEY="${user_config.openrouter_api_key}" python3 ${CLAUDE_PLUGIN_ROOT}/scripts/buddy_generate.py --all --no-send
```

All emotions + create Telegram sticker pack:
```bash
OPENROUTER_API_KEY="${user_config.openrouter_api_key}" TELEGRAM_BOT_TOKEN="${user_config.telegram_bot_token}" python3 ${CLAUDE_PLUGIN_ROOT}/scripts/buddy_generate.py --all --sticker-pack
```

Send to Telegram chat:
```bash
OPENROUTER_API_KEY="${user_config.openrouter_api_key}" python3 ${CLAUDE_PLUGIN_ROOT}/scripts/buddy_generate.py <emotion> --chat "${user_config.telegram_chat}"
```

Custom pose:
```bash
OPENROUTER_API_KEY="${user_config.openrouter_api_key}" python3 ${CLAUDE_PLUGIN_ROOT}/scripts/buddy_generate.py "wearing tiny captain hat on a yacht"
```

### 5. Show result

Read the generated PNG via Read tool — files are saved to `${CLAUDE_PLUGIN_DATA}/stickers/<buddy_name>/` or `~/.claude/buddy-stickers/<buddy_name>/`.

---

## 18 Species x 12 Unique Emotions

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

## Prerequisites

Plugin `userConfig` will prompt for credentials on first enable. Alternatively set env vars:

- `OPENROUTER_API_KEY` — **required** for image generation ([openrouter.ai](https://openrouter.ai), free $5 credit)
- `TELEGRAM_BOT_TOKEN` — optional, for creating sticker packs ([@BotFather](https://t.me/BotFather))
- Telegram MTProto session at `~/.claude/scripts/telegram-mcp/` — optional, for sending stickers to chats
- Python: `pip install httpx telethon Pillow`
