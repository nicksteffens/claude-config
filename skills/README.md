# Claude Code Skills

This directory contains custom [Claude Code Skills](https://code.claude.com/docs/en/skills) - modular capabilities that Claude automatically loads when relevant.

## What Are Skills?

Skills are model-invoked (Claude decides when to use them based on context) vs slash commands which are user-invoked. Each skill is a folder containing a `SKILL.md` file with YAML frontmatter.

## Available Skills

| Skill | Description |
|-------|-------------|
| `shortcut-teams` | Static reference for Shortcut team UUIDs - prevents repeated API calls |
| `daily-log` | Reliable daily log management with correct file paths and templates |

## Creating Your Own Skills

1. Create a folder: `~/.claude/skills/your-skill-name/`
2. Add a `SKILL.md` file with required frontmatter
3. Claude will auto-discover and use it when relevant

### Required Structure

```markdown
---
name: your-skill-name
description: Brief description of when Claude should use this skill.
---

# Your Skill Title

Content and instructions here...
```

## Why Skills Are Gitignored

Skills in this directory often contain org-specific data (team IDs, user IDs, internal URLs) that shouldn't be committed to version control. Each user should create their own skills with their org's data.

See `examples/` for templates you can copy and customize.
