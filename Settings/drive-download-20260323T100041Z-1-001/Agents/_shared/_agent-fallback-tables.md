# Agent-Specific Fallback Tables

**Version:** 1.0  
**Purpose:** When primary approach fails, switch to fallback  
**Source:** v8 Dashboard learnings — persisting with failing approach caused 8 iterations

---

## 🎯 How to Use Fallbacks

```
IF primary approach fails after 2 attempts:
  1. Log the failure
  2. Inform user: "Switching to alternative approach"
  3. Apply fallback
  4. Continue
```

---

## 📊 Analysis Agents

### @data-analyst

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Pie chart labels overlap | Outside labels with pull | Labels still overlap after margin increase | HTML legend (`textinfo: 'none'`) |
| Bar label near baseline | Outside label | Label crosses reference line | Inside label with white text |
| Data too large to analyze | Full dataset analysis | >1M rows or timeout | Sample 10% + extrapolate |
| User hypothesis unclear | Test user's hypothesis | User says "I don't know" | Generate 3 hypotheses to choose from |
| Chart type unclear | Recommend based on data | User rejects recommendation | Show decision tree, let user choose |

### @data-visualization-expert

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Complex chart | Plotly interactive | User needs static image | Generate PNG via screenshot |
| Color accessibility | Brand colors | Fails WCAG contrast | High-contrast mode colors |
| Chart too dense | Full data | >50 data points | Top N + "Other" grouping |
| Code doesn't run | Python/Plotly | Import errors | Provide Chart.js alternative |

### @financial-modeler

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Complex model | Full DCF model | User needs quick estimate | 3-statement simplified |
| Missing data | Request all data | User can't provide | Use industry benchmarks |
| Scenario explosion | 5 scenarios | Too many combinations | Focus on 3: Base, Bull, Bear |

---

## 🎨 Creation Agents

### @presentation-maker

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Content overflow | Reduce text | Still doesn't fit | Split into 2 slides |
| Chart in slide | Inline chart | Renders poorly | Link to full dashboard |
| Gamma formatting | Rich markdown | Gamma rejects | Simplified markdown |
| Print issues | CSS print media | Browser adds headers | iframe print or PDF export |

### @layout-architect

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Table breaks across page | CSS page-break-inside | Still breaks | Move entire table to next page |
| Content overflows page | Reduce content | Can't reduce | Add page, split content |
| Element overlap | Adjust positioning | Still overlaps | Add clearfix, margin spacing |
| Font doesn't render | Custom font | Font missing | System font stack |

### @workshop-exercise-designer

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Exercise too long | Full exercise | Exceeds time budget | Shortened "express" version |
| Group size mismatch | Designed for 5 | Group is 3 or 10 | Provide variations |
| Materials unavailable | Physical materials | User can't print | Digital-only version |

### @visual-designer

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Complex illustration | Custom SVG | Too time-consuming | Icon + text description |
| Brand color conflict | Exact brand colors | Poor contrast | Adjusted brand palette |
| Animation issues | CSS animation | Browser compatibility | Static with transition |

---

## ✍️ Content Agents

### @copywriter

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Tone mismatch | User's brand voice | Voice file unclear | Ask 3 tone questions |
| Word count exceeded | Full version | Over limit | Summarized version |
| Industry jargon | Technical terms | User needs simpler | Plain language version |

### @email-composer

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Email too long | Full content | >300 words | Executive summary + full in attachment |
| Formatting breaks | Rich HTML | Client strips formatting | Plain text version |
| CTA unclear | Subtle CTA | Low engagement expected | Bold, explicit CTA |

---

## 🤖 Automation Agents

### @web-scraper-ninja

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Page blocks request | Standard request | 403/captcha | Enable stealth mode |
| Stealth blocked | Browser stealth | Still blocked | Proxy rotation |
| Proxy blocked | Proxy pool | Still blocked | Apify/cloud service |
| Dynamic content | Wait for selector | Element never loads | JavaScript execution |
| Pagination fails | Next button click | Button not found | URL pattern increment |

### @n8n-workflow-architect

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Node doesn't exist | Native node | Not in n8n | HTTP Request to API |
| Webhook fails | Webhook trigger | Webhook unreachable | Polling schedule |
| Rate limited | Full speed | API rate limit hit | Add delay nodes |

---

## 🧠 Meta Agents

### @orchestration-agent

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Agent skips protocol | Monitor compliance | Agent skips intake | Force agent to ask questions |
| Agent fails | Primary agent | Agent errors | Alternative agent or manual |
| User overwhelmed | Full workflow | User says "too complex" | Simplified 3-step version |

### @prompt-architect

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| User can't answer questions | Detailed intake | User frustrated | Provide defaults, confirm |
| Prompt too complex | Full RISEN framework | User confused | Simplified 3-line prompt |

---

## 📈 Productivity Agents

### @report-automator

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Template mismatch | Auto-detect template | Can't identify structure | Ask user to highlight sections |
| Data refresh fails | Live data connection | Connection error | Use cached data + timestamp |
| Formula errors | Auto-generate formulas | Formulas break | Hardcode values + flag for review |

### @project-commander

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Timeline too aggressive | Proposed timeline | User says impossible | Identify scope cuts |
| Dependencies circular | Dependency graph | Circular detected | Flag for human resolution |
| Resource conflict | Auto-assign | Resource unavailable | Show alternatives |

---

## 🎯 Strategy Agents

### @expert-panel

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Expert role unclear | Pre-defined experts | None fit the topic | Generate custom expert persona |
| Consensus impossible | Multi-expert discussion | Experts disagree | Present all viewpoints, let user decide |

### @idea-forge

| Situation | Primary | Fallback Trigger | Fallback |
|-----------|---------|------------------|----------|
| Ideas too similar | Diverse generation | All ideas converge | Apply "opposite thinking" technique |
| User rejects all ideas | Generated ideas | All rejected | Ask "What would you NOT reject?" |

---

## 🔧 Implementation

### Adding Fallbacks to Agents

Copy this template into agent `.md` file:

```markdown
## 🔄 Fallback Protocol

### Situation: [Specific situation]
**Primary approach:** [Default solution]
**Fallback trigger:** [When to switch]
**Fallback approach:** [Alternative solution]

### Fallback Behavior
When primary fails after 2 attempts:
1. Log: "Primary approach failed: [reason]"
2. Inform user: "Switching to [fallback] approach"
3. Execute fallback
4. Document in MEMORY.md
```

---

*Last Updated: January 14, 2026*




