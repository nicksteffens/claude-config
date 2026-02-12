---
name: shortcut-designer-iteration
description: Get Designer Team's current iteration and assign stories to it
user_invocable: true
---

# Shortcut Designer Iteration

Get the Designer Team's current/active iteration and assign stories to it. Iterations are pre-created and follow a 2-week sprint schedule.

## When to Use

- Get the current active iteration for the Designer Team
- Assign stories to the Designer Team's current iteration
- Bulk assign multiple stories to the active iteration

## Instructions

1. **Get Active Iteration**
   - Use `mcp__shortcut__iterations-get-active` with Designer Team filter
   - Team ID: `696925b3-5d50-4a5c-8856-78a67f65fe4c`
   - Parse response to get iteration ID, name, and date range
   - **IMPORTANT**: Iterations are pre-created - never create new ones

2. **Parse Story IDs (if provided)**
   - Accept story IDs as arguments: space-separated, comma-separated, or with "sc-" prefix
   - Strip "sc-" prefix if present
   - Examples: `165234`, `sc-165234`, `165234,165235`, `165234 165235`

3. **Assign Stories to Iteration**
   - Use `mcp__shortcut__stories-update` for each story
   - Set `iteration` field to the active iteration ID
   - Handle errors gracefully (invalid story ID, permission issues)

4. **Display Results**
   - Show iteration details: name, dates, ID, status
   - If stories were assigned, confirm each one
   - Show any errors for failed assignments

## Important Guidelines

- **Never Create Iterations**: They're pre-planned and already exist
- **Team Filtering**: Always filter by Designer Team ID
- **Workspace**: CoherentPath only (use `mcp__shortcut__*` tools)
- **Error Handling**:
  - No active iteration → tell user to check Shortcut (should always exist)
  - Invalid story IDs → report which ones failed
  - Already assigned → confirm before overwriting

## Tool Usage

- **MCP Shortcut Tools**:
  - `mcp__shortcut__iterations-get-active` - Get active iteration for Designer Team
  - `mcp__shortcut__stories-update` - Assign stories to iteration
  - `mcp__shortcut__stories-get-by-id` - Optional: verify story before assignment

## Examples

<example description="Get current iteration only">
User: "/shortcut-designer-iteration"

Steps:
1. Call `mcp__shortcut__iterations-get-active` with teamId: "696925b3-5d50-4a5c-8856-78a67f65fe4c"
2. Display:
   ```
   Current Designer Team Iteration:
   Name: Designer 26.3 - Q1 R1 (Feb 2–Feb 15) Sp 3
   ID: 185482
   Dates: Feb 2, 2026 → Feb 17, 2026
   Status: started
   ```
</example>

<example description="Assign stories to current iteration">
User: "/shortcut-designer-iteration 165234 165235 165236"

Steps:
1. Get active iteration (ID: 185482)
2. Parse story IDs: [165234, 165235, 165236]
3. Update each story with iteration: 185482
4. Display:
   ```
   Current Iteration: Designer 26.3 - Q1 R1 (Feb 2–Feb 15) Sp 3

   Assigned to iteration 185482:
   ✓ Story 165234
   ✓ Story 165235
   ✓ Story 165236

   All 3 stories assigned successfully.
   ```
</example>

<example description="Assign with sc- prefix and commas">
User: "/shortcut-designer-iteration sc-165234,sc-165235"

Steps:
1. Parse story IDs, strip "sc-" prefix: [165234, 165235]
2. Get active iteration
3. Assign stories
4. Display confirmation
</example>

<example description="Handle errors">
User: "/shortcut-designer-iteration 165234 999999 165235"

Steps:
1. Get active iteration
2. Try to assign each story
3. Display:
   ```
   Current Iteration: Designer 26.3 - Q1 R1 (Feb 2–Feb 15) Sp 3

   Results:
   ✓ Story 165234 - assigned
   ✗ Story 999999 - not found
   ✓ Story 165235 - assigned

   2 of 3 stories assigned successfully.
   ```
</example>

## Usage Patterns

### Show current iteration
```bash
/shortcut-designer-iteration
```

### Assign single story
```bash
/shortcut-designer-iteration 165234
/shortcut-designer-iteration sc-165234
```

### Assign multiple stories (space-separated)
```bash
/shortcut-designer-iteration 165234 165235 165236
```

### Assign multiple stories (comma-separated)
```bash
/shortcut-designer-iteration 165234,165235,165236
/shortcut-designer-iteration sc-165234,sc-165235,sc-165236
```

## Iteration Naming Pattern

Designer Team iterations follow this pattern:
- **Format**: `Designer YY.N - Quarter Release (Date Range) Sp N`
- **Example**: `Designer 26.3 - Q1 R1 (Feb 2–Feb 15) Sp 3`
- **Older Format**: `[Designer Team] YY.N | Quarter Release | Date Range | Sprint N`
- **Schedule**: 2-week sprints, pre-created in advance

## Notes

- **Team UUID**: `696925b3-5d50-4a5c-8856-78a67f65fe4c` (Designer Team)
- **Workspace**: CoherentPath (not Movable Ink legacy workspace)
- **Pre-planned**: Iterations are created in advance - never create new ones
- **Active Iteration**: Determined by status ("started") and current date within range
- **Future Enhancement**: Support other teams by accepting team name argument
- **Future Enhancement**: Assign to specific iteration by name/ID (not just active)
