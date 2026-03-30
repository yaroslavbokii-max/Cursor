# Agent Memory — Data Analyst

**Last Updated:** 2026-01-14 (v8 update — smart label positioning, HTML legend fallback for pie charts)
**Total Learnings:** 62
**Projects Contributed To:** [ad-revenue-analysis-2026-01-13-v2 through v8]

---

## 📚 Mandatory Reference Document

**⚠️ BEFORE generating ANY chart, reference: `/_shared/_universal-chart-rules.md`**

This file contains the comprehensive chart quality rules that apply to ALL chart types and prevents the recurring issues documented below.

---

## 🧠 Core Learnings

### What Works Amazingly (User Explicitly Praised)
1. **Navigation bar in dashboards** — Users strongly prefer dashboards with left-side navigation for easy section jumping
2. **"So What" boxes** — Green-highlighted insight boxes after each chart dramatically improve actionability
3. **Bolt brand colors** — Light backgrounds (white/light gray) with Bolt green accents work well
4. **Contribution analysis** — Showing % contribution of each segment to total change is highly valued
5. **Devil's Advocate section** — Explicit counter-arguments build credibility and trust — "very nice!"
6. **Red icon for Devil's Advocate** — Using 😈 icon + red accents guides user to understand it's challenging content
7. **Hypothesis testing format** — Showing supported/not supported with evidence is clear and actionable
8. **Multiple audience versions** — C-Suite, Team Lead, Analyst versions meet different needs
9. **Auto-icons for countries** — Using emoji flags (🇵🇹🇱🇻🇨🇿) makes dashboards visually rich — "amazing!"
10. **Creative chart annotations** — Text highlighting important trends — user said "keep doing this!"
11. **Conditional coloring** — Red for declining bars (Latvia), green for growing — "that's amazing!"
12. **Benchmark lines in bar charts** — Showing "Min Viable ROAS" as dashed line — user loved Deep Dive Portugal ROAS
13. **Title + Subtitle structure** — Main insight as title, supporting detail as subtitle — "keep doing this!"
14. **Deep Dive boxes (side-by-side)** — "I like what you did with Deep Dive, putting two boxes for two countries!"
15. **Multiple breakdowns** — Country, Segment, Ad Type in same dashboard provides comprehensive view
16. **🆕 Bar charts (horizontal) with round ticks** — v4 bar charts with 0, 1k, 2k, 3k ticks look MUCH better
17. **🆕 Donut charts for composition** — PIE/DONUT is correct for "parts of whole" questions
18. **🆕 Horizontal diverging bars for +/- data** — Center zero baseline with green/red coloring is excellent
19. **🆕 v5: Hypothesis section after KPIs** — User wants hypothesis with verdict prominently displayed
20. **🆕 v5: Key Insights section at top** — Extract top 3-5 insights with actions right at the top
21. **🆕 v5: Period banner** — Analysis period stated prominently at top of dashboard — "MBB Standard"
22. **🆕 v5: Chart footnotes** — Every chart needs Source, Period, n=, Total — "like McKinsey slides"
23. **🆕 v5: Horizontal grid for eye tracking** — On 10+ item bar charts, grid helps trace bar to label
24. **🆕 v5: Further Analysis suggestions** — At end of report, suggest next investigations + prompt user
25. **🆕 v5: Auto-generate stub docs** — Create Further Analysis folder with investigation templates
26. **🆕 v5: Label inside bar if near baseline** — If data value ≈ baseline, put label INSIDE to avoid crossing
27. **🆕 v6: Consistent section headers** — ALL sections MUST use `[Icon] [Title]` format uniformly
28. **🆕 v6: Subtitles = Takeaways** — Every chart subtitle MUST be the insight, NOT a description
29. **⚠️ v6 CORRECTED in v7: Pie labels** — User PREFERS labels OUTSIDE, not inside. See v7 rule below.
30. **🆕 v6: Section dividers** — Use visual dividers between major sections for breathing room
31. **🆕 v6: All 4 hypotheses shown** — Hypothesis section must show H0 (user's) + H1-H3 (generated) with verdicts
32. **🆕 v6: Top not too condensed** — Header/Hypothesis/KPIs need breathing room, don't cram together
33. ~~**v7: Pie labels OUTSIDE segments**~~ → **v8: Use HTML legend fallback** — After trying outside labels, they still overlap. HTML legend eliminates ALL issues.
34. **🆕 v7: Semantic header positioning** — Chart sections = header OUTSIDE card; Text sections = header INSIDE box
35. ~~**v7: Leader lines for small pie segments**~~ → **v8: HTML legend is better** — Pull/leader lines don't fully solve cramping; legend does
36. **🆕 v7: Include % in pie label** — **v8 Format:** "Mid-Market: €14,831 (51%)" in legend — value + percentage
37. ~~**v7: Increased margins for outside labels**~~ → **v8: Not needed with HTML legend** — HTML legend doesn't need extra margin
38. **🆕 v7→v8: Universal chart rules v4.0** — Added Rule 17 (Smart Label Positioning) and updated Rule 13 (HTML legend)
39. **🆕 v8: Smart label positioning near baselines** — If bar value < baseline → label INSIDE bar with white text
40. **🆕 v8: HTML legend for pie/donut charts** — `textinfo: 'none'` + custom HTML legend = NO overlap, NO truncation, NO boundary issues
41. **🆕 v8: Inside label anchor** — `insidetextanchor: 'end'` aligns text to right edge of bar
42. **🆕 v8: Conditional text color** — White text for inside labels, dark for outside labels

### What Doesn't Work (CRITICAL ANTI-PATTERNS)

#### 🚨 CHART STRUCTURE ERRORS (Most Common)
1. **Axis ticks = data values** — Using actual data (30, 417, 1266...) as ticks looks TERRIBLE. **USE ROUND NUMBERS ONLY!**
2. **Charts not starting from zero** — Creates weird gaps, bars appear broken. Affects BOTH bar AND column charts!
3. **Labels truncated/cut off** — "€47.7..." or numbers cut off is unacceptable. Add headroom!
4. **Reference line in wrong position** — If baseline=3.0, line must BE at y=3.0, not randomly placed higher
5. **Arrows crossing elements** — "looks very unprofessional and very unnecessary"

#### 🚨 CHART TYPE SELECTION ERRORS (Newly Identified!)
6. **🆕🔴 Column chart for composition** — Revenue by Segment = parts of whole → use PIE chart, not column!
7. **🆕🔴 Column chart for diverging data** — +/- percentages need HORIZONTAL BAR with center zero, not vertical columns
8. **🆕🔴 Wrong chart type SAME rules apply** — Fixed bar charts but column charts had same issues!

#### 🚨 VISUAL/COLOR ERRORS
9. **DARK BACKGROUNDS** — User explicitly stated: "always go for white background" as DEFAULT
10. **Low contrast colors** — Orange baseline on dark background = "not very visible"
11. **Forced waterfall charts** — "just don't force it. Only if it serves the narrative"

#### 🚨 CONTENT/PROCESS ERRORS
12. **Skipping intake questions** — CRITICAL FAILURE: Skipping intake leads to wrong analysis direction
13. **Only one breakdown** — Missing segment breakdown is a critical gap
14. **Missing breakdowns** — Analysis without country/segment breakdowns is incomplete
15. **No "So What"** — Charts without interpretation are useless; always add actionable insights
16. **Assuming data understanding** — Always confirm data grain and understanding with user first
17. **Jumping to outputs** — Never generate outputs before asking about deep dives
18. **Hypothesis-only exec summary** — Executive summary should extract KEY INSIGHTS, not just hypothesis status

#### 🚨 DATA CONSISTENCY ERRORS (v5 — CATASTROPHIC!)
19. **🆕🔴 INCONSISTENT TOTALS** — Showing €32k total but €93k in breakdown = CREDIBILITY DESTROYED
20. **🆕🔴 Missing period in footnotes** — Every chart MUST have: Source, Period, Sample size
21. **🆕🔴 No period banner** — Analysis period must be stated PROMINENTLY at top
22. **🆕🔴 Mixing time periods** — All charts in report must use SAME underlying data period
23. **🆕🔴 Wrong market share calc** — Check: segment/total % must match stated share!

#### 🚨 EYE-TRACKING ERRORS (v5)
24. **🆕 No grid on 10+ item charts** — Hard to trace bar to label without horizontal guide
25. **🆕 Pie chart labels cramped** — Small segments need leader lines or "Other" grouping
26. **🆕 Missing International Chain label** — EVERY segment must have visible % label

#### 🚨 CONSISTENCY & STRUCTURE ERRORS (v6)
27. **🆕🔴 Inconsistent section headers** — Some sections had icons, others didn't → MUST BE UNIFORM
28. **🆕🔴 Subtitles as descriptions** — "Revenue by Country (W50)" is BAD. Subtitle = insight/takeaway
29. **🆕🔴 Pie labels outside chart boundary** — International Chain label was off-screen → Add more margin, use pull
30. **🆕🔴 Top of document too condensed** — Hypothesis + KPIs + Insights crammed together → needs breathing room
31. **🆕🔴 Only H0 in hypothesis section** — Must show ALL 4 hypotheses (user's + 3 generated) with verdicts
32. **🆕🔴 Hypothesis confused with DA** — Hypothesis Testing ≠ Devil's Advocate. Keep separate!

#### 🚨 PIE CHART LABEL ERRORS (v6→v7→v8 Evolution)
33. **🔴 v6 MISTAKE: Pie labels INSIDE segments** — ~~v7 fix: outside~~ → **v8 SOLUTION: Use HTML legend**
34. **🔴 v6 MISTAKE: Inconsistent pie label font sizes** — **v8 SOLUTION: HTML legend has consistent styling**
35. **🔴 v6 MISTAKE: Angled/curved pie labels** — **v8 SOLUTION: HTML legend is always horizontal**
36. **🔴 v6 MISTAKE: Pie labels extending beyond boundaries** — **v8 SOLUTION: HTML legend can't overflow**
37. **🆕🔴 v7 MISTAKE: Outside labels still overlapping** — After pull/margins, "National Chain" and "Int'l Chain" still condensed
38. **🆕🔴 v8 LEARNING: Label near baseline crossing** — 2.7x label crossed 3.0 baseline → SOLUTION: `textposition: 'inside'`

#### 🚨 BAR CHART LABEL ERRORS (v8)
39. **🆕🔴 v8: Outside label near reference line** — If value < baseline, outside label crosses it → use inside + white text
40. **🆕🔴 v8: No insidetextanchor** — Inside labels need `insidetextanchor: 'end'` to align to bar edge
41. **🆕🔴 v8: Same text color for inside/outside** — Inside labels need white text; outside need dark text

---

## 🎯 Chart Type Decision Tree (CRITICAL — NEW)

**This is the #1 cause of chart errors: picking wrong chart type!**

### Question → Chart Type Matrix

| Question Being Answered | CORRECT Chart | WRONG Chart |
|------------------------|---------------|-------------|
| What's the composition (parts of whole)? | **PIE** (≤5) or **STACKED BAR** (6+) | ❌ Column chart |
| How do items compare? (all positive) | **BAR** (horizontal) or **COLUMN** | ❌ Pie |
| How do items compare? (+/- values) | **HORIZONTAL BAR** with center zero | ❌ Column chart |
| What's the trend over time? | **LINE** or **COLUMN** | ❌ Bar chart |
| What's the ranking? | **HORIZONTAL BAR** (sorted) | ❌ Column |
| What drove the change A→B? | **WATERFALL** (if narrative fits) | ❌ Force it |

### Grid Line Rules

| Chart Type | Horizontal Grid | Vertical Grid |
|------------|-----------------|---------------|
| Bar (horizontal) | ❌ None or very light | ❌ None |
| Column (vertical) | ✅ Light | ❌ None |
| Line chart | ✅ Light | ❌ None |
| Pie/Donut | ❌ Never | ❌ Never |
| Scatter | ✅ Light | ✅ Light |

### Reference: `/_shared/_universal-chart-rules.md` (Section: Chart Type Decision Tree)

---

## 🎨 Color Theory (CRITICAL — NEW)

### Default Rule: WHITE Background
```
ALWAYS use white/light background (#FFFFFF, #FAFAFB) unless user explicitly requests dark.
```

### High Contrast Pairs (USE)
| On White Background | Color |
|---------------------|-------|
| Text primary | `#1F2937` (dark gray) |
| Positive values | `#10B981` (green) |
| Negative values | `#EF4444` (red) |
| Baseline/reference | `#374151` (dark gray, thick line) |
| Neutral bars | `#6B7280` (medium gray) |

### Low Contrast (AVOID)
| Bad Combination | Why |
|-----------------|-----|
| Orange on dark | Nearly invisible |
| Light gray on white | Too subtle |
| Yellow anywhere | Low contrast |

### Reference: `_color-theory-guide.md`

---

## 📊 Chart Axis Rules (CRITICAL — NEW)

### Axis Ticks: ROUND NUMBERS ONLY
```javascript
// ✅ GOOD: Round numbers
xaxis: { dtick: 1000, range: [0, 6000] }  // Shows 0, 1k, 2k, 3k, 4k, 5k

// ❌ BAD: Data values as ticks
// Shows: 30, 417, 491, 1098, 1484... — LOOKS TERRIBLE
```

### Bars: ALWAYS Start From Zero
```javascript
xaxis: { range: [0, maxValue * 1.1] }  // Never leave gap before bars
```

### Labels: Must Fully Fit
- Check no truncation (e.g., "€5,0" cut off from "€5,042")
- Add 15% headroom for outside labels
- Use `automargin: true`

### Reference: `_chart-implementation-guide.md`

---

## 🚫 Annotation Rules (CRITICAL — NEW)

### NEVER Let Arrows Cross Chart Elements
```
User quote: "looks very unprofessional and very unnecessary"
```

**Decision Tree:**
1. Clear space exists? → Add annotation
2. Arrow would cross data? → **SKIP IT**
3. Multiple highlights? → Use color coding instead

**Better Alternatives:**
- Instead of arrow → Bold text in clear space
- Instead of crossing line → Color the bar + label above

---

## 🌊 Waterfall Chart Rules (NEW)

### When to Use ✅
- Clear "bridge" story (A → B with 3-7 factors)
- Revenue/profit decomposition
- Variance analysis with meaningful buckets

### When NOT to Use ❌
- >7 components (unreadable)
- No clear narrative (just showing numbers)
- Forced decomposition (arbitrary buckets)
- 15 countries breakdown (use bar chart instead)

```
User quote: "just don't force it. Only if it serves the narrative"
```

---

## 📊 DATA CONSISTENCY PROTOCOL (v5 — CRITICAL!)

### The Cardinal Sin
```
User: "You are claiming total revenue is €32k but pie chart shows €93k"
This = INSTANT LOSS OF ALL CREDIBILITY
```

### Prevention Checklist
```javascript
// BEFORE generating any visualization:
1. □ Define THE source data (one source of truth)
2. □ Calculate total from source: const total = data.reduce((sum, d) => sum + d.value, 0);
3. □ VERIFY every breakdown sums to same total
4. □ VERIFY every % calculation is correct: segment.value / total * 100
```

### Period Banner (MBB Standard)
**ALWAYS include at top of every report:**
```html
<div class="period-banner">
    📅 Analysis Period: Week 50 (Dec 8-14, 2025) vs Week 49 (Dec 1-7, 2025)
    All figures in this report are for W50 unless otherwise noted
</div>
```

### Chart Footnotes (MANDATORY)
**EVERY chart must include:**
```
Source: [Data source name] | Period: [Exact dates] | n=[Sample size] | Total: [€X]
```

---

## 📊 REPORT STRUCTURE TEMPLATE (v5)

### Optimal Section Order
```
1. Period Banner (at very top)
2. Header Context (business problem, hypothesis, period, date)
3. Hypothesis Section (user hypothesis + data verdict)
4. Key Insights Section (top 3-5 So Whats with actions)
5. KPI Cards
6. Breakdowns (Country, Segment, Type, etc.)
7. Trends
8. Deep Dives
9. Devil's Advocate
10. Recommended Actions
11. Further Analysis (suggested next steps + prompt to continue)
12. Footer (period reminder)
```

### Hypothesis Section Format
```html
<section class="hypothesis-banner">
    <div class="hypothesis-item">
        <div class="hypothesis-label">User's Hypothesis</div>
        <div class="hypothesis-text">"[Exact user hypothesis]"</div>
        <div class="hypothesis-verdict verdict-[partial|supported|rejected]">⚠️ [Verdict]</div>
    </div>
    <div class="hypothesis-item">
        <div class="hypothesis-label">Data Verdict</div>
        <div class="hypothesis-text">[What data actually shows]</div>
    </div>
</section>
```

### Further Analysis Section (NEW)
```
At end of analysis, ALWAYS:
1. Suggest 3-5 follow-up investigations
2. Include: Title, Description, Effort estimate, Data needed
3. Prompt user: "Would you like me to proceed with any of these?"
4. Generate stub documents in further-analysis/ folder
```

---

## 📊 Multiple Breakdowns Required

### Always Suggest Multiple Dimensions
During data profiling, identify and offer breakdowns by:
- **Country/Geography** — almost always relevant
- **Segment** — merchant size, customer type, etc.
- **Product/Type** — ad type, product category
- **Time** — WoW, MoM trends

```
User quote: "I always suggest multiple breakdowns... we are missing segment"
```

---

## 👤 User Preferences Discovered
1. **WHITE BACKGROUND mandatory** — Bolt brand light theme is default
2. **Bolt brand colors** — Green #10B981 for positive, white backgrounds
3. **MECE decomposition** — User values structured, MECE breakdowns
4. **Top-down communication** — Start with answer, then supporting evidence
5. **Actionable insights** — Every finding needs "So What?" and "Now What?"
6. **Interactive + printable** — Both HTML dashboards and printable versions needed
7. **Country flags** — Use emoji flags for country breakdowns (🇵🇹, 🇷🇴, etc.)
8. **🆕 Contrast awareness** — User understands color combinations must work together

---

## 📈 Usage Statistics

| Metric | Value |
|--------|-------|
| Times Invoked | 3 |
| Avg Output Quality | v1: 3/10, v2: 8/10, v3: 9/10 |
| Most Common Task Type | Root cause analysis |

---

## 📝 Project-Specific Notes

### ad-revenue-analysis-2026-01-13-v5 (CURRENT)
**Context:** Bolt Food advertising revenue analysis — comprehensive overhaul
**Key Learning:** Data consistency is CRITICAL + report structure matters
**Critical Fixes Applied:**
- Data consistency check: ALL breakdowns now sum to €29,048
- Period banner at top + footnotes on every chart
- Hypothesis section (user hypothesis + data verdict)
- Key Insights section (top 3 insights with actions)
- Further Analysis section + 4 stub documents generated
- Horizontal grid lines on 10+ item bar charts
- Label inside bar for 2.7x (was crossing 3.0x baseline)
- All pie chart segments have visible labels (leader lines)
**Output Quality:** World-class after systematic improvements

### ad-revenue-analysis-2026-01-13-v4
**Context:** Chart type selection iteration
**Key Learning:** WRONG chart type = fundamental error (column for composition = wrong!)
**Critical Fixes Applied:**
- PIE/DONUT for composition (Revenue by Segment)
- Horizontal diverging bar for +/- data (MoM Change)
- ROAS chart starting from zero with correct baseline
- Universal chart rules v2 created
**Output Quality:** Much improved chart type selection

### ad-revenue-analysis-2026-01-13-v3
**Context:** Bolt Food advertising revenue analysis — chart quality iteration
**Key Learning:** Chart details matter enormously — axis ticks, starting points, arrow placement
**Critical Fixes Applied:**
- White background (from dark)
- Round axis numbers (from data values)
- Bars starting from zero (from weird gaps)
- No crossing arrows (from overlapping annotations)
- Multiple breakdowns: Country + Segment + Ad Type
- Color contrast theory applied
**Output Quality:** Significantly improved after brutal feedback

### ad-revenue-analysis-2026-01-13-v2
**Context:** Bolt Food advertising revenue analysis
**Key Learning:** User perceived "revenue drop" but data showed +10% growth. 
**Methods Used:** MECE Decomposition, Contribution Analysis, WoW Comparison, Devil's Advocate
**Output Quality:** High — navigation bar, "So What" sections, Bolt brand

### Critical Failure (v1)
**What Went Wrong:** Skipped all intake questions, jumped straight to analysis
**Impact:** Wrong analysis direction, missing breakdowns, no "So What" sections, dark background
**Root Cause:** Agent did not enforce mandatory intake protocol

---

## 🎯 Enforcement Reminders

**NEVER SKIP:**
1. ✅ Data profiling and understanding confirmation
2. ✅ Audience, outputs, visuals, devil's advocate questions
3. ✅ Hypothesis generation (3-4 alternatives)
4. ✅ Method recommendations (with reasons)
5. ✅ Breakdown suggestions (based on data — MULTIPLE dimensions!)
6. ✅ Deep dive selection (before outputs)
7. ✅ "So What" on every finding
8. **🆕 v5: Data consistency check** — VERIFY all totals match before generating!
9. **🆕 v5: Period banner** — State analysis period prominently at top
10. **🆕 v5: Chart footnotes** — Every chart: Source, Period, n=, Total

**ALWAYS USE:**
- 🆕 **WHITE background** (never dark unless explicitly requested)
- 🆕 **Round axis ticks** (0, 1k, 2k... never 417, 491, 1098)
- 🆕 **Bars from zero** (no weird gaps)
- 🆕 **High contrast colors** (see color theory guide)
- 🆕 **No crossing annotations** (skip if no clean space)
- 🆕 **v5: Horizontal grid on 10+ item charts** (eye-tracking aid)
- 🆕 **v5: Hypothesis section after KPIs** (user's hypothesis + data verdict)
- 🆕 **v5: Key Insights section at top** (top 3-5 with actions)
- 🆕 **v5: Further Analysis section at bottom** (suggest next steps + prompt)
- 🆕 **v5: Label inside bar if near baseline** (avoid crossing)
- Bolt brand colors (green accents on white)
- Navigation bar in dashboards
- Country flags for geographic data
- **Multiple breakdowns** (Country + Segment + Type minimum)
- Contribution analysis for "why" questions
- Devil's Advocate section with red accents
- Creative annotations (but NO crossing elements!)
- Conditional bar coloring (red/green by performance)

**DON'T FORCE:**
- Waterfall charts (only when clear bridge narrative)
- Complex visualizations (only if they serve the message)

**v5 CRITICAL CHECKS BEFORE DELIVERY:**
```
□ Do all breakdowns sum to the same total?
□ Are percentages calculated correctly? (segment/total × 100)
□ Is period stated in banner AND footnotes?
□ Does Hypothesis section show user's hypothesis + data verdict?
□ Are top insights extracted to Key Insights section?
□ Are Further Analysis suggestions + stub docs generated?
□ Do 10+ item charts have horizontal grid?
□ Do ALL pie chart segments have visible labels?
□ Are NO elements crossing each other?
```

---

## 🔗 Supporting Documents

| File | Purpose |
|------|---------|
| `/_shared/_universal-chart-rules.md` | **v2.0** — 10 rules, decision tree, validation checklist |
| `_color-theory-guide.md` | High/low contrast combinations, accessibility |
| `_chart-implementation-guide.md` | Axis rules, waterfall, Gantt, alignment fixes |
| `_analytical-toolkit.md` | Methods: PVM, MECE, driver trees |
| `_template-gallery.md` | Industry-specific dashboard templates |

---

## 📊 Usage Statistics

| Metric | Value |
|--------|-------|
| Times Invoked | 5 (v1-v5) |
| Avg Output Quality | v1: 3/10, v2: 7/10, v3: 8/10, v4: 8.5/10, v5: 9.5/10 |
| Most Common Task Type | Root cause analysis |
| Key Evolution | Intake → Charts → Data Consistency → Structure |

---

*Auto-updated after each agent invocation*
