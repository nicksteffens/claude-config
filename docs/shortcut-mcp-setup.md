# Setting Up Shortcut MCP Server for Claude Code

## Prerequisites
- Claude Code installed and running
- Shortcut account with API access
- Shortcut API token

## Setup Steps

### 1. Get Your Shortcut API Token
1. Log into your Shortcut account at https://app.shortcut.com
2. Click on your profile picture in the top right corner
3. Select "Settings" from the dropdown menu
4. In the left sidebar, click on "API Tokens"
5. Click "Generate Token" button
6. Give your token a descriptive name (e.g., "Claude Code MCP")
7. Copy the generated token immediately (you won't be able to see it again)

### 2. Configure Claude Code

Open your `~/.claude.json` configuration file and add the following MCP server configuration:

```json
{
  "mcpServers": {
    "shortcut": {
      "command": "npx",
      "args": [
        "-y",
        "@shortcut/mcp@latest"
      ],
      "env": {
        "SHORTCUT_API_TOKEN": "YOUR_ACTUAL_API_TOKEN_HERE"
      }
    }
  },
  // ... rest of your existing configuration
}
```

**Important:** Replace `YOUR_ACTUAL_API_TOKEN_HERE` with your actual Shortcut API token from step 1.

### 3. Restart Claude Code
After adding the configuration, restart Claude Code for the changes to take effect.

### 4. Verify Setup
Once restarted, you can verify the setup by running:
- `/mcp` - to see available MCP servers
- The Shortcut server should appear in the list

## Available Features
With the Shortcut MCP server, Claude Code can:
- Read and search Shortcut stories
- Create new stories
- Update existing stories
- Manage story workflows
- Access project information

## Troubleshooting
- If the server doesn't start, check that your API token is valid
- Ensure you have internet connectivity for npx to download the latest version
- Check Claude Code logs for any error messages
- Make sure you copied the full API token without any extra spaces

## Security Notes
- Keep your API token secure and never commit it to version control
- Consider using environment variables for the token if sharing configurations
- The token has access to your Shortcut data, so treat it like a password
- If you suspect your token is compromised, revoke it immediately in Shortcut settings