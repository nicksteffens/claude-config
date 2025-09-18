# PR Audit Command

You are conducting a comprehensive audit of open pull requests that need review attention with enhanced tracking and analysis.

## Instructions

1. **Create audit tracking** using TodoWrite tool to track progress
2. **Get detailed PR data** using GitHub CLI with comprehensive information
3. **Enhance with change statistics** for better context
4. **Link to Shortcut stories** where possible using MCP Shortcut integration
5. **Filter and categorize** PRs based on review status and priority
6. **Create organized output** with actionable insights

## Enhanced Data Collection

### Primary PR Data
```bash
gh pr list --state open --json number,title,author,isDraft,reviewDecision,url,headRefName,additions,deletions,changedFiles,createdAt,updatedAt --limit 50
```

### Detailed File Changes (for high-priority PRs)
```bash
gh pr diff <pr-number> --name-only
```

## TodoWrite Integration

Create audit tracking with:
```
TodoWrite: [
  {"content": "Fetch all open PRs with detailed metadata", "status": "pending", "priority": "high"},
  {"content": "Analyze change statistics for large PRs", "status": "pending", "priority": "medium"},
  {"content": "Link PRs to Shortcut stories where available", "status": "pending", "priority": "medium"},
  {"content": "Categorize PRs by review urgency", "status": "pending", "priority": "high"},
  {"content": "Generate final audit report", "status": "pending", "priority": "high"}
]
```

## Shortcut Integration

For PRs with branch names containing `sc-[number]` or titles with story references:
- Use `mcp__shortcut__stories-get-by-id` to fetch story details
- Include story status, epic, and iteration information
- Flag blocked or high-priority stories

## Enhanced Filtering Logic

### Priority Scoring
- **Critical**: Large PRs (>500 lines) needing review
- **High**: PRs linked to active sprint stories
- **Medium**: Standard PRs requiring review
- **Low**: Small PRs (<50 lines) or documentation

### Categories
- **🚨 Critical Review Needed**: Large changes, active sprint stories
- **⚡ Standard Review**: Normal PRs requiring review
- **📝 Quick Review**: Small changes, docs, tests
- **🔄 Awaiting Changes**: PRs with requested changes
- **📊 Analytics**: Change statistics and trends

## Enhanced Output Template

```markdown
## 🔍 PR Audit Report - [Date]

### 🚨 Critical Review Needed
- [#XXXX - Title](URL) by Author **[+XXX/-XXX lines, XX files]**
  - 📋 Story: [sc-XXXXX](shortcut-url) - Epic: Name - Sprint: Active
  - ⏰ Age: X days since created

### ⚡ Standard Review Required  
- [#XXXX - Title](URL) by Author **[+XXX/-XXX lines, XX files]**
  - 📋 Story: [sc-XXXXX](shortcut-url) - Status: In Development

### 📝 Quick Reviews
- [#XXXX - Title](URL) by Author **[+XX/-XX lines]**

### 🔄 Awaiting Changes
- [#XXXX - Title](URL) by Author **[Changes requested X days ago]**

### 📊 Audit Statistics
- **Total PRs requiring attention**: XX
- **Average age**: X days  
- **Largest PR**: XXX lines changed
- **Sprint-related PRs**: X/XX
- **Recommended review order**: [List of PR numbers by priority]
```

## Advanced Analysis

### Change Impact Assessment
- Flag PRs with >500 line changes as "Large"
- Identify PRs touching critical files (migrations, configs)
- Calculate review complexity score based on file types

### Story Context Integration
- Match branch patterns: `sc-[number]`, `[author]/sc-[number]/[description]`
- Fetch story status, blockers, and deadline information
- Prioritize PRs linked to current sprint iteration

### Team Workload Analysis
- Group PRs by author to identify review bottlenecks
- Track review velocity (time from creation to first review)
- Suggest review assignments based on code ownership

Focus on creating an actionable, prioritized list that helps the team efficiently allocate review time and identify blockers.