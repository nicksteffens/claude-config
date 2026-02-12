---
name: shortcut-workspaces
description: Static reference for Shortcut team UUIDs, mention names, and workflow IDs across both workspaces. Use this when creating or assigning Shortcut stories instead of querying the API for team lists.
user_invocable: true
---

# Shortcut Workspaces Reference

**Do not query the API for team lists** - use this reference directly.

## Data Source

Workspace data is loaded from `~/.claude/skills/shortcut-workspaces-data.json`

**Setup Instructions:**
1. Copy `shortcut-workspaces-data.sample.json` to `shortcut-workspaces-data.json`
2. Fill in your organization's team UUIDs, mention names, and workflow IDs
3. The actual data file is gitignored for security

## Usage

When you need team information:

1. **Read the data file**:
   ```bash
   DATA=$(cat ~/.claude/skills/shortcut-workspaces-data.json)
   ```

2. **Parse with jq** to get specific teams:
   ```bash
   # Get CoherentPath teams
   jq '.coherentpath.teams' ~/.claude/skills/shortcut-workspaces-data.json

   # Get specific team by name
   jq '.coherentpath.teams[] | select(.name == "Design System & Front End Guild Team")' \
     ~/.claude/skills/shortcut-workspaces-data.json

   # Get team UUID by mention name
   jq -r '.coherentpath.teams[] | select(.mention == "design-system-team") | .uuid' \
     ~/.claude/skills/shortcut-workspaces-data.json
   ```

3. **Get user information**:
   ```bash
   # Your user UUID for CoherentPath
   jq -r '.coherentpath.user.uuid' ~/.claude/skills/shortcut-workspaces-data.json

   # Your team memberships
   jq -r '.coherentpath.user.team_memberships[]' ~/.claude/skills/shortcut-workspaces-data.json
   ```

## MCP Tool Prefixes

Data file includes MCP tool prefixes for each workspace:
- **CoherentPath (Primary)**: Check `.coherentpath.mcp_prefix` → `mcp__shortcut__*`
- **Movable Ink (Legacy)**: Check `.movableink.mcp_prefix` → `mcp__shortcut-mi__*`

## Data Structure

The JSON file has this structure:
```json
{
  "coherentpath": {
    "workspace_name": "CoherentPath",
    "mcp_prefix": "mcp__shortcut__",
    "user": {
      "name": "...",
      "mention": "...",
      "uuid": "...",
      "team_memberships": [...]
    },
    "teams": [
      {
        "name": "Team Name",
        "uuid": "team-uuid",
        "mention": "team-mention",
        "workflow_id": 500000000
      }
    ]
  },
  "movableink": { ... }
}
```

## Common Operations

### Get Team UUID for Story Creation
```bash
TEAM_UUID=$(jq -r '.coherentpath.teams[] | select(.mention == "design-system-team") | .uuid' \
  ~/.claude/skills/shortcut-workspaces-data.json)
```

### Get Default Workflow for Team
```bash
WORKFLOW_ID=$(jq -r '.coherentpath.teams[] | select(.mention == "design-system-team") | .workflow_id' \
  ~/.claude/skills/shortcut-workspaces-data.json)
```

### Get Your User UUID
```bash
MY_UUID=$(jq -r '.coherentpath.user.uuid' ~/.claude/skills/shortcut-workspaces-data.json)
```

### Get All Teams as Table (for reference)
```bash
jq -r '.coherentpath.teams[] | "\(.name) | \(.uuid) | @\(.mention) | \(.workflow_id)"' \
  ~/.claude/skills/shortcut-workspaces-data.json
```

## Notes

- **Data file location**: `~/.claude/skills/shortcut-workspaces-data.json` (gitignored)
- **Sample file**: `shortcut-workspaces-data.sample.json` (tracked for reference)
- **Security**: Never commit the actual data file - it contains org-specific UUIDs
- **Updates**: When teams change, update the JSON file directly
