#!/bin/bash
# Claude Buddy Stickers — one-line installer
# Usage: curl -sL https://raw.githubusercontent.com/Voronik1801/claude-buddy-stickers/main/install.sh | bash

set -e

echo "🎨 Installing Claude Buddy Stickers..."

# Clone to temp
TMPDIR=$(mktemp -d)
git clone --depth 1 https://github.com/Voronik1801/claude-buddy-stickers.git "$TMPDIR/buddy-stickers" 2>/dev/null

# Copy skill + scripts to current project
mkdir -p .claude/skills/sticker-pack .claude/scripts
cp "$TMPDIR/buddy-stickers/skills/sticker-pack/SKILL.md" .claude/skills/sticker-pack/
cp "$TMPDIR/buddy-stickers/scripts/buddy_generate.py" .claude/scripts/
cp "$TMPDIR/buddy-stickers/scripts/buddy_react.py" .claude/scripts/

# Install Python deps
pip install httpx telethon Pillow -q 2>/dev/null || pip3 install httpx telethon Pillow -q 2>/dev/null

# Cleanup
rm -rf "$TMPDIR"

echo ""
echo "✅ Installed!"
echo ""
echo "📁 Files:"
echo "   .claude/skills/sticker-pack/SKILL.md"
echo "   .claude/scripts/buddy_generate.py"
echo "   .claude/scripts/buddy_react.py"
echo ""
echo "🔑 Next: add OPENROUTER_API_KEY to .claude/settings.local.json"
echo "   Get free key at https://openrouter.ai"
echo ""
echo "🚀 Then tell Claude: \"generate stickers for my buddy\""
