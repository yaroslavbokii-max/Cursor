# Agent Memory — Workshop Exercise Designer

**Last Updated:** 2026-01-13
**Total Learnings:** 7
**Projects Contributed To:** [MECE Workshop 2026-01-13]

---

## 🧠 Core Learnings

### What Works Well
1. **`page-break-inside: avoid` on ALL exercise elements** — Tables, answer boxes, exercise boxes NEVER break across pages
2. **Fixed page dimensions** — Using exact A4 (210mm × 297mm) with controlled margins
3. **Print instructions banner** — Embedding Chrome print settings in HTML reduces user confusion
4. **Clear exercise structure** — Numbered boxes with distinct visual styling
5. **Answer boxes with ample space** — Dotted borders, minimum 60px height
6. **Grouping related content** — Keep question + answer space on same page

### What Doesn't Work
1. **Tables breaking mid-row** — Always use `page-break-inside: avoid` on tables
2. **Relying on browser print defaults** — Must use `@page { margin: 0 }` and instruct users
3. **Dense exercise layouts** — Leave breathing room, use more pages if needed
4. **Floating elements near page breaks** — They can shift unexpectedly

### User Preferences Discovered
- **Format:** A4 Portrait for worksheets
- **Style:** Clear numbered exercises, visual distinction between question/answer areas
- **Print:** 1:1 match between screen and print is essential
- **Output location:** `/Projects/[project-name]/` NOT agent folders

---

## 📊 Usage Statistics

| Metric | Value |
|--------|-------|
| Times Invoked | 1 |
| Exercises Created | 6 |
| Avg Output Quality | Excellent (after page break fixes) |
| Most Common Task Type | Framework application exercises |

---

## 🔗 Context Connections

### Works Best With
- @presentation-maker — When: workshop needs slide templates
- @visual-designer — When: exercises need visual aids
- @knowledge-extractor — When: extracting framework knowledge for exercises
- @layout-architect — When: page breaks and print formatting critical

### Struggles With
- Very complex multi-part exercises on single page (split into multiple pages)
- Large tables (keep rows together, consider splitting table)

---

## 📝 Project-Specific Notes

### MECE Workshop (2026-01-13)
- **Context:** 35-minute practice section with individual, pair, and group exercises
- **Exercises Created:** 6 (2 individual, 2 pair, 2 group activities)
- **What Worked:** 
  - Clear visual hierarchy (exercise boxes, answer boxes)
  - `page-break-inside: avoid` on all components
  - Industry-specific examples (food delivery)
- **What to Improve:** 
  - Always add `page-break-inside: avoid` from the start
  - Test print preview before first delivery
  - Keep tables within single pages

---

## 📚 Exercise Type Effectiveness

| Exercise Type | Times Used | Notes |
|---------------|------------|-------|
| Fill-in-blank MECE tree | 2 | Works well for individual work |
| Spot-the-overlap | 1 | Good for pair discussions |
| Case study breakdown | 2 | Excellent for group work |
| Quick quiz | 1 | Good warm-up activity |

---

## 🎯 Mandatory CSS for Exercises

```css
/* CRITICAL: Never break these across pages */
.exercise-box,
.answer-box,
table,
.keep-together {
    page-break-inside: avoid !important;
}

/* Remove browser header/footer space */
@page {
    size: A4 portrait;
    margin: 0;
}
```

---

## 📋 Mandatory Protocols

All exercise outputs MUST follow:
- `_output-validation-protocol.md` — Content fit, print validation
- `_print-output-standards.md` — CSS rules, page breaks, colors

---

*Auto-updated after each agent invocation*
