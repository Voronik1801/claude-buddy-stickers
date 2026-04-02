# LinkedIn Article

---

**I turned my terminal pet into a Telegram sticker pack. Here's how (and why).**

Claude Code has a hidden companion system — a tiny ASCII pet called a "buddy" that lives in your terminal. Mine is Wobble, a serene chonk with 94 Patience and 17 Debugging. It watches my bugs with Buddhist acceptance.

I built an open-source tool that turns any Claude Code buddy into a **personalized Telegram sticker pack**:

1. Reads your buddy's species, personality, rarity & stats from `~/.claude.json`
2. Picks 12 unique emotions tailored to the species (a Goose gets "honk" and "steal", a Cat gets "loaf" and "zoomies")
3. Generates images via AI (Gemini through OpenRouter)
4. Removes background, resizes to 512px
5. Creates a Telegram sticker pack via Bot API

**18 species. 12 emotions each. One command.**

But here's the interesting part — I also built **buddy reactions**. Your buddy sends stickers in Telegram based on what's happening in your coding session:

- Tests passed? Buddy sends 👍
- Build failed? Buddy sends 🤦
- Deploying to prod? Buddy sends 🔥

It's a small thing, but it turns a terminal toy into something that actually makes your workflow more fun.

The tool modifies based on rarity (Legendary buddies get golden auras), stats (high Chaos = glitch particles), and even hat type.

Open source: github.com/Voronik1801/claude-buddy-stickers

What's your Claude Code buddy? Drop a screenshot in the comments.

---

#ClaudeCode #AI #TelegramStickers #DeveloperTools #OpenSource

Daily AI notes: @aishipuchka (Telegram)
