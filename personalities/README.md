# Droid Personalities

Swappable Star Wars droid personalities for Claude Code. Changes tone, statusline, and spinner verbs.

## Usage

```
/personality
```

Pick a droid. Tone and statusline update immediately. Spinner verbs take effect next session.

## What Gets Changed

| Component | File | Effect |
|---|---|---|
| Tone & voice | `~/.claude/CLAUDE.md` | `## Tone & Personality` section replaced |
| Status bar | `~/.claude/statusline-command.sh` | Tag, quips, and mood thresholds rewritten |
| Spinner verbs | `~/.claude/settings.json` | `spinnerVerbs` key updated |

## Available Droids

| Droid | Tag | Vibe |
|---|---|---|
| **Chopper (C1-10P)** | `C1-10P` | Grumpy beeps, reluctant compliance, blames you for everything |
| **K-2SO** | `K-2SO` | Deadpan probability calculations, blunt assessments, dry wit |
| **HK-47** | `HK-47` | "Statement:", menacingly polite, calls you meatbag |
| **B1 Battle Droid** | `B1-0X` | "Roger roger", nervous, easily confused, surprisingly helpful |

## Adding a New Personality

Create a `.md` file in this directory:

```markdown
---
name: Droid Name
tag: SHORT-TAG
description: One-line personality summary
---

## Tone
- Personality bullet points (these go into CLAUDE.md)

## Spinner Verbs
- PresentTenseVerb1
- PresentTenseVerb2

## Quips
### angry
- "Quip shown when context > 80%"

### grumpy
- "Quip shown when context 50-80%"

### annoyed
- "Quip shown when context 20-50%"

### fresh
- "Quip shown when context < 20%"
```

### Rules

- **tag**: Short identifier for the statusline bracket `[TAG]`
- **Spinner verbs**: Present tense, capitalized — replaces the default "Cogitating", "Churning", etc.
- **Quips**: Use `${CONTEXT}` to interpolate context percentage. 4 per mood. Rotates every 15 seconds.
- **Tone bullets**: 5-7 lines. Always include "Still technically excellent" and "Don't overdo it" variants.

## Testing the Statusline

```bash
echo '{"model":{"display_name":"Claude Opus 4.6"},"context_window":{"used_percentage":15},"workspace":{"current_dir":"/Users/you/project"}}' | bash ~/.claude/statusline-command.sh
```

Output format: `[TAG] Model Name | directory | quip`
