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

## Development Rules

See `CLAUDE.md` for detailed development protocols including:
- Git workflow requirements
- Commit message conventions
- Branch naming strategies
- Pre-approved permissions