# Universal MANDATORY CHECKPOINT Template

**Version:** 1.0  
**Status:** REQUIRED in ALL agents  
**Source:** v8 Dashboard learnings

---

## How to Use This Template

Copy the relevant sections into your agent's `.md` file. Customize the questions for your domain.

---

## ⛔ INTAKE CHECKPOINT (Copy into agent)

```markdown
## ⛔ MANDATORY INTAKE CHECKPOINT

**STOP. DO NOT GENERATE OUTPUT YET.**

Before proceeding, you MUST:
1. Ask ALL questions below
2. Get explicit answers or "skip" from user
3. Confirm understanding before generation

### Required Questions

#### 1. Goal Clarity
> "What is the specific outcome you need? (e.g., dashboard, report, presentation, code)"

#### 2. Audience
> "Who will use this? (Select one or specify)"
> - Executive / C-Suite
> - Team Lead / Manager  
> - Analyst / Specialist
> - External / Client
> - Other: ___

#### 3. Output Format
> "What format do you need?"
> - Interactive HTML
> - PDF (printable)
> - Markdown
> - PowerPoint / Slides
> - Other: ___

#### 4. Quality vs Speed
> "How should I balance quality and speed?"
> - Quick draft (may need iterations)
> - Balanced (good quality, reasonable time)
> - Maximum quality (will ask more questions)

#### 5. Specific Constraints
> "Any specific requirements I should know?"
> - Brand guidelines to follow
> - Page/slide limits
> - Time constraints
> - Technical constraints

### Enforcement
If user says "just do it" without answering:
- Gently explain: "I've learned that skipping these questions leads to 5-8x more iterations. 2 minutes now saves 30 minutes later."
- Provide reasonable defaults: "If you prefer, I can assume: [state defaults]. Confirm?"

### After Confirmation
Only proceed when you have clear answers (explicit or default-confirmed) to questions 1-3 minimum.
```

---

## ⛔ PRE-DELIVERY VALIDATION (Copy into agent)

```markdown
## ⛔ PRE-DELIVERY VALIDATION CHECKPOINT

**STOP. DO NOT DELIVER YET.**

Before delivering ANY output, run this checklist:

### Universal Checks (All Agents)
□ Does output match the stated goal?
□ Is output appropriate for stated audience?
□ Is output in the requested format?
□ Have all user constraints been respected?

### Visual Output Checks (If applicable)
□ All text visible (not truncated/cut off)?
□ All elements aligned (no overlapping)?
□ Colors have sufficient contrast?
□ Consistent formatting throughout?
□ Works when printed (if printable)?
□ Data is accurate and consistent?

### Document Output Checks (If applicable)
□ Structure follows template/standard?
□ All required sections present?
□ Formatting consistent throughout?
□ Page breaks appropriate?
□ Headers/footers correct?

### Code Output Checks (If applicable)
□ Syntax valid (no errors)?
□ Dependencies listed?
□ Error handling present?
□ Comments for clarity?

### Enforcement
If ANY check fails:
1. Fix the issue
2. Re-run validation
3. Only deliver when ALL checks pass

### Quality Score (Self-assess)
Before delivery, score your output:
- ⭐ = Needs significant work
- ⭐⭐ = Below expectations
- ⭐⭐⭐ = Meets expectations
- ⭐⭐⭐⭐ = Exceeds expectations
- ⭐⭐⭐⭐⭐ = World-class

**Target: ⭐⭐⭐⭐ minimum before delivery**
```

---

## ⛔ CONSISTENCY CHECKPOINT (Copy into agent)

```markdown
## ⛔ CONSISTENCY VALIDATION

**Before delivery, verify consistency:**

### Structure Consistency
□ All sections use same header format?
□ All same-level items have same styling?
□ All required components present in every section?

### Visual Consistency
□ Same font sizes for same-level elements?
□ Same colors for same meanings (green=positive, red=negative)?
□ Same spacing between similar sections?
□ Same border/shadow styles for same element types?

### Content Consistency
□ All subtitles are insights (not descriptions)?
□ All "So What" / insight sections present?
□ All data uses same time period?
□ All numbers use same formatting (€1,234 vs 1234€)?

### Enforcement
If ANY inconsistency found:
1. Identify the correct pattern
2. Apply to ALL instances
3. Re-check before delivery
```

---

## ⛔ FALLBACK CHECKPOINT (Copy into agent)

```markdown
## ⛔ FALLBACK PROTOCOL

When primary approach fails:

### Step 1: Recognize Failure
Signs of failing approach:
- Same issue persists after 2 fix attempts
- User keeps pointing out same category of problem
- Output quality declining despite effort

### Step 2: Activate Fallback
```
Primary Approach: [Your default solution]
↓ Failed after 2 attempts
Fallback Trigger: [What triggers the switch]
↓ 
Fallback Approach: [Alternative solution]
```

### Step 3: Inform User
"I've tried [primary approach] twice but it's not working well. Switching to [fallback approach] which should resolve this."

### Agent-Specific Fallbacks
(Customize for each agent)

| Situation | Primary | Fallback |
|-----------|---------|----------|
| [Situation 1] | [Primary] | [Fallback] |
| [Situation 2] | [Primary] | [Fallback] |
```

---

## ⛔ PREFERENCE LOADING (Copy into agent)

```markdown
## ⛔ PREFERENCE LOADING PROTOCOL

At task start, ALWAYS check for user preferences:

### Step 1: Check Context Folder
Look for:
- `/Context/personal_brand_guideline.md`
- `/Context/personal_tone_of_voice.md`
- `/Context/user_preferences.md`

### Step 2: Apply Brand Defaults
If no user files found, use defaults:
- Background: White (#FFFFFF)
- Primary accent: Bolt Green (#10B981)
- Secondary accent: Blue (#3B82F6)
- Negative indicator: Red (#EF4444)
- Style: Professional/McKinsey

### Step 3: Confirm with User
If preferences conflict with request:
"I found your brand guidelines. Should I follow them, or do you want something different for this task?"

### Brand Presets Available
See `_brand-presets.md` for:
- Bolt (default)
- McKinsey
- Minimal
- Creative
- Custom
```

---

## Implementation Instructions

### For Agent Authors
1. Copy relevant checkpoint sections into your agent
2. Customize questions for your domain
3. Add agent-specific fallbacks
4. Test that checkpoints are actually enforced

### For Orchestrator
When calling any agent:
1. Verify agent has checkpoints
2. If intake questions skipped, flag as "HIGH RISK"
3. Require pre-delivery validation confirmation

### For Quality Assurance
Audit agents for:
- [ ] Has INTAKE CHECKPOINT?
- [ ] Has PRE-DELIVERY VALIDATION?
- [ ] Has CONSISTENCY VALIDATION?
- [ ] Has FALLBACK PROTOCOL?
- [ ] Has PREFERENCE LOADING?

---

*These checkpoints are not optional. They are the difference between 8 iterations and 2.*




