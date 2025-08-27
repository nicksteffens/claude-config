# Daily Log Update Slash Command

Update the daily log gist at the end of each session.

## Gist Information
- **Gist ID**: `5e2da7e26d47e0e734935cdcdbb1df73`
- **Update Command**: `gh gist edit 5e2da7e26d47e0e734935cdcdbb1df73`

## Process
1. **Download current log**: `gh gist view 5e2da7e26d47e0e734935cdcdbb1df73 --raw > /tmp/daily-log.md`

2. **Ask the template questions** from the daily log:
   - What was the main objective for today's session?
   - How long did we work together today?
   - What was your role/involvement in the work? (directing, collaborating, reviewing, etc.)
   - What specific challenge(s) did we encounter that were most significant?
   - What was the most valuable part of our collaboration today?
   - Any specific lessons learned or insights you'd like documented?
   - Are there any follow-up items or things to remember for future sessions?
   - How would you rate the overall success of today's session? (1-10 scale)

3. **Check if today's date section exists** (## YYYY-MM-DD format)
   - If section exists: append new session entry under that date
   - If section doesn't exist: create new date section and add entry

4. **Format the session entry** with:
   - Session Overview (duration, objective, success rating)
   - What We Accomplished ✅
   - Challenges Encountered 🔧 
   - Most Valuable Collaboration
   - Key Insight
   - Follow-Up Items 📝
   - Role Distribution
   - Success Factors (if rating 6+)

5. **Update the local copy** with the new entry in the correct date section

6. **Clean duplicate headers**: Check if file starts with duplicate "Movable Ink + Claude Daily Log" lines and remove them, keeping only the markdown header "# Movable Ink + Claude Daily Log"

7. **Upload updated log**: `gh gist edit 5e2da7e26d47e0e734935cdcdbb1df73 /tmp/daily-log.md`

8. **Confirm the update** was successful

## Example Usage
Run this at the end of each Claude Code session to maintain comprehensive session logs.