# Daily Logs Standalone Site — Design Spec

**Date:** 2026-04-13
**Status:** Approved
**Author:** Nicklas Steffens + Claude

## Summary

Extract daily logs from `claude-config` into a standalone repository published to GitHub Pages using Astro + Starlight. The site serves as a personal portfolio showcasing AI-assisted development work with rich navigation, filtering, and search.

## Goals

1. **Liberate daily logs** from the private `claude-config` repo into a public, standalone repo
2. **Publish as a portfolio site** on GitHub Pages — professional, navigable, searchable
3. **Migrate existing content** (~100+ sessions across Aug 2025 – Apr 2026) with structured frontmatter
4. **Enable filtering and search** by repo, tag, rating, date
5. **Update the daily-log workflow** to write to the new repo (skill migrates to plugin repo separately)

## Technology Choices

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Static site generator | Astro | Content-focused, excellent Markdown support, partial hydration |
| Theme | Starlight | Built-in search (Pagefind), sidebar nav, dark mode, polished UI |
| Content format | One file per session | Enables Astro content collections, individual frontmatter, clean filtering |
| Deployment | GitHub Pages via Actions | Push-to-deploy, zero infrastructure |
| Hosting | GitHub Pages | Free, reliable, custom domain support |

## Repository Structure

**Repo:** `nicksteffens/daily-logs` (new, public)

```
daily-logs/
├── astro.config.mjs
├── package.json
├── src/
│   ├── content/
│   │   ├── config.ts              # Content collection schema
│   │   └── docs/                  # Starlight content dir
│   │       ├── index.mdx          # Homepage with stats
│   │       ├── 2025/
│   │       │   ├── 08/
│   │       │   │   ├── 2025-08-01-session-1.md
│   │       │   │   ├── 2025-08-01-session-2.md
│   │       │   │   └── ...
│   │       │   ├── 09/
│   │       │   └── ...
│   │       └── 2026/
│   │           ├── 01/
│   │           └── ...
│   ├── components/               # Custom Astro components
│   │   ├── StatsCard.astro
│   │   ├── Timeline.astro
│   │   └── TagFilter.astro
│   └── pages/
│       ├── tags/[tag].astro      # Tag filtering pages
│       └── timeline.astro        # Timeline view
├── scripts/
│   └── migrate.ts                # One-time migration script
└── .github/
    └── workflows/
        └── deploy.yml            # GitHub Pages deployment
```

## Content Schema

### Session File Format

Each session is a markdown file at `src/content/docs/YYYY/MM/YYYY-MM-DD-session-N.md`:

```markdown
---
title: "Front-end tunnel prototype"
date: 2026-04-01
session: 1
duration: "1 hour"
rating: 10
objective: "Prototype the front-end tunnel reverse proxy"
repos: ["front-end", "railsapp", "cli"]
tags: ["tunnel", "prototype", "multi-repo"]
role: "directing"
shortcut: "sc-194515"
---

### What We Accomplished
- ...

### Challenges Encountered
- ...

### Most Valuable Collaboration
...

### Key Insight
...

### Follow-Up Items
- [ ] ...

### Role Distribution
**Human:** ...
**Claude:** ...

### Success Factors
...
```

### Frontmatter Schema (Zod via Astro)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Session title (derived from objective) |
| `date` | date | yes | Session date |
| `session` | number | yes | Session number for the day (1, 2, 3...) |
| `duration` | string | yes | Session duration |
| `rating` | number | yes | Success rating (1-10) |
| `objective` | string | yes | Main objective |
| `repos` | string[] | no | Repositories worked on |
| `tags` | string[] | no | Topic tags |
| `role` | string | no | User's role (directing, collaborating, reviewing) |
| `shortcut` | string | no | Shortcut story ID |

## Site Features

### Navigation (Starlight sidebar)

```
Sidebar:
├── Home (stats overview)
├── Timeline (chronological view)
├── Tags (all tags index)
├── 2026/
│   ├── April
│   ├── March
│   ├── February
│   └── January
└── 2025/
    ├── December
    ├── November
    ├── October
    ├── September
    └── August
```

### Homepage (`index.mdx`)

- Total session count and date range
- Average rating
- Sessions per month (visual bar or sparkline)
- Most-used repos and tags
- Links to timeline and latest sessions

### Search

Pagefind (included with Starlight) — client-side full-text search across all sessions.

### Tag Filtering (`/tags/[tag]`)

Dynamic pages listing all sessions with a given tag. Each tag page shows sessions in reverse chronological order with title, date, rating, and repos.

### Timeline View (`/timeline`)

Chronological (reverse-chron) view of all sessions. Filterable by year/month. Shows session cards with key metadata.

### Custom Components

- **StatsCard** — reusable stat display (count, average, etc.)
- **Timeline** — session timeline with date grouping
- **TagFilter** — tag chip cloud with active state

## Migration Plan

### Migration Script (`scripts/migrate.ts`)

A Node.js script that:

1. Reads each monthly markdown file from a source directory (default: `~/.claude/daily-logs/`)
2. Parses session boundaries:
   - Splits on `## YYYY-MM-DD` headings for date boundaries
   - Splits on `---` separators within a date for multi-session days
   - Detects "Session N Overview" markers for session numbering
3. Extracts structured data from each session:
   - **Date** from `## YYYY-MM-DD` heading
   - **Session number** from position or "Session N" markers
   - **Duration, objective, rating** from the `### Session Overview` block
   - **Repos** inferred from PR references, branch names, repo mentions
   - **Tags** auto-generated from content keywords + repo names
   - **Role** from `### Role Distribution` block
4. Generates individual markdown files with frontmatter
5. Places files in `src/content/docs/YYYY/MM/YYYY-MM-DD-session-N.md`

### Migration Validation

- Script outputs session count per month
- Compare against existing index file session counts
- Spot-check entries for correct frontmatter extraction
- Tags can be hand-curated after initial generation

### Yearly Summaries

Port existing `index.md` content as overview pages (e.g., `src/content/docs/2025/index.mdx`).

## Deployment

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist/
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

### Repo Settings

Enable GitHub Pages with "GitHub Actions" as source.

## Daily-Log Skill Updates

**Note:** The skill itself migrates to the plugin repo as a separate effort. This section documents the behavioral changes needed.

### New behavior:

- **Configurable target path** — reads log repo location from config
- **File creation** — creates individual session files instead of appending to monthly files
- **Path format:** `src/content/docs/YYYY/MM/YYYY-MM-DD-session-N.md`
- **Session numbering** — checks for existing files with the same date prefix to determine N
- **Frontmatter generation** — populates all schema fields from session Q&A
- **Git workflow** — commits and pushes to the log repo (triggers deploy)

## Out of Scope

- Plugin repo migration of the daily-log skill (separate effort)
- Custom domain configuration (can be added later)
- RSS feed (Starlight doesn't include one; can be added as a plugin)
- Analytics/visitor tracking
