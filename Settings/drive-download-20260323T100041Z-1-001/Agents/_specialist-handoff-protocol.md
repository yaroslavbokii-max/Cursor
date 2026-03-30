# Specialist Handoff Protocol

**Version:** 1.0  
**Applies To:** All Agents  
**Purpose:** Automatically detect when to involve specialist agents and execute seamless handoffs

---

## The Problem

Current state: Agents work in isolation. If @data-analyst encounters a visualization challenge, it doesn't automatically call @data-visualization-expert.

**What should happen:**
- Agents recognize their limitations
- Automatically suggest or invoke specialists
- Seamless context handoff
- User stays informed but not burdened

---

## Handoff Trigger Detection

### Capability Boundary Signals

| Signal in Output | Current Agent | Specialist Needed | Auto-Invoke? |
|------------------|---------------|-------------------|--------------|
| "For better visualization..." | Any | @data-visualization-expert | Yes |
| "Financial projections would require..." | Any | @financial-modeler | Suggest |
| "This needs professional design..." | Any | @visual-designer | Suggest |
| "Legal review recommended..." | Any | @contract-reviewer | Suggest |
| "Market sizing would help..." | @product-architect | @market-researcher | Yes |
| "Competitor data needed..." | Any | @competitive-analyst | Yes |
| "This could be automated..." | Any | @n8n-workflow-architect | Suggest |
| "User research would inform..." | @prd-architect | @customer-insight-analyst | Yes |

### Quality Threshold Triggers

| Condition | Action |
|-----------|--------|
| Confidence score < ⭐⭐⭐ | Suggest specialist review |
| Output outside core capability | Auto-suggest specialist |
| User requests "make it better" | Identify enhancement specialist |
| Complex multi-domain task | Propose agent team |

---

## Handoff Types

### Type 1: Silent Enhancement (Automatic)

**When:** Specialist can clearly improve output without user input.

```markdown
[DATA-ANALYST working]

Detection: "Generating 5 charts..."
→ Auto-invoke: @data-visualization-expert (silent)
→ Result: Charts meet McKinsey standards automatically

[User sees only: polished output]
```

**Candidates for Silent Enhancement:**
- Visualization polish → @data-visualization-expert
- Layout optimization → @layout-architect
- SEO optimization → @seo-optimizer (for content)
- Accessibility check → @style-guardian

### Type 2: Suggested Handoff (User Approval)

**When:** Significant scope change or resource commitment.

```markdown
[PRODUCT-ARCHITECT working]

"I've outlined the product strategy. To strengthen this, I recommend:

🔄 **Suggested Enhancement:**
→ @market-researcher: Add TAM/SAM/SOM analysis
→ @competitive-analyst: Add competitor positioning
→ @customer-insight-analyst: Add user research summary

[Yes, add all] [Select specific] [Continue without]"
```

### Type 3: Escalation Handoff (Required)

**When:** Agent cannot proceed without specialist.

```markdown
[CODE-GENERATOR working]

"⚠️ I've hit a limitation. This requires:

🚨 **Required Specialist:**
→ @database-architect: The data model design is outside my expertise.

I can continue with assumptions, or wait for specialist input.

[Call @database-architect] [Continue with assumptions] [Stop here]"
```

---

## Context Handoff Format

### Standard Handoff Package

When one agent calls another:

```yaml
handoff_package:
  from_agent: "@data-analyst"
  to_agent: "@data-visualization-expert"
  timestamp: "2026-01-13T10:30:00Z"
  
  context:
    task_summary: "Creating executive dashboard for Q4 results"
    user_preferences:
      style: "McKinsey"
      colors: "Bolt brand"
      format: "Interactive HTML"
    
  deliverables_so_far:
    - type: "analysis"
      summary: "5 key insights identified"
      data: "[reference to data]"
    
  specific_request:
    what: "Create 5 publication-ready charts"
    requirements:
      - "One chart per insight"
      - "Takeaway titles"
      - "Solstice Gold highlights"
    
  constraints:
    deadline: "User waiting"
    max_charts: 5
    
  return_to: "@data-analyst"
  return_format: "Chart code + image paths"
```

