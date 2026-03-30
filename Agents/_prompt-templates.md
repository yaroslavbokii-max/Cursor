# Prompt Templates — The Radiant Operator Agent Stack

**Version:** 1.0.0  
**Last Updated:** 2026-01-12

---

## 📋 Quick Reference

This document provides **3 universal prompt templates** that work with the Agent Stack. Fill in the bracketed sections and paste directly to the Orchestrator or any specialized agent.

> **Pro Tip:** The more context you provide upfront, the fewer clarifying questions you'll receive.

---

## 🎯 The Three Universal Templates

### Template 1: The Task Executor
**Best for:** Clear, defined tasks with known outputs

```
### TASK
[Describe what you want to accomplish in 1-2 sentences]

### CONTEXT
- **Project/Client:** [Name or description]
- **Audience:** [Who will see/use the output]
- **Format:** [Deliverable type: doc, presentation, data, code, etc.]

### INPUT
[Paste your data, provide file paths, or describe what you have]

### OUTPUT REQUIREMENTS
- **Must include:** [List 2-3 essential elements]
- **Style:** [Formal/casual, detailed/concise, etc.]
- **Length:** [Approximate size or scope]

### DEADLINE/PRIORITY
[Optional: urgent, EOD, this week, etc.]
```

**Example filled:**
```
### TASK
Create a weekly business review presentation for our food delivery operations.

### CONTEXT
- **Project/Client:** Bolt Food Czech Republic
- **Audience:** Country leadership team
- **Format:** Google Slides (via Gamma paste)

### INPUT
CSV attached with last week's metrics: orders, revenue, courier efficiency.

### OUTPUT REQUIREMENTS
- **Must include:** Week-over-week comparison, top 3 wins, top 3 challenges
- **Style:** McKinsey-level professional, data-driven
- **Length:** 8-10 slides maximum

### DEADLINE/PRIORITY
Need by Tuesday morning
```

---

### Template 2: The Problem Solver
**Best for:** Complex problems, analysis requests, strategic thinking

```
### PROBLEM STATEMENT
[What challenge are you facing? Be specific.]

### BACKGROUND
- **What you've tried:** [Previous attempts, if any]
- **Constraints:** [Budget, time, resources, technical limits]
- **Success criteria:** [How will you know it's solved?]

### DATA/CONTEXT AVAILABLE
[What information do you have access to?]
- Data sources: [List]
- Documents: [File paths or descriptions]
- Stakeholders: [Who's involved]

### DESIRED OUTCOME
[What does the ideal solution look like?]

### APPROACH PREFERENCE
- [ ] Give me options, I'll decide
- [ ] Give me your best recommendation
- [ ] Walk me through the analysis first
```

**Example filled:**
```
### PROBLEM STATEMENT
Courier utilization has dropped 15% month-over-month, but we don't know why.

### BACKGROUND
- **What you've tried:** Checked for seasonal effects - doesn't explain it
- **Constraints:** Can't increase courier pay this quarter
- **Success criteria:** Identify root cause, propose 3 actionable fixes

### DATA/CONTEXT AVAILABLE
- Data sources: Looker dashboards, courier activity logs
- Documents: /Users/jakub/Desktop/PACT/Context/Bolt_Food_Metrics_Glossary.md
- Stakeholders: Operations manager, courier lead

### DESIRED OUTCOME
Clear diagnosis + implementation plan for next sprint

### APPROACH PREFERENCE
- [x] Give me your best recommendation
```

---

### Template 3: The Creative Generator
**Best for:** Content creation, brainstorming, ideation

```
### CREATE
[What type of content: post, article, script, design, campaign, etc.]

### FOR
- **Platform/Channel:** [LinkedIn, blog, presentation, etc.]
- **Target audience:** [Who will consume this]
- **Tone:** [Professional, casual, inspiring, technical, etc.]

### KEY MESSAGE
[What's the ONE thing you want people to remember?]

### INSPIRATION/REFERENCES
[Optional: Examples you like, competitors to learn from, style guides]
- Reference 1: [Link or description]
- Reference 2: [Link or description]

### CONSTRAINTS
- **Length:** [Word count, slide count, duration]
- **Brand elements:** [Colors, fonts, logos to include]
- **Avoid:** [Topics, phrases, or styles to skip]

### VARIATIONS NEEDED
- [ ] Just one version
- [ ] 2-3 options to choose from
- [ ] Multiple formats (e.g., long + short version)
```

