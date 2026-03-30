# 🚫 Blocking Validation Protocol v1.0

## Purpose
**VALIDATION MUST PASS BEFORE DELIVERY.** No exceptions.

This protocol ensures that outputs with critical errors are NEVER delivered to users.

---

## 🔴 Enforcement Rules

### Rule 1: Validation Runs Automatically
Every HTML output MUST include the validation block from `_output-validation-block.html`.
Validation runs on page load — no user action required.

### Rule 2: Critical Errors Block Delivery
If validation detects ANY critical error:
- Output is marked as **FAILED**
- User sees error panel with fix instructions
- "Acknowledge" button is **DISABLED** until errors fixed
- Agent must fix errors before redelivering

### Rule 3: Warnings Allow Delivery With Acknowledgment
If only warnings (no critical errors):
- Output is marked as **WARNING**
- User can acknowledge and proceed
- Warnings are logged to MEMORY.md

### Rule 4: Agent Self-Check Before Delivery
Before generating ANY output, agent must mentally verify:
```
□ Does output have @page { margin: 0 }?
□ Does output have page-break-after on pages/slides?
□ Does output have page-break-inside: avoid on tables/cards?
□ Does output have print-color-adjust: exact?
□ Is content within density limits?
□ Are all images accessible (alt text)?
□ Is data internally consistent?
```

---

## 📋 Validation Categories

### 🔴 CRITICAL (Blocks Delivery)

| Check | What It Catches | Auto-Fix Available? |
|-------|-----------------|---------------------|
| Missing `@page { margin: 0 }` | Browser adds headers/footers | Yes |
| Missing `page-break-after` | Pages merge when printing | Yes |
| Data inconsistency | Percentages ≠ 100%, parts ≠ total | No |
| Overflow visible on slides | Content bleeds outside | Yes |
| Chart axis not from zero | Misleading visualization | No |

### 🟡 HIGH WARNING (Should Fix)

| Check | What It Catches | Auto-Fix Available? |
|-------|-----------------|---------------------|
| Missing `page-break-inside: avoid` | Tables break across pages | Yes |
| Content over density limit | Too many words per slide | No |
| Chart labels overlap | Unreadable visualization | No |
| Missing baseline reference | Chart lacks context | No |

### 🟠 MEDIUM WARNING (Nice to Fix)

| Check | What It Catches | Auto-Fix Available? |
|-------|-----------------|---------------------|
| Missing `print-color-adjust` | Backgrounds may not print | Yes |
| Images without alt text | Accessibility issue | No |
| Non-round axis labels | Visual clutter | Yes |
| Low color contrast | Readability issue | No |

---

## 🔧 Auto-Fix Capability

For fixable issues, the validation system can automatically apply corrections:

```javascript
const autoFixes = {
    'missing-page-margin': {
        description: 'Add @page { margin: 0 }',
        fix: () => {
            const style = document.createElement('style');
            style.textContent = '@media print { @page { margin: 0 !important; } }';
            document.head.appendChild(style);
        }
    },
    'missing-page-break': {
        description: 'Add page-break-after to pages/slides',
        fix: () => {
            document.querySelectorAll('.page, .slide').forEach(el => {
                el.style.pageBreakAfter = 'always';
            });
        }
    },
    'missing-print-color': {
        description: 'Add print-color-adjust',
        fix: () => {
            const style = document.createElement('style');
            style.textContent = '* { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }';
            document.head.appendChild(style);
        }
    }
};
```

---

## 📊 Validation Panel UI

### Failed State (Critical Errors)
```
╔══════════════════════════════════════════════════════════════════╗
║ ❌ VALIDATION FAILED — Cannot deliver until errors are fixed     ║
╠══════════════════════════════════════════════════════════════════╣
║ 🔴 CRITICAL: Missing @page { margin: 0 }                        ║
║    → Browser will add headers/footers when printing              ║
║    [Auto-Fix Available] [Show Details]                           ║
╠══════════════════════════════════════════════════════════════════╣
║ [Apply Auto-Fixes]  [Show All Issues]  [Acknowledge] (disabled)  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Warning State (No Critical Errors)
```
╔══════════════════════════════════════════════════════════════════╗
║ ⚠️ VALIDATION PASSED WITH WARNINGS                               ║
╠══════════════════════════════════════════════════════════════════╣
║ 🟡 HIGH: Slide 3 has 142 words (recommended: <100)               ║
║    → Consider splitting into two slides                          ║
╠══════════════════════════════════════════════════════════════════╣
║ [Show All Warnings]  [✓ Acknowledge & Continue]                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Passed State (No Issues)
```
╔══════════════════════════════════════════════════════════════════╗
║ ✅ VALIDATION PASSED — All checks OK                             ║
╠══════════════════════════════════════════════════════════════════╣
║ Print CSS: ✓ | Content: ✓ | Charts: ✓ | Accessibility: ✓        ║
╠══════════════════════════════════════════════════════════════════╣
║ [Show Details]  [✓ OK]                                           ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🔄 Integration with Agents

### At Output Generation
1. Agent generates HTML output
2. Agent embeds validation block (mandatory)
3. Agent runs self-check before delivery
4. If self-check finds critical issues → Fix before delivering
5. Deliver output to user

### At User View
1. User opens HTML output
2. Validation runs automatically
3. Results shown in panel
4. If critical errors → User cannot dismiss panel
5. If warnings → User can acknowledge
6. If passed → User can dismiss with one click

---

## 📝 Logging

All validation results are logged:

```markdown
### Validation Log Entry
- **Timestamp:** [ISO timestamp]
- **Output:** [filename]
- **Result:** [PASSED / WARNING / FAILED]
- **Critical Errors:** [count]
- **Warnings:** [count]
- **Auto-Fixes Applied:** [list]
- **User Action:** [Acknowledged / Fixed / N/A]
```

---

## ⚡ Quick Reference

### Agent Checklist (Before Delivery)
```
□ Validation block embedded?
□ Self-check passed?
□ Critical errors = 0?
□ Warnings documented?
```

### User Actions
- **FAILED:** Cannot proceed until agent fixes
- **WARNING:** Can acknowledge and proceed
- **PASSED:** Can dismiss immediately

---

*This protocol is NON-NEGOTIABLE. All agents must comply.*




