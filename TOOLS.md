# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## 🔧 API Keys & Services

### Search Engines (Priority Order)

1. **Tavily** (Primary) - AI-optimized search
   - API Key: `~/.openclaw/.env` (TAVILY_API_KEY)
   - Use for: Tech news, research, general queries
   - Command: `node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "query"`

2. **Brave Search** (Fallback) - Requires BRAVE_API_KEY
   - Status: Not configured

### Notes
- Tavily is the default search engine for all web queries
- For tech/news queries, always prefer Tavily
