# Daily Log - 2026

## Overview
This directory contains all daily log entries for 2026, organized by month.

## Monthly Files
- **[2026-01.md](2026-01.md)** - January 2026 (10 sessions)
- **[2026-02.md](2026-02.md)** - February 2026 (25 sessions)

## Monthly Summaries

### February 2026 Summary
**Total Sessions:** ~25 sessions across 10 days
**Primary Focus:** GitHub→Shortcut automation, DV/Studio frontend consolidation research, CoffeeScript removal, personal projects
**Average Rating:** ~9.5/10

**Key Achievements:**
- Built complete GitHub Issues → Shortcut sync automation using TDD (Increments 1–9)
- Batch-synced 63 existing open issues to Shortcut in one session
- Implemented automatic Shortcut story owner assignment from GitHub PR/issue assignments
- Deep research and documentation for sc-185800 (DV & Studio frontend consolidation spike — 7 research docs)
- Built `react-frontend-dashboard` routing prototype proving "Dashboard as Frontend Gateway" concept
- Converted prototype to monorepo with shared Vite build and MUI sidebar with app-owned component slots
- Removed all CoffeeScript from Rails app (compile → JS, delete sources, remove gems)
- Configured dual Shortcut MCP servers and created `shortcut-workspaces` skill
- Set up global MCP servers with Anthropic API key; improved README with forking instructions
- Migrated all Shortcut workspace references from `coherentpath` to `movableink-epd`
- Created Designer Team iteration management skill
- Created Van Range Planner PWA (personal project — 350-mile daily range rings)

**Repos Worked On:**
claude-config, front-end, railsapp, front-end-infra

**Notable Insights:**
- TDD in infrastructure automation works brilliantly — each increment proved correctness before proceeding
- Auth is the linchpin for DV/Studio frontend consolidation — SSO and session sharing must be solved first
- The "Dashboard as Frontend Gateway" pattern lets Studio mount via Rails iframe without breaking its existing routing
- `workspace-agnostic` `[sc-####]` comment format prevents deduplication failures when workspace URLs change

---

### January 2026 Summary
**Total Sessions:** 10 sessions across 4 days
**Primary Focus:** V4 API enhancements, AI Assistant UI, ESLint migration, build infrastructure
**Average Rating:** 8.5/10

**Key Achievements:**
- Added cross-company lookup to V4 `CampaignPicsController` with auto company switch and `meta.company_switched` response
- Enabled Move Campaign tool for internal users with hierarchy-restricted company search (`useCompaniesInTreeSearch`)
- Implemented operator-only fields (`force_ignore_usage`, `individual_blocks`) in V4 serializer and controller
- Migrated AI Assistant button to floating canvas position; added gradient border to DesignerDialog
- Added Data Sources and Integration guidance to Designer Assistant base instructions (sc-177542)
- Migrated 97 lint errors from `prefer-ink-components` rule across 60+ files (Card, Dialog, Drawer, Select, TextField)
- Fixed `@embroider/macros` build failure by adding resolution; removed all-numeric SHA workarounds
- Deprecated `daily-log-agent` in favor of `daily-log` skill

**Repos Worked On:**
railsapp, front-end, front-end-infra, claude-config

**Notable Insights:**
- When React Query has `staleTime: Infinity`, use `resetQueries` instead of `invalidateQueries` to force a fresh fetch
- Git's rename detection is powerful — rebasing preserves changes even after significant file moves
- The ESLint rule auto-fixer doesn't account for API differences (InkChip `chipProps` vs `label`) — a bug worth reporting
- Skills are preferable to agents for simple workflows: keep file operations in the main conversation, skip context handoff overhead

---

## Statistics
- **Total sessions**: 35+ sessions (January – February 2026)
- **Primary repositories**: front-end, railsapp, claude-config, front-end-infra
- **Success rate**: Nearly all sessions rated 8+/10, multiple perfect 10/10 runs
- **Key focus areas**: Shortcut automation, DV/Studio frontend consolidation, V4 API work, AI assistant features, build tooling

---

*For template questions and format, see [../template.md](../template.md)*
