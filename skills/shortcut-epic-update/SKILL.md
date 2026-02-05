---
name: shortcut-epic-update
description: Update Shortcut epics using the API directly (since MCP doesn't support epic updates). Handles linking to objectives, changing state, updating owners, etc.
user_invocable: false
---

# Shortcut Epic Update

Updates Shortcut epics via the Shortcut API when the MCP server doesn't provide update functionality.

## When to Use

- Linking epics to objectives (`objective_ids`)
- Changing epic state or workflow state
- Updating epic name or description
- Changing epic owner
- Any other epic field updates not supported by MCP

## API Tokens

**CRITICAL**: Tokens are stored in `~/.claude/skills/shortcut-tokens.json`

File format (see `shortcut-tokens.sample.json` for template):
```json
{
  "coherentpath": "your_coherentpath_token",
  "movableink": "your_movableink_token"
}
```

Use the correct token key for the workspace:
- **CoherentPath** → `coherentpath`
- **Movable Ink** → `movableink`

## Instructions

1. **Determine the workspace** from context or ask the user
   - CoherentPath (CP) = default/primary
   - Movable Ink (MI) = legacy

2. **Read the API token** from the config file:
   ```bash
   TOKEN=$(jq -r '.coherentpath' ~/.claude/skills/shortcut-tokens.json)
   # or
   TOKEN=$(jq -r '.movableink' ~/.claude/skills/shortcut-tokens.json)
   ```

3. **Get the epic ID** to update

4. **Build the update payload** with only the fields to change:
   ```json
   {
     "objective_ids": [186645],
     "name": "New epic name",
     "description": "Updated description",
     "state": "in progress",
     "owner_ids": ["uuid-here"]
   }
   ```

5. **Execute the curl command**:
   ```bash
   curl -X PUT "https://api.app.shortcut.com/api/v3/epics/{epic_id}" \
     -H "Content-Type: application/json" \
     -H "Shortcut-Token: $TOKEN" \
     -d '{json_payload}'
   ```

6. **Verify the update** by checking the response JSON

## Common Update Operations

### Link to Objective
```json
{
  "objective_ids": [186645]
}
```

### Change State
```json
{
  "state": "in progress"
}
```

### Update Owner
```json
{
  "owner_ids": ["69696143-c308-4c11-a058-ee700eb89122"]
}
```

### Update Name and Description
```json
{
  "name": "New Epic Name",
  "description": "Updated description text"
}
```

## Important Guidelines

- **Only include fields you want to change** - omitted fields remain unchanged
- **Use proper JSON formatting** in the curl `-d` parameter
- **Validate epic ID** exists before updating
- **Check the response** for errors (4xx/5xx status codes)
- **Never expose API tokens** in output - they're embedded in curl commands

## Tool Usage

- **Bash**: Execute curl commands to call Shortcut API
- **Read**: Optional - read shortcut-workspaces skill for reference

## Examples

<example>
User: "Link epic 186646 to objective 186645 in CoherentPath"

Steps:
1. Workspace: CoherentPath → read coherentpath token
2. Read token: `TOKEN=$(jq -r '.coherentpath' ~/.claude/skills/shortcut-tokens.json)`
3. Epic ID: 186646
4. Payload: `{"objective_ids": [186645]}`
5. Execute curl:
   ```bash
   curl -X PUT "https://api.app.shortcut.com/api/v3/epics/186646" \
     -H "Content-Type: application/json" \
     -H "Shortcut-Token: $TOKEN" \
     -d '{"objective_ids": [186645]}'
   ```
6. Verify response contains `"objective_ids": [186645]`
</example>

## Notes

- **API tokens** stored in `~/.claude/skills/shortcut-tokens.json` (gitignored)
- **Sample format** in `shortcut-tokens.sample.json` (committed for reference)
- This skill and tokens file are excluded from git via `.gitignore`
- Future: Submit PR to useshortcut/mcp-server-shortcut to add epic update support
- Shortcut API docs: https://developer.shortcut.com/api/rest/v3#Update-Epic
