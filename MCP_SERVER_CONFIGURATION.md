# MCP Server Configuration Documentation

**Last Updated:** 2026-02-17
**Purpose:** Backup of MCP server configurations for Claude Code

## Overview

This document contains the complete MCP server configuration for restoring settings if they get deleted. All MCP servers are configured in Claude Code's settings.

## Active MCP Servers

### 1. Shortcut (Main Workspace)
**Server ID:** `shortcut`
**Type:** Project Management - Coherent Path workspace
**Features:**
- Story management (create, update, search, get by ID)
- Iteration management (active, upcoming, create)
- Epic and objective management
- Workflow and team information
- Labels, comments, and relationships
- Branch name generation
- External links management

**Authentication:**
- Uses Shortcut API token
- Token should be configured in Claude Code MCP settings

**Key Tools:**
- `stories-get-by-id`
- `stories-search`
- `stories-create`
- `stories-update`
- `iterations-get-active`
- `epics-search`
- `teams-list`
- `workflows-get-default`

---

### 2. Shortcut MI (Movable Ink Workspace)
**Server ID:** `shortcut-mi`
**Type:** Project Management - Movable Ink workspace
**Features:** Same as main Shortcut workspace but for MI-specific projects

**Authentication:**
- Separate Shortcut API token for MI workspace
- Token configured in Claude Code MCP settings

**Note:** This is a duplicate of the Shortcut server but pointing to a different workspace

---

### 3. MUI MCP
**Server ID:** `mui-mcp`
**Type:** Documentation - Material-UI Component Library
**Repository:** https://github.com/michaellatman/mcp-mui

**Features:**
- Access to MUI documentation across multiple versions
- Component API references
- Implementation examples

**Supported Packages:**
- @mui/material (v5.17.1, v6.4.12, v7.2.0)
- @mui/x-charts (v7.29.1, v8.8.0)
- @mui/x-common-concepts (v7.29.7, v8.8.0)
- @mui/x-data-grid (v7.29.7, v8.8.0)
- @mui/x-date-pickers (v7.29.4, v8.8.0)
- @mui/x-tree-view (v7.29.1, v8.8.0)

**Key Tools:**
- `useMuiDocs` - Fetch documentation from llms.txt files
- `fetchDocs` - Retrieve specific documentation pages

**Documentation Sources:**
- All hosted at `llms.mui.com`

---

### 4. Figma Dev Mode MCP Server
**Server ID:** `figma-dev-mode-mcp-server`
**Type:** Design Integration
**Repository:** https://github.com/figma/figma-mcp-server

**Features:**
- Generate UI code from Figma designs
- Extract design tokens and variables
- Screenshot generation
- Code Connect mapping (link Figma components to code)
- FigJam support

**Key Tools:**
- `get_design_context` - Generate code from Figma nodes
- `get_variable_defs` - Extract design variables
- `get_screenshot` - Generate component screenshots
- `get_code_connect_map` - View Figma→Code mappings
- `add_code_connect_map` - Create new mappings
- `get_code_connect_suggestions` - AI-suggested mappings
- `get_metadata` - Get node structure in XML
- `get_figjam` - Extract from FigJam boards

**Authentication:**
- Requires Figma desktop app to be running
- Communicates via local server (likely localhost:9000 or similar)

**Node ID Format:**
- Standard: `123:456` or `123-456`
- From URL: Extract from `?node-id=1-2` → `1:2`

---

### 5. IDE (VS Code Integration)
**Server ID:** `ide`
**Type:** Development Environment Integration

**Features:**
- Language server diagnostics
- Jupyter notebook code execution

**Key Tools:**
- `getDiagnostics` - Get language diagnostics from VS Code
- `executeCode` - Execute Python code in Jupyter kernel

**Requirements:**
- VS Code must be running
- For Jupyter: notebook file must be open

---

### 6. Notion MCP
**Server ID:** `notionMCP`
**Type:** Knowledge Base Integration
**Repository:** https://github.com/notionhq/notion-mcp-server

**Features:**
- Search across Notion workspace and connected sources (Slack, Google Drive, GitHub, Jira, etc.)
- Page and database management
- Comments and discussions
- Data source queries (SQL-like)
- Meeting notes integration
- Team and user management

