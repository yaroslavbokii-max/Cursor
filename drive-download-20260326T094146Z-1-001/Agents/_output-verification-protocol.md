# Output Verification Protocol

**Version:** 1.0  
**Applies To:** All agents that generate outputs (code, visualizations, documents)  
**Purpose:** Verify outputs work before delivering to user

---

## The Problem

Current state: Agents generate outputs but don't verify they work.

**What goes wrong:**
- Generated code has syntax errors
- Charts don't render correctly
- Documents have broken formatting
- Users get frustrated with broken outputs

**What should happen:**
- Generate output
- Verify it works (parse, compile, render)
- Fix any issues automatically
- Only deliver verified output

---

## Verification Flow

```
AGENT GENERATES OUTPUT
          │
          ▼
┌─────────────────────────────────────┐
│  STEP 1: SYNTAX VERIFICATION        │
│  ├── Code: Does it parse?           │
│  ├── JSON: Is it valid?             │
│  ├── HTML: Is it well-formed?       │
│  └── Markdown: Is it renderable?    │
└─────────────────────────────────────┘
          │
          ├── FAIL ──→ Auto-fix syntax
          │
          ▼
┌─────────────────────────────────────┐
│  STEP 2: SEMANTIC VERIFICATION      │
│  ├── Code: Does logic make sense?   │
│  ├── Data: Are values reasonable?   │
│  ├── References: Do links work?     │
│  └── Dependencies: Are they available│
└─────────────────────────────────────┘
          │
          ├── FAIL ──→ Flag for review
          │
          ▼
┌─────────────────────────────────────┐
│  STEP 3: EXECUTION VERIFICATION     │
│  ├── Code: Does it run?             │
│  ├── Charts: Do they render?        │
│  ├── Workflows: Do they execute?    │
│  └── Documents: Do they display?    │
└─────────────────────────────────────┘
          │
          ├── FAIL ──→ Debug and retry
          │
          ▼
┌─────────────────────────────────────┐
│  STEP 4: OUTPUT QUALITY CHECK       │
│  ├── Does output match requirements?│
│  ├── Is format correct?             │
│  ├── Are all sections complete?     │
│  └── Quality score acceptable?      │
└─────────────────────────────────────┘
          │
          ▼
      DELIVER TO USER
      (with verification badge)
```

---

## Verification by Output Type

### Code Verification

```markdown
## Code Verification Report

**Language:** Python | JavaScript | TypeScript | SQL
**Lines:** [count]

### Syntax Check
| Check | Status |
|-------|--------|
| Parses without errors | ✅/❌ |
| No syntax warnings | ✅/❌ |
| Imports resolve | ✅/❌ |

### Semantic Check
| Check | Status |
|-------|--------|
| No undefined variables | ✅/❌ |
| Type consistency | ✅/❌ |
| No obvious logic errors | ✅/❌ |

### Execution Check
| Check | Status |
|-------|--------|
| Runs with sample data | ✅/❌ |
| Produces expected output | ✅/❌ |
| No runtime errors | ✅/❌ |

### Security Check
| Check | Status |
|-------|--------|
| No hardcoded secrets | ✅/❌ |
| Input validation present | ✅/❌ |
| No obvious vulnerabilities | ✅/❌ |

**Verification Badge:** 🔒 VERIFIED ✅
```

### Chart/Visualization Verification

```markdown
## Visualization Verification Report

**Type:** Bar | Line | Scatter | Pie | etc.
**Library:** Plotly | Chart.js | Matplotlib

### Syntax Check
| Check | Status |
|-------|--------|
| Valid chart configuration | ✅/❌ |
| Data format correct | ✅/❌ |
| All required fields present | ✅/❌ |

### Render Check
| Check | Status |
|-------|--------|
| Chart renders without errors | ✅/❌ |
| All data points visible | ✅/❌ |
| Labels display correctly | ✅/❌ |
| Legend present and accurate | ✅/❌ |

### Accessibility Check
| Check | Status |
|-------|--------|
| Color contrast sufficient | ✅/❌ |
| Alt text provided | ✅/❌ |
| Not color-only encoding | ✅/❌ |

**Verification Badge:** 📊 VERIFIED ✅
```

### HTML/Document Verification

