# Agent Memory — Layout Architect

**Last Updated:** 2026-01-13
**Total Learnings:** 10
**Projects Contributed To:** [MECE Workshop 2026-01-13]

---

## 🧠 Core Learnings

### What Works Well
1. **`@page { margin: 0 }`** — Critical CSS rule that removes browser header/footer space
2. **`page-break-inside: avoid`** — Prevents tables, exercise boxes, and diagrams from breaking across pages
3. **`overflow: hidden` on containers** — Ensures content cannot extend beyond boundaries
4. **Print instructions banner** — Embedding Chrome print settings instructions directly in HTML
5. **Fixed page dimensions** — Using exact A4 (210mm × 297mm) or slide (960×540px) dimensions
6. **Content-first format selection** — Choose page size AFTER estimating content, not before
7. **Adding pages vs. shrinking text** — Always prefer more pages over smaller fonts

### What Doesn't Work
1. **Relying on browser defaults** — Chrome adds headers/footers by default that shift content
2. **A5 for dense content** — If content overflows A5, use A4 (don't force smaller text)
3. **Assuming print matches screen** — Must explicitly set `@page { margin: 0 }` and instruct users
4. **Breaking tables** — Tables split mid-row look broken; keep them together
5. **Footer overlap** — Content extending into footer zones looks unprofessional

### User Layout Preferences
- **Preferred page size:** A4 Portrait for worksheets, Landscape 16:9 for slides
- **Preferred margins:** 15-18mm for print safety
- **Preferred fonts:** Inter (body), SF Mono (code/trees)
- **Print requirement:** 1:1 match between screen and printed output

---

## 📊 Usage Statistics

| Metric | Value |
|--------|-------|
| Times Invoked | 1 |
| Documents Formatted | 4 (slides, exercises, cheatsheet, guide) |
| Most Common Format | A4 Portrait |
| Avg Output Quality | Excellent (after iterations) |

---

## 📄 Document Type Preferences

### By Document Type
| Type | Page Size | Orientation | Special Settings |
|------|-----------|-------------|------------------|
| Presentation Slides | 960×540px | Landscape | Fixed content area, footer protection |
| Exercises/Worksheets | A4 | Portrait | `page-break-inside: avoid` on all boxes |
| Cheat Sheets | A4 | Portrait | Two-column grid, compact spacing |
| Reports | A4 | Portrait | Standard margins |

---

## 🎯 Critical CSS Rules (Always Include)

```css
/* Remove browser header/footer space */
@page {
    size: A4 portrait;  /* or appropriate */
    margin: 0;
}

@media print {
    html, body {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Never break these */
    table, .exercise-box, .answer-box, .diagram, .keep-together {
        page-break-inside: avoid !important;
    }
    
    /* Don't orphan headings */
    h1, h2, h3 {
        page-break-after: avoid !important;
    }
}
```

---

## 🔗 Context Connections

### Works Best With
- @presentation-maker — When: Formatting slide layouts
- @visual-designer — When: Ensuring visual fit
- @report-automator — When: Print formatting reports
- @data-visualization-expert — When: Chart sizing and placement
- @workshop-exercise-designer — When: Page breaks for exercises

### Common Workflows
1. Presentation → Slides → Print validation → Delivery
2. Workshop → Exercises + Cheatsheet → Print validation → Delivery
3. Report → Format → Print preview → Delivery

---

## 📝 Project-Specific Notes

### MECE Workshop (2026-01-13)
- **Context:** 60-minute workshop materials
- **Document Types:** Slides (HTML), Exercises (HTML), Cheatsheet (HTML), Guide (MD)
- **What Worked:** 
  - `@page { margin: 0 }` for perfect print alignment
  - Print instructions banner
  - `page-break-inside: avoid` on tables and exercise boxes
- **What to Improve:** 
  - Always include print instructions from first version
  - Test print preview before first delivery
  - Content-first format selection (don't pre-decide A5 vs A4)

---

## 🎯 Improvement Queue

### Lessons Implemented
- ✅ Print instructions banner standard
- ✅ `@page { margin: 0 }` in all outputs
- ✅ Content overflow protection
- ✅ Table break prevention

### Known Limitations
- Chrome print dialog requires user action (can't auto-set margins)
- Must remind users to uncheck "Headers and footers"

---

## 📋 Mandatory Protocols

All layout outputs MUST follow:
- `_output-validation-protocol.md` — Content fit, print validation
- `_print-output-standards.md` — CSS rules, page breaks, colors

---

*Auto-updated after each agent invocation*
