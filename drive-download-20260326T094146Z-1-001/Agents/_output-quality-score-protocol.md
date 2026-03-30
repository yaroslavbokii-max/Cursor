# Output Quality Score Protocol

> **Version:** 1.0  
> **Created:** 2026-01-13  
> **Purpose:** Self-assess outputs before delivery to catch issues proactively

---

## 🎯 Core Principle

**Don't deliver until you've checked your own work.**

Every output should pass a quality gate before the user sees it.

---

## 📊 Quality Scoring Matrix

### Score Calculation

| Criterion | Weight | Score (0-10) |
|-----------|--------|--------------|
| **Completeness** | 20% | Does it address all requirements? |
| **Accuracy** | 20% | Are facts/data correct? |
| **Clarity** | 20% | Is it easy to understand? |
| **Format** | 15% | Does it follow standards? |
| **Usability** | 15% | Can user use it immediately? |
| **Polish** | 10% | Professional finishing? |

**Total Score = Weighted average (0-100)**

---

## 🚦 Quality Thresholds

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | ⭐⭐⭐⭐⭐ Excellent | Deliver with confidence |
| 80-89 | ⭐⭐⭐⭐ Good | Deliver, note minor improvements |
| 70-79 | ⭐⭐⭐ Acceptable | Deliver with caveats |
| 60-69 | ⭐⭐ Needs Work | Fix before delivery |
| <60 | ⭐ Poor | Rebuild |

---

## ✅ Quality Checklists by Output Type

### Presentations

```markdown
## Pre-Delivery Checklist

### Completeness (0-10)
- [ ] All requested slides present
- [ ] Agenda matches content
- [ ] Objectives addressed
- [ ] Call to action included

### Accuracy (0-10)
- [ ] Data points verified
- [ ] Sources cited where needed
- [ ] Terminology correct
- [ ] No contradictions

### Clarity (0-10)
- [ ] One message per slide
- [ ] Titles are takeaways (not topics)
- [ ] Visuals support text
- [ ] Jargon minimized

### Format (0-10)
- [ ] Content fits slide boundaries
- [ ] Font sizes appropriate
- [ ] Consistent styling
- [ ] Print-ready (if required)

### Usability (0-10)
- [ ] Gamma-ready (if requested)
- [ ] Speaker notes included
- [ ] Timing estimates provided
- [ ] Standalone comprehensible

### Polish (0-10)
- [ ] No typos
- [ ] Alignment consistent
- [ ] Professional appearance
- [ ] Brand guidelines followed

**SCORE: ___/100**
```

---

### Documents/Reports

```markdown
## Pre-Delivery Checklist

### Completeness (0-10)
- [ ] All sections present
- [ ] Executive summary included
- [ ] Recommendations clear
- [ ] Next steps defined

### Accuracy (0-10)
- [ ] Data verified
- [ ] Calculations correct
- [ ] Citations included
- [ ] Logic sound

### Clarity (0-10)
- [ ] Structure logical
- [ ] Language appropriate for audience
- [ ] Key points highlighted
- [ ] Transitions smooth

### Format (0-10)
- [ ] Consistent formatting
- [ ] Proper headings hierarchy
- [ ] Tables/figures numbered
- [ ] Page breaks appropriate

### Usability (0-10)
- [ ] Actionable insights
- [ ] Easy to navigate
- [ ] Key info findable
- [ ] Appendix organized

### Polish (0-10)
- [ ] Grammar/spelling checked
- [ ] Consistent terminology
- [ ] Professional tone
- [ ] Clean layout

**SCORE: ___/100**
```

---

### Workshop Materials

