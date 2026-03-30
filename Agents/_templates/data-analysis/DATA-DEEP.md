# 📊 Template: DATA-DEEP

**Type:** Deep Dive Analysis
**Outputs:** Dashboard + Summary + Detailed appendix
**Best For:** Answering specific business questions with data

---

## 📋 Structure

### 1. Executive Summary
**One page maximum**
- Primary finding (1 sentence)
- Supporting evidence (2-3 bullets)
- Confidence level (High/Medium/Low)
- Recommendation (1 sentence)
- Key metric change

### 2. Hypothesis Section
**What we're testing**
- User's hypothesis
- Alternative hypotheses (2-3)
- How we'll test each
- Data sources used

### 3. Methodology
**How we analyzed**
- Data period (e.g., Week 50 vs Week 49)
- Data sources
- Key metrics defined
- Limitations/caveats

### 4. Analysis Context Banner
**Always visible at top of dashboard**
```
┌─────────────────────────────────────────────────────────┐
│ ANALYSIS: [Title]                                       │
│ Period: [Date range]  |  Baseline: [Comparison period]  │
│ Hypothesis: [One sentence]                              │
└─────────────────────────────────────────────────────────┘
```

### 5. Top 3 Insights + Actions
**Above the fold**
| # | Insight | So What | Action |
|---|---------|---------|--------|
| 1 | [Finding] | [Implication] | [Specific action] |
| 2 | [Finding] | [Implication] | [Specific action] |
| 3 | [Finding] | [Implication] | [Specific action] |

### 6. KPI Summary
**Key metrics at a glance**
- Format: Big number + trend + vs target
- Max 6 KPIs visible
- RAG status (Red/Amber/Green)

### 7. Primary Analysis
**The main investigation**
- Chart with key finding
- Insight as chart title (not description)
- Annotations for important points

### 8. Breakdowns
**Dimensional analysis**
- By segment
- By time period
- By geography
- By channel
- By product/category

### 9. Driver Analysis
**What's causing the change?**
- PVM decomposition (if applicable)
- Driver tree
- Contribution waterfall

### 10. Devil's Advocate
**Challenge the hypothesis**
- Alternative explanations
- Confounding factors
- Data limitations
- What could disprove this

### 11. Recommendations
**What to do**
- Specific actions
- Owners
- Timeline
- Expected impact

### 12. Next Steps
**Further analysis**
- What questions remain
- What data would help
- Suggested deep dives

---

## 📊 Dashboard Layout

```
┌─────────────────────────────────────────────────────────┐
│ [HEADER: Title | Period | Hypothesis]                   │
├─────────────────────────────────────────────────────────┤
│ [TOP 3 INSIGHTS + ACTIONS]                              │
├─────────────────────────────────────────────────────────┤
│ [KPI SUMMARY: 4-6 metrics with trends]                  │
├─────────────────────────────────────────────────────────┤
│ [PRIMARY CHART: Main finding visualization]              │
├───────────────────────────┬─────────────────────────────┤
│ [BREAKDOWN 1]             │ [BREAKDOWN 2]               │
├───────────────────────────┼─────────────────────────────┤
│ [BREAKDOWN 3]             │ [DRIVER ANALYSIS]           │
├───────────────────────────┴─────────────────────────────┤
│ [DEVIL'S ADVOCATE / ALTERNATIVE HYPOTHESES]             │
├─────────────────────────────────────────────────────────┤
│ [RECOMMENDATIONS + NEXT STEPS]                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Visualization Rules

### Chart Selection
| Question | Chart Type |
|----------|------------|
| How has it changed over time? | Line chart |
| How does it compare? | Bar chart (horizontal for many items) |
| What's the composition? | Donut or stacked bar |
| What's driving the change? | Waterfall |
| How are things distributed? | Histogram or box plot |
| What's the relationship? | Scatter plot |

### Chart Quality Checklist
- [ ] Y-axis starts from zero (bar/column)
- [ ] Round numbers for axis labels
- [ ] Data labels visible and not overlapping
- [ ] Title = Insight (not description)
- [ ] Subtitle = Context (period, segment)
- [ ] Source footnote included
- [ ] Colors consistent across charts
- [ ] Baseline visible (if comparing to target)

---

## 📝 Intake Questions

Before starting analysis, confirm:

1. **Business question:** What specific question are we answering?
2. **Hypothesis:** What do you think is happening? Why?
3. **Period:** What time period? What comparison?
4. **Audience:** Who will see this? (C-suite/Team Lead/Analyst)
5. **Breakdowns:** Which dimensions matter? (Segment, Geo, Channel)
6. **Depth:** How much devil's advocate?
7. **Output:** Dashboard only? + Summary? + Detailed?

---

## 🖨️ Print Requirements

### Dashboard (HTML)
- Navigation bar for sections
- Print button with options
- `@page { margin: 0 }` for clean print

### Summary (PDF-ready)
- 1-2 pages
- Key charts embedded
- Insights and recommendations

### Detailed Appendix
- All data tables
- Methodology details
- Additional breakdowns

---

## ⚠️ Common Mistakes to Avoid

1. **Jumping to conclusions** — Test alternative hypotheses
2. **Correlation ≠ causation** — State what you can prove
3. **Cherry-picking** — Show data that challenges hypothesis too
4. **No "so what"** — Every chart needs an insight and action
5. **Too many metrics** — Focus on what matters
6. **Misleading charts** — Follow universal chart rules

---

## 🔄 Audience Versions

| Audience | What Changes |
|----------|--------------|
| **C-Suite** | Max 3 pages, 5 charts, big decisions only |
| **Team Lead** | Full dashboard, all breakdowns, actions |
| **Analyst** | + Detailed methodology, data tables, code |
| **External** | Polish visuals, add context, remove jargon |

---

*Template version: 1.0 | Last updated: 2026-01-14*




