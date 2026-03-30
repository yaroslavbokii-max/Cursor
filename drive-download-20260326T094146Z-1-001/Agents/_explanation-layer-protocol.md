# Explanation Layer Protocol

**Version:** 1.0  
**Applies To:** All analysis agents  
**Purpose:** Make reasoning transparent and outputs understandable

---

## The Problem

Current state: Agents give answers without explaining how they got there.

**What users experience:**
- "Here's the answer" (but why?)
- "Revenue dropped because X" (how do you know?)
- "Recommendation: Do Y" (based on what logic?)

**What should happen:**
- Show the reasoning chain
- Explain key assumptions
- Highlight uncertainties
- Present alternative interpretations

---

## The Explanation Framework

### Every Analysis Output Includes:

```markdown
## [Main Finding/Recommendation]

---

### 🧠 How I Got Here

**Reasoning Chain:**
1. [First observation/data point]
2. [Logical inference from #1]
3. [Supporting evidence]
4. [Conclusion drawn]

**Key Assumptions:**
- [Assumption 1] — If wrong: [potential impact]
- [Assumption 2] — If wrong: [potential impact]

**Data Used:**
- [Data source 1]: [How it contributed]
- [Data source 2]: [How it contributed]

**What I Didn't Consider:**
- [Factor not analyzed] — Why: [reason]

---

### 🔄 Alternative Interpretations

**Other possible explanations:**
1. **[Alternative 1]** — Likelihood: [Low/Medium/High]
   - Evidence for: [supporting points]
   - Evidence against: [contradicting points]
   
2. **[Alternative 2]** — Likelihood: [Low/Medium/High]
   - Evidence for: [supporting points]
   - Evidence against: [contradicting points]

**Why I chose my interpretation:**
[Brief explanation of why primary conclusion is most supported]

---

### 🎯 Confidence Assessment

**Overall Confidence:** ⭐⭐⭐⭐ (High)

| Factor | Assessment |
|--------|------------|
| Data quality | ✅ Strong |
| Logical chain | ✅ Sound |
| Assumptions | ⚠️ 1 key assumption |
| Alternative ruled out | ✅ Yes |

**What would increase confidence:**
- [Additional data/analysis needed]
```

---

## Explanation Depth Levels

### Level 1: Quick Summary (Default for Simple Tasks)

```markdown
**Finding:** Revenue dropped 15% due to increased churn in SMB segment.

**Quick reasoning:** Churn rate doubled in SMB (from 5% to 10%), 
accounting for 80% of the revenue decline. Other segments stable.

**Confidence:** High (data is complete, pattern is clear)
```

### Level 2: Standard Explanation (Default for Analysis)

```markdown
**Finding:** Revenue dropped 15% due to increased churn in SMB segment.

**Reasoning:**
1. Analyzed revenue by segment → SMB down 25%, Enterprise flat, Mid-market +5%
2. Checked customer counts → SMB lost 200 customers (net)
3. Analyzed churn timing → Spike after pricing change in March
4. Correlated with NPS → SMB NPS dropped from 45 to 28

**Key assumption:** Pricing change is causal (correlation is strong but 
other factors not ruled out completely).

**Alternative:** Could be competitor action in SMB space. Evidence: 
2 new competitors launched in Q1. Less likely because churn started 
before competitor launches.

**Confidence:** High
```

### Level 3: Deep Explanation (For Critical Decisions)

