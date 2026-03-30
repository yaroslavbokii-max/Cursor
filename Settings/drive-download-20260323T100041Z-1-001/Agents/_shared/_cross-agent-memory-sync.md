# Cross-Agent Memory Sync System

**Version:** 1.0  
**Status:** ACTIVE  
**Purpose:** When one agent learns something, relevant agents learn it too

---

## 🎯 Problem Statement

When @data-analyst learns "pie chart labels should use HTML legend," the @data-visualization-expert doesn't automatically know this. This leads to:
- Same mistakes repeated across agents
- Inconsistent quality
- Wasted iterations

## 🔄 Solution: Learning Propagation System

### Learning Categories

| Category | Source Agents | Target Agents |
|----------|---------------|---------------|
| **Chart Quality** | data-analyst, data-visualization-expert | operations-dashboard-builder, presentation-maker, report-automator |
| **Print/Layout** | layout-architect, presentation-maker | workshop-exercise-designer, report-automator, visual-designer |
| **Intake Protocol** | orchestration-agent | ALL agents |
| **Brand/Styling** | brand-architect, visual-designer | ALL output-generating agents |
| **Content Structure** | copywriter, report-automator | email-composer, personal-brand-builder |
| **Data Handling** | data-analyst, data-enrichment-agent | financial-modeler, customer-insight-analyst |

---

## 📋 Propagation Rules

### Rule 1: Chart Quality Learnings

When ANY of these agents learns a chart rule:
- `@data-analyst`
- `@data-visualization-expert`
- `@operations-dashboard-builder`

**Propagate to:**
```yaml
targets:
  - data-analyst/MEMORY.md
  - data-visualization-expert/MEMORY.md
  - operations-dashboard-builder/MEMORY.md
  - presentation-maker/MEMORY.md
  - report-automator/MEMORY.md
```

**Format:**
```markdown
## Cross-Agent Learning: Chart Quality
**Source:** @[source-agent] | **Date:** [date]
**Learning:** [description]
**Evidence:** [what happened]
**Rule:** [generalized rule]
```

### Rule 2: Intake Protocol Learnings

When `@orchestration-agent` learns about intake failures:

**Propagate to:** ALL agents

**Format:**
```markdown
## Cross-Agent Learning: Intake Protocol
**Source:** @orchestration-agent | **Date:** [date]
**Learning:** [description]
**Enforcement:** [how to prevent]
```

### Rule 3: Visual/Layout Learnings

When ANY of these agents learns a layout rule:
- `@layout-architect`
- `@presentation-maker`
- `@visual-designer`

**Propagate to:**
```yaml
targets:
  - layout-architect/MEMORY.md
  - presentation-maker/MEMORY.md
  - visual-designer/MEMORY.md
  - workshop-exercise-designer/MEMORY.md
  - report-automator/MEMORY.md
  - gamma-optimizer/MEMORY.md
```

---

## 🔧 Implementation

### Automatic Sync Script

```javascript
// cross-agent-sync.js
// Run after any MEMORY.md update

const LEARNING_CATEGORIES = {
  'chart_quality': {
    keywords: ['chart', 'axis', 'label', 'pie', 'bar', 'visualization', 'plotly'],
    targets: [
      'analysis/data-analyst',
      'analysis/data-visualization-expert',
      'product/operations-dashboard-builder',
      'creation/presentation-maker',
      'productivity/report-automator'
    ]
  },
  'intake_protocol': {
    keywords: ['intake', 'checkpoint', 'mandatory', 'question', 'skip'],
    targets: ['ALL']  // Special flag for all agents
  },
  'visual_layout': {
    keywords: ['layout', 'print', 'page', 'margin', 'overflow', 'alignment'],
    targets: [
      'creation/layout-architect',
      'creation/presentation-maker',
      'creation/visual-designer',
      'creation/workshop-exercise-designer',
      'productivity/report-automator',
      'creation/gamma-optimizer'
    ]
  },
  'brand_styling': {
    keywords: ['brand', 'color', 'font', 'style', 'theme', 'bolt'],
    targets: ['ALL_OUTPUT_GENERATORS']
  },
  'content_structure': {
    keywords: ['structure', 'headline', 'subtitle', 'section', 'hierarchy'],
    targets: [
      'content/copywriter',
      'content/email-composer',
      'productivity/report-automator',
      'content/personal-brand-builder'
    ]
  }
};

function categorizelearning(learningText) {
  const categories = [];
  for (const [category, config] of Object.entries(LEARNING_CATEGORIES)) {
    if (config.keywords.some(kw => learningText.toLowerCase().includes(kw))) {
      categories.push(category);
    }
  }
  return categories;
}

function getTargetAgents(categories) {
  const targets = new Set();
  for (const category of categories) {
    const categoryTargets = LEARNING_CATEGORIES[category].targets;
    if (categoryTargets.includes('ALL')) {
      // Return special flag
      return 'ALL';
    }
    categoryTargets.forEach(t => targets.add(t));
  }
  return Array.from(targets);
}

function formatCrossAgentLearning(sourceAgent, learning, date) {
  return `
