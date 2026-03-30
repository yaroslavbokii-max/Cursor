# Output Validation Protocol

**Version:** 2.0  
**Updated:** 2026-01-13  
**Purpose:** Ensure all agent outputs are properly formatted, fit their intended medium, render correctly, and print perfectly

---

## 🔴 Critical: Print/Screen 1:1 Match

The #1 cause of output failures: **browser-added headers/footers** that shift content and break page alignment.

### Mandatory CSS Rules

```css
/* CRITICAL: Remove ALL browser header/footer space */
@page {
    size: A4 portrait;  /* or appropriate size */
    margin: 0;
}

@media print {
    html, body {
        background: white !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Hide print instructions in print */
    .print-banner, .no-print { 
        display: none !important; 
    }
}
```

### Mandatory Print Instructions Banner

**Every printable HTML file MUST include:**

```html
<div class="print-banner">
    <h3>🖨️ Print Instructions</h3>
    <p>For perfect 1:1 match between screen and print:</p>
    <button onclick="window.print()">Print Document</button>
    <div class="steps">
        <strong>In Chrome Print Dialog:</strong><br>
        1. More settings → Margins: <strong>None</strong><br>
        2. Uncheck <strong>"Headers and footers"</strong><br>
        3. Check <strong>"Background graphics"</strong>
    </div>
</div>
```

---

## 1. Page Fitting Rules

### Content-First Format Selection

**DO NOT pre-decide format.** Instead:

1. **Estimate content size** before choosing format
2. **Select format** that fits content with 10-15% margin
3. **Validate** content actually fits
4. **Adjust** if needed (more pages, not smaller text)

### Format Guidelines

| Content Type | Default | Alternative if overflow |
|--------------|---------|------------------------|
| Slides/Presentations | Landscape 16:9 (960×540px) | Increase slide count |
| Cheatsheets | A4 Portrait | Add pages, NOT smaller text |
| Exercises/Worksheets | A4 Portrait | Add pages |
| Reports | A4 Portrait | Add pages |
| Quick Reference | A5 Landscape | Upgrade to A4 |

### Anti-Overflow Rules

```
❌ NEVER:
- Reduce font below 10px for body text
- Overflow content outside page bounds
- Let content touch page edges
- Use horizontal scroll
- Ignore footer zones

✅ ALWAYS:
- Add pages if content doesn't fit
- Maintain minimum margins (15mm for print)
- Test print preview before finalizing
- Leave 10-15% breathing room
- Protect footer zones from content
```

### Slide Content Protection

```css
/* Fixed slide dimensions with footer protection */
.slide {
    width: 960px;
    height: 540px;
    padding: 40px 50px 60px 50px; /* Extra bottom for footer */
    overflow: hidden; /* CRITICAL */
    position: relative;
}

.slide-content {
    height: 420px;  /* Fixed - leaves room for footer */
    overflow: hidden;
}

.footer {
    position: absolute;
    bottom: 16px;
    left: 50px;
    right: 50px;
}
```

---

## 2. Content Density Guidelines

### McKinsey Style (Recommended)

| Element | Maximum | Guideline |
|---------|---------|-----------|
| Words per slide | 40-60 | Less is more |
| Bullet points per section | 3-5 | Use sub-bullets sparingly |
| Font size (body) | Min 14px | 16px preferred |
| Font size (headers) | 28-36px | Clear hierarchy |
| Lines per bullet | 1-2 | One idea per bullet |

### Breathing Room

- **Presentations:** 60% content, 40% white space
- **Worksheets:** 70% content, 30% white space
- **Cheatsheets:** 75% content, 25% white space

---

## 3. Page Break Control

### CSS Rules (Mandatory)

```css
/* NEVER break these elements across pages */
table,
.answer-box,
.exercise-box,
.diagram,
.card,
.keep-together {
    page-break-inside: avoid !important;
}

/* Don't leave headings orphaned */
h1, h2, h3 {
    page-break-after: avoid !important;
}

/* Force breaks where needed */
.page-break-before { page-break-before: always; }
.page-break-after { page-break-after: always; }
```

### Table-Specific Rules

Tables MUST NEVER break mid-row:

```css
table {
    page-break-inside: avoid !important;
}

/* If table MUST span pages, keep header visible */
thead {
    display: table-header-group;
}
```

---

## 4. Diagram Rendering Rules

### Semantic Accuracy (CRITICAL)

Diagrams MUST visually represent their stated meaning:

| Concept | CORRECT Visual | WRONG Visual |
|---------|---------------|--------------|
| **Mutually Exclusive** | Shapes with GAPS between (NOT touching) | Overlapping shapes |
| **Collectively Exhaustive** | Shapes that FILL container (NO gaps) | Shapes with empty space |
| **Overlapping (bad example)** | Venn-style overlapping circles | Separate shapes |
| **Tree/Hierarchy** | Vertical indented structure | Horizontal inline text |

### ME Diagram (Correct)

```svg
<!-- Two circles NOT touching -->
<svg width="200" height="100">
  <circle cx="50" cy="50" r="35" fill="#e7f3ff" stroke="#0066cc"/>
  <circle cx="150" cy="50" r="35" fill="#e7f3ff" stroke="#0066cc"/>
  <!-- Gap between them shows mutual exclusivity -->
</svg>
```

### CE Diagram (Correct)

```svg
<!-- Segments fill entire container with NO gaps -->
<svg width="200" height="100">
  <rect x="0" y="0" width="200" height="100" stroke="#28a745"/>
  <rect x="2" y="2" width="64" height="96" fill="#c8e6c9"/>
  <rect x="68" y="2" width="64" height="96" fill="#a5d6a7"/>
  <rect x="134" y="2" width="64" height="96" fill="#81c784"/>
</svg>
```