**Example filled:**
```
### CREATE
LinkedIn post announcing my promotion to Country Manager

### FOR
- **Platform/Channel:** LinkedIn
- **Target audience:** My professional network (food delivery industry, tech)
- **Tone:** Humble but confident, personal, inspiring

### KEY MESSAGE
Hard work + great team = amazing results. Grateful and excited for what's next.

### INSPIRATION/REFERENCES
- Reference 1: See /Users/jakub/Desktop/PACT/Context/personal_tone_of_voice.md
- Reference 2: Posts from other industry leaders I admire

### CONSTRAINTS
- **Length:** 150-200 words (LinkedIn sweet spot)
- **Brand elements:** Use my "Radiant Operator" tagline
- **Avoid:** Bragging, corporate-speak, generic phrases

### VARIATIONS NEEDED
- [x] 2-3 options to choose from
```

---

## 🔧 Template Modifiers

Add these to any template for more control:

### Depth Modifier
```
### DEPTH CONTROL
- [ ] Quick & rough (80% quality, fast)
- [ ] Standard (balanced)
- [ ] Deep & thorough (take your time, highest quality)
```

### Review Modifier
```
### REVIEW MODE
- [ ] Show me the plan before executing
- [ ] Execute fully, ask questions only if blocked
- [ ] Iterative: show draft → get feedback → refine
```

### Format Modifier
```
### OUTPUT FORMAT
- [ ] Markdown (for documents)
- [ ] HTML (for web/dashboards)
- [ ] Paste-ready for Gamma
- [ ] Code (runnable)
- [ ] CSV/Structured data
```

---

## 💡 Tips for Better Prompts

### DO ✅
1. **Be specific** — "Q4 revenue analysis" not "analyze data"
2. **Provide context files** — Reference your Context folder
3. **State the format** — What should the output look like?
4. **Name your audience** — Who will see this?
5. **Include examples** — "Like this but for..."

### DON'T ❌
1. **Don't be vague** — "Make it good" doesn't help
2. **Don't skip context** — Agents can't read your mind
3. **Don't assume** — State obvious things anyway
4. **Don't forget format** — Pres vs doc vs data matters
5. **Don't rush** — 30 seconds on the prompt saves 30 minutes

---

## 🚀 Quick Starters

Copy-paste these minimal prompts when you're in a hurry:

### Analysis Quick Start
```
Analyze [this data/file] for [specific question]. 
Audience: [who]. 
Format: [type]. 
Key metric: [what matters most].
```

### Content Quick Start
```
Write [content type] for [platform].
Topic: [subject].
Tone: [style].
Length: [size].
```

### Automation Quick Start
```
Automate [this task].
Trigger: [when should it run].
Input: [what data/signal].
Output: [what should happen].
```

---

## 📚 Template Selection Guide

| Your Need | Best Template | Agents Likely Used |
|-----------|--------------|-------------------|
| Weekly report | Task Executor | @report-automator, @data-analyst |
| Figure out why X | Problem Solver | @data-analyst, @expert-panel |
| LinkedIn post | Creative Generator | @copywriter, @personal-brand-builder |
| Presentation | Task Executor | @presentation-maker, @data-visualization-expert |
| New feature idea | Problem Solver | @prd-architect, @product-architect |
| Workshop design | Task Executor | @workshop-exercise-designer, @facilitation-guide-generator |
| Scrape data | Task Executor | @web-scraper-ninja |
| Process improvement | Problem Solver | @process-optimizer (planned) |

---

## 🔄 Learning Loop

After completing any task with the agent stack:

```
### FEEDBACK (Optional but appreciated)
- What worked: [Specific wins]
- What missed: [Gaps or issues]
- For next time: [Suggestions]
```

This feedback automatically updates agent MEMORY.md files for continuous improvement.

---

*"The quality of your output is directly proportional to the quality of your input."*





