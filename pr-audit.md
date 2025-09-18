# PR Audit Command

You are conducting a comprehensive audit of open pull requests that need review attention.

## Instructions

1. **Get all open PRs** using GitHub CLI with detailed information
2. **Filter and categorize** PRs based on review status:
   - Non-draft PRs requiring initial review (reviewDecision: "REVIEW_REQUIRED")
   - PRs with requested changes (reviewDecision: "CHANGES_REQUESTED") 
   - Exclude approved PRs, drafts, and dependabot PRs
3. **Create organized output** with clickable links and key details

## Output Format

Create a structured markdown list with:
- **Priority PRs Needing Review** (non-draft, no review yet)
- **PRs Awaiting Changes** (have feedback, need author action)
- **Summary statistics**

## Commands to Run

```bash
gh pr list --state open --json number,title,author,isDraft,reviewDecision,url,headRefName --limit 50
```

## Filtering Logic

- Include: `isDraft: false` AND `reviewDecision: "REVIEW_REQUIRED"`
- Include: `reviewDecision: "CHANGES_REQUESTED"` 
- Exclude: `isDraft: true`
- Exclude: `reviewDecision: "APPROVED"`
- Exclude: `author.login: "app/dependabot"`

## Output Template

```markdown
## 🔍 Open PRs Needing Review

**Non-draft PRs requiring review:**
- [#XXXX - Title](URL) by Author

**PRs with requested changes:**
- [#XXXX - Title](URL) by Author

**Total: X PRs requiring initial review + Y PRs needing changes addressed**
```

Focus on actionable PRs that team members can immediately review or that authors need to update.