### Implementation Priority

1. **Pure SVG** (preferred) — Most reliable, scales perfectly
2. **CSS-styled HTML** — Good for text-heavy trees
3. **Unicode box-drawing** — For simple trees in code blocks
4. **External images** — When complex illustration needed

---

## 5. Print-Safe Colors

### Colors That Print Well

| Color | Hex | Use |
|-------|-----|-----|
| Navy | `#1e3a5f` | Headers, primary text |
| Blue | `#0066cc` | Accent, links |
| Green | `#28a745` | Success, good examples |
| Red | `#dc3545` | Danger, bad examples |
| Dark Gray | `#333`, `#666` | Body text, muted |
| Yellow BG | `#fff8e1` | Callouts (with dark text) |

### Colors to Avoid

- Very light grays (< `#e0e0e0`) — may not print
- Gradients with subtle transitions — may band
- Pure yellow text — invisible on white paper
- Neon colors — unpredictable printing

---

## 6. Gamma Optimization

### Best Practices for Gamma Input

1. **One slide per `---` separator**
2. **Clear visual hints** using `[VISUAL: description]` format
3. **Simple markdown** — avoid complex nesting
4. **Table format** for data comparison
5. **Include color suggestions** for brand consistency

### Visual Hint Format

```markdown
[VISUAL: Brief description of desired image/diagram]

Examples:
[VISUAL: Professional team in workshop setting, diverse, modern office]
[VISUAL: Two non-overlapping circles labeled A and B, blue theme]
[VISUAL: Horizontal funnel: Acquisition → Activation → Retention]
```

### Gamma Tips Section (Add to end of Gamma input)

```markdown
---

## 📌 Gamma Tips for Best Results

**Color Scheme:**
- Primary: #1e3a5f (navy)
- Accent: #0066cc (blue)  
- Success: #28a745 (green)
- Danger: #dc3545 (red)

**Key Diagrams:**
1. Slide 3: Two separate circles for ME concept
2. Slide 5: Overlapping circles (bad example)
3. Slide 9: Three-stage funnel

**Style:** McKinsey-inspired, minimal text, professional

**Images:** Business professionals, diverse, modern settings
```

---

## 7. Output Location Rules

**NEVER save outputs under agent folders.**

### Correct Structure

```
/PACT/
├── Agents/          # Agent definitions ONLY
│   └── NEW/
│       └── [category]/
│           └── [agent-name]/
│               ├── [agent-name].md    # Definition
│               ├── MEMORY.md          # Learnings
│               └── changelog.md       # History
│
└── Projects/        # ALL outputs go here
    └── [project-name-yyyy-mm-dd]/
        ├── presentation-slides.html
        ├── gamma-input.md
        ├── exercises-worksheets.html
        ├── cheatsheet.html
        ├── facilitator-guide.md
        └── [additional-assets]/
```

### Naming Convention

```
Project folder: [project-name-yyyy-mm-dd] or [project-name]
Files: [deliverable-type].[extension]

Examples:
/Projects/mece-workshop-2026-01-13/
/Projects/q4-review/quarterly-report-2026-01-15.html
```

---

## 8. Workshop Package Standard

Every workshop SHOULD include:

| Deliverable | Format | Purpose |
|-------------|--------|---------|
| `presentation-slides.html` | HTML (printable) | Facilitator display |
| `gamma-input.md` | Markdown | Gamma import |
| `exercises-worksheets.html` | HTML (printable) | Participant handouts |
| `cheatsheet.html` | HTML (printable) | Quick reference |
| `facilitator-guide.md` | Markdown | Timing + answers |

---

## 9. Pre-Delivery Checklist

### Content Fit ✓
- [ ] All content visible on screen (no horizontal scroll)
- [ ] Text doesn't extend beyond page/slide boundaries
- [ ] Diagrams fit within their containers
- [ ] No content hidden behind footers
- [ ] Footer zones protected

### Print Preview ✓
- [ ] Opened print preview in Chrome
- [ ] Set margins to "None"
- [ ] Unchecked "Headers and footers"
- [ ] Checked "Background graphics"
- [ ] Each page matches screen view

### Tables ✓
- [ ] No tables split across pages
- [ ] `page-break-inside: avoid` applied
- [ ] Cell content doesn't overflow

### Diagrams ✓
- [ ] SVG diagrams render correctly
- [ ] Colors are print-safe
- [ ] Labels are readable at print size
- [ ] **Semantic accuracy:** ME = gap, CE = no gap

### Gamma Ready ✓
- [ ] `[VISUAL: description]` hints included
- [ ] Slide separators (`---`) in place
- [ ] Gamma Tips section at end
- [ ] Simple markdown structure

---

## 10. Quality Gates

| Gate | Check | Action if Fail |
|------|-------|----------------|
| **Fit** | Content fits page with margin | Add pages or change format |
| **Render** | All elements display correctly | Fix or simplify |
| **Print** | Print preview matches screen | Add `@page { margin: 0 }` |
| **Semantic** | Diagrams match their meaning | Redesign diagram |
| **Readable** | Text is clear and scannable | Increase size/spacing |
| **Location** | Output in `/Projects/` folder | Move file |

---

## Related Protocols

- `_print-output-standards.md` — Detailed CSS and print rules
- `_confidence-scoring-protocol.md` — Output confidence ratings
- `_specialist-handoff-protocol.md` — When to delegate

---

*This protocol is mandatory for all content-generating agents.*
*Version 2.0 incorporates lessons from MECE Workshop project (2026-01-13)*
