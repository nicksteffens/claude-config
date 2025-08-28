# Claude Development Rules for Movable Ink

**Repository:** https://github.com/nicksteffens/claude-config  
**Documentation:** See `/docs/` directory for detailed guides

## Automatic Workflow Protocols

### SESSION START PROTOCOL
**When entering a new repository directory:** ALWAYS automatically run `/repo-assess` to check:
- Package manager configuration (volta/npm/yarn)
- Git branch safety and create feature branch if needed
- Pre-commit hooks and commit message requirements
- Pull request templates
- Testing commands
- Existing issues/PRs to avoid duplicates

### SESSION END PROTOCOL
**At the end of each development session:** Use the `daily-log-agent` to autonomously create session logs with:
- Main objectives accomplished  
- Session duration and success rating (provided by user)
- Challenges encountered and lessons learned
- Follow-up items for future sessions

## Permissions Overview

**See `settings.json`** for complete tool permissions configuration including:
- Auto-approved tools (allow list)
- Prohibited actions (deny list) 
- Interactive confirmations (ask list)

### Key Safety Rules
- **File deletion**: ALWAYS use `trash` command, NEVER use `rm` for safety
- **Merging PRs**: Never merge PRs we didn't create without explicit permission
- **Main branch commits**: Always blocked - create feature branch instead
- **Publishing**: NPM packages, deployments, releases require explicit permission

### Preferred Behavior
- **Be proactive**: Make reasonable implementation decisions without asking
- **Batch questions**: Ask multiple related questions together when possible
- **Explain actions**: Briefly describe what you're doing for complex operations
- **Course correct**: If I say stop or change direction, adapt immediately

## Repository Assessment (ALWAYS DO FIRST)

### 1. Package Manager Detection
- **ALWAYS check `package.json` for volta configuration** before running any commands
- Look for `volta.node` and `volta.yarn` or `volta.npm` fields
- **Rule**: If volta specifies yarn, use `yarn` commands. If no yarn specified, use `npm`
- Check for `packageManager` field as backup indicator
- Never assume - always verify before running package commands

### 2. Pre-commit and Git Hooks
- **ALWAYS check for `.husky/` directory** and examine hook files
- Read `pre-commit` and `commit-msg` hook scripts to understand requirements
- **ALWAYS use conventional commit format** without being reminded
- Follow the exact format expected by the repository's commitlint configuration

### 3. Pull Request Templates
- **Check for `.github/pull_request_template.md`** or `PULL_REQUEST_TEMPLATE.md` in repo root
- Read template structure and follow all required sections
- Include summary, test plan, and any other sections specified

### 4. Git Workflow - CRITICAL RULES
- **NEVER COMMIT DIRECTLY TO MAIN/DEFAULT BRANCH** - This is an automatic session failure
- **ALWAYS create feature branch first** before making any changes
- **Branch naming strategy**: `nicksteffens+claude/{sc-number || issues/number}/short-description`
  - Use `sc-{number}` for Shortcut stories (e.g. `nicksteffens+claude/sc-165234/fix-user-invitations`)
  - Use `issues/{number}` for GitHub issues (e.g. `nicksteffens+claude/issues/369/remove-empty-state-margins`)
- **Workflow**: 
  1. `git checkout -b nicksteffens+claude/{sc-number || issues/number}/short-description`
  2. Make changes and commit to feature branch
  3. Push feature branch: `git push -u origin branch-name`
  4. Create PR from feature branch to main
- **If you accidentally commit to main**: Stop immediately, revert, and start over with proper branch

### 5. Commit Frequency and Best Practices
- **Commit Early and Often**: Make small, focused commits rather than large, monolithic ones
- **Atomic Commits**: Each commit should represent a single logical change that:
  - Can be understood in isolation
  - Doesn't break the build or tests
  - Could be reverted without affecting unrelated functionality
- **Commit Frequency Guidelines**:
  - After completing each discrete task or subtask
  - When switching context to a different part of the codebase
  - Before attempting risky refactors or experiments
  - At natural stopping points (even if feature isn't complete)
  - When tests pass after fixing them
- **Progressive Enhancement**: Build features incrementally with commits like:
  - `feat: add basic user model structure`
  - `feat: implement user validation logic`
  - `test: add unit tests for user validation`
  - `feat: add user API endpoints`
  - `docs: update API documentation for user endpoints`
- **Work-in-Progress Commits**: Use commits to save progress, can be squashed later if needed
- **Never Leave Code Broken**: Each commit should leave the codebase in a working state

### 6. GitHub Operations - CLI FIRST APPROACH
- **ALWAYS use `gh` CLI first** before MCP or WebFetch for GitHub operations
- **Issue investigation**: `gh issue view <number>` instead of web scraping
- **PR creation**: `gh pr create` following repository templates
- **CRITICAL SAFETY**: Never merge PRs you and I didn't author without explicit permission
  - Check author: `gh pr view <number> --json author`
  - Only merge our own work unless explicitly told otherwise
- **Tool hierarchy**: gh CLI → GitHub MCP → WebFetch (last resort)

### 7. Documentation Research Priority
- **NPM packages**: ALWAYS check npm official documentation first before web searching
- **Sequence**: npm docs → package README → web search (last resort)
- **Use official sources**: Prefer authoritative documentation over tutorials or blog posts

---

**Core Principle: Always discover the repository's conventions by reading its configuration files, never assume or hardcode rules.**
