# 📚 Template Library

**Total Templates:** 25+
**Categories:** 6
**Usage:** Reference these in your prompts or let orchestrator suggest

---

## 🎯 How to Use

### Option 1: Reference in Prompt
```
@orchestration-agent

Use template: WORKSHOP-60MIN
Topic: AIDA copywriting
Audience: Marketing team
```

### Option 2: Let Orchestrator Suggest
```
@orchestration-agent

I need a workshop about [topic].
```
_Orchestrator will suggest appropriate template._

---

## 📊 Templates by Category

### 🎓 WORKSHOPS

| ID | Name | Duration | Structure | Best For |
|----|------|----------|-----------|----------|
| `WORKSHOP-30MIN` | Quick Workshop | 30 min | 15 theory + 15 practice | Single concept |
| `WORKSHOP-60MIN` | Standard Workshop | 60 min | 25 theory + 35 practice | Framework training |
| `WORKSHOP-90MIN` | Deep Dive Workshop | 90 min | 30 theory + 60 practice | Complex topics |
| `WORKSHOP-HALF-DAY` | Half-Day Workshop | 4 hours | Multiple modules | Skill building |

#### WORKSHOP-60MIN Template
```yaml
name: "Standard 60-Minute Workshop"
duration: 60
structure:
  - section: "Opening"
    time: 5
    content: "Hook, agenda, objectives"
  - section: "Theory Block 1"
    time: 10
    content: "Core concept introduction"
  - section: "Theory Block 2"
    time: 10
    content: "Deep dive + examples"
  - section: "Exercise 1"
    time: 10
    content: "Individual practice"
  - section: "Exercise 2"
    time: 12
    content: "Group activity"
  - section: "Exercise 3"
    time: 8
    content: "Application challenge"
  - section: "Wrap-up"
    time: 5
    content: "Key takeaways, Q&A, next steps"
deliverables:
  - slides: "15-20 slides"
  - exercises: "3 exercises on separate pages"
  - cheatsheet: "A5 quick reference"
  - facilitator_guide: "Timing + speaker notes"
```

---

### 📈 PRESENTATIONS

| ID | Name | Duration | Slides | Best For |
|----|------|----------|--------|----------|
| `PRES-PITCH` | Pitch Deck | 5-10 min | 10-12 | Investor, sales |
| `PRES-EXEC` | Executive Update | 15 min | 8-10 | Board, C-suite |
| `PRES-TEAM` | Team Update | 20-30 min | 15-20 | Team meetings |
| `PRES-TRAINING` | Training Session | 30-60 min | 20-30 | Skill training |
| `PRES-KEYNOTE` | Keynote | 30-45 min | 25-35 | Conference |

#### PRES-EXEC Template
```yaml
name: "Executive Update"
duration: 15
slides:
  - slide: 1
    type: "title"
    content: "Topic + Date + Presenter"
  - slide: 2
    type: "executive_summary"
    content: "3 key points in 30 seconds"
  - slide: 3
    type: "context"
    content: "Why this matters now"
  - slide: 4-6
    type: "findings"
    content: "Key insights (1 per slide)"
  - slide: 7
    type: "implications"
    content: "So what? Business impact"
  - slide: 8
    type: "recommendations"
    content: "Clear next steps"
  - slide: 9
    type: "asks"
    content: "What you need from audience"
  - slide: 10
    type: "appendix_intro"
    content: "Backup slides available"
style:
  density: "executive"
  words_per_slide: 40-50
  visual_ratio: "70% visual, 30% text"
```

---

### 📊 DATA ANALYSIS

| ID | Name | Outputs | Best For |
|----|------|---------|----------|
| `DATA-EXPLORE` | Exploratory Analysis | Summary + insights | Initial look at data |
| `DATA-DEEP` | Deep Dive Analysis | Full report + dashboard | Answering specific question |
| `DATA-COMPARE` | Comparison Analysis | Side-by-side + drivers | A vs B, before/after |
| `DATA-TREND` | Trend Analysis | Time series + forecast | Historical patterns |
| `DATA-DASH` | Dashboard Only | Interactive HTML | Ongoing monitoring |

