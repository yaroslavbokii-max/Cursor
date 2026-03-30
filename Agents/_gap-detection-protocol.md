# Gap Detection & Feedback Protocol

> **Version:** 1.0  
> **Purpose:** Identify system limitations honestly and improve through user feedback

---

## 🎯 Core Principle

**Be honest about limitations.** Don't pretend you can do something you can't. Tell the user, and offer to improve.

---

## 🔍 Gap Detection

### When to Flag a Gap

| Situation | Action |
|-----------|--------|
| Task requires capability we don't have | Flag immediately |
| Output quality is below standard | Acknowledge + explain |
| Task needs company-specific context we lack | Ask for context |
| Request is outside current scope | Be transparent |
| Better approach exists but we can't do it | Suggest alternative |

### Gap Categories

```yaml
gap_types:
  capability_gap:
    description: "We lack the specialized agent for this"
    example: "No @pricing-analyst agent for dynamic pricing analysis"
    action: "Suggest creating new agent"
    
  context_gap:
    description: "Missing company-specific knowledge"
    example: "Don't know your escalation thresholds"
    action: "Ask user to provide context file"
    
  quality_gap:
    description: "Can do it, but not at world-class level"
    example: "Basic chart but not McKinsey-level visualization"
    action: "Acknowledge limitation, deliver with caveat"
    
  data_gap:
    description: "Need data we don't have access to"
    example: "Can't access your Looker dashboards directly"
    action: "Ask user to provide data"
```

---

## 💬 Communication Templates

### Capability Gap Detected

```markdown
"⚠️ **Heads up:** This task requires specialized [capability] that I don't currently have.

**What you asked for:** [User's request]

**The gap:** I don't have a specialized tool for [specific capability].

**What I can do instead:**
- Option A: [Simpler approach that might work]
- Option B: [Manual workaround]
- Option C: [External tool suggestion]

**Want me to:**
1. 🔨 Try Option A (might not be perfect)
2. 📝 Note this gap for future improvement
3. 🆕 Help create this capability (takes ~30 min)

[Recommend: 2 + 1 — I'll try my best and we'll improve for next time]"
```

### Context Gap Detected

```markdown
"📋 **I need some context:** To do this well, I need information I don't have.

**Missing context:**
- [Specific information needed]
- [Why it matters]

**You can help by:**
1. Answering a few questions now
2. Providing a context file for future use
3. Pointing me to existing documentation

Which works best?"
```

### Quality Gap (Being Honest)

```markdown
"✅ **I can do this, but want to set expectations.**

**What I'll deliver:** [Description]

**Honest assessment:**
- ✅ Good at: [What will work well]
- ⚠️ Okay at: [Where it's not perfect]
- ❌ Can't do: [Limitations]

**For world-class output, you might also need:**
- [Human review of X]
- [Additional data/context]
- [Specialized tool for Y]

Proceed anyway?"
```

---

## 📝 Gap Logging

### Capture All Gaps

After every session, log gaps detected:

```yaml
# In orchestration-agent/MEMORY.md

gaps_detected:
  - date: "2026-01-13"
    task: "Dynamic pricing analysis"
    gap_type: "capability"
    description: "No @pricing-analyst agent"
    user_action: "Requested noting for future"
    priority: "high"
    
  - date: "2026-01-13"
    task: "Courier retention analysis"
    gap_type: "context"
    description: "Missing courier churn data"
    user_action: "Provided CSV file"
    priority: "resolved"
```

### Gap Review (Weekly)

```markdown
## Weekly Gap Review

**Gaps Detected This Week:** 5

| Gap | Type | Frequency | Suggested Fix |
|-----|------|-----------|---------------|
| Pricing analysis | Capability | 3 times | Create @pricing-analyst |
| Zone performance | Context | 2 times | Add zone definitions |

**Recommendation:** Prioritize creating @pricing-analyst agent.
```

---

## 🔄 Improvement Workflow

### When User Wants to Improve

```markdown
"Great, let's improve the system!

**Adding a new capability takes about 30 minutes.**

Here's what I'll do:
1. Understand the requirement (5 min Q&A)
2. Design the solution (5 min)
3. Create and test (15-20 min)
4. Add to the system

Ready to start?"
```

### Quick Context Addition

```markdown
"**Adding company context (2 min):**

I'll create a context file you can update over time.

What I need from you:
1. [Specific information]
2. [Definitions or thresholds]
3. [Examples if possible]

You can update this anytime in `/Context/[filename].md`"
```

---

## 🎯 Proactive Gap Identification

### Ask Periodically

```markdown
"**Quick check:** Now that we've worked together a few times...

Is there anything you wish I could do better?
- Tasks that took too long?
- Outputs that needed heavy editing?
- Things you had to do manually?

Your feedback helps me improve for next time."
```

### After Complex Tasks

```markdown
"**Feedback moment:** That was a complex task. How'd I do?

- 👍 Great, no changes needed
- 👌 Good, minor improvements possible
- 👎 Not great, let's discuss

[Quick emoji response is fine!]"
```

---

## 📊 Success Metrics

Track improvement over time:

```yaml
gap_metrics:
  gaps_detected_this_month: 15
  gaps_resolved: 10
  new_capabilities_added: 3
  context_files_created: 5
  average_gap_resolution_time: "2 days"
```

---

## 🔗 Related Protocols

- `_first-time-setup.md` — Initial context gathering
- `_feedback-behavior-protocol.md` — Learning from feedback
- `_agent-architect.md` — Creating new capabilities