```markdown
## Document Verification Report

**Type:** HTML | Markdown | PDF
**Sections:** [count]

### Structure Check
| Check | Status |
|-------|--------|
| Valid markup | ✅/❌ |
| All sections present | ✅/❌ |
| Headings hierarchy correct | ✅/❌ |

### Content Check
| Check | Status |
|-------|--------|
| No placeholder text | ✅/❌ |
| Links functional | ✅/❌ |
| Images accessible | ✅/❌ |

### Display Check
| Check | Status |
|-------|--------|
| Renders correctly | ✅/❌ |
| Mobile-friendly | ✅/❌ |
| Print-safe | ✅/❌ |

**Verification Badge:** 📄 VERIFIED ✅
```

### Workflow Verification (@n8n-workflow-architect)

```markdown
## Workflow Verification Report

**Name:** [workflow name]
**Nodes:** [count]

### Structure Check
| Check | Status |
|-------|--------|
| All nodes connected | ✅/❌ |
| Start node present | ✅/❌ |
| No orphan nodes | ✅/❌ |

### Configuration Check
| Check | Status |
|-------|--------|
| All required fields set | ✅/❌ |
| Credentials configured | ✅/❌ |
| Error handling present | ✅/❌ |

### Execution Check
| Check | Status |
|-------|--------|
| Dry run successful | ✅/❌ |
| Sample data processes | ✅/❌ |
| Output matches expected | ✅/❌ |

**Verification Badge:** ⚙️ VERIFIED ✅
```

---

## Auto-Fix Capabilities

### Syntax Errors

```markdown
IF syntax_error DETECTED:
  1. Identify error location
  2. Determine fix type:
     - Missing bracket → Add bracket
     - Typo in keyword → Correct spelling
     - Missing import → Add import
     - Indentation error → Fix indentation
  3. Apply fix
  4. Re-verify
  5. If still failing → Ask for human help
```

### Common Fixes

| Error Type | Auto-Fix |
|------------|----------|
| Missing semicolon | Add semicolon |
| Unclosed bracket | Close bracket |
| Undefined variable | Add declaration or import |
| Type mismatch | Add type conversion |
| Missing comma in JSON | Add comma |
| Invalid escape sequence | Fix escape |

### When Auto-Fix Fails

```markdown
"⚠️ I couldn't automatically fix this issue:

**Error:** [description]
**Location:** [file:line]
**Attempted fix:** [what was tried]

**Options:**
A) I'll explain the issue so you can fix it
B) Let me try a different approach
C) Skip this part and continue
```

---

## Verification Badges

### Badge Types

| Badge | Meaning |
|-------|---------|
| 🔒 VERIFIED ✅ | All checks passed |
| ⚠️ VERIFIED WITH NOTES | Passed with minor issues |
| 🔧 MANUALLY VERIFIED | User confirmed it works |
| ❌ UNVERIFIED | Could not verify (proceed with caution) |

### Badge Display

```markdown
---
## Output: [Title]

**🔒 Verification Status: VERIFIED ✅**

Checks passed:
- ✅ Syntax valid
- ✅ Executes successfully
- ✅ Output matches requirements

---

[Actual output content]
```

---

## Agent-Specific Verification

### @code-generator

```markdown
BEFORE delivering code:
1. Parse all files for syntax errors
2. Check imports are valid
3. Run with sample data
4. Generate verification report
5. Include in delivery
```

### @data-visualization-expert

```markdown
BEFORE delivering charts:
1. Validate chart config JSON
2. Check data binding
3. Render in headless browser (conceptually)
4. Check accessibility
5. Include verification badge
```

### @presentation-maker

```markdown
BEFORE delivering slides:
1. Validate HTML structure
2. Check all slides render
3. Verify no broken images
4. Check print layout
5. Include verification badge
```

### @n8n-workflow-architect

```markdown
BEFORE delivering workflow:
1. Validate workflow JSON
2. Check all nodes configured
3. Verify connections valid
4. Run validation endpoint
5. Include verification badge
```

---

## Metrics to Track

| Metric | Target |
|--------|--------|
| First-time verification pass rate | >90% |
| Auto-fix success rate | >80% |
| User-reported failures post-verification | <5% |
| Average verification time | <5 seconds |

---

## Implementation Checklist

For each generation agent:

- [ ] Add syntax verification step
- [ ] Add semantic verification step
- [ ] Implement auto-fix for common issues
- [ ] Add verification badge to output
- [ ] Log verification results in MEMORY.md
- [ ] Track verification metrics

---

*"Test it before you ship it. Every time."*




