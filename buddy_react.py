#!/usr/bin/env python3
"""Buddy React — send buddy stickers as reactions to Claude Code events.

Hook into PostToolUse to make your buddy react with stickers in Telegram.
Reads tool output from stdin (Claude Code hook format), picks an emotion,
sends the matching sticker from your buddy's sticker pack.

Usage in settings.json:
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
"""

import json
import os
import sys

try:
    import httpx
except ImportError:
    sys.exit(0)  # silently skip if not installed

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
BUDDY_STICKER_PACK = os.environ.get("BUDDY_STICKER_PACK", "")

# Keywords in tool output → emotion mapping
REACTIONS = {
    # Success
    "passed": "approve",
    "success": "approve",
    "✅": "approve",
    "done": "approve",
    "created": "itworks",
    "deployed": "itworks",

    # Failure
    "error": "facepalm",
    "failed": "facepalm",
    "❌": "facepalm",
    "traceback": "bug",
    "exception": "bug",

    # Chaos
    "force": "chaos",
    "production": "chaos",
    "deploy": "chaos",
    "rm -rf": "chaos",

    # Patience
    "installing": "meditate",
    "building": "meditate",
    "compiling": "meditate",
    "downloading": "meditate",

    # Time
    "timeout": "deadline",
    "slow": "deadline",

    # Rest
    "sleep": "sleep",
    "idle": "sleep",
}


def get_reaction(tool_output: str) -> str | None:
    """Determine which emotion to react with based on tool output."""
    lower = tool_output.lower()
    for keyword, emotion in REACTIONS.items():
        if keyword in lower:
            return emotion
    return None


def send_sticker(emotion: str):
    """Send a sticker from the buddy's pack."""
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, BUDDY_STICKER_PACK]):
        return

    # Get sticker set
    resp = httpx.get(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getStickerSet",
        params={"name": BUDDY_STICKER_PACK},
        timeout=10,
    ).json()

    if not resp.get("ok"):
        return

    # Find sticker by emoji mapping
    EMOJI_MAP = {
        "zen": "🧘", "bug": "🐛", "sarcasm": "😒", "chaos": "🔥",
        "approve": "👍", "vibrate": "📳", "meditate": "✨", "deadline": "⏰",
        "facepalm": "🤦", "sleep": "😴", "itworks": "🎉", "hug": "🤗",
    }

    target_emoji = EMOJI_MAP.get(emotion, "🧘")
    stickers = resp["result"]["stickers"]

    # Find matching sticker by emoji
    file_id = None
    for s in stickers:
        if target_emoji in s.get("emoji", ""):
            file_id = s["file_id"]
            break

    if not file_id and stickers:
        file_id = stickers[0]["file_id"]  # fallback to first

    if file_id:
        httpx.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendSticker",
            json={"chat_id": TELEGRAM_CHAT_ID, "sticker": file_id},
            timeout=10,
        )


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_output = data.get("tool_output", {}).get("content", "")
    if isinstance(tool_output, list):
        tool_output = " ".join(str(p) for p in tool_output)

    reaction = get_reaction(str(tool_output))
    if reaction:
        send_sticker(reaction)


if __name__ == "__main__":
    main()
