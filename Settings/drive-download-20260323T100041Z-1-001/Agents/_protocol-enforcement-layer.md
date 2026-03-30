# Protocol Enforcement Layer

> **Version:** 1.0  
> **Created:** 2026-01-13  
> **Purpose:** MANDATORY checks before ANY output delivery — no exceptions

---

## 🔴 CRITICAL: This Is Not Optional

Protocols are not "reference documents." They are **mandatory gates**.

Every content-generating agent MUST pass these checks before delivery.

---

## 🚦 Enforcement Checkpoints

### Checkpoint 1: Pre-Build (Before Starting)

```
BEFORE generating any content:

□ User preferences loaded?
  → Check MEMORY for saved preferences
  → If new user, run first-time setup

□ Brand context loaded?
  → Check for brand files
  → Apply preset or ask user

□ Content density confirmed?
  → Ask if not specified in request

□ Output formats confirmed?
  → Screen / Print / Gamma / All

□ Preview offered (if complex)?
  → Slides > 5 OR pages > 3 → OFFER PREVIEW
```

### Checkpoint 2: Post-Build (Before Delivery)

```
BEFORE delivering any output:

□ Quality Score calculated?
  → Run _output-quality-score-protocol.md checklist
  → Score must be ≥ 80 to deliver
  → Score < 80 → FIX FIRST

□ Content fits boundaries?
  → No overflow
  → No text cut off
  → Footer zones protected

□ Print standards applied (if printable)?
  → @page { margin: 0 }
  → page-break-inside: avoid on tables
  → Print instructions banner included

□ Diagram semantics correct?
  → ME = shapes with gaps
  → CE = shapes fill container
  → Trees render correctly

□ Brand applied consistently?
  → Colors match preset
  → Typography consistent
  → Whitespace appropriate
```

---

## 🛑 Hard Stops (Cannot Proceed)

These MUST be fixed before delivery:

| Issue | Action |
|-------|--------|
| Quality Score < 70 | Rebuild, don't deliver |
| Content overflow | Reduce content or add pages |
| Tables break across pages | Add page-break-inside: avoid |
| Missing print instructions | Add banner |
| Diagram semantically wrong | Redesign diagram |

---

## ⚠️ Soft Warnings (Note to User)

These can be delivered with caveats:

| Issue | Message |
|-------|---------|
| Quality Score 70-79 | "Output is acceptable but could be improved. Want me to polish?" |
| Dense content | "This is more detailed than McKinsey style. Intentional?" |
| Non-standard colors | "Using custom colors that differ from your brand preset." |

---

## 📋 Per-Agent Enforcement

### @presentation-maker

```
PRE-BUILD:
✓ Brand preset loaded
✓ Content density confirmed
✓ Slide count estimated
✓ Preview offered if > 5 slides

POST-BUILD:
✓ Quality Score ≥ 80
✓ All slides fit 960x540
✓ No footer overflow
✓ Print instructions included
✓ Gamma input generated (if requested)
```

### @workshop-exercise-designer

```
PRE-BUILD:
✓ Brand preset loaded
✓ Exercise count confirmed
✓ Print format confirmed (A4/A5)

POST-BUILD:
✓ Quality Score ≥ 80
✓ Tables don't break
✓ Answer boxes adequate size
✓ Page breaks correct
✓ Print instructions included
```

### @data-visualization-expert

```
PRE-BUILD:
✓ Brand colors loaded
✓ Chart type appropriate
✓ Data validated

POST-BUILD:
✓ Quality Score ≥ 80
✓ Semantic accuracy (ME/CE correct)
✓ Print-safe colors
✓ Labels readable
✓ SVG properly formed
```

### @layout-architect

```
PRE-BUILD:
✓ Page size confirmed
✓ Orientation confirmed
✓ Content volume assessed

POST-BUILD:
✓ Quality Score ≥ 80
✓ @page { margin: 0 } applied
✓ page-break-inside: avoid applied
✓ 1:1 screen-print match
✓ Print instructions included
```

---

## 🔄 Enforcement Workflow

```
User Request
    │
    ▼
┌─────────────────────────────┐
│ CHECKPOINT 1: PRE-BUILD     │
│                             │
│ □ Preferences loaded        │
│ □ Brand loaded              │
│ □ Density confirmed         │
│ □ Formats confirmed         │
│ □ Preview offered           │
│                             │
│ ALL PASSED? → Continue      │
│ ANY FAILED? → Fix first     │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ BUILD OUTPUT                │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ CHECKPOINT 2: POST-BUILD    │
│                             │
│ □ Quality Score ≥ 80        │
│ □ Content fits              │
│ □ Print standards           │
│ □ Diagram semantics         │
│ □ Brand consistency         │
│                             │
│ ALL PASSED? → Deliver       │
│ ANY FAILED? → Fix first     │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│ DELIVER OUTPUT              │
│                             │
│ Include quality summary:    │
│ "Quality: 92/100 ⭐⭐⭐⭐⭐"   │
└─────────────────────────────┘
```

---

## 💬 Enforcement Messages

### When Checks Pass

```markdown
"✅ **Quality Check Passed** (92/100)

All standards met:
- Content fits perfectly
- Print-ready with instructions
- Brand consistent
- Diagrams accurate

Delivering your output now..."
```

### When Checks Fail

```markdown
"⚠️ **Quality Check Found Issues** (68/100)

Issues detected:
- ❌ Table on page 2 would break across pages
- ❌ Slide 7 content overflows footer zone
- ⚠️ Content density higher than your preference

**Fixing automatically...** (15 seconds)

[Or: Let me fix] [Deliver anyway with issues noted]"
```

### When Auto-Fix Applied

```markdown
"🔧 **Auto-fixed 2 issues:**
- Added page break before table
- Split slide 7 into two slides

Quality Score: 68 → 89 ✅

Ready to deliver?"
```

---

## 📊 Tracking Enforcement

Log enforcement results in agent MEMORY:

```yaml
enforcement_log:
  - date: "2026-01-13"
    output: "MECE Workshop"
    pre_build_check: passed
    post_build_check: failed_then_fixed
    initial_score: 68
    final_score: 89
    issues_found:
      - "table_break"
      - "slide_overflow"
    issues_auto_fixed: 2
    user_overrides: 0
```

Use this to:
- Identify common issues
- Improve agent defaults
- Track quality over time

---

## 🔗 Related Protocols

- `_output-quality-score-protocol.md` — Scoring criteria
- `_output-validation-protocol.md` — Validation rules
- `_print-output-standards.md` — Print-specific rules




