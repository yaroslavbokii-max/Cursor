# Agent Memory Protocol

**Version:** 1.0  
**Purpose:** Define how agents learn, remember, and improve from each interaction  
**Applies to:** All agents in the system

---

## Overview

The Memory Protocol enables agents to:
1. **Learn** from each project and interaction
2. **Remember** what works and what doesn't
3. **Improve** over time based on accumulated knowledge
4. **Share** learnings with the orchestration system

---

## MEMORY.md Structure

Every agent folder contains a `MEMORY.md` file with this structure:

```markdown
# Agent Memory — [Agent Name]

**Last Updated:** [Auto-updated timestamp]
**Total Learnings:** [Count]
**Projects Contributed To:** [Count]

---

## 🧠 Core Learnings

### What Works Well
<!-- Techniques, approaches, patterns that consistently produce good results -->
- [Learning] — Source: [Project/Date]

### What Doesn't Work
<!-- Anti-patterns, approaches to avoid, common mistakes -->
- [Anti-pattern] — Source: [Project/Date]

### Edge Cases & Special Handling
<!-- Unusual situations and how to handle them -->
- [Edge case] — Handling: [Approach]

---

## 👤 User Preferences Discovered

<!-- Preferences learned from interactions with this specific user -->
- [Preference category]: [Specific preference]

---

## 📊 Usage Statistics

| Metric | Value |
|--------|-------|
| Times Invoked | 0 |
| Projects Contributed | 0 |
| Most Common Task Type | — |
| Avg Satisfaction Score | — |

---

## 🔗 Agent Collaboration Insights

### Works Best With
<!-- Which agents combine well with this one -->
- @[agent-name] — When: [scenario] — Why: [reason]

### Handoff Improvements Needed
<!-- Where agent-to-agent handoffs could be smoother -->
- To @[agent-name]: [Issue and potential improvement]

### Struggles With
<!-- Scenarios where this agent underperforms -->
- [Scenario] — Workaround: [solution if any]

---

## 📝 Project-Specific Notes

<!-- Append new entries here, unlimited history -->

### [Project Name] — [Date]
**Context:** [What was the project about]
**Task:** [What this agent was asked to do]
**What Worked:** 
- [Specific success 1]
- [Specific success 2]

**What Could Improve:**
- [Improvement 1]
- [Improvement 2]

**User Feedback:** [Direct or inferred feedback]

**Learnings Applied to Core:** [Yes/No — if Yes, which section updated]

---

*Memory auto-updated after each agent invocation*
```

---

## Memory Update Protocol

### When to Update Memory

Memory updates occur:
1. **After each task completion** — Automatic by orchestration agent
2. **When user provides feedback** — Explicit or implicit
3. **When patterns emerge** — After 3+ similar situations
4. **During retrospectives** — When user reviews agent performance

### What to Capture

| Category | Capture When... | Example |
|----------|-----------------|---------|
| **What Works** | User approves output, technique succeeds | "Using Pyramid Principle for executive summaries increases approval rate" |
| **What Doesn't Work** | User requests changes, approach fails | "Bullet-heavy slides rejected for C-suite audiences" |
| **User Preferences** | User specifies preference or shows pattern | "Prefers dark color schemes for presentations" |
| **Edge Cases** | Unusual situation requires special handling | "Multi-language audiences need simplified visuals" |
| **Collaboration Insights** | Agent combination produces good/bad results | "@data-analyst → @presentation-maker works well for board decks" |

### Memory Update Format

When updating memory, use this format:

```markdown
### [Project Name] — [YYYY-MM-DD]
**Context:** [1-2 sentence project description]
**Task:** [What the agent did]
**What Worked:** 
- [Specific item]

**What Could Improve:**
- [Specific item]

**User Feedback:** [Quote or observation]

**Learnings Applied to Core:** [Yes/No]
```

---

## Memory Injection Protocol

### Before Agent Invocation

The Orchestration Agent should:

1. **Read agent's MEMORY.md** 
2. **Extract relevant learnings** based on current task
3. **Inject as context** in the agent prompt

### Injection Format

```markdown
## 📚 Relevant Learnings from Memory

**What Works for Tasks Like This:**
- [Relevant learning 1]
- [Relevant learning 2]

**What to Avoid:**
- [Relevant anti-pattern]

**User Preferences to Apply:**
- [Relevant preference]
```

### Selective Injection

Don't inject all memory — select based on:
- Task type match
- Audience match
- Output type match
- Recent relevance (newer = more relevant)

---

## Memory Maintenance

### Consolidation (Monthly)

When a pattern appears 5+ times:
1. Promote to "Core Learnings" section
2. Keep 1-2 representative examples
3. Archive detailed project notes

### Archival (Quarterly)

Move old project notes (>3 months) to:
- `MEMORY-archive-[YYYY-Q#].md`
- Keep summary in main MEMORY.md

### Pruning (As Needed)

Remove learnings that are:
- Outdated (agent capabilities changed)
- Contradicted by newer learnings
- No longer relevant to user's needs

---

## Cross-Agent Memory Sharing

### Orchestration Agent Responsibilities

The Orchestration Agent maintains awareness of:
- All agent memories
- Cross-agent patterns
- System-wide learnings

### Shared Learnings Format

Some learnings apply to multiple agents. These go in:
- `_shared-learnings.md` at NEW/ root level

```markdown
# Shared Agent Learnings

## Applies to All Agents
- [Learning that benefits everyone]

## Applies to: @agent-1, @agent-2
- [Learning specific to these agents]
```

---

## Integration with Agent Structure

### Required Addition to Each Agent

Every agent `.md` file must include:

```markdown
## Memory Protocol

This agent maintains memory in `MEMORY.md`. After completing any task:

1. **Capture** what worked and what didn't
2. **Note** any user preferences discovered
3. **Record** collaboration insights with other agents
4. **Update** MEMORY.md via orchestration agent

Memory is injected before each invocation to apply learned patterns.
```

### Memory-Aware Prompting

Agents should reference memory in their workflow:

```markdown
## Phase 1: Context Gathering

Before starting:
- [ ] Check MEMORY.md for relevant learnings
- [ ] Apply user preferences from memory
- [ ] Note what to avoid based on past failures
```

---

## Implementation Checklist

For each agent migration:

- [ ] Create `MEMORY.md` file with template structure
- [ ] Add "Memory Protocol" section to agent `.md`
- [ ] Update workflow to include memory check
- [ ] Test memory injection in orchestration

---

*Memory Protocol v1.0 — Enabling agents that learn and improve*




