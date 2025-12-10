---
name: shortcut-teams
description: Static reference for Shortcut team UUIDs and mention names. Use this when creating or assigning Shortcut stories instead of querying the API for team lists.
---

# Shortcut Teams Reference

Use these UUIDs when creating or assigning Shortcut stories. **Do not query the API for team lists** - use this reference directly.

## How to Populate This File

Run this command to get your teams, then copy the relevant data here:

```bash
# Using the Shortcut MCP tool
mcp__shortcut__teams-list
```

Or use the Shortcut API directly:

```bash
curl -s -H "Shortcut-Token: $SHORTCUT_API_TOKEN" \
  "https://api.app.shortcut.com/api/v3/teams" | jq '.[] | {name, id, mention_name}'
```

## Commonly Used Teams

| Team Name | UUID | Mention Name |
|-----------|------|--------------|
| Example Team | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` | `@example-team` |
| Another Team | `yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy` | `@another-team` |

## All Active Teams

<!-- Add your full team list here -->

| Team Name | UUID | Mention Name |
|-----------|------|--------------|
| ... | `...` | `@...` |

## Your User Information

- **Name:** Your Name
- **Mention:** `@your-mention-name`
- **UUID:** `your-user-uuid`
- **Team Memberships:** List your teams here