```markdown
## Finding: Revenue dropped 15% due to increased churn in SMB segment

---

### Full Reasoning Chain

**Step 1: Initial Observation**
- Total revenue: $5M → $4.25M (-15%)
- Time period: Q1 → Q2 2026

**Step 2: Segmentation Analysis**
| Segment | Q1 Revenue | Q2 Revenue | Change |
|---------|------------|------------|--------|
| Enterprise | $2.5M | $2.5M | 0% |
| Mid-market | $1.0M | $1.05M | +5% |
| SMB | $1.5M | $1.125M | -25% |

→ SMB accounts for 100% of the decline

**Step 3: SMB Deep Dive**
- Customer count: 500 → 300 (net loss of 200)
- New customers: 50
- Churned customers: 250
- Churn rate: 5% → 50% (10x increase)

**Step 4: Timing Analysis**
- Churn spike: March 15-April 15
- Event correlation: Pricing change announced March 1, effective March 15
- Lag: Immediate churn after price increase

**Step 5: Customer Feedback**
- Exit surveys (n=150): 78% cited "price too high"
- NPS before price change: 45
- NPS after price change: 28

**Step 6: Alternative Hypotheses Tested**
| Hypothesis | Evidence For | Evidence Against | Verdict |
|------------|--------------|------------------|---------|
| Pricing | Strong (timing, surveys) | None | Most likely |
| Competitor | 2 new entrants Q1 | Churn started before launches | Unlikely primary |
| Product issues | Some support tickets | No spike in tickets | Unlikely |
| Economic conditions | SMB generally struggling | Our mid-market up | Unlikely |

---

### Assumptions & Limitations

**Key Assumptions:**
1. **Exit survey data is representative**
   - Sample: 150 of 250 churned (60%)
   - Potential bias: Most vocal customers
   - If wrong: May overstate pricing as cause
   
2. **No confounding variables**
   - Checked: seasonality, product changes, support issues
   - Not checked: individual customer circumstances
   - If wrong: Other factors could contribute

**Data Limitations:**
- No competitive pricing data (can't compare directly)
- Limited visibility into customer decision process
- SMB segment not further sub-segmented

---

### Confidence Assessment

**Overall: ⭐⭐⭐⭐ (High, not Very High)**

Why not Very High:
- Can't completely rule out competitor effect
- Exit survey has potential bias
- Didn't interview churned customers directly

What would make it Very High:
- Direct customer interviews
- Competitor pricing comparison
- Win-back experiment with original pricing

---

### Recommendation & Next Steps

**Primary Recommendation:** Reconsider SMB pricing

**Supporting Actions:**
1. Win-back campaign with discount for churned SMBs
2. Competitive pricing analysis
3. SMB customer interviews (n=20)
4. Consider tiered pricing for SMB
```

---

## When to Use Each Level

| Situation | Level | Trigger |
|-----------|-------|---------|
| Simple lookup | Skip explanation | Clear factual answer |
| Quick analysis | Level 1 | User wants speed |
| Standard analysis | Level 2 | Default for analysis |
| Strategic decision | Level 3 | High-stakes, user asks "why" |
| User challenges finding | Level 3 | Defense needed |

---

## Agent-Specific Explanation Templates

### @data-analyst

```markdown
**Analysis:** [Finding]

**Data examined:**
- [Dataset 1]: [rows, columns, time period]
- [Dataset 2]: [rows, columns, time period]

**Method used:** [Statistical method or approach]

**Key finding path:**
1. [Data observation]
2. [Pattern identified]
3. [Hypothesis formed]
4. [Validation performed]
5. [Conclusion reached]

**Statistical confidence:** [if applicable, p-value, CI]

**Limitations:**
- [What the data can't tell us]
```

### @financial-modeler

```markdown
**Projection:** [Number/Range]

**Model inputs:**
| Input | Value | Source | Sensitivity |
|-------|-------|--------|-------------|
| [Input 1] | [value] | [source] | High/Medium/Low |

**Calculation logic:**
1. [First calculation step]
2. [Second calculation step]
3. [Final calculation]

**Key driver:** [Which input matters most]

**If assumptions change:**
- [Input 1] +10% → Output [change]
- [Input 1] -10% → Output [change]
```

### @competitive-analyst

```markdown
**Assessment:** [Competitive position]

**Information sources:**
- [Source 1]: [Date, reliability]
- [Source 2]: [Date, reliability]

**Analysis method:**
1. [How competitors were identified]
2. [How data was gathered]
3. [How comparison was made]

**Confidence by competitor:**
| Competitor | Data Quality | Recency |
|------------|--------------|---------|
| [Comp 1] | High | <30 days |
| [Comp 2] | Medium | 60 days |

**What we don't know:**
- [Information gap 1]
- [Information gap 2]
```

---

## User Controls

```markdown
"Here's my analysis. How much detail would you like on my reasoning?

[📝 Summary] — Just the key points
[📊 Standard] — Reasoning + assumptions
[🔬 Full Depth] — Complete analysis chain

Your default: [Current setting]"
```

---

## Implementation Checklist

For each analysis agent:

- [ ] Add reasoning chain to outputs
- [ ] Include key assumptions
- [ ] Present alternative interpretations
- [ ] Add confidence assessment
- [ ] Support multiple depth levels
- [ ] Track explanation quality feedback

---

*"If you can't explain it, you don't understand it well enough." — Einstein (attributed)*




