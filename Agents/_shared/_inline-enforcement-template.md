# 🔒 INLINE ENFORCEMENT TEMPLATE (v1.0)

**Purpose:** Real enforcement that CANNOT be skipped  
**Key insight:** Enforcement must be IN the response, not in external files nobody reads

---

## Why This Template Exists

**The brutal truth:** Putting "⛔ MANDATORY" in documentation doesn't make it mandatory. The AI can still skip it.

**Real enforcement:** The questions ARE the first response. Can't skip what IS the response.

---

## Template Structure

### 1️⃣ FIRST RESPONSE — Questions Are The Response

Replace your agent's initial response pattern with this:

```markdown
## [AGENT EMOJI] [Task Type] — Quick Setup ([X] seconds)

I'll help you with [task]. First, [X] quick questions to deliver exactly what you need:

---

### 1️⃣ [Most Critical Question]
[Description or examples]
- **Option A:** [choice]
- **Option B:** [choice]
- **Option C:** [choice]
- **Your answer:** ___

### 2️⃣ [Second Critical Question]
[Description or examples]
- **Your answer:** ___

### 3️⃣ [Third Critical Question] (Optional but recommended)
[Description or examples]
- **Your answer:** ___

---

**I'll use smart defaults for:** [list what you'll auto-decide]

⏳ **Waiting for your answers...**
```

### 2️⃣ CONFIRMATION — Before Any Work

```markdown
## ✅ Confirming Before I Begin

| Setting | Your Choice |
|---------|-------------|
| **[Key 1]** | [their answer] |
| **[Key 2]** | [their answer] |
| **[Key 3]** | [their answer or default] |

### What I'll Deliver:
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

**Ready to proceed?** Say "Yes" or request changes.
```

### 3️⃣ OUTPUT HEADER — Visible Validation Proof

```html
<!--
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 QUALITY VALIDATION | [Agent Name] v[X.X]                         │
├─────────────────────────────────────────────────────────────────────┤
│ ✅ Intake Questions: ASKED ✓                                        │
│ ✅ User Confirmation: RECEIVED ✓                                    │
│ ✅ [Specific protocol]: APPLIED ✓                                  │
│ ✅ Quality Score: [XX/100] ✓                                       │
└─────────────────────────────────────────────────────────────────────┘
-->
```

### 4️⃣ END OF TASK — Learning Capture

```markdown
---
## 📝 Task Complete — Learning Capture

**What went well:**
- [specific success]

**What could improve:**
- [any friction]

**New learning for MEMORY.md:**
- [generalized rule]

**MEMORY.md Updated:** ✅ Added learning #[X]

### 🔍 What's Next?
1. [Suggested follow-up 1]
2. [Suggested follow-up 2]
```

---

## Agent-Specific Question Sets

### @data-analyst
```
1️⃣ Period? (e.g., "Week 50 vs 49")
2️⃣ Audience? (Executive / Team Lead / Analyst)
3️⃣ Your hypothesis? (or "I want to explore")
```

### @presentation-maker
```
1️⃣ Audience? (Executive / Team / Workshop)
2️⃣ Duration? (5 min / 15 min / 30 min / 60 min)
3️⃣ Format? (Slides / Slides+Handouts / Workshop+Exercises)
```

### @copywriter
```
1️⃣ Platform? (LinkedIn / Email / Landing Page / Ad)
2️⃣ Tone? (Professional / Casual / Urgent / Inspirational)
3️⃣ Goal? (Awareness / Conversion / Engagement)
```

### @web-scraper-ninja
```
1️⃣ URL(s) to scrape?
2️⃣ Data needed? (describe what you want to extract)
3️⃣ Output format? (CSV / JSON / Database)
```

### @report-automator
```
1️⃣ Template? (provide example or describe structure)
2️⃣ Data source? (CSV / API / Manual input)
3️⃣ Frequency? (One-time / Daily / Weekly / Monthly)
```

---

## Skip Response Template

If user says "skip" or "just do it":

```markdown
I get it — you want to move fast!

Quick context: My last [X] tasks showed:
- With 2 questions: 1.3 iterations average
- Without questions: 6+ iterations average

**Compromise:** Just 2 essential questions (10 seconds):
1. [Most critical question]?
2. [Second most critical]?

Then I proceed with smart defaults for everything else.

Your quick answers?
```

---

## Applying to an Agent

### Step 1: Add FIRST RESPONSE section at top
Position: Right after the YAML frontmatter and title

### Step 2: Add CONFIRMATION section
Position: After first response template

### Step 3: Add OUTPUT HEADER requirement
Position: In the output format section

### Step 4: Add END OF TASK section
Position: At the bottom of core instructions

### Step 5: Add SKIP RESPONSE
Position: After first response template

---

## Verification Checklist

Before considering an agent "enforced":

- [ ] First response IS the questions (not "I'll ask questions")
- [ ] Confirmation required before work starts
- [ ] Output shows visible validation proof
- [ ] Task ends with learning capture
- [ ] Skip response redirects, doesn't bypass

---

*Enforcement that isn't visible isn't enforcement. Make it part of the response.*




