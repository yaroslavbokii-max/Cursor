# 🧠 Automated Memory Update Protocol v1.0

## Purpose
Ensure every task contributes learnings to the agent stack automatically.
No more stale MEMORY.md files.

---

## 🔴 MANDATORY: After Every Task

At the END of every agent invocation, BEFORE final delivery:

```markdown
## 📝 Learning Capture (Auto-Generated)

### Task Summary
- **Task:** [one-line description]
- **Agent(s):** [@agent1, @agent2]
- **Iterations:** [number]
- **Final Quality Score:** [X/100]

### What Worked
1. [Something that worked well]
2. [Another thing]

### What Didn't Work
1. [Issue encountered]
   - **Fix applied:** [how it was fixed]
   - **Generalize:** [should this apply to other agents? Y/N]

### Protocol Compliance
- [ ] Asked all intake questions
- [ ] Validated before delivery
- [ ] Applied brand guidelines
- [ ] Met quality threshold

### New Learning (if any)
**Learning:** [one sentence]
**Applies to:** [@agent1, @agent2, ...]
**Add to:** [_shared/_[topic]-learnings.md or agent MEMORY.md]
```

---

## 📁 Memory File Structure

### Agent-Specific Memory (`[agent]/MEMORY.md`)
```markdown
# Agent Memory — [Agent Name]

**Last Updated:** [date]
**Total Learnings:** [count]
**Projects Contributed To:** [list]

---

## 🧠 Core Learnings
[Accumulated wisdom specific to this agent]

## 📊 Usage Statistics
[Invocation count, success rate, common issues]

## 📝 Recent Tasks
[Last 5 task summaries with outcomes]

## 🔗 Agent Collaboration Notes
[What other agents work well with this one]

---
*Auto-updated after each invocation*
```

### Shared Learnings (`_shared/_[topic]-learnings.md`)
```markdown
# 📚 Learnings: [Topic] ([Date])

## Context
[Why this learning exists]

## Critical Discoveries
[Numbered list of key findings]

## Reusable Fixes
[Code snippets, CSS templates, etc.]

## Agents to Update
[Which agents need this knowledge]

---
*Auto-updated when topic-relevant tasks complete*
```

---

## 🔄 Sync Protocol

### When to Sync Across Agents

1. **Print-related learning** → Sync to:
   - `@presentation-maker`
   - `@layout-architect`
   - `@workshop-exercise-designer`
   - `@data-visualization-expert`
   - `@data-analyst`

2. **Chart/visualization learning** → Sync to:
   - `@data-analyst`
   - `@data-visualization-expert`
   - `@presentation-maker`

3. **Brand/style learning** → Sync to:
   - `@visual-designer`
   - `@presentation-maker`
   - `@report-automator`
   - `@style-guardian`

4. **Workflow/orchestration learning** → Sync to:
   - `@orchestration-agent`
   - `@agent-architect`

---

## 📋 Append Format

When updating MEMORY.md, use this exact format for consistent parsing:

```markdown
---

### [DATE] — [Task Name]
- **Type:** [Workshop / Analysis / Report / etc.]
- **Outcome:** [Success / Partial / Failed]
- **Iterations:** [N]
- **Key Learning:** [One sentence]
- **Action Taken:** [What was updated as a result]
```

---

## ⚡ Quick Reference

### At Task Start
1. Load agent MEMORY.md
2. Check for relevant shared learnings
3. Apply past learnings to current task

### At Task End
1. Capture task outcome
2. Identify new learnings
3. Append to agent MEMORY.md
4. If generalizable → Create/update shared learning file
5. If cross-agent → Notify orchestrator for sync

---

## 🎯 Success Metrics

**Target:**
- 100% of tasks result in memory update
- Shared learnings created for any issue that affects 2+ agents
- Memory files reviewed weekly for consolidation

**Measurement:**
- Track `Last Updated` dates
- Count learnings per week
- Track iteration reduction over time

---

*This protocol must be followed by ALL agents. No exceptions.*




