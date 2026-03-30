# Feedback Behavior Modification Protocol

**Version:** 1.0  
**Applies To:** All Agents  
**Purpose:** Turn user feedback into actual behavior changes, not just logged data

---

## The Problem

Current state: Agents ask "Was this helpful?" but do nothing with the answer.

**What should happen:**
- Positive feedback → Reinforce that approach
- Negative feedback → Adjust behavior immediately
- Pattern detection → Proactive improvements

---

## Feedback Loop Architecture

```
USER FEEDBACK
      │
      ▼
┌─────────────────────────────────────┐
│  PHASE 1: CAPTURE                   │
│  ├── Implicit (behavior signals)    │
│  └── Explicit (thumbs up/down)      │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  PHASE 2: CLASSIFY                  │
│  ├── What aspect? (format, depth,   │
│  │   accuracy, relevance, tone)     │
│  └── Severity? (minor, moderate,    │
│       major)                        │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  PHASE 3: RESPOND                   │
│  ├── Immediate (this session)       │
│  ├── Persistent (MEMORY.md update)  │
│  └── Systemic (agent file update)   │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  PHASE 4: VERIFY                    │
│  └── Check if adjustment worked     │
└─────────────────────────────────────┘
```

---

## Phase 1: Feedback Capture

### Implicit Signals (Detect Without Asking)

| Signal | Meaning | Action |
|--------|---------|--------|
| User edits output significantly | Format/content mismatch | Learn structure preference |
| User asks for shorter version | Too verbose | Reduce default length |
| User asks for more detail | Too brief | Increase default depth |
| User says "not what I meant" | Misunderstood request | Ask clarifying questions |
| User abandons workflow | Major issue | Flag for review |
| User immediately requests redo | Output quality issue | Adjust approach |
| User copies output directly | Success | Reinforce approach |
| User shares/exports output | High success | Strong reinforcement |

### Explicit Signals (Lightweight Capture)

**After every major output:**

```markdown
"Done! Quick feedback (optional):

[👍 Great] [👎 Needs work] [⏭️ Skip]

If needs work, what would help?
- [ ] Different format
- [ ] More/less detail  
- [ ] Different tone
- [ ] Missing something
- [ ] Other: ___"
```

**Rules:**
- Max 1 question
- Default to "Skip" after 5 seconds
- Never block workflow for feedback
- Capture reason only if thumbs down

---

## Phase 2: Feedback Classification

### Aspect Detection

| User Says | Aspect | Example Fix |
|-----------|--------|-------------|
| "Too long" | **Length** | Reduce word count 30% |
| "Too short" | **Length** | Expand with examples |
| "Too technical" | **Tone** | Simplify language |
| "Too basic" | **Depth** | Add technical detail |
| "Wrong format" | **Format** | Switch output type |
| "Missing X" | **Coverage** | Add X to checklist |
| "Not relevant" | **Relevance** | Clarify requirements first |
| "Inaccurate" | **Accuracy** | Add validation step |

### Severity Assessment

| Severity | Indicators | Response Speed |
|----------|------------|----------------|
| **Minor** | Small edit, "almost" | End of session |
| **Moderate** | Significant edit, redo request | Immediate |
| **Major** | Abandonment, frustration | Immediate + systemic |

---

## Phase 3: Behavior Modification

### Immediate Response (This Session)

**When user signals "too long":**
```markdown
"Got it — adjusting to be more concise. Here's a shorter version:

[Revised output at 60% length]

Is this better? I'll remember this preference."
```

**When user signals "wrong format":**
```markdown
"Let me reformat that. What works better?

A) Bullet points
B) Table
C) Paragraph
D) Other: ___

[Immediately apply choice]"
```

**When user signals "missing something":**
```markdown
"What's missing? I'll add it and remember for next time.

Missing: ___

[Add to output + add to agent's checklist]"
```

### Persistent Response (MEMORY.md Update)

**Auto-update after feedback:**

```yaml
# In MEMORY.md

feedback_patterns:
  - date: 2026-01-13
    type: "too_verbose"
    context: "data analysis report"
    action: "reduce default length by 30%"
    
  - date: 2026-01-13
    type: "missing_element"
    context: "presentation"
    element: "executive summary slide"
    action: "always include exec summary"

user_preferences_learned:
  default_length: "concise"
  preferred_format: "bullet_points"
  detail_level: "high_level_first"
  tone: "professional_casual"
```

### Systemic Response (Agent Updates)

**When pattern repeats 3+ times:**

1. Flag for agent enhancement
2. Add to agent's default behavior
3. Document in changelog

**Example:**
```markdown
## Changelog — Data Analyst

### [6.3] — 2026-01-13
### Changed
- Default output length reduced 30% (based on repeated feedback)
- Executive summary now always included (user preference pattern)
```

---

## Phase 4: Verification Loop

### Check If Adjustment Worked

**After applying adjustment:**

```markdown
"I adjusted based on your feedback. Is this version better?

[New output]

[👍 Yes, perfect] [👎 Still not right] [🔄 Try different approach]"
```

### Track Adjustment Success

```yaml
# In MEMORY.md

adjustment_outcomes:
  - adjustment: "reduced length 30%"
    success: true
    keep_permanent: true
    
  - adjustment: "added technical detail"
    success: false
    note: "user wanted less, not more"
    revert: true
```

---

## Implementation for Each Agent

### Content Agents (@copywriter, @personal-brand-builder)

```markdown
Feedback triggers:
- "Too salesy" → Reduce persuasion intensity
- "Too formal" → Adjust tone to casual
- "Not my voice" → Request example of preferred voice
- "Needs hook" → Strengthen opening
```

### Analysis Agents (@data-analyst, @financial-modeler)

```markdown
Feedback triggers:
- "Too many charts" → Reduce visualization count
- "Need more context" → Add interpretation
- "Wrong metric" → Clarify metric definitions upfront
- "Missing comparison" → Add benchmarks by default
```

### Creation Agents (@presentation-maker, @pitch-deck-creator)

```markdown
Feedback triggers:
- "Too many slides" → Consolidate
- "Not visual enough" → Increase image/chart ratio
- "Missing flow" → Add transition statements
- "Wrong audience level" → Adjust complexity
```

---

## Feedback Aggregation Rules

### When to Generalize Learning

| Pattern | Threshold | Action |
|---------|-----------|--------|
| Same feedback, same agent | 2x | Update agent defaults |
| Same feedback, different agents | 3x | Update cross-cutting protocol |
| Contradictory feedback | Any | Ask for clarification |

### When NOT to Generalize

- One-off project requirements
- Context-specific adjustments
- Contradicts core agent philosophy

---

## Example Session Flow

```markdown
USER: "Create a LinkedIn post about AI productivity"

AGENT: [Generates 1200-word post]

USER: [👎] "Too long"

AGENT: "Got it — here's a shorter version (400 words):

[Shorter post]

I'll remember you prefer concise LinkedIn posts. 
Is this length better? [👍] [👎]"

USER: [👍]

AGENT: [Silently updates MEMORY.md:
  linkedin_post_length: "short (400 words)"
  learned_from: "explicit feedback"
  date: "2026-01-13"
]

--- Next session ---

USER: "Write another LinkedIn post"

AGENT: [Generates 400-word post without asking]
"Here's your post (keeping it concise as you prefer)."
```

---

## Metrics to Track

| Metric | Target | Current |
|--------|--------|---------|
| Feedback response rate | <1 second | TBD |
| Adjustment success rate | >80% | TBD |
| Repeat negative feedback | <10% | TBD |
| User satisfaction trend | ↑ | TBD |

---

*"The best feedback system is one users don't notice — it just works."*




