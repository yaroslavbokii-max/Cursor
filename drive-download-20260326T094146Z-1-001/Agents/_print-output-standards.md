# Print Output Standards Protocol

> **Version:** 1.0  
> **Created:** 2026-01-13  
> **Purpose:** Ensure perfect 1:1 match between screen display and printed output

---

## 🎯 Core Principle

**What you see on screen MUST match what prints.**

Browser-added headers/footers, incorrect margins, and content overflow are the #1 causes of print failures.

---

## 📋 Mandatory CSS Rules

### 1. Page Setup (Critical)

```css
/* Remove ALL browser header/footer space */
@page {
    size: A4 portrait;  /* or: A4 landscape, A5 portrait, etc. */
    margin: 0;
}

/* Reset body for print */
@media print {
    html, body {
        background: white !important;
        margin: 0 !important;
        padding: 0 !important;
    }
}
```

### 2. Page Break Control

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

/* Don't leave headings orphaned at bottom of page */
h1, h2, h3 {
    page-break-after: avoid !important;
}

/* Force page breaks where needed */
.page-break-before {
    page-break-before: always;
}

.page-break-after {
    page-break-after: always;
}
```

### 3. Content Overflow Protection

```css
/* Fixed page dimensions */
.page {
    width: 210mm;      /* A4 width */
    height: 297mm;     /* A4 height */
    padding: 15mm 18mm;
    overflow: hidden;  /* CRITICAL: Hide any overflow */
    position: relative;
}

/* For slides */
.slide {
    width: 960px;
    height: 540px;
    overflow: hidden;
    position: relative;
}

/* Protected content area (leaves room for footer) */
.slide-content {
    height: 420px;     /* Fixed height */
    overflow: hidden;  /* Prevent overflow into footer */
}
```

---

## 🖨️ Print Instructions Banner

**Every printable HTML file MUST include this banner:**

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

**Banner CSS:**

```css
.print-banner {
    background: #333;
    color: white;
    padding: 16px 24px;
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 100;
}

@media print {
    .print-banner { display: none !important; }
}
```

---

## 📐 Page Size Reference

| Format | Dimensions | Use Case |
|--------|------------|----------|
| A4 Portrait | 210mm × 297mm | Worksheets, exercises, reports |
| A4 Landscape | 297mm × 210mm | Wide tables, dashboards |
| A5 Portrait | 148mm × 210mm | Cheatsheets (if content fits) |
| A5 Landscape | 210mm × 148mm | Quick reference cards |
| 16:9 Landscape | 960px × 540px | Presentation slides |

**Rule:** Choose page size based on content, NOT convention. If content doesn't fit A5, use A4.

---

## 🎨 Print-Safe Colors

### Colors That Print Well
- Dark blues: `#1e3a5f`, `#0066cc`
- Greens: `#28a745`, `#218838`
- Reds: `#dc3545`
- Grays: `#333`, `#666`
- Yellows (with dark text): `#fff8e1`, `#ffc107`

### Colors to Avoid
- Very light grays (< `#e0e0e0`) — may not print
- Gradients with subtle transitions — may band
- Pure yellow text — invisible on white paper

### Background Graphics
Always remind users to check **"Background graphics"** in print settings, otherwise colored backgrounds won't print.

---

## ✅ Pre-Delivery Checklist

Before delivering ANY printable HTML output:

### Content Fit
- [ ] All content visible on screen (no horizontal scroll)
- [ ] Text doesn't extend beyond page/slide boundaries
- [ ] Diagrams fit within their containers
- [ ] No content hidden behind footers

### Print Preview
- [ ] Opened print preview in Chrome
- [ ] Set margins to "None"
- [ ] Unchecked "Headers and footers"
- [ ] Checked "Background graphics"
- [ ] Each page matches screen view

### Tables
- [ ] No tables split across pages
- [ ] Table headers visible on each page (if table spans pages)
- [ ] Cell content doesn't overflow

### Diagrams
- [ ] SVG diagrams render correctly
- [ ] Colors are print-safe
- [ ] Labels are readable at print size

---

## 🔧 Troubleshooting

### Problem: Content shifts when printing
**Cause:** Browser headers/footers taking space  
**Fix:** User must uncheck "Headers and footers" in print dialog

### Problem: Tables break mid-row
**Cause:** Missing `page-break-inside: avoid`  
**Fix:** Add CSS rule to table element

### Problem: Colors don't print
**Cause:** "Background graphics" unchecked  
**Fix:** User must check this option

### Problem: Page numbers showing in wrong place
**Cause:** Browser adding its own page numbers  
**Fix:** Uncheck "Headers and footers"

### Problem: Content overflows slide
**Cause:** Too much content OR missing overflow:hidden  
**Fix:** Reduce content OR add overflow protection

---

## 📁 File Naming Convention

```
/Projects/[project-name]/
├── presentation-slides.html    # Printable slides
├── gamma-input.md              # Gamma-ready markdown
├── exercises-worksheets.html   # Printable exercises
├── cheatsheet.html             # Quick reference
├── facilitator-guide.md        # Timing + answers
└── [additional-assets]/        # Images, data, etc.
```

---

## 🔗 Related Protocols

- `_output-validation-protocol.md` — Visual output validation
- `_content-density-guidelines.md` — Text limits per element
- `_gamma-optimization-guide.md` — Gamma best practices