### Minimal Handoff (for quick enhancements)

```yaml
quick_handoff:
  to: "@layout-architect"
  task: "Fix page breaks in this HTML"
  content: "[HTML content]"
  return_to: "caller"
```

---

## Handoff Decision Matrix

### When to Hand Off vs. Do It Yourself

| Scenario | DIY | Hand Off |
|----------|-----|----------|
| Simple chart needed | ✅ Use basic charting | ❌ |
| Complex visualization | ❌ | ✅ @data-visualization-expert |
| Basic formatting | ✅ Apply standard format | ❌ |
| Print-ready layout | ❌ | ✅ @layout-architect |
| Simple copy edit | ✅ Fix it yourself | ❌ |
| Brand voice alignment | ❌ | ✅ @style-guardian |
| Quick math | ✅ Calculate | ❌ |
| Financial model | ❌ | ✅ @financial-modeler |

### Handoff Priority Rules

1. **User experience first** — Don't interrupt flow for minor improvements
2. **Quality over speed** — Hand off if DIY would be mediocre
3. **Transparency** — Always tell user when handing off (even silently)
4. **Single thread** — Max 2 parallel handoffs to avoid confusion

---

## Agent Capability Map

### Who Can Help With What

```yaml
capability_map:
  visualization:
    primary: "@data-visualization-expert"
    backup: "@data-analyst"
    
  financial_analysis:
    primary: "@financial-modeler"
    backup: "@data-analyst"
    
  market_intelligence:
    primary: "@competitive-analyst"
    secondary: "@market-researcher"
    
  content_quality:
    brand_voice: "@style-guardian"
    seo: "@seo-optimizer"
    copy_improvement: "@copywriter"
    
  technical:
    code: "@code-generator"
    database: "@database-architect"
    automation: "@n8n-workflow-architect"
    
  layout_design:
    primary: "@layout-architect"
    secondary: "@visual-designer"
    
  people_topics:
    hr: "@people-leader-coach"
    customers: "@customer-insight-analyst"
    accounts: "@account-manager-helper"
```

---

## Implementation for Key Agents

### @data-analyst Handoff Triggers

```markdown
IF generating_charts AND chart_count > 2:
  → HANDOFF to @data-visualization-expert
  → Package: data, insights, style preferences
  → Return: polished chart code

IF financial_analysis_needed:
  → SUGGEST @financial-modeler
  → User confirms before handoff

IF competitive_context_missing:
  → SUGGEST @competitive-analyst
  → Optional enhancement
```

### @presentation-maker Handoff Triggers

```markdown
IF data_heavy_slides > 3:
  → HANDOFF to @data-visualization-expert
  → For chart optimization

IF print_output_requested:
  → HANDOFF to @layout-architect
  → For page break handling

IF investor_audience:
  → SUGGEST @pitch-deck-creator
  → Specialized investor structure
```

### @orchestration-agent Handoff Coordination

```markdown
FOR complex_workflows:
  1. Identify all specialists needed
  2. Plan handoff sequence
  3. Execute with minimal user interruption
  4. Aggregate results
  5. Present unified output
```

---

## User Communication

### Transparent Handoff Messages

**Silent enhancement (after):**
```markdown
"I enhanced the visualizations using @data-visualization-expert 
for McKinsey-quality output."
```

**Suggested handoff:**
```markdown
"Your analysis is ready. To take it further, I can bring in:
• @financial-modeler for ROI projections
• @competitive-analyst for market context

Want me to add these? [Yes] [No thanks]"
```

**Required escalation:**
```markdown
"I've reached a point where I need specialist help:
• @database-architect for the data model

This will take ~2 minutes. [Proceed] [Skip this part]"
```

---

## Handoff Metrics

| Metric | Target |
|--------|--------|
| Handoff detection accuracy | >90% |
| Silent enhancement success | >95% |
| User acceptance of suggestions | >60% |
| Handoff latency | <5 seconds |
| Context loss rate | <5% |

---

*"A great team is one where everyone knows when to pass the ball."*




