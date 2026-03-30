# Agent Stack — Cursor project instructions

This folder is a **standalone knowledge & agent library** (downloaded bundle). Use it as the project root when working with Bolt Food analytics, Databricks SQL, QBR/MBR workflows, and the custom agent prompts under `Agents/`.

## Layout

| Path | Purpose |
|------|---------|
| `Agents/` | Specialized agent definitions (orchestration, data-analyst, PRD, strategy, etc.), templates under `Agents/_templates/`, protocols (`_quick-start.md`, `_first-time-setup.md`). |
| `Databricks & QBRs/` | Databricks connection guide, schema notes, MBR Maker, analysis framework — **start with `COLLEAGUE_SETUP_GUIDE.md`**. |
| `Promo_Campaigns _  Bolt Food/` | Bolt Food promo / cohort / ROAS reference text. |
| `.firecrawl/` | Scraped sample data (optional). |

## How to work here

1. **Fast onboarding:** Read `Agents/_quick-start.md`.
2. **Full coordination pattern:** `Agents/meta/orchestration-agent/orchestration-agent.md` (or lean `orchestration-agent-v8-lean.md` for shorter context).
3. **SQL / warehouse:** Follow `Databricks & QBRs/COLLEAGUE_SETUP_GUIDE.md`; keep secrets in `.env` (never commit). Use `tables-reference.md` and `schema_notes.md` for naming.
4. **Data analysis deliverables:** `Agents/analysis/data-analyst/` + `Agents/_templates/data-analysis/`.
5. **Presentations / exec summaries:** `Agents/_templates/presentations/PRES-EXEC.md`.

## Conventions

- Prefer **concrete, cited numbers** when analyzing metrics; align metric names with internal Looker/glossary when the user provides them.
- **Ukrainian** for user-facing explanations when the user writes in Ukrainian; **English** for slides, decks, or stakeholders who expect English (confirm if unclear).
- Do not invent Databricks credentials; use the user’s `.env` and existing `HTTP_PATH` from the colleague guide.

## What not to do

- Do not paste PAT tokens or `.env` contents into chat.
- Do not treat `.firecrawl/` as production source of truth without validation.
