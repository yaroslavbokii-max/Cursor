# Output Quality Scoring System

**Version:** 1.0  
**Status:** MANDATORY for all output-generating agents  
**Source:** v8 Dashboard learnings — quality gates prevent rework

---

## 🎯 Purpose

Every output must be scored BEFORE delivery. This ensures:
1. Quality is quantified, not subjective
2. Minimum standards are enforced
3. Users get consistently high-quality outputs
4. Poor outputs are improved before delivery

---

## 📊 Universal Quality Rubric

### Score Range
- **5/5 (100%)** — World-class, could win awards
- **4/5 (80%)** — Excellent, ready for executive presentation
- **3/5 (60%)** — Good, meets basic requirements
- **2/5 (40%)** — Below expectations, needs improvement
- **1/5 (20%)** — Unacceptable, major rework needed

### Minimum Score to Deliver
- **Standard outputs:** 80% (4/5 average)
- **Executive-facing:** 90% (4.5/5 average)
- **External/client-facing:** 95% (4.75/5 average)

---

## 📋 Scoring Categories

### 1. Goal Achievement (Weight: 30%)

| Score | Criteria |
|-------|----------|
| 5 | Exceeds stated goal, includes valuable extras |
| 4 | Fully achieves stated goal |
| 3 | Achieves most of the goal |
| 2 | Partially achieves goal, missing key elements |
| 1 | Does not achieve stated goal |

**Questions to ask:**
- Does this output answer the user's question?
- Does it solve the user's problem?
- Does it provide what was requested?

### 2. Audience Appropriateness (Weight: 20%)

| Score | Criteria |
|-------|----------|
| 5 | Perfectly tailored, anticipates audience needs |
| 4 | Well-suited to audience |
| 3 | Generally appropriate |
| 2 | Partially appropriate, some mismatches |
| 1 | Wrong for audience |

**Questions to ask:**
- Is the detail level right for the audience?
- Is the language appropriate?
- Is the format what they expect?

### 3. Visual Quality (Weight: 20%)

| Score | Criteria |
|-------|----------|
| 5 | Award-winning design, perfect execution |
| 4 | Professional, polished |
| 3 | Clean, acceptable |
| 2 | Minor visual issues |
| 1 | Poor visual quality, formatting issues |

**Questions to ask:**
- Is formatting consistent?
- Are all elements aligned?
- Is there sufficient contrast?
- Would this pass the "conference room test"?

### 4. Accuracy & Consistency (Weight: 20%)

| Score | Criteria |
|-------|----------|
| 5 | 100% accurate, internally consistent |
| 4 | Accurate, consistent |
| 3 | Minor inconsistencies, no errors |
| 2 | Some errors or inconsistencies |
| 1 | Significant errors |

**Questions to ask:**
- Do all numbers add up correctly?
- Are time periods consistent?
- Are terms used consistently?

### 5. Actionability (Weight: 10%)

| Score | Criteria |
|-------|----------|
| 5 | Clear next steps, ready to act |
| 4 | Actionable insights |
| 3 | Some actionable elements |
| 2 | Limited actionability |
| 1 | Not actionable |

**Questions to ask:**
- Does it include "so what" interpretations?
- Are recommendations clear?
- Can the user take action based on this?

---

## 🧮 Score Calculation

### Formula

```
Total Score = (Goal × 0.30) + (Audience × 0.20) + (Visual × 0.20) + (Accuracy × 0.20) + (Action × 0.10)
```

### Example Calculation

```
Goal Achievement:    4/5 × 0.30 = 1.20
Audience:            5/5 × 0.20 = 1.00
Visual Quality:      4/5 × 0.20 = 0.80
Accuracy:            4/5 × 0.20 = 0.80
Actionability:       4/5 × 0.10 = 0.40
─────────────────────────────────────
TOTAL:               4.20/5 = 84%
```

---

## 📊 Agent-Specific Scoring

### @data-analyst

**Additional criteria:**
- Data profiling completed?
- Multiple hypotheses tested?
- Breakdowns included?
- Devil's advocate section?
- Charts follow universal rules?

### @presentation-maker

**Additional criteria:**
- One message per slide?
- Content within density limits?
- Print-ready?
- Gamma-compatible?

### @data-visualization-expert

**Additional criteria:**
- Chart type appropriate for data?
- All universal chart rules followed?
- Code validated and runnable?
- Accessibility (WCAG) compliant?

### @layout-architect

**Additional criteria:**
- No page break issues?
- No element overlap?
- Print preview matches output?
- Margins appropriate for binding?

### @copywriter

**Additional criteria:**
- Tone matches brand voice?
- Within word count?
- Clear CTA?
- SEO considerations (if applicable)?

---

## 📝 Quality Score Template

Include this in every output delivery:

```markdown
## 📊 Quality Score Report

**Output:** [Description]
**Generated:** [Date/Time]
**Agent:** [Agent name/version]

### Scores

| Category | Score | Notes |
|----------|-------|-------|
| Goal Achievement | _/5 | [Brief note] |
| Audience Appropriateness | _/5 | [Brief note] |
| Visual Quality | _/5 | [Brief note] |
| Accuracy & Consistency | _/5 | [Brief note] |
| Actionability | _/5 | [Brief note] |

### Total Score: **__%**

### Quality Gate
- [x] Minimum score met (≥80%)
- [x] No critical issues
- [x] Pre-delivery validation passed

### Known Limitations
- [List any known issues or limitations]

### Recommendations for Improvement
- [If score < 90%, list what could improve it]
```

---

## 🚦 Quality Gates

### Gate 1: Pre-Generation
Before generating:
- [ ] Intake questions answered
- [ ] Requirements clear
- [ ] Context loaded

### Gate 2: Mid-Generation
During generation:
- [ ] Following protocols
- [ ] Consistent formatting
- [ ] No obvious errors

### Gate 3: Pre-Delivery
Before delivering:
- [ ] Quality score calculated
- [ ] Score meets minimum
- [ ] Validation checklist passed
- [ ] No critical issues

### Gate 4: Post-Delivery
After delivery:
- [ ] User feedback captured
- [ ] MEMORY updated
- [ ] Issues logged for improvement

---

## 📈 Score Tracking

### Per-Agent Metrics

Track over time:
- Average quality score
- Score trend (improving/declining)
- Common failure points
- User feedback correlation

### Cross-Agent Metrics

Compare:
- Which agents score highest
- Common issues across agents
- Impact of v8 learnings

### Dashboard

The `_agent-health-dashboard.html` includes quality score tracking.

---

## 🔄 Continuous Improvement

When score < target:

1. **Identify lowest category**
2. **Review related protocols**
3. **Check MEMORY for similar issues**
4. **Apply fixes**
5. **Re-score**
6. **Document learning**

---

## 📚 Related Documents

- `_v8-learnings-protocol.md` — Learnings that improve scores
- `_mandatory-checkpoint-template.md` — Ensures quality at each gate
- `_agent-health-dashboard.html` — Tracks scores over time
- Individual agent MEMORY.md files

---

*Every output should be scored. No exceptions.*




