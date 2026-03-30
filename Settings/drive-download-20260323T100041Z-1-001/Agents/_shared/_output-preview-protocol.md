# 📋 Output Preview Protocol

**Version:** 1.0  
**Purpose:** Generate quick previews before full output to validate direction

---

## Overview

Before investing time in full output generation, agents must offer a preview mode that shows the user a quick wireframe/outline of what will be produced.

---

## Preview Types by Output

### 1. Dashboard Preview
```markdown
📊 DASHBOARD PREVIEW

**Title:** Ad Revenue Analysis W50 vs W49

**Sections (6):**
├── Header with Period Banner
├── KPI Summary (4 metrics)
├── Hypothesis Testing Section
├── Top 3 Insights
├── Charts:
│   ├── Revenue Trend (line)
│   ├── Revenue by Country (bar)
│   ├── Revenue by Segment (pie)
│   ├── MoM Change (diverging bar)
│   └── ROAS by Ad Type (bar with baseline)
├── Devil's Advocate
└── Further Analysis Prompts

**Brand:** Bolt (Green #34D399)
**Style:** White background, minimal

Ready to generate? [Yes] [Adjust sections] [Change style]
```

### 2. Presentation Preview
```markdown
🎯 PRESENTATION PREVIEW

**Title:** MECE Framework Workshop
**Total Slides:** 25
**Duration:** 60 minutes

**Slide Outline:**
1. Title Slide
2. Agenda (3 parts)
3-8. Theory Section (6 slides)
   - What is MECE
   - Why it matters
   - Examples
   - Anti-patterns
9-20. Practice Section (12 slides)
   - Exercise 1: Classify
   - Exercise 2: Build
   - Exercise 3: Apply
21-25. Closing
   - Key Takeaways
   - Resources
   - Q&A

**Outputs:** Slides (HTML), Exercises (PDF), Cheatsheet (A5)

Ready to generate? [Yes] [Add slides] [Remove section]
```

### 3. Report Preview
```markdown
📄 REPORT PREVIEW

**Title:** Weekly Business Review
**Pages:** ~12
**Audience:** C-Suite

**Structure:**
├── Executive Summary (1 page)
├── Key Metrics Dashboard (2 pages)
├── Revenue Analysis (3 pages)
│   ├── Overview
│   ├── By Segment
│   └── Drivers
├── Operational Highlights (2 pages)
├── Risks & Issues (1 page)
├── Actions & Next Steps (1 page)
└── Appendix (2 pages)

**Data Sources:** 3 CSVs loaded
**Charts Planned:** 8

Ready to generate? [Yes] [Adjust depth] [Add section]
```

### 4. Analysis Preview
```markdown
🔍 ANALYSIS PREVIEW

**Question:** Why is ad revenue dropping?
**Hypothesis:** H0: Seasonality

**Planned Analysis:**
├── Data Profiling
│   └── 5 tables, 45 columns, 12K rows
├── Descriptive Statistics
├── Period Comparison (W50 vs W49)
├── Breakdowns:
│   ├── By Country
│   ├── By Segment
│   ├── By Ad Type
│   └── By Product
├── Statistical Tests
│   └── T-test for significance
├── Driver Analysis
│   └── Top 5 contributors
└── Devil's Advocate
    └── 3 alternative hypotheses

**Outputs:** Dashboard, Executive Summary, CSV export

Ready to proceed? [Yes] [Add breakdown] [Skip section]
```

---

## Implementation Rules

### Rule 1: Always Offer Preview
```
Before generating ANY output > 1 page:
1. Generate preview structure
2. Show to user
3. Wait for confirmation
4. Only then proceed
```

### Rule 2: Preview Must Be Fast
- Preview generation: < 5 seconds
- Full generation: As needed
- Preview should be ~5% of full effort

### Rule 3: Preview Shows Structure Not Content
- Section titles ✅
- Content placeholders ✅
- Full text ❌
- Complete charts ❌

### Rule 4: Allow Quick Adjustments
User should be able to:
- Add/remove sections
- Change order
- Adjust depth
- Switch style/brand

### Rule 5: Remember Preferences
If user always skips preview:
- Offer to disable for this session
- Learn their typical preferences

---

## Integration with Agents

### In Agent SKILL.md:

```markdown
## ⚡ OUTPUT PREVIEW PHASE

Before full generation, I will show you a preview:

**Preview includes:**
- Output structure/outline
- Section breakdown
- Estimated length/duration
- Planned visualizations

**You can then:**
- ✅ Approve and generate
- ✏️ Request adjustments
- 🔄 Start over with new approach

*Skip preview? Say "skip preview" to go directly to generation.*
```

---

## Benefits

1. **Time Savings**: Catch misalignment early
2. **User Control**: Adjust before full effort
3. **Quality**: Better outputs through iteration
4. **Trust**: User sees what's coming
5. **Learning**: System learns preferences

---

## Anti-Patterns

❌ **Don't:** Generate full output then ask if it's right  
❌ **Don't:** Make preview as complex as full output  
❌ **Don't:** Skip preview for long outputs  
❌ **Don't:** Force preview when user wants speed  
❌ **Don't:** Show preview without action options

---

*Implement this protocol in all creation, analysis, and documentation agents.*