**Key Tools:**

**Search & Retrieval:**
- `notion-search` - Semantic search with filters
- `notion-fetch` - Get page/database by URL or ID
- `notion-get-comments` - Retrieve discussions

**Content Management:**
- `notion-create-pages` - Create new pages
- `notion-update-page` - Update existing pages
- `notion-move-pages` - Move pages to new parent
- `notion-duplicate-page` - Duplicate pages

**Database Operations:**
- `notion-create-database` - Create new databases
- `notion-update-data-source` - Update database schema
- `notion-query-data-sources` - SQL queries on databases
- `notion-query-meeting-notes` - Query meeting notes

**Comments:**
- `notion-create-comment` - Add comments to pages
- `notion-get-comments` - Retrieve page discussions

**Organization:**
- `notion-get-teams` - List teamspaces
- `notion-get-users` - List workspace users

**Authentication:**
- Notion API token required
- Configure in Claude Code MCP settings

**Enhanced Markdown Format:**
- Notion uses custom Markdown syntax
- Full spec available via: `notion://docs/enhanced-markdown-spec`

---

## CLI Setup Commands (Global/User-Scoped)

To add all MCP servers globally (user-scoped, available across all projects), run these commands:

```bash
# Shortcut - Coherent Path workspace
claude mcp add shortcut --scope user -e SHORTCUT_API_TOKEN="<your-coherent-path-token>" -- npx -y @shortcut/mcp@latest

# Shortcut - Movable Ink workspace
claude mcp add shortcut-mi --scope user -e SHORTCUT_API_TOKEN="<your-movable-ink-token>" -- npx -y @shortcut/mcp@latest

# Notion
claude mcp add notion --scope user --transport http https://mcp.notion.com/mcp

# MUI
claude mcp add mui-mcp --scope user -- npx -y @mui/mcp@latest

# Movable UI
claude mcp add movable-ui --scope user -- npx -y @movable/ui-mcp
```

**Note:** Get your Shortcut API tokens from:
- Coherent Path: Shortcut Settings → API Tokens
- Movable Ink: Shortcut Settings → API Tokens (MI workspace)

## Configuration Location

All MCP servers are configured in Claude Code settings, typically at:
- **User-scoped:** `~/.claude.json` → `mcpServers` (line 386+)
- **Project-scoped:** `~/.claude.json` → `projects[projectPath]` → `mcpServers`
- **Settings UI:** Claude Code → Settings → MCP Servers

## Restoring Configuration

If MCP settings are deleted:

1. Open Claude Code settings
2. Navigate to MCP Servers section
3. Add each server using the information above
4. Configure authentication tokens:
   - **Shortcut:** Get API token from Shortcut Settings → API Tokens
   - **Notion:** Get integration token from Notion Settings → Integrations
   - **Figma:** Ensure Figma desktop app is running
   - **MUI:** No auth required (public docs)
   - **IDE:** No auth required (local VS Code)

## Environment Variables / Secrets

Store API tokens securely:
- Do not commit tokens to git repositories
- Use environment variables or secure credential storage
- Rotate tokens periodically

## Testing MCP Servers

After configuration, test each server:
```
# Shortcut
- Try searching for a story
- Fetch a known story by ID

# Notion
- Search for a page
- Fetch a known page

# MUI
- Query documentation for a component

# Figma
- Ensure Figma desktop app is running
- Try fetching design context for a node

# IDE
- Check if VS Code is detected
- Test getDiagnostics if applicable
```

## Troubleshooting

**Common Issues:**

1. **"Server not found" errors:**
   - Check server name matches exactly
   - Restart Claude Code

2. **Authentication failures:**
   - Verify API tokens are valid
   - Check token permissions/scopes

3. **Figma not working:**
   - Ensure Figma desktop app is running
   - Check local server is accessible

4. **Notion queries failing:**
   - Verify integration has access to pages/databases
   - Check Notion API token permissions

## Additional Notes

- MCP servers can be added/removed without restarting Claude Code
- Some servers may require specific versions or dependencies
- Keep this documentation updated when adding new servers
- Back up MCP configuration regularly

---

**Backup Created:** 2026-02-17
**Location:** `/Users/nsteffens/.claude/MCP_SERVER_CONFIGURATION.md`