#### DATA-DEEP Template
```yaml
name: "Deep Dive Analysis"
structure:
  - section: "Executive Summary"
    content: "Key finding, recommendation, confidence"
  - section: "Hypothesis"
    content: "What we're testing + alternatives"
  - section: "Methodology"
    content: "Data sources, period, approach"
  - section: "Findings"
    subsections:
      - "Primary analysis"
      - "Supporting evidence"
      - "Counterarguments"
  - section: "Breakdowns"
    content: "By segment, time, geography, etc."
  - section: "So What"
    content: "Business implications"
  - section: "Recommendations"
    content: "Specific actions with owners"
  - section: "Next Steps"
    content: "Further analysis needed"
deliverables:
  - dashboard: "Interactive HTML"
  - summary: "1-page PDF"
  - appendix: "Detailed data"
```

---

### 📝 REPORTS

| ID | Name | Length | Best For |
|----|------|--------|----------|
| `REPORT-WEEKLY` | Weekly Update | 1-2 pages | Team updates |
| `REPORT-MONTHLY` | Monthly Review | 3-5 pages | Manager reviews |
| `REPORT-QUARTERLY` | Quarterly Business Review | 10-15 pages | QBR presentations |
| `REPORT-PROJECT` | Project Status | 2-3 pages | Project tracking |
| `REPORT-POSTMORTEM` | Post-Mortem | 3-5 pages | Incident review |

#### REPORT-WEEKLY Template
```yaml
name: "Weekly Update Report"
sections:
  - name: "Highlights"
    content: "Top 3 wins this week"
    format: "Bullet points"
  - name: "Metrics"
    content: "Key numbers vs target"
    format: "Table with RAG status"
  - name: "Progress"
    content: "Initiative status"
    format: "Kanban or checklist"
  - name: "Blockers"
    content: "Issues needing help"
    format: "Problem + Ask"
  - name: "Next Week"
    content: "Focus areas"
    format: "Priorities 1-3"
style:
  length: "1-2 pages"
  tone: "Concise, factual"
  update_frequency: "Every Monday"
```

---

### ✉️ COMMUNICATIONS

| ID | Name | Length | Best For |
|----|------|--------|----------|
| `EMAIL-UPDATE` | Status Update | 3-5 sentences | Quick updates |
| `EMAIL-REQUEST` | Request Email | 5-7 sentences | Asking for something |
| `EMAIL-ANNOUNCE` | Announcement | 1 paragraph | News, changes |
| `EMAIL-FOLLOWUP` | Follow-Up | 3-4 sentences | After meeting |
| `PUSH-PROMO` | Push Notification | <100 chars | Marketing |

#### EMAIL-REQUEST Template
```yaml
name: "Request Email"
structure:
  - element: "Subject"
    format: "[Action]: [Topic] by [Date]"
    example: "Review needed: Q1 budget by Friday"
  - element: "Opening"
    format: "Context in 1 sentence"
  - element: "Request"
    format: "Clear ask with deadline"
  - element: "Why"
    format: "Brief reason (optional)"
  - element: "Details"
    format: "Specifics if needed"
  - element: "Close"
    format: "Thank you + next step"
style:
  tone: "Direct, respectful"
  length: "Under 150 words"
```

---

### 🛠️ OPERATIONAL

| ID | Name | Format | Best For |
|----|------|--------|----------|
| `OPS-PROCESS` | Process Document | Steps + diagram | SOPs |
| `OPS-CHECKLIST` | Checklist | Checkboxes | Repetitive tasks |
| `OPS-TEMPLATE` | Team Template | Form | Data collection |
| `OPS-DASHBOARD` | Ops Dashboard | HTML | Real-time monitoring |
| `OPS-RUNBOOK` | Runbook | Steps + troubleshooting | On-call |

