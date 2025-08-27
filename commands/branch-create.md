# Branch Creation Slash Command

Create a new feature branch following the established naming convention.

## Branch Naming Convention
- **Format**: `nicksteffens+claude/{sc-number || issues/number}/short-description`
- **For Shortcut stories**: `sc-{number}` (e.g. `nicksteffens+claude/sc-165234/fix-user-invitations`)
- **For GitHub issues**: `issues/{number}` (e.g. `nicksteffens+claude/issues/369/remove-empty-state-margins`)

## Process
1. **Ask user for ticket/issue reference** (Shortcut story number or GitHub issue number)
2. **Ask for brief description** for the branch name
3. **Create branch**: `git checkout -b nicksteffens+claude/{reference}/{description}`
4. **Confirm branch creation** and show current branch

## Example Interaction
- "What Shortcut story or GitHub issue are you working on?"
- "What's a brief description for this work?"
- "Creating branch: `nicksteffens+claude/sc-165234/fix-user-invitations`"

**Always ensure you're on the correct base branch (usually main) before creating the feature branch.**