---
name: daily-log
description: Reliable daily log management for development sessions. Use this skill when adding session entries to daily logs to ensure correct file paths and formatting.
---

# Daily Log Management

## File Path Convention

Daily logs are stored at: `~/.claude/daily-logs/YYYY/YYYY-MM.md`

Example: December 2025 logs are at `~/.claude/daily-logs/2025/2025-12.md`

## Adding Log Entries - Step by Step

1. **Determine the file path:**
   ```
   ~/.claude/daily-logs/YYYY/YYYY-MM.md
   ```
   Use current year and month (e.g., `2025/2025-12.md`)

2. **Check if date heading exists:**
   - Search for `## YYYY-MM-DD` in the file
   - If found, append new session under it (separated by `---`)
   - If not found, add the heading at the end of the file

3. **Use the session template below**

4. **Multiple sessions same day:**
   - Separate with `---` horizontal rule
   - Each session gets its own "Session Overview" block

## Session Template

```markdown
## YYYY-MM-DD

### Session Overview
**Duration:** [time]
**Main Objective:** [objective]
**Success Rating:** [X]/10

### What We Accomplished
- [bullet points]

### Challenges Encountered
- [bullet points or "None"]

### Most Valuable Collaboration
[description]

### Key Insight
[main learning]

### Follow-Up Items
- [ ] [action items]

### Role Distribution
**Human:** [role]
**Claude:** [role]

### Success Factors
[what made it successful, if rating 6+]

---
```

## Questions to Ask User

1. What was the main objective for today's session?
2. How long did we work together today?
3. What was your role/involvement? (directing, collaborating, reviewing)
4. What specific challenges did we encounter?
5. What was the most valuable part of our collaboration?
6. Any lessons learned or insights to document?
7. Any follow-up items for future sessions?
8. How would you rate overall success? (1-10)

## Bash Script for File Management

```bash
#!/bin/bash
YEAR=$(date +%Y)
MONTH=$(date +%m)
TODAY=$(date +%Y-%m-%d)
LOG_DIR="$HOME/.claude/daily-logs/$YEAR"
LOG_FILE="$LOG_DIR/$YEAR-$MONTH.md"

mkdir -p "$LOG_DIR"

if [ ! -f "$LOG_FILE" ]; then
  MONTH_NAME=$(date +%B)
  echo "# Daily Logs - $MONTH_NAME $YEAR" > "$LOG_FILE"
  echo "" >> "$LOG_FILE"
fi

echo "Log file: $LOG_FILE"
echo "Today's date heading: ## $TODAY"
```