#### OPS-CHECKLIST Template
```yaml
name: "Operational Checklist"
structure:
  - section: "Pre-Flight"
    items:
      - "Verify [X]"
      - "Confirm [Y]"
      - "Check [Z]"
  - section: "Execution"
    items:
      - "Step 1: [Action]"
      - "Step 2: [Action]"
      - "Step 3: [Action]"
  - section: "Verification"
    items:
      - "Confirm [outcome]"
      - "Document [result]"
  - section: "Cleanup"
    items:
      - "Archive [files]"
      - "Notify [stakeholders]"
format:
  printable: true
  page_size: "A4"
  checkboxes: "Interactive in HTML, empty squares in print"
```

---

## 🎯 Quick Selection Guide

### By Time Available

| Time | Templates |
|------|-----------|
| 5 min | `EMAIL-UPDATE`, `PUSH-PROMO` |
| 15 min | `EMAIL-REQUEST`, `PRES-EXEC`, `REPORT-WEEKLY` |
| 30 min | `WORKSHOP-30MIN`, `DATA-EXPLORE`, `PRES-TEAM` |
| 60 min | `WORKSHOP-60MIN`, `DATA-DEEP`, `REPORT-MONTHLY` |
| 2+ hours | `WORKSHOP-HALF-DAY`, `REPORT-QUARTERLY` |

### By Audience

| Audience | Templates |
|----------|-----------|
| Executive | `PRES-EXEC`, `DATA-COMPARE`, `REPORT-QUARTERLY` |
| Team Lead | `PRES-TEAM`, `REPORT-WEEKLY`, `DATA-DASH` |
| Individual Contributors | `OPS-CHECKLIST`, `OPS-PROCESS`, `WORKSHOP-*` |
| External | `PRES-PITCH`, `EMAIL-ANNOUNCE`, `PRES-KEYNOTE` |

### By Output Type

| Need | Templates |
|------|-----------|
| Slides | `PRES-*`, `WORKSHOP-*` |
| Documents | `REPORT-*`, `OPS-PROCESS` |
| Dashboards | `DATA-DASH`, `OPS-DASHBOARD` |
| Quick Reference | Workshop cheatsheets, `OPS-CHECKLIST` |

---

## 📁 Template Files

Each template has a detailed file in `_templates/`:

```
_templates/
├── _TEMPLATE-LIBRARY.md    # This file
├── workshops/
│   ├── WORKSHOP-30MIN.md
│   ├── WORKSHOP-60MIN.md
│   ├── WORKSHOP-90MIN.md
│   └── WORKSHOP-HALF-DAY.md
├── presentations/
│   ├── PRES-PITCH.md
│   ├── PRES-EXEC.md
│   ├── PRES-TEAM.md
│   ├── PRES-TRAINING.md
│   └── PRES-KEYNOTE.md
├── data-analysis/
│   ├── DATA-EXPLORE.md
│   ├── DATA-DEEP.md
│   ├── DATA-COMPARE.md
│   ├── DATA-TREND.md
│   └── DATA-DASH.md
├── reports/
│   ├── REPORT-WEEKLY.md
│   ├── REPORT-MONTHLY.md
│   ├── REPORT-QUARTERLY.md
│   ├── REPORT-PROJECT.md
│   └── REPORT-POSTMORTEM.md
├── communications/
│   ├── EMAIL-UPDATE.md
│   ├── EMAIL-REQUEST.md
│   ├── EMAIL-ANNOUNCE.md
│   ├── EMAIL-FOLLOWUP.md
│   └── PUSH-PROMO.md
└── operational/
    ├── OPS-PROCESS.md
    ├── OPS-CHECKLIST.md
    ├── OPS-TEMPLATE.md
    ├── OPS-DASHBOARD.md
    └── OPS-RUNBOOK.md
```

---

*Templates save time. Use them.*




