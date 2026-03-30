# Cross-Agent Memory Sharing Protocol

**Version:** 1.0  
**Applies To:** All Agents  
**Purpose:** Enable agents to learn from each other and share context across the stack

---

## The Problem

Current state: Each agent has its own `MEMORY.md` in isolation. Learnings don't propagate.

**Example of the problem:**
- @data-analyst learns "User prefers concise tables"
- @presentation-maker doesn't know this
- User has to re-teach the same preference

**What should happen:**
- Learnings propagate to related agents
- User preferences are global (with overrides)
- Domain knowledge is shared
- Anti-patterns are collective

---

## Memory Architecture

```
MEMORY HIERARCHY
      │
      ▼
┌─────────────────────────────────────┐
│  LEVEL 1: USER GLOBAL               │
│  /Agents/NEW/_global-memory.md      │
│  ├── User preferences               │
│  ├── Cross-project learnings        │
│  └── Global anti-patterns           │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  LEVEL 2: CATEGORY SHARED           │
│  /Agents/NEW/[category]/_memory.md  │
│  ├── Category-specific learnings    │
│  ├── Inter-agent discoveries        │
│  └── Domain knowledge               │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  LEVEL 3: AGENT LOCAL               │
│  /Agents/NEW/[cat]/[agent]/MEMORY.md│
│  ├── Agent-specific learnings       │
│  ├── Task-specific patterns         │
│  └── Local overrides                │
└─────────────────────────────────────┘
```

---

## Level 1: Global Memory (_global-memory.md)

**Location:** `/Agents/NEW/_global-memory.md`

```yaml
# Global User Memory
# Applies to ALL agents unless overridden

user_profile:
  name: "Jakub"
  role: "CEO / Former McKinsey"
  industry: "Food Delivery"
  communication_style: "Direct, professional, data-driven"

global_preferences:
  output_format: "Markdown preferred, HTML for visuals"
  detail_level: "Executive summary first, details available"
  tone: "Professional but warm (Radiant Operator)"
  length: "Concise by default"
  visualization_style: "McKinsey / MBB"
  brand_files:
    tone: "/Users/jakubhostacny/Desktop/PACT/Context/personal_tone_of_voice.md"
    visual: "/Users/jakubhostacny/Desktop/PACT/Context/personal_brand_guideline.md"

global_anti_patterns:
  - "Never use 3D charts"
  - "Never use pie charts for >5 categories"
  - "Never use rainbow color schemes"
  - "Never start with caveats — lead with insight"
  - "Never use 'as an AI' language"

global_learnings:
  - learning: "User prefers actionable recommendations over analysis"
    source: "@data-analyst"
    date: "2026-01-10"
    applies_to: ["analysis", "strategy"]
    
  - learning: "User values speed over perfection for first drafts"
    source: "@presentation-maker"
    date: "2026-01-11"
    applies_to: ["all"]

project_context:
  current_projects:
    - name: "Q1 Strategy Review"
      relevant_agents: ["@data-analyst", "@presentation-maker"]
    - name: "Personal Brand Launch"
      relevant_agents: ["@personal-brand-builder", "@copywriter"]
```

---

## Level 2: Category Shared Memory

**Example: `/Agents/NEW/analysis/_memory.md`**

```yaml
# Analysis Category Shared Memory
# Shared across: @data-analyst, @data-visualization-expert, 
#                @financial-modeler, @contract-reviewer, @knowledge-extractor

category_learnings:
  data_handling:
    - "Always profile data before analysis"
    - "Check for missing values explicitly"
    - "Validate outliers before removing"
    
  visualization:
    - "User prefers bar charts over pie charts"
    - "Always use Bolt brand colors for work projects"
    - "Include takeaway in chart title"
    
  output_format:
    - "Lead with insight, support with data"
    - "Max 5 key points per analysis"
    - "Include confidence level on all insights"

shared_discoveries:
  - discovery: "Data often has timezone issues - always check"
    from: "@data-analyst"
    useful_for: ["@financial-modeler", "@report-automator"]
    
  - discovery: "User's Bolt metrics follow specific glossary"
    from: "@data-analyst"
    context_file: "/Users/jakubhostacny/Desktop/PACT/Context/Bolt_Food_Metrics_Glossary.md"
    useful_for: ["all_analysis_agents"]

cross_agent_handoff_notes:
  data_analyst_to_viz_expert:
    - "Always include raw data, not just summaries"
    - "Specify which insight to highlight"
    
  financial_modeler_to_presentation:
    - "Include both model and key assumptions"
    - "Highlight sensitivity ranges"
```

---

## Level 3: Agent Local Memory

**Existing `MEMORY.md` files — enhanced with inheritance**

