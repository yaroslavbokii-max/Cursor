# 🎯 PRIORITY ACTION PLAN

Based on the brutal review, here's what to fix in order of impact.

---

## 🔴 P0 — DO THIS WEEK (Highest Impact)

### 1. Add Chart Code Generation to `@data-analyst`
**Current:** Describes charts
**Target:** Outputs runnable Plotly.js code for every chart

```javascript
// Example output from @data-analyst
const revenueChart = {
    data: [{
        x: ['Week 48', 'Week 49', 'Week 50'],
        y: [32000, 35000, 29000],
        type: 'bar',
        marker: { color: '#34D399' }
    }],
    layout: {
        title: 'Revenue Dropped 17% WoW in Week 50',
        yaxis: { tickprefix: '€', tickformat: ',.0f' }
    }
};
Plotly.newPlot('revenue-div', revenueChart.data, revenueChart.layout);
```

**Files to update:**
- `analysis/data-analyst/data-analyst.md` — Add code generation section
- `_shared/_chart-code-templates.md` — Create Plotly/Chart.js templates

### 2. Simplify `@orchestration-agent`
**Current:** 1,168 lines
**Target:** 300 lines max

**Remove:**
- Verbose explanations (users don't read them)
- Redundant protocol references
- Over-complicated routing logic

**Keep:**
- First response template
- Confirmation template
- Agent selection logic
- Quality gate

### 3. Consolidate Agents (62 → 35)
**Execute the consolidation plan:**

| Merge | Into |
|-------|------|
| context-builder, research-to-prompt | @knowledge-extractor |
| seo-optimizer | @copywriter |
| personal-brand-builder | @brand-architect |
| pitch-deck-creator, gamma-optimizer | @presentation-maker |
| facilitation-guide-generator, interactive-content-compiler | @workshop-exercise-designer |
| style-guardian | @quality-assurance-reviewer |
| contract-reviewer, document-processor, data-enrichment | @knowledge-extractor |
| okr-coach, process-optimizer | @project-commander |
| productivity-system-designer | @team-template-generator |
| market-researcher | @gtm-strategist |
| competitive-analyst | @product-architect |
| decision-framework-builder | @idea-forge |

---

## 🟠 P1 — DO NEXT WEEK (High Impact)

### 4. Add Actual Puppeteer Execution to `@web-scraper-ninja`

```markdown
## New Capability: Real-Time Scraping

When user confirms, execute:

1. Use `mcp_puppeteer_puppeteer_navigate` to load page
2. Use `mcp_puppeteer_puppeteer_screenshot` to verify
3. Use `mcp_puppeteer_puppeteer_evaluate` to extract data
4. Return structured JSON/CSV

### Example Execution Flow:
[User confirms scrape]
→ Navigate to URL
→ Wait for JS render
→ Screenshot for verification
→ Extract data via evaluate
→ Format and return
```

**Files to update:**
- `automation/web-scraper-ninja/web-scraper-ninja.md` — Add execution section

### 5. Add PowerPoint Generation to `@presentation-maker`

Option A: Use python-pptx (requires terminal execution)
Option B: Generate detailed HTML that exports to PDF cleanly
Option C: Direct Google Slides API (requires auth)

**Recommendation:** Option B — Enhance HTML to be PPT-equivalent

```html
<!-- Enhanced HTML slide format -->
<section class="slide" data-slide-number="1">
    <div class="slide-header">TITLE</div>
    <div class="slide-body">CONTENT</div>
    <div class="slide-footer">© Company 2026</div>
</section>
```

### 6. Add n8n Workflow Generation to `@report-automator`

```markdown
## New Capability: Auto-Generate n8n Workflow

When user wants automated reports, generate:

1. Schedule Trigger (cron for weekly/monthly)
2. Data Fetch (HTTP Request / Google Sheets)
3. Data Transform (Code node)
4. Report Generation (Template filling)
5. Delivery (Email / Slack)

### Example n8n Workflow Output:
{
    "nodes": [
        {"type": "n8n-nodes-base.scheduleTrigger", ...},
        {"type": "n8n-nodes-base.googleSheets", ...},
        {"type": "n8n-nodes-base.code", ...},
        {"type": "n8n-nodes-base.gmail", ...}
    ]
}
```

---

## 🟡 P2 — DO THIS MONTH (Medium Impact)

### 7. Add Conversation Scripts to `@people-leader-coach`

```markdown
## New Capability: Word-for-Word Scripts

### Giving Tough Feedback Script:
"[Name], I wanted to share some observations with you. 
In the [specific situation], I noticed [specific behavior]. 
The impact was [specific consequence]. 
Going forward, what I need to see is [specific expectation].
What are your thoughts on this?"

### Pre-Scripted Responses to Pushback:
- If defensive: "I hear that you see it differently. Help me understand your perspective."
- If silent: "I know this is a lot to process. Take a moment if you need."
- If emotional: "I can see this is hard to hear. That's not my intention."
```

### 8. Force Disagreement in `@expert-panel`

```markdown
## New Rule: Mandatory Devil's Advocate

At least ONE expert MUST:
- Strongly disagree with the majority
- Present data/evidence for their view
- NOT be convinced by others

### Example:
Expert 1: "We should expand to Germany" ✅
Expert 2: "Agreed, the market is ready" ✅
Expert 3: "I DISAGREE. Here's why this will fail..." ⚠️ MANDATORY
```

### 9. Add Tracking to `@habit-architect`

```markdown
## New Capability: Simple Tracking

### Daily Check-In Format:
"Did you [habit] today? (yes/no/partial)"

### Weekly Review:
| Day | Completed | Notes |
|-----|-----------|-------|
| Mon | ✅ | Did 10 min |
| Tue | ❌ | Forgot |
| ... | ... | ... |

### Progress Visualization:
[Generate streak calendar, completion %, trend line]
```

---

## 🟢 P3 — DO NEXT MONTH (Lower Impact)

### 10. Add External Data Sources

| Agent | Data Source |
|-------|-------------|
| @gtm-strategist | Industry reports, market size data |
| @competitive-analyst | G2, Capterra, LinkedIn |
| @financial-modeler | Yahoo Finance, SEC filings |
| @seo-optimizer | Google Search Console, SEMrush |

---

## 📋 IMPLEMENTATION CHECKLIST

### Week 1 (P0)
- [ ] Add chart code generation to @data-analyst
- [ ] Simplify @orchestration-agent to 300 lines
- [ ] Add deprecation notices to 20+ agents
- [ ] Update @knowledge-extractor with merged capabilities
- [ ] Update @copywriter with SEO
- [ ] Update @presentation-maker with pitch deck

### Week 2 (P1)
- [ ] Add Puppeteer execution to @web-scraper-ninja
- [ ] Enhance HTML slides in @presentation-maker
- [ ] Add n8n workflow output to @report-automator

### Week 3 (P2)
- [ ] Add conversation scripts to @people-leader-coach
- [ ] Add forced disagreement to @expert-panel
- [ ] Add tracking to @habit-architect

### Week 4 (P3)
- [ ] Research external data integrations
- [ ] Prototype one integration

---

## 🎯 SUCCESS METRICS

| Metric | Current | Target |
|--------|---------|--------|
| Agent count | 62 | 35 |
| Avg agent length | 500+ lines | 200 lines |
| Code output agents | 0 | 5+ |
| External integrations | 0 | 3+ |
| User iterations to success | 3-5 | 1-2 |

---

*Start with P0. Everything else can wait.*