```markdown
## Pre-Delivery Checklist

### Completeness (0-10)
- [ ] All deliverables present (slides, exercises, guide)
- [ ] Timing adds up correctly
- [ ] All exercises have answers
- [ ] Facilitator guide complete

### Accuracy (0-10)
- [ ] Content factually correct
- [ ] Examples relevant to audience
- [ ] Exercise answers verified
- [ ] Timing realistic

### Clarity (0-10)
- [ ] Instructions clear
- [ ] Learning objectives obvious
- [ ] Exercises self-explanatory
- [ ] Flow logical

### Format (0-10)
- [ ] Slides fit boundaries
- [ ] Worksheets print correctly
- [ ] Cheatsheet readable
- [ ] Consistent styling

### Usability (0-10)
- [ ] Facilitator can run without preparation
- [ ] Participants can follow exercises
- [ ] Materials standalone
- [ ] Timing annotations present

### Polish (0-10)
- [ ] No typos
- [ ] Professional appearance
- [ ] Diagrams clear
- [ ] Brand-consistent

**SCORE: ___/100**
```

---

### Data Analysis

```markdown
## Pre-Delivery Checklist

### Completeness (0-10)
- [ ] All questions answered
- [ ] Methodology explained
- [ ] Limitations acknowledged
- [ ] Recommendations included

### Accuracy (0-10)
- [ ] Data sources verified
- [ ] Calculations checked
- [ ] Statistical validity
- [ ] No correlation/causation confusion

### Clarity (0-10)
- [ ] Findings clear
- [ ] Visualizations appropriate
- [ ] Technical terms explained
- [ ] So-what evident

### Format (0-10)
- [ ] Charts properly labeled
- [ ] Axes clear
- [ ] Color-blind friendly
- [ ] Print-ready

### Usability (0-10)
- [ ] Actionable insights
- [ ] Executive summary present
- [ ] Data accessible for follow-up
- [ ] Reproducible approach

### Polish (0-10)
- [ ] Consistent number formatting
- [ ] Clean visualizations
- [ ] Professional presentation
- [ ] No chart junk

**SCORE: ___/100**
```

---

## 💬 Reporting Quality Score

### Internal Assessment (Not shown to user unless asked)

```yaml
quality_assessment:
  completeness: 9
  accuracy: 8
  clarity: 9
  format: 10
  usability: 8
  polish: 9
  total_score: 88
  rating: "⭐⭐⭐⭐ Good"
  
  notes:
    - "Minor: Could add more context in slide 4"
    - "Strength: Visualizations are excellent"
```

### User-Facing Summary (When score < 90)

```markdown
"📊 **Quality Check:** 88/100 (Good)

✅ Strengths: Clear structure, excellent visuals
⚠️ Note: Slide 4 could use more context

Want me to improve it, or is this good to go?"
```

### When Score < 70

```markdown
"🔧 **Quality Check:** 65/100 (Needs Work)

I've identified some issues:
- [ ] Missing executive summary
- [ ] Chart labels unclear
- [ ] Recommendations vague

Let me fix these before you review. Give me 5 minutes."
```

---

## 🔄 Continuous Improvement

### Track Quality Over Time

```yaml
# In agent MEMORY.md

quality_scores:
  - project: "MECE Workshop"
    output: "presentation"
    score: 88
    issues: ["initial overflow fixed"]
    
  - project: "Q4 Review"
    output: "report"  
    score: 92
    issues: []
```

### Learn from Patterns

If quality consistently drops in certain areas:
1. Identify pattern (e.g., "charts often unclear")
2. Add to agent's MEMORY as improvement focus
3. Add extra validation step for that criterion

---

## ⚡ Quick Quality Check (For Simple Outputs)

When full checklist is overkill:

```markdown
## Quick Check (5 items)

- [ ] Does it answer the user's question?
- [ ] Is it formatted correctly?
- [ ] Are there any obvious errors?
- [ ] Can the user use it immediately?
- [ ] Would I be proud to show this?

All yes → Deliver
Any no → Fix first
```

---

## 🔗 Related Protocols

- `_output-validation-protocol.md` — Detailed validation rules
- `_print-output-standards.md` — Print-specific quality
- `_confidence-scoring-protocol.md` — Confidence in findings




