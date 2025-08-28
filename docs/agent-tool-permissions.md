# Agent Tool Permissions

## Overview

This document clarifies tool permissions and access patterns for Claude agents in this configuration.

## Default Agent Permissions

By default, agents described with "(Tools: *)" in the Task function should have access to all available tools. However, explicit tool specifications in agent frontmatter provide clarity and can override defaults.

## PR Reviewer Agent Tool Requirements

The `pr-reviewer` agent requires specific tools to execute autonomous PR reviews:

### GitHub CLI Access (via Bash)
- `gh pr view` - Extract PR metadata, author, files, and status
- `gh pr diff` - Analyze code changes and diffs
- `gh pr review` - Submit reviews with approval/changes/comments  
- `gh pr checks` - Verify CI/CD status
- `gh api` - Direct GitHub API access for advanced operations

**Important**: All GitHub CLI commands (`gh pr *`, `gh api *`) must be executed via the Bash tool, not direct MCP calls.

### File Analysis Tools
- `Read` - Read specific files for code analysis
- `Grep` - Search for patterns in code changes
- `Glob` - Find files matching patterns
- `LS` - List directory contents

### Shortcut Integration
- `mcp__shortcut__get-story` - Get story details for acceptance criteria
- `mcp__shortcut__search-stories` - Find related stories
- `mcp__shortcut__get-story-branch-name` - Generate proper branch names

### External Resources
- `WebFetch` - Access external documentation during review process

## Tool Specification Format

Tools can be specified in agent YAML frontmatter:

```yaml
---
name: agent-name
description: Agent description...
tools: 
  - Bash
  - Read
  - Grep
  - Glob
  - LS
  - mcp__shortcut__get-story
  - mcp__shortcut__search-stories
  - mcp__shortcut__get-story-branch-name
  - WebFetch
---
```

## Troubleshooting Tool Permissions

If an agent fails due to tool permission issues:

1. Check agent YAML frontmatter for explicit tool specifications
2. Verify that required tools are listed in the tools array
3. Ensure GitHub CLI commands are accessible via Bash tool
4. Test MCP tool availability for Shortcut integration

## Best Practices

- Always specify critical tools explicitly in agent definitions
- Document tool requirements in agent descriptions
- Test agent functionality with minimal required tool set
- Use Bash for GitHub CLI operations rather than direct MCP calls