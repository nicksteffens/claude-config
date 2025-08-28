# Claude Configuration Repository

This repository contains Claude Code configuration files and development rules for Movable Ink projects.

## Files

- **`CLAUDE.md`** - Development rules and protocols for Claude Code sessions
- **`settings.example.json`** - Example settings file with auth tokens and permissions
- **`.gitignore`** - Excludes sensitive files like actual settings.json with real tokens
- **`commands/`** - Slash command files for common workflows
- **`agents/`** - Specialized agent configurations

## Setup

```bash
# Copy example settings to create your settings file
cp settings.example.json settings.json
```

Then edit `settings.json` and replace placeholders with your actual values:
- `ANTHROPIC_AUTH_TOKEN`: Your Claude API token
- `ANTHROPIC_BASE_URL`: Your proxy URL (if using one)
- `additionalDirectories`: Paths to your project directories

## Security

The actual `settings.json` file is excluded from git to prevent token exposure. Only commit the example file.

## Commands

Slash commands are invoked by typing `/command-name` in Claude Code. Available commands:

- **`/repo-assess`** - Repository assessment and safety checks (run first in any new repo)
- **`/branch-create`** - Create feature branch with proper naming conventions
- **`/daily-log`** - Update session log with accomplishments and insights
- **`/commit-conventional`** - Guide for conventional commit formatting
- **`/github-workflow`** - GitHub CLI-first operations with safety checks
- **`/pr-review`** - Pull request review workflows
- **`/add-reviewers`** - Add reviewers to pull requests

## Agents

Specialized agents for complex tasks:

- **`frontend-architecture-lead (pfe)`** - Expert guidance on frontend architecture, infrastructure, and technical decisions

### Using Agents
```
ask pfe how should I structure this new component?
ask pfe what's the best way to handle this API integration?
```

## Daily Log

Our collaborative sessions are systematically documented to track progress, insights, and lessons learned. Each session includes objectives, accomplishments, challenges, and follow-up items with performance ratings.

**Key Features:**
- Organized by year and month for easy navigation
- Standardized template questions ensure comprehensive coverage
- Version controlled for historical tracking and analysis
- Migrated from gist to repository structure (August 2025)

**Usage:** Run `/daily-log` at the end of each session to update the current month's log file.

See [daily-logs/README.md](daily-logs/README.md) for complete documentation and usage instructions.

## Documentation

Additional setup guides and documentation:

- **[Shortcut MCP Setup](docs/shortcut-mcp-setup.md)** - Configure Shortcut integration for story management and workflow automation

## Development Rules

See `CLAUDE.md` for detailed development protocols including:
- Git workflow requirements
- Commit message conventions
- Branch naming strategies
- Pre-approved permissions