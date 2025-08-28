# Daily Log Update Slash Command

Update the daily log in the repository at the end of each session.

## Repository Structure
Daily logs are now organized in the repository under `daily-logs/` directory:
- **Template**: `daily-logs/template.md` - Contains template questions and format
- **Monthly files**: `daily-logs/YYYY/YYYY-MM.md` - One file per month
- **Current month**: Automatically determined based on today's date

## Process
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
