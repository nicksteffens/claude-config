# Claude Configuration Repository

This repository contains Claude Code configuration files and development rules for Movable Ink projects.

## Files

- **`CLAUDE.md`** - Development rules and protocols for Claude Code sessions
- **`settings.example.json`** - Example settings file with auth tokens and permissions
- **`.gitignore`** - Excludes sensitive files like actual settings.json with real tokens

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

## Development Rules

See `CLAUDE.md` for detailed development protocols including:
- Git workflow requirements
- Commit message conventions
- Branch naming strategies
- Pre-approved permissions