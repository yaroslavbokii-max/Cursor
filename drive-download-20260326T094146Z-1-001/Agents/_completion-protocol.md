# Task Completion Protocol

**Version:** 1.0  
**Applies To:** All Agents  
**Purpose:** Know when to stop. Define "done."

---

## The Problem

Current state: Agents keep working until user says stop.

**What goes wrong:**
- Over-engineering simple tasks
- Never-ending refinement loops
- User doesn't know if we're done
- No clear "ship it" moment

**What should happen:**
- Clear success criteria before starting
- Stop when criteria met
- Explicit "done" declaration
- User knows we're finished

---

## The Completion Framework

### Before Starting Any Task

```markdown
## Task: [Description]

**Success Criteria:**
- [ ] [Criterion 1] — How we'll know it's met
- [ ] [Criterion 2] — How we'll know it's met
- [ ] [Criterion 3] — How we'll know it's met

**Definition of Done:**
When all criteria are checked, task is complete.

**Quality Threshold:**
- Minimum: [What "good enough" looks like]
- Target: [What "great" looks like]
- Stretch: [What "exceptional" looks like]
```

### During Task Execution

```markdown
## Progress Check

**Criteria Status:**
- [✅] Criterion 1 — Met at [time]
- [🔄] Criterion 2 — In progress (70%)
- [⬜] Criterion 3 — Not started

**Current quality level:** Minimum reached
**Continue to:** Target level

**Estimated to completion:** [X minutes/hours]
```

### At Task Completion

```markdown
## ✅ Task Complete

**All success criteria met:**
- [✅] Criterion 1
- [✅] Criterion 2
- [✅] Criterion 3

**Quality achieved:** Target level

**Deliverables:**
1. [Output 1] — [Description]
2. [Output 2] — [Description]

**Not included (by design):**
- [What we intentionally didn't do]
- [Why it wasn't in scope]

**If you want more:**
- [Option to expand]
- [Option to refine]
```

---

## Standard Success Criteria by Task Type

### Data Analysis

```markdown
Success criteria:
- [ ] Key insight identified and explained
- [ ] Supporting data provided
- [ ] Confidence level stated
- [ ] So What / Now What included
- [ ] Alternative hypotheses considered

Quality levels:
- Minimum: Insight + data
- Target: + alternatives + recommendations
- Stretch: + predictive model
```

### Presentation Creation

```markdown
Success criteria:
- [ ] All required sections present
- [ ] Narrative flows logically
- [ ] Takeaway in each title
- [ ] Visual guidelines followed
- [ ] Exportable format ready

Quality levels:
- Minimum: Complete slides
- Target: + speaker notes
- Stretch: + handout version
```

### Content Writing

```markdown
Success criteria:
- [ ] Target length achieved
- [ ] Key message clear
- [ ] Tone matches brief
- [ ] CTA included (if applicable)
- [ ] No placeholder text

Quality levels:
- Minimum: Draft ready for review
- Target: Publish-ready
- Stretch: + A/B variants
```

### Code Generation

```markdown
Success criteria:
- [ ] All requirements implemented
- [ ] Code runs without errors
- [ ] Tests included
- [ ] Documentation present
- [ ] Security reviewed

Quality levels:
- Minimum: Working code
- Target: + tests + docs
- Stretch: + optimization + edge cases
```

### Workflow Automation

```markdown
Success criteria:
- [ ] All steps automated
- [ ] Error handling present
- [ ] Tested with sample data
- [ ] Documentation provided

Quality levels:
- Minimum: Works manually triggered
- Target: + scheduled + alerts
- Stretch: + monitoring + optimization
```

---

## Stop Signals

### When to Stop Automatically

| Signal | Action |
|--------|--------|
| All criteria met | Declare done |
| Quality threshold reached | Offer to continue or ship |
| Diminishing returns | Flag and recommend stop |
| User says "that's good" | Stop immediately |
| User says "ship it" | Finalize and deliver |

### When to Keep Going

| Signal | Action |
|--------|--------|
| Criteria not met | Continue working |
| User wants more | Add to criteria |
| Quality below minimum | Must continue |
| Critical error found | Fix before done |

---

## Quality vs. Time Trade-offs

### The Quality Ladder

```
Level 5: Exceptional (150% effort)
    │
Level 4: Excellent (120% effort)
    │
Level 3: Target ← Default stop point
    │
Level 2: Good (80% effort)
    │
Level 1: Minimum (60% effort)
    │
Level 0: Not acceptable (blocked)
```

### When to Accept Lower Quality

```markdown
Accept Minimum when:
- User explicitly requests speed
- Deadline is tight
- Task is low-stakes
- First draft / exploration

Never accept below Minimum:
- Core criteria must always be met
- Errors must always be fixed
- Misleading outputs not allowed
```

---

## User Communication

### "I'm Done" Message

```markdown
"✅ **Task Complete**

I've finished [task description]. Here's what I delivered:

**What you got:**
1. [Deliverable 1]
2. [Deliverable 2]

**Quality level:** Target (publish-ready)

**Want me to continue?**
[🎯 Ship it] [✨ Polish more] [🔄 Different approach]"
```

### "I Could Do More" Message

```markdown
"I've reached the target quality level. 

**What I could add (if you want):**
- [Enhancement 1] — ~10 min
- [Enhancement 2] — ~15 min
- [Enhancement 3] — ~20 min

[✅ Done for now] [⬆️ Level up]"
```

### "I'm Stuck" Message

```markdown
"⚠️ I've hit a blocker.

**What's stopping me:**
[Clear description of blocker]

**To continue, I need:**
- [Requirement 1]
- [Requirement 2]

[Provide info] [Skip this part] [Change approach]"
```

---

## Scope Management

### Scope Creep Detection

```markdown
IF user_adds_requirements DURING task:
  1. Acknowledge the addition
  2. Assess impact on completion
  3. Options:
     A) Add to current task (extends timeline)
     B) Complete current, then new task
     C) Replace current criteria
  4. Get explicit choice
```

### Scope Communication

```markdown
"You've added [new requirement]. This changes things:

**Option A:** Add to current task
- New completion time: +[X]
- Quality impact: [may reduce other areas]

**Option B:** Finish current, then tackle new
- Current finishes: [time]
- New starts after

**Option C:** Replace [existing criterion] with new
- Tradeoff: [what we won't do]

Which works better for you?"
```

---

## Implementation

### For Each Agent

Add to workflow:

```markdown
1. **Define success criteria** before starting
2. **Track progress** against criteria
3. **Declare completion** when criteria met
4. **Offer extension** if more is possible
5. **Log completion** in metrics
```

### Completion Log Format

```yaml
completion_log:
  task_id: "task-2026-01-13-001"
  task_type: "data_analysis"
  
  criteria:
    - criterion: "Key insight identified"
      met: true
      met_at: "10:15:00"
    - criterion: "Recommendations provided"
      met: true
      met_at: "10:18:00"
      
  quality_achieved: "target"
  time_to_completion: "12 minutes"
  extensions_offered: ["deeper analysis", "presentation"]
  extension_accepted: false
  
  user_feedback: "positive"
```

---

*"Done is better than perfect. But know what 'done' means before you start."*




