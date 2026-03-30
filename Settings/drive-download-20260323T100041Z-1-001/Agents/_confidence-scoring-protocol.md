# Confidence Scoring Protocol

**Version:** 1.0  
**Applies To:** All Agents  
**Purpose:** Add uncertainty awareness and quality signals to all outputs

---

## Overview

Every agent output should include a confidence indicator. This helps users understand:
- How reliable the output is
- What assumptions were made
- Where to apply skepticism
- When to seek additional validation

---

## The Confidence Score Framework

### Score Levels

| Score | Label | Meaning | User Action |
|-------|-------|---------|-------------|
| ⭐⭐⭐⭐⭐ | **Very High** | Based on direct data/facts, no significant assumptions | Trust and use |
| ⭐⭐⭐⭐ | **High** | Strong evidence, minor assumptions | Use with light review |
| ⭐⭐⭐ | **Medium** | Reasonable inference, moderate assumptions | Review before using |
| ⭐⭐ | **Low** | Limited data, significant assumptions | Validate independently |
| ⭐ | **Very Low** | Speculative, best guess | Treat as hypothesis only |

---

## When to Apply Scores

### Always Score These Outputs

| Output Type | Example | Why Score It |
|-------------|---------|--------------|
| **Data insights** | "Revenue dropped due to X" | Causation claims need validation |
| **Recommendations** | "You should do Y" | Actions have consequences |
| **Projections** | "Revenue will be $X in Q3" | Future is uncertain |
| **Comparisons** | "Option A is better than B" | Subjective judgment involved |
| **Code** | Generated functions | May have edge cases |

### Don't Need Scores

- Factual lookups (definitions, formulas)
- Template outputs (no judgment involved)
- Procedural instructions (step-by-step guides)

---

## Confidence Score Components

### What Affects Confidence

| Factor | Increases ⬆️ | Decreases ⬇️ |
|--------|--------------|--------------|
| **Data quality** | Complete, recent, verified | Missing, old, unverified |
| **Assumptions** | Few, explicit, reasonable | Many, implicit, uncertain |
| **Validation** | Cross-checked, consistent | Single source, contradictions |
| **Expertise match** | Within agent's domain | Outside core capability |
| **Complexity** | Simple, deterministic | Complex, many variables |

### Score Calculation

```
Base Score = 5 (start high, deduct for issues)

Deductions:
- Missing data: -1 per major gap
- Strong assumptions: -1 per assumption
- Limited validation: -1
- Out of domain: -1
- High complexity without validation: -1

Final Score = max(1, Base Score - Deductions)
```

---

## Output Format

### Standard Confidence Block

```markdown
---
**🎯 Confidence Score: ⭐⭐⭐⭐ (High)**

| Factor | Assessment |
|--------|------------|
| Data quality | ✅ Complete, recent data |
| Assumptions | ⚠️ 1 assumption: [description] |
| Validation | ✅ Cross-checked with [source] |

**What could change this:** [Key uncertainty]
---
```

### Compact Format (for inline use)

```markdown
*Confidence: ⭐⭐⭐⭐ (High) — based on complete data, 1 assumption about [X]*
```

### Detailed Format (for critical outputs)

```markdown
## 🎯 Confidence Assessment

**Overall Score: ⭐⭐⭐ (Medium)**

### Score Breakdown

| Component | Score | Notes |
|-----------|-------|-------|
| Data completeness | 4/5 | Missing Q4 data |
| Assumption count | 3/5 | 2 significant assumptions |
| Validation level | 3/5 | Single source |
| Domain match | 5/5 | Core capability |
| Complexity handling | 3/5 | Multiple variables |

### Key Assumptions
1. **[Assumption 1]** — If wrong: [impact]
2. **[Assumption 2]** — If wrong: [impact]

### What Would Increase Confidence
- [ ] Get Q4 data
- [ ] Validate with [second source]
- [ ] Test assumption 1 with [method]

### Recommendation
Given medium confidence, I suggest:
- Using this as a starting point
- Validating [specific aspect] before acting
- Revisiting if [trigger condition]
```

---

## Agent-Specific Guidelines

### @data-analyst
```markdown
Score based on:
- Data quality and completeness
- Statistical significance (if applicable)
- Causation vs. correlation clarity
- Alternative hypotheses ruled out
```

### @presentation-maker
```markdown
Score based on:
- Source material reliability
- Logical flow strength
- Audience fit assessment
- Visual recommendations' appropriateness
```

### @web-scraper-ninja
```markdown
Score based on:
- Data freshness
- Extraction accuracy
- Site structure stability
- Anti-detection success
```

### @financial-modeler
```markdown
Score based on:
- Input assumption reliability
- Benchmark alignment
- Model logic soundness
- Scenario coverage
```

### @competitive-analyst
```markdown
Score based on:
- Data recency
- Source diversity
- Inference quality
- Market dynamics stability
```

---

## User Communication

### When Score is High (⭐⭐⭐⭐-⭐⭐⭐⭐⭐)

```markdown
"I'm confident in this output. It's based on [good data/solid evidence].
The main thing to note is [any caveat]."
```

### When Score is Medium (⭐⭐⭐)

```markdown
"This is my best assessment based on available information.
I'd recommend validating [specific aspect] before acting.
Key assumption: [what I assumed and why]."
```

### When Score is Low (⭐-⭐⭐)

```markdown
"⚠️ Treat this as a hypothesis, not a conclusion.
I have limited data on [gap] and assumed [assumptions].
Before using this, I'd suggest:
1. [Validation step 1]
2. [Validation step 2]"
```

---

## Implementation Checklist

For each agent, add to the output generation section:

- [ ] Calculate confidence score using framework
- [ ] Include confidence block in output
- [ ] List key assumptions explicitly
- [ ] Suggest validation steps for lower scores
- [ ] Flag when output is outside core capability

---

## Examples

### High Confidence Example
```markdown
## Analysis: Q3 Revenue Drop

**Finding:** Revenue dropped 15% due to increased churn in the SMB segment.

**🎯 Confidence: ⭐⭐⭐⭐⭐ (Very High)**
- ✅ Complete data for all segments
- ✅ Causation verified (SMB churn rate doubled)
- ✅ Alternative causes ruled out (pricing, seasonality)
```

### Medium Confidence Example
```markdown
## Recommendation: Enter European Market

**Recommendation:** Expand to Germany first, then France.

**🎯 Confidence: ⭐⭐⭐ (Medium)**
- ✅ Market size data is solid
- ⚠️ Assumption: Regulatory environment won't change significantly
- ⚠️ Limited competitive intel in France
- Suggest: Validate French competitive landscape before final decision
```

### Low Confidence Example
```markdown
## Projection: 2027 Revenue

**Projection:** $50M ARR by 2027

**🎯 Confidence: ⭐⭐ (Low)**
- ⚠️ 3-year forecast with multiple assumptions
- ⚠️ Assumes market growth continues at current rate
- ⚠️ Assumes no major competitive disruption
- ⚠️ Assumes successful product launches

**Use as:** Directional guidance only. Revisit quarterly.
```

---

*"Uncertainty acknowledged is better than false certainty." — This protocol ensures we're honest about what we know and don't know.*




