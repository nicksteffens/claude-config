# GitHub Workflow Slash Command

Optimized GitHub operations using CLI-first approach, MCP as fallback.

## Tool Preference Hierarchy
1. **PRIMARY: GitHub CLI (`gh`)** - Fast, direct, well-established
2. **FALLBACK: GitHub MCP** - When CLI doesn't support the operation
3. **LAST RESORT: WebFetch** - Only when both above fail

## Common GitHub Operations

### Issue Management
```bash
# View issue details
gh issue view <number>

# List issues
gh issue list --assignee @me
gh issue list --state open --label bug

# Create issue
gh issue create --title "Title" --body "Description"

# Comment on issue
gh issue comment <number> --body "Comment text"
```

### Pull Request Operations
```bash
# Create PR
gh pr create --title "Title" --body "Description"

# View PR details
gh pr view <number>

# List PRs
gh pr list --author @me
gh pr list --state open

# Review PR
gh pr review <number> --approve
gh pr review <number> --request-changes --body "Comments"

# Merge PR - SAFETY CHECK REQUIRED
gh pr merge <number> --squash
```

### Repository Information
```bash
# View repo details
gh repo view

# Clone repo
gh repo clone owner/repo

# Fork repo
gh repo fork owner/repo
```

## CRITICAL SAFETY RULES

### PR Merge Safety Check
**NEVER merge a PR that you and I didn't author without explicit permission**
1. **Check PR author**: `gh pr view <number> --json author`
2. **If author is NOT you (nicksteffens) or Claude**: **STOP** and ask for permission
3. **Only merge PRs we created together** unless explicitly told otherwise
4. **Always confirm merge action** before executing

### Workflow Integration
1. **Always use `gh issue view <number>`** instead of web scraping
2. **Create PRs with `gh pr create`** using repository templates
3. **Link issues automatically** with "Fixes #123" in PR body
4. **Use `gh` for all GitHub operations** before considering alternatives
5. **Safety check all destructive operations** (merge, close, delete)

## MCP Fallback Scenarios
- Complex API operations not supported by CLI
- Bulk operations requiring programmatic access
- When CLI authentication fails

**Default approach**: Try `gh` command first, explain what you're doing, then proceed with safety checks.