## 🔄 Cross-Agent Learning
**Source:** @${sourceAgent} | **Date:** ${date}
**Category:** ${learning.category}

### Learning
${learning.description}

### Evidence
${learning.evidence}

### Generalized Rule
${learning.rule}

### Action Required
${learning.action}
`;
}

// Export for use
module.exports = { categorizelearning, getTargetAgents, formatCrossAgentLearning };
```

---

## 📝 Manual Sync Protocol

When updating ANY agent's MEMORY.md:

### Step 1: Categorize the Learning
```
Is this learning about:
□ Chart/visualization quality?
□ Intake/protocol enforcement?
□ Visual layout/print?
□ Brand/styling?
□ Content structure?
□ Other (agent-specific only)?
```

### Step 2: If Cross-Agent Relevant
```markdown
Add to source agent MEMORY.md:
---
## New Learning: [Title]
**Date:** [date]
**Cross-Agent:** YES
**Categories:** [list]
**Description:** [learning]
**Rule:** [generalized rule]
---
```

### Step 3: Propagate to Targets
```
For each target agent in the category:
1. Open target agent's MEMORY.md
2. Add cross-agent learning section
3. Reference source agent
```

---

## 📊 Sync Status Tracking

### Sync Log Format

```markdown
# Cross-Agent Sync Log

## Latest Syncs

| Date | Source | Learning | Targets | Status |
|------|--------|----------|---------|--------|
| 2026-01-14 | @data-analyst | HTML legend for pie charts | 5 agents | ✅ Complete |
| 2026-01-14 | @data-analyst | Smart label positioning | 5 agents | ✅ Complete |
| 2026-01-14 | @orchestration-agent | Intake enforcement | ALL | ✅ Complete |
```

---

## ✅ v8 Learnings to Propagate

These learnings from the v8 Dashboard exercise should be synced to all relevant agents:

### Learning 1: HTML Legend for Pie Charts
```yaml
source: data-analyst
category: chart_quality
targets: [data-visualization-expert, operations-dashboard-builder, presentation-maker]
learning: "When pie chart labels overlap despite pull/margins, switch to textinfo='none' + HTML legend"
rule: "RULE 13 in _universal-chart-rules.md"
```

### Learning 2: Smart Label Positioning
```yaml
source: data-analyst
category: chart_quality
targets: [data-visualization-expert, operations-dashboard-builder, presentation-maker]
learning: "If bar value < reference line, position label INSIDE bar with white text"
rule: "RULE 17 in _universal-chart-rules.md"
```

### Learning 3: Mandatory Intake Enforcement
```yaml
source: orchestration-agent
category: intake_protocol
targets: ALL
learning: "Agents MUST NOT skip documented intake questions"
rule: "MANDATORY CHECKPOINT in _mandatory-checkpoint-template.md"
```

### Learning 4: Pre-Delivery Validation
```yaml
source: data-analyst
category: intake_protocol
targets: ALL_OUTPUT_GENERATORS
learning: "All outputs must pass validation checklist before delivery"
rule: "PRE-DELIVERY VALIDATION in _mandatory-checkpoint-template.md"
```

### Learning 5: Consistency Enforcement
```yaml
source: data-analyst
category: visual_layout
targets: [presentation-maker, report-automator, workshop-exercise-designer]
learning: "All same-level elements must have identical formatting throughout document"
rule: "CONSISTENCY CHECKLIST in _mandatory-checkpoint-template.md"
```

### Learning 6: Semantic Header Positioning
```yaml
source: data-analyst
category: visual_layout
targets: [presentation-maker, layout-architect, visual-designer]
learning: "Chart sections = header outside; Text sections = header inside"
rule: "RULE 16 in _universal-chart-rules.md"
```

---

## 🔗 Related Documents

- `_universal-chart-rules.md` — Chart-specific rules (v4.0)
- `_mandatory-checkpoint-template.md` — Universal checkpoints
- `_v8-learnings-protocol.md` — Generalized v8 learnings
- Individual agent MEMORY.md files

---

*Last Updated: January 14, 2026*




