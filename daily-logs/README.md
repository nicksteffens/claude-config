# Daily Log

This directory contains our collaborative session logs, migrated from gist to provide better organization and version control.

## Structure

```
daily-logs/
├── README.md            # This file
├── template.md          # Template questions and format
└── 2025/
    ├── 2025-08.md      # August 2025 entries
    └── index.md        # 2025 overview
```

## Usage

### Adding New Entries
Use the `/daily-log` command or `daily-log-agent` at the end of each session:

#### Option 1: Command + Agent (Recommended)
```bash
/daily-log
```
- Executes safety checks (branch verification, duplicate detection)
- Hands off to `daily-log-agent` for autonomous workflow
- Agent extracts session context and handles file operations
- User provides only assessment and rating

#### Option 2: Direct Agent
```bash
ask daily-log-agent to log today's session
```
- Bypasses safety checks for direct autonomous logging
- Agent handles complete workflow autonomously
- User provides session assessment and rating

### Workflow Process
1. **Safety Checks**: Branch safety, duplicate session detection (command only)
2. **Context Extraction**: Agent analyzes conversation for objective, duration, accomplishments
3. **Content Generation**: Agent creates formatted log entry with session details
4. **User Assessment**: Agent asks for rating, challenges, insights, follow-up items
5. **File Operations**: Agent updates monthly file and commits changes

### Finding Sessions
- **Recent sessions**: Check current month file (e.g., `2025/2025-08.md`)
- **Specific date**: Navigate to the appropriate monthly file
- **Search across all logs**: Use `grep -r "search term" daily-logs/`

## Migration Notes

- **Original source**: [Daily Log Gist](https://gist.github.com/nicksteffens/5e2da7e26d47e0e734935cdcdbb1df73)
- **Migration date**: August 28, 2025
- **Total entries migrated**: 12 date sections across August 2025
- **Content preservation**: All original formatting and content maintained

## Archive Policy

- **Current month**: Active file for new entries
- **Previous months**: Archived, read-only for reference
- **Annual organization**: One directory per year (2025/, 2026/, etc.)

## Template Questions

See `template.md` for the standard questions asked at the end of each session. These ensure consistent, comprehensive logging of our collaborative work.