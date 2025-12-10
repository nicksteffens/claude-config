# MCP Servers Configuration Guide

This guide covers setting up and configuring MCP (Model Context Protocol) servers for Claude Code.

## Table of Contents
- [General Setup](#general-setup)
- [Shortcut MCP Server](#shortcut-mcp-server)
- [Notion MCP Server](#notion-mcp-server)
- [MUI MCP Server](#mui-mcp-server)
- [Movable UI MCP Server](#movable-ui-mcp-server)
- [Agent Tool Permissions](#agent-tool-permissions)
- [Troubleshooting](#troubleshooting)

---

## General Setup

MCP servers are configured in `~/.claude.json` under the `mcpServers` key. Each server has a unique name and configuration.

### Configuration Location
- **Global servers**: `~/.claude.json` → `mcpServers`
- **Project servers**: `~/.claude.json` → `projects[path].mcpServers`

### Server Types
- `stdio` - Local command-based servers
- `http` - HTTP-based remote servers

---

## Shortcut MCP Server

Integrates with Shortcut (formerly Clubhouse) for project management.

### Prerequisites
- Shortcut account with API access
- Shortcut API token

### Get Your Shortcut API Token
1. Log into your Shortcut account at https://app.shortcut.com
2. Click on your profile picture in the top right corner
3. Select "Settings" from the dropdown menu
4. In the left sidebar, click on "API Tokens"
5. Click "Generate Token" button
6. Give your token a descriptive name (e.g., "Claude Code MCP")
7. Copy the generated token immediately (you won't be able to see it again)

### Configuration

```json
{
  "mcpServers": {
    "shortcut": {
      "command": "npx",
      "args": ["-y", "@shortcut/mcp@latest"],
      "env": {
        "SHORTCUT_API_TOKEN": "YOUR_API_TOKEN_HERE"
      }
    }
  }
}
```

### Available Features
- Read and search Shortcut stories
- Create new stories
- Update existing stories
- Manage story workflows
- Access project and iteration information
- Link stories to PRs and branches

---

## Notion MCP Server

Integrates with Notion for workspace access via OAuth authentication.

### Prerequisites
- Notion account
- Browser access for OAuth flow

### Configuration

```json
{
  "mcpServers": {
    "notionMCP": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.notion.com/mcp"]
    }
  }
}
```

### Authentication
The Notion MCP uses OAuth for authentication:
1. On first connection, a browser window opens for Notion login
2. Authorize Claude Code to access your Notion workspace
3. Select which pages/databases to share with the integration
4. OAuth tokens are cached and refresh automatically

### Reconnecting
If the connection fails, use `/mcp` in Claude Code and select the option to reconnect. You may need to re-authenticate if your OAuth token has expired.

### Available Features
- Search pages and databases
- Read page content
- Create new pages
- Update existing pages
- Query databases
- Access workspace users and teams

---

## MUI MCP Server

Provides access to Material UI documentation.

### Configuration

```json
{
  "mcpServers": {
    "mui-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@mui/mcp@latest"],
      "env": {}
    }
  }
}
```

### Available Features
- Access MUI component documentation
- Fetch API references for components
- Query MUI design tokens and theming

---

## Movable UI MCP Server

Local MCP server for Movable Ink's UI component library.

### Prerequisites
- Local clone of the `movable-ink/ui` repository
- Built MCP server (`mcp-server/dist/index.js`)

### Configuration

```json
{
  "mcpServers": {
    "movable-ui": {
      "type": "stdio",
      "command": "node",
      "args": ["/Users/nsteffens/github/movable-ink/ui/mcp-server/dist/index.js"],
      "env": {}
    }
  }
}
```

### Available Features
- List available components
- Get component details and props
- Access design tokens
- View component examples from Storybook
- Search components by category
- Get ESLint rules

---

## Agent Tool Permissions

### Tool Specification in Agents

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
  - mcp__shortcut__stories-get-by-id
  - mcp__shortcut__stories-search
  - mcp__notionMCP__notion-search
  - mcp__notionMCP__notion-fetch
  - WebFetch
---
```

### PR Reviewer Agent Tool Requirements

The `pr-reviewer` agent requires:

**GitHub CLI Access (via Bash)**
- `gh pr view` - Extract PR metadata
- `gh pr diff` - Analyze code changes
- `gh pr review` - Submit reviews
- `gh pr checks` - Verify CI/CD status

**File Analysis Tools**
- `Read`, `Grep`, `Glob`, `LS`

**Shortcut Integration**
- `mcp__shortcut__stories-get-by-id`
- `mcp__shortcut__stories-search`
- `mcp__shortcut__stories-get-branch-name`

---

## Troubleshooting

### General Issues
- Run `/mcp` to see server status and reconnect options
- Check that npm/npx is available in your PATH
- Ensure internet connectivity for remote servers

### Shortcut Server
- Verify API token is valid and not expired
- Check token has necessary permissions
- Ensure no extra spaces in token value

### Notion Server
- Re-authenticate if OAuth token expired
- Verify pages are shared with the integration
- Check browser isn't blocking popup for OAuth flow

### Local Servers (Movable UI)
- Ensure the server is built (`npm run build` in mcp-server directory)
- Verify the path to `index.js` is correct
- Check Node.js version compatibility

### Security Notes
- Keep API tokens secure and never commit to version control
- Use environment variables for sensitive values when sharing configs
- Revoke tokens immediately if compromised
