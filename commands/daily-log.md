# Daily Log Update Slash Command

Update the daily log in the repository at the end of each session.

## Usage
```
/daily-log
```

Executes safety checks then hands off to the daily-log-agent for autonomous workflow execution. The agent handles content generation while you provide session assessment and rating.

## Repository Structure
Daily logs are now organized in the repository under `daily-logs/` directory:
- **Template**: `daily-logs/template.md` - Contains template questions and format
- **Monthly files**: `daily-logs/YYYY/YYYY-MM.md` - One file per month
- **Current month**: Automatically determined based on today's date

## Process

### Directory Setup (Always First)
```bash
# Ensure we're working in the ~/.claude directory
claude_dir="$HOME/.claude"
if [[ ! -d "$claude_dir" ]]; then
  echo "❌ ~/.claude directory not found"
  echo "Please ensure the claude-config repository is cloned to ~/.claude"
  exit 1
fi

# Change to ~/.claude directory for all operations
cd "$claude_dir" || {
  echo "❌ Failed to change to ~/.claude directory"
  exit 1
}
echo "📁 Working in ~/.claude directory"
```

### Branch Safety Check
```bash
# Check if we're on main/master branch
current_branch=$(git branch --show-current)
if [[ "$current_branch" != "main" && "$current_branch" != "master" ]]; then
  echo "❌ Daily log updates must be made on main/master branch"
  echo "Current branch: $current_branch"
  echo ""
  read -p "Should I switch to main branch? (y/n): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    git checkout main
    current_branch="main"
  else
    echo "Exiting daily-log. Run on main/master branch when ready."
    exit 1
  fi
fi

# Ensure branch is up-to-date
echo "🔄 Checking if $current_branch is up-to-date..."
git fetch origin
if ! git diff --quiet HEAD origin/$current_branch; then
  echo "❌ Branch $current_branch is behind origin"
  echo ""
  read -p "Should I pull latest changes? (y/n): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    git pull origin $current_branch
  else
    echo "Exiting daily-log. Pull latest changes when ready."
    exit 1
  fi
fi
echo "✅ Branch $current_branch is up-to-date"
```

### Duplicate Session Check
```bash
# Check if we've already logged this specific task/objective
today=$(date +%Y-%m-%d)
current_year=$(date +%Y)
current_month=$(date +%Y-%m)
daily_log_file="daily-logs/$current_year/$current_month.md"

if [[ -f "$daily_log_file" ]] && grep -q "## $today" "$daily_log_file"; then
  echo "📋 Checking for duplicate sessions..."
  
  # Extract recent session objectives from today's entries
  recent_objectives=$(awk "/## $today/,/^## [0-9]/ { if (/\*\*Main Objective:\*\*/) print }" "$daily_log_file" | sed 's/.*Main Objective:\*\* //' | head -3)
  
  if [[ -n "$recent_objectives" ]]; then
    echo "Recent session objectives for today:"
    echo "$recent_objectives" | nl
    echo ""
    read -p "Are you logging a new/different task than above? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      echo "Skipping daily-log to prevent duplicate session entry."
      exit 0
    fi
    echo "✅ Proceeding with new session entry"
  fi
fi
```

### Agent Handoff
```bash
# After safety checks pass, hand off to daily-log-agent
echo "🤖 Daily log agent will handle workflow"
exit 0  # Signal for daily-log-agent to take over
```

1. **Determine current month file**: Based on today's date (e.g., `daily-logs/2025/2025-08.md`)

2. **Ask the template questions** from `daily-logs/template.md`:
   - What was the main objective for today's session?
   - How long did we work together today?
   - What was your role/involvement in the work? (directing, collaborating, reviewing, etc.)
   - What specific challenge(s) did we encounter that were most significant?
   - What was the most valuable part of our collaboration today?
   - Any specific lessons learned or insights you'd like documented?
   - Are there any follow-up items or things to remember for future sessions?
   - How would you rate the overall success of today's session? (1-10 scale)

3. **Check if today's date section exists** (## YYYY-MM-DD format)
   - If monthly file doesn't exist: create new monthly file with header
   - If date section exists: append new session entry under that date
   - If date section doesn't exist: create new date section and add entry

4. **Format the session entry** using template from `daily-logs/template.md`:
   - Session Overview (duration, objective, success rating)
   - What We Accomplished ✅
   - Challenges Encountered 🔧 
   - Most Valuable Collaboration
   - Key Insight
   - Follow-Up Items 📝
   - Role Distribution
   - Success Factors (if rating 6+)

5. **Update the monthly file** with the new entry in chronological order

6. **Git workflow** (if in a git repository):
   - Add the updated monthly file to git
   - Commit with conventional commit format
   - Push changes (if on a feature branch)

## Monthly File Format
```markdown
# Daily Log - [Month Year]

## YYYY-MM-DD

### Session Overview
**Duration:** [duration]  
**Main Objective:** [objective]  
**Success Rating:** [rating]/10  

[... rest of entry following template format ...]
```

## Legacy Gist Information
- **Original Gist ID**: `5e2da7e26d47e0e734935cdcdbb1df73` (migrated to repository)
- **Migration completed**: August 28, 2025

## Example Usage
Run this at the end of each Claude Code session to maintain comprehensive session logs in version control.