```yaml
# Agent-specific MEMORY.md header

inherits_from:
  global: "../../_global-memory.md"
  category: "../_memory.md"
  
local_overrides:
  # Override global preference for this agent
  detail_level: "High detail (analysis needs depth)"
  
agent_specific_learnings:
  # Learnings that only apply to this agent
  - learning: "For this user, always include SQL queries"
    context: "data analysis"
    date: "2026-01-12"
```

---

## Memory Propagation Rules

### When Learnings Propagate UP (Local → Global)

| Condition | Action |
|-----------|--------|
| Same learning in 3+ agents | Promote to category memory |
| Same learning in 2+ categories | Promote to global memory |
| User explicitly says "always" | Immediate global promotion |
| Core preference (format, tone) | Immediate global promotion |

### When Learnings Propagate DOWN (Global → Local)

| Condition | Action |
|-----------|--------|
| New agent created | Inherits global + category |
| User preference changes | Push to all relevant agents |
| Anti-pattern discovered | Push to all agents |

### Conflict Resolution

```
Priority (highest to lowest):
1. Explicit user instruction (this session)
2. Agent local override
3. Category shared memory
4. Global memory
5. Agent defaults
```

---

## Memory Sync Protocol

### On Agent Start

```python
def load_memory(agent):
    # 1. Load global memory
    global_mem = load("../../_global-memory.md")
    
    # 2. Load category memory
    category_mem = load("../_memory.md")
    
    # 3. Load local memory
    local_mem = load("MEMORY.md")
    
    # 4. Merge with priority
    effective_memory = merge(
        global_mem,      # base
        category_mem,    # overlay
        local_mem        # final override
    )
    
    return effective_memory
```

### On Learning Captured

```python
def save_learning(agent, learning, scope):
    if scope == "local":
        append_to("MEMORY.md", learning)
        
    elif scope == "category":
        append_to("../_memory.md", learning)
        notify_category_agents(learning)
        
    elif scope == "global":
        append_to("../../_global-memory.md", learning)
        notify_all_agents(learning)
```

### Periodic Sync (Background)

```python
def nightly_memory_sync():
    # 1. Find repeated local learnings
    repeated = find_repeated_learnings(threshold=3)
    
    # 2. Promote to appropriate level
    for learning in repeated:
        if repeated_across_categories(learning):
            promote_to_global(learning)
        else:
            promote_to_category(learning)
    
    # 3. Clean up duplicates
    deduplicate_memories()
    
    # 4. Archive old learnings (>90 days unused)
    archive_stale_learnings()
```

---

## Shared Context Types

### 1. User Preferences (Global)

```yaml
preferences:
  output:
    format: "Markdown"
    length: "Concise"
    style: "Professional"
  interaction:
    questions: "Minimal, smart defaults"
    involvement: "Balanced"
```

### 2. Domain Knowledge (Category)

```yaml
domain_knowledge:
  food_delivery:
    key_metrics: ["GMV", "AOV", "Orders", "Frequency"]
    context_file: "Bolt_Food_Metrics_Glossary.md"
    seasonal_patterns: "Weekend peaks, lunch/dinner rushes"
    
  saas:
    key_metrics: ["MRR", "Churn", "CAC", "LTV"]
    typical_targets: "LTV:CAC > 3:1"
```

### 3. Anti-Patterns (Global)

```yaml
anti_patterns:
  never_do:
    - "Use passive voice for recommendations"
    - "Include caveats before insights"
    - "Use jargon without explanation"
    - "Present data without context"
    
  always_do:
    - "Lead with the takeaway"
    - "Include 'So What?' and 'Now What?'"
    - "Provide actionable next steps"
```

### 4. Successful Patterns (Category/Local)

```yaml
successful_patterns:
  - pattern: "Start data analysis with hypothesis"
    success_rate: "95%"
    agent: "@data-analyst"
    shareable: true
    
  - pattern: "Use SCR for executive summaries"
    success_rate: "90%"
    agent: "@presentation-maker"
    shareable: true
```

---

## Implementation Checklist

### Phase 1: Create Shared Memory Files
- [ ] Create `_global-memory.md`
- [ ] Create category `_memory.md` files
- [ ] Update agent MEMORY.md with `inherits_from`

### Phase 2: Update Agent Loading
- [ ] Add memory inheritance logic
- [ ] Implement conflict resolution
- [ ] Add propagation triggers

### Phase 3: Enable Sync
- [ ] Implement learning promotion
- [ ] Add cross-agent notification
- [ ] Create deduplication logic

---

## Example: Cross-Agent Learning Flow

```
Day 1:
@data-analyst learns: "User wants SQL queries included"
→ Saved to local MEMORY.md

Day 3:
@financial-modeler learns same thing
→ Pattern detected: 2 analysis agents

Day 5:
@data-visualization-expert receives same feedback
→ Pattern threshold (3) reached
→ AUTO-PROMOTE to analysis/_memory.md
→ All analysis agents now include queries by default
```

---

*"Individual agents are smart. A connected system is wise."*




