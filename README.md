# Claude Buddy Stickers

> Turn your Claude Code buddy into a Telegram sticker pack. One command. Every species. Every emotion.

<p align="center">
  <img src="examples/zen.png" width="120" />
  <img src="examples/chaos.png" width="120" />
  <img src="examples/facepalm.png" width="120" />
  <img src="examples/sleep.png" width="120" />
  <img src="examples/itworks.png" width="120" />
  <img src="examples/hug.png" width="120" />
</p>

## What is this?

Claude Code has a **buddy** — a tiny ASCII pet in your terminal. It has a species, personality, stats, and rarity.

This tool reads your buddy from `~/.claude.json` and generates a **Telegram sticker pack** with 12 emotions unique to your buddy's species.

A Goose gets `honk`, `steal`, `chase`. A Cat gets `loaf`, `zoomies`, `knock`. A Chonk gets `zen`, `vibrate`, `meditate`. **18 species supported.**

---

## Install

### Option A: One-liner (recommended)

Run in your project directory:

```bash
curl -sL https://raw.githubusercontent.com/Voronik1801/claude-buddy-stickers/main/install.sh | bash
```

This copies the skill and scripts to `.claude/` and installs Python deps.

### Option B: Tell Claude Code

Just paste this into Claude Code:

> Install buddy stickers from https://github.com/Voronik1801/claude-buddy-stickers — clone the repo, copy SKILL.md to .claude/skills/sticker-pack/, copy scripts to .claude/scripts/, install httpx telethon Pillow

Claude will do everything automatically.

### Option C: Manual

```bash
git clone https://github.com/Voronik1801/claude-buddy-stickers.git
cd claude-buddy-stickers
pip install httpx telethon Pillow

mkdir -p .claude/skills/sticker-pack .claude/scripts
cp skills/sticker-pack/SKILL.md .claude/skills/sticker-pack/
cp scripts/buddy_generate.py .claude/scripts/
cp scripts/buddy_react.py .claude/scripts/
```

---

## Setup API Key (2 minutes)

1. Go to [openrouter.ai](https://openrouter.ai) — sign up, get **$5 free credit**
2. Copy your key from [openrouter.ai/keys](https://openrouter.ai/keys)
3. Add to `.claude/settings.local.json`:

```json
{
  "env": {
    "OPENROUTER_API_KEY": "sk-or-v1-your-key-here"
  }
}
```

---

## Generate Stickers

Tell Claude Code:

> **"generate stickers for my buddy"**

Or via CLI:

```bash
# Check your buddy
python3 .claude/scripts/buddy_generate.py --info

# Generate all 12 stickers
OPENROUTER_API_KEY="..." python3 .claude/scripts/buddy_generate.py --all --no-send
```

Stickers saved to `~/.claude/buddy-stickers/<buddy-name>/`.

---

## Create a Telegram Sticker Pack (optional)

Want a real Telegram sticker pack you can share?

### Step 1. Create a Telegram bot

1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Send `/newbot`, follow the prompts
3. Copy the bot token (looks like `123456789:ABCdef...`)
4. **Important:** Open your new bot and press `/start`

### Step 2. Set up Telegram MTProto (one-time)

The script needs your Telegram account to create sticker packs:

1. Go to [my.telegram.org](https://my.telegram.org) → API Development Tools
2. Get your `API_ID` and `API_HASH`
3. Create a session:

```bash
mkdir -p ~/.claude/scripts/telegram-mcp
cat > ~/.claude/scripts/telegram-mcp/.env << EOF
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
EOF

python3 -c "
from telethon import TelegramClient
client = TelegramClient(
    '~/.claude/scripts/telegram-mcp/session',
    your_api_id,
    'your_api_hash'
)
client.start()  # Enter phone number and code when prompted
client.disconnect()
"
```

### Step 3. Generate stickers + create pack

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key"
export TELEGRAM_BOT_TOKEN="123456789:ABCdef..."

python3 scripts/buddy_generate.py --all --sticker-pack
```

You'll get a link like `https://t.me/addstickers/your_buddy_by_your_bot` — share it with anyone!

---

## Use as Claude Code Skill

Copy to your project so you can just ask Claude "generate stickers for my buddy":

```bash
mkdir -p .claude/skills/sticker-pack .claude/scripts

cp skills/sticker-pack/SKILL.md .claude/skills/sticker-pack/
cp scripts/buddy_generate.py .claude/scripts/
cp scripts/buddy_react.py .claude/scripts/
```

Add API keys to `.claude/settings.local.json`:
```json
{
  "env": {
    "OPENROUTER_API_KEY": "sk-or-v1-your-key",
    "TELEGRAM_BOT_TOKEN": "123456789:ABCdef..."
  }
}
```

Then in Claude Code, just say: **"generate stickers for my buddy"** or **"make a sticker pack"**.

---

## Buddy Reactions (bonus)

Your buddy can react with stickers when things happen in your code:

| What happened | Buddy sends |
|---------------|------------|
| Tests passed | 👍 approve |
| Build failed | 🤦 facepalm |
| Error/exception | 🐛 bug |
| Deploy to prod | 🔥 chaos |
| Installing deps | ✨ meditate |
| Timeout | ⏰ deadline |

Add to your `.claude/settings.local.json` hooks:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 .claude/scripts/buddy_react.py",
        "timeout": 10
      }]
    }]
  }
}
```

---

## All 18 Species

<details>
<summary>Click to see species and their unique emotions</summary>

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

Stats > 70 add bonuses: Debugging (detective hat), Patience (zen lines), Chaos (glitch), Wisdom (halo), Snark (raised eyebrow). Shiny buddies get rainbow shimmer.

## How It Works

```
~/.claude.json           buddy_generate.py           Telegram
┌──────────┐     ┌─────────────────────┐     ┌──────────────┐
│ name     │     │ 1. Detect species   │     │ Sticker Pack │
│ personality ──>│ 2. Pick 12 emotions │────>│ 12 stickers  │
│ stats    │     │ 3. Generate via AI  │     │ + emojis     │
│ rarity   │     │ 4. Remove background│     │              │
└──────────┘     │ 5. Resize to 512px  │     │ t.me/add...  │
                 └─────────────────────┘     └──────────────┘
```

## License

MIT

---

*Your buddy is watching. It has opinions about your code. Now it can express them as stickers.*
