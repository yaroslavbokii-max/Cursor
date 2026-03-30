# 🚀 Agent Stack Quick Start Guide

**Time to read:** 5 minutes
**Time to first output:** 10 minutes

---

## What Is This?

This is a collection of **52 specialized AI agents** that help you create world-class outputs:
- Presentations & slides
- Data analysis & dashboards
- Reports & documents
- Workshops & exercises
- And much more

Think of it as having a team of expert consultants available 24/7.

---

## 🏁 Getting Started (3 Steps)

### Step 1: Open Cursor AI
This agent stack works inside Cursor AI. Open your project and make sure you have access to Claude.

### Step 2: Start with the Orchestrator
For most tasks, start by mentioning the orchestrator:

```
@NEW/meta/orchestration-agent/orchestration-agent.md

I want to create a presentation about [topic] for [audience].
```

The orchestrator will:
1. Ask clarifying questions
2. Select the right agents
3. Coordinate the workflow
4. Deliver quality-validated outputs

### Step 3: Answer the Questions
The orchestrator will ask about:
- **Brand/Style:** Bolt, McKinsey, Minimal, etc.
- **Audience:** Executive, Team, External
- **Content Density:** How text-heavy?
- **Outputs:** HTML, PDF, Gamma-ready?
- **Depth:** Quick, Balanced, or Deep iteration

Answer these, and it handles the rest.

---

## 📁 Folder Structure

```
Agents/NEW/
├── _shared/                 # Shared protocols & rules
├── analysis/                # Data analysis agents
│   ├── data-analyst/        # Dashboards, insights
│   ├── data-visualization-expert/
│   └── knowledge-extractor/
├── creation/                # Content creation
│   ├── presentation-maker/  # Slides & decks
│   ├── layout-architect/    # Print formatting
│   └── workshop-exercise-designer/
├── meta/                    # Meta agents
│   ├── orchestration-agent/ # START HERE
│   └── quality-assurance-reviewer/
├── content/                 # Writing agents
│   ├── copywriter/
│   └── email-composer/
└── ... (more categories)
```

---

## 🎯 Common Use Cases

### "I need a presentation"
```
@orchestration-agent

Create a 30-minute presentation about [topic] for [audience].
Format: offline workshop
Include exercises and a cheat sheet.
```

### "I need to analyze data"
```
@orchestration-agent

I have a CSV file with [data description].
Help me understand why [metric] is [trend].
I need a dashboard for my team.
```

### "I need a workshop"
```
@orchestration-agent

Create a 60-minute workshop on [topic].
25 min theory, 35 min practice.
Audience: [who]
```

### "I need a report"
```
@orchestration-agent

Write a [weekly/monthly/quarterly] report based on [data].
Audience: [executive/team/external]
Include key insights and recommendations.
```

---

## ⚡ Quick Reference: Key Agents

| Need | Agent | Trigger |
|------|-------|---------|
| **Coordinate complex tasks** | `@orchestration-agent` | Start here for multi-step work |
| **Slides & presentations** | `@presentation-maker` | Direct for simple slides |
| **Data dashboards** | `@data-analyst` | Analysis + visualization |
| **Beautiful charts** | `@data-visualization-expert` | Chart-specific work |
| **Print formatting** | `@layout-architect` | Fix print/page issues |
| **Exercises & worksheets** | `@workshop-exercise-designer` | Workshop materials |
| **Writing & copy** | `@copywriter` | Marketing copy, CTAs |
| **Email drafts** | `@email-composer` | Business emails |

---

## 🎨 Brand Presets

Available styles (ask or specify):

| Preset | Colors | Best For |
|--------|--------|----------|
| **Bolt** | Green (#34D399) | Modern, tech |
| **McKinsey** | Blue/Gray | Consulting, executive |
| **Minimal** | Black/White | Clean, professional |
| **Radiant** | Gold/White | Premium, standout |
| **Data Dark** | Dark mode | Dashboards |
| **Warm Earth** | Browns/Greens | Organic, friendly |
| **Custom** | Your colors | Brand-specific |

---

## 📦 What You Get

Every output includes:

1. **HTML file** — Interactive, viewable in browser
2. **PDF-ready** — Print button with proper page breaks
3. **Validation** — Quality checked automatically
4. **Quality score** — 0-100 rating shown

For presentations, also:
- **Gamma-ready markdown** — Paste into Gamma for instant slides

---

## ✅ Quality Validation

Every output shows a validation panel:

- **✅ PASSED** — Ready to use
- **⚠️ WARNINGS** — Minor issues, can proceed
- **❌ FAILED** — Must fix before using

The panel tells you exactly what's wrong and how to fix it.

---

## 💡 Pro Tips

### 1. Be Specific
❌ "Make a presentation"
✅ "Make a 20-minute presentation about AIDA copywriting for marketing professionals. Include 3 exercises."

### 2. Provide Context
- Who is the audience?
- What do they already know?
- What action should they take after?

### 3. Iterate
First output won't be perfect. Give feedback:
- "Make slide 3 more visual"
- "Reduce text on all slides"
- "Add more food delivery examples"

### 4. Use the Right Agent
- Complex task → `@orchestration-agent`
- Simple, single-purpose task → Direct agent (e.g., `@copywriter`)

---

## 🆘 Troubleshooting

### "Output doesn't print correctly"
- Use Chrome browser
- Set margins to "None"
- Uncheck "Headers and footers"
- Check validation panel for issues

### "Too much text on slides"
- Specify content density: "Executive style (minimal text)"
- Give feedback: "Reduce to 3 bullets per slide"

### "Wrong style/colors"
- Specify brand: "Use Bolt brand (green)"
- Or: "Use colors #34D399 and #1F2937"

### "Missing something I asked for"
- Check if you answered all intake questions
- Be explicit: "I need: 1) slides, 2) handout, 3) cheatsheet"

---

## 📚 Learn More

- **Full documentation:** `_catalog.md` — Complete agent catalog
- **Protocols:** `_shared/` — All rules and standards
- **Examples:** Ask for examples of any output type

---

## 🚀 Your First Task

Try this right now:

```
@NEW/meta/orchestration-agent/orchestration-agent.md

Create a 5-slide introduction to [topic you know well].
Audience: My team
Style: Minimal
```

See how it works. Then try something more complex.

---

**Welcome to the Agent Stack. Let's create world-class outputs together.**




