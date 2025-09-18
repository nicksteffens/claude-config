# Issue Labeling Guide

This guide outlines the comprehensive label system for consistent issue classification and management.

## Label Categories

### Priority Labels
Use **exactly one** priority label per issue:

- `priority: critical` 🔴 - Protocol violations, system failures, agent behavior that breaks core functionality
- `priority: high` 🟠 - Workflow blockers, major issues that prevent normal operation
- `priority: medium` 🟡 - Standard improvements, normal bugs and feature requests
- `priority: low` 🟢 - Nice-to-have features, minor enhancements

### Type Labels
Use **one or more** type labels to categorize the issue:

- `type: agent` 🔵 - Agent-specific issues (daily-log-agent, pr-reviewer, etc.)
- `type: workflow` 🟣 - Automation/CI workflows, GitHub Actions
- `type: template` 🔵 - Templates and documentation improvements
- `type: security` 🔴 - Permissions, safety, and security-related issues
- `type: command` 🔵 - Slash commands and command-line tools

### Status Labels
Use **exactly one** status label to track progress:

- `status: needs-investigation` 🟣 - Requires analysis before work can begin
- `status: ready-for-work` 🟢 - Defined and actionable, ready for implementation
- `status: in-progress` 🟡 - Currently being worked on
- `status: blocked` 🔴 - Cannot proceed due to dependencies or blockers

### Component Labels
Use **one or more** component labels to identify affected areas:

- `component: daily-log` 🟢 - Daily logging system and related workflows
- `component: pr-review` 🟢 - PR review workflows and pr-reviewer agent
- `component: docs` 🟢 - Documentation, README, guides

## Default GitHub Labels
Keep these existing labels for compatibility:

- `bug` - General bug reports
- `enhancement` - Feature requests and improvements
- `documentation` - Documentation-specific issues
- `question` - Questions and clarifications

## Labeling Examples

### Critical Agent Issue
```
Labels: priority: critical, type: agent, component: daily-log, bug
```

### New Slash Command Request
```
Labels: priority: medium, type: command, enhancement, status: ready-for-work
```

### Documentation Update
```
Labels: priority: low, type: template, component: docs, documentation
```

### Workflow Investigation
```
Labels: priority: high, type: workflow, status: needs-investigation
```

## Retroactive Labeling

When applying labels to existing issues:

1. **Priority**: Assess impact and urgency
2. **Type**: Identify the nature of the issue
3. **Status**: Evaluate current progress state
4. **Component**: Tag affected systems

## Label Management

- Labels should be applied when issues are created or during triage
- Update status labels as work progresses
- Use multiple type/component labels when issues span multiple areas
- Maintain one priority and one status label per issue