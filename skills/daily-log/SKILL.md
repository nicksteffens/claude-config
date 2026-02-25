---
name: daily-log
description: Reliable daily log management for development sessions. Use this skill when adding session entries to daily logs to ensure correct file paths and formatting.
---

# Daily Log Management

## File Path Convention

Daily logs are stored at: `~/.claude/daily-logs/YYYY/YYYY-MM.md`

Example: December 2025 logs are at `~/.claude/daily-logs/2025/2025-12.md`

## Adding Log Entries - Wizard Workflow

**ALWAYS use the AskUserQuestion wizard to gather session details** - it's much easier than manual entry.

### Step 1: Gather Session Details via Wizard

Use `AskUserQuestion` with these question sets:

**First Question Set (Basic Info):**
1. **Duration** - How long did we work together?
   - Options: "30-45 minutes", "1 hour", "1.5-2 hours", "2+ hours"
2. **Success Rating** - How would you rate today's session?
   - Options: "10/10 - Exceptional", "8-9/10 - Excellent", "6-7/10 - Good", "4-5/10 - Fair"
3. **Your Role** - What was your primary role?
   - Options: "Directing", "Collaborating", "Reviewing", "Learning"
4. **Most Valuable** - What was the most valuable aspect?
   - Customize options based on session context

**Second Question Set (Details):**
1. **Challenges** - What challenges did we encounter? (multiSelect: true)
   - Customize options based on session context
   - Always include "No significant challenges" option
2. **Key Insight** - What's the main learning/insight?
   - Customize options based on session context
3. **Follow-up Items** - Any tasks for future sessions? (multiSelect: true)
   - Customize options based on session context
   - Always include "None - complete for now" option

### Step 2: Create Log Entry

1. **Determine the file path:**
   ```bash
   YEAR=$(date +%Y)
   MONTH=$(date +%m)
   TODAY=$(date +%Y-%m-%d)
   LOG_FILE="$HOME/.claude/daily-logs/$YEAR/$YEAR-$MONTH.md"
   ```

2. **Check if date heading exists:**
   - Search for `## YYYY-MM-DD` in the file
   - If found, append new session under it (separated by `---`)
   - If not found, add the heading at the end of the file

3. **Use wizard responses to populate the session template**

4. **Multiple sessions same day:**
   - Separate with `---` horizontal rule
   - Each session gets its own "Session Overview" block

### Step 3: Commit the Log Entry

After writing the log entry, ALWAYS commit it to the ~/.claude git repo:

```bash
git -C ~/.claude checkout main
git -C ~/.claude add daily-logs/
git -C ~/.claude commit -m "docs: add daily log for YYYY-MM-DD"
```

IMPORTANT: `~/.claude` IS a git repo (nicksteffens/claude-config).
Use `git -C ~/.claude` to operate on it from any working directory.
Daily logs should ALWAYS be committed to the main branch.
After committing, ask the user if they'd like to push (`git -C ~/.claude push origin main`).

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

## Example Wizard Implementation

```javascript
// First question set - Basic info
AskUserQuestion({
  questions: [
    {
      question: "How long did we work together today?",
      header: "Duration",
      multiSelect: false,
      options: [
        {label: "30-45 minutes", description: "Quick focused session"},
        {label: "1 hour", description: "Standard session length"},
        {label: "1.5-2 hours", description: "Extended working session"},
        {label: "2+ hours", description: "Deep dive session"}
      ]
    },
    {
      question: "How would you rate today's session overall?",
      header: "Success",
      multiSelect: false,
      options: [
        {label: "10/10 - Exceptional", description: "Everything went perfectly, exceeded expectations"},
        {label: "8-9/10 - Excellent", description: "Highly productive, met all objectives"},
        {label: "6-7/10 - Good", description: "Accomplished goals with some minor issues"},
        {label: "4-5/10 - Fair", description: "Made progress but faced challenges"}
      ]
    },
    {
      question: "What was your primary role during this session?",
      header: "Your Role",
      multiSelect: false,
      options: [
        {label: "Directing", description: "Provided high-level guidance and decisions"},
        {label: "Collaborating", description: "Active pair programming and problem solving"},
        {label: "Reviewing", description: "Primarily reviewing and approving Claude's work"},
        {label: "Learning", description: "Observing and learning new techniques"}
      ]
    },
    {
      question: "What was the most valuable aspect of our collaboration?",
      header: "Value",
      multiSelect: false,
      options: [
        // Customize based on session context
        {label: "Option 1", description: "Description"},
        {label: "Option 2", description: "Description"}
      ]
    }
  ]
})

// Second question set - Details
AskUserQuestion({
  questions: [
    {
      question: "What challenges did we encounter during this session?",
      header: "Challenges",
      multiSelect: true,  // Allow multiple challenges
      options: [
        // Customize based on session context
        {label: "Challenge 1", description: "Description"},
        {label: "Challenge 2", description: "Description"},
        {label: "No significant challenges", description: "Session went smoothly overall"}
      ]
    },
    {
      question: "What's the key insight or learning from today?",
      header: "Insight",
      multiSelect: false,
      options: [
        // Customize based on session context
        {label: "Insight 1", description: "Description"},
        {label: "Insight 2", description: "Description"}
      ]
    },
    {
      question: "Any follow-up items for future sessions?",
      header: "Follow-up",
      multiSelect: true,  // Allow multiple follow-up items
      options: [
        // Customize based on session context
        {label: "Task 1", description: "Description"},
        {label: "Task 2", description: "Description"},
        {label: "None - complete for now", description: "No immediate follow-up needed"}
      ]
    }
  ]
})
```

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

## Important Notes

- **Always customize wizard options** based on session context for "Most Valuable" and "Challenges" questions
- **Use multiSelect: true** for challenges and follow-up items (can select multiple)
- **Use multiSelect: false** for duration, success rating, role, and key insight (single choice)
- **Provide clear descriptions** for each option to help user make informed choices
- **Include "None" options** where appropriate (no challenges, no follow-up items)
