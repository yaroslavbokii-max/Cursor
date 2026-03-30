# Agent Memory — Presentation Maker

**Last Updated:** 2026-01-14
**Total Learnings:** 14
**Projects Contributed To:** [MECE Workshop 2026-01-13, AIDA Workshop 2026-01-14]

---

## 🧠 Core Learnings

### What Works Well
1. **Fixed slide dimensions (960×540px)** — Ensures consistent layout across all slides
2. **Protected content area** — Using `.slide-content { height: 420px; overflow: hidden }` prevents footer overlap
3. **Print instructions banner** — Including clear Chrome print settings in HTML eliminates user confusion
4. **Breathing room** — McKinsey style (40-60 words/slide, 60% content / 40% whitespace) produces professional results
5. **Dual output** — Providing both `gamma-input.md` and `presentation-slides.html` covers both Gamma users and direct print needs

### What Doesn't Work
1. **Dense slides** — Too much text causes overflow and looks unprofessional
2. **Relying on defaults** — Browser print settings (headers/footers, margins) break layout
3. **Complex JavaScript diagrams** — Mermaid.js and similar can fail to render; use pure SVG instead
4. **Trusting content will fit** — ALWAYS validate before delivery
5. **A5 for content-heavy materials** — Use A4 and add pages instead

### User Preferences Discovered
- **Style:** McKinsey-inspired, minimal text, maximum impact
- **Print:** Must work with Chrome → Print → Margins: None + no headers/footers
- **Gamma:** Prefers "Paste text" workflow with `[VISUAL: description]` hints
- **Output location:** Projects go to `/Projects/[project-name]/`, NOT agent folders

---

## 📊 Usage Statistics

| Metric | Value |
|--------|-------|
| Times Invoked | 1 |
| Avg Output Quality | Excellent (after iterations) |
| Most Common Task Type | Workshop presentation |

---

## 🔗 Context Connections

### Works Best With
- @visual-designer — When: needing framework diagrams, infographics
- @data-visualization-expert — When: presentations require data visualizations (use SVG!)
- @workshop-exercise-designer — When: workshop presentations need exercises
- @knowledge-extractor — When: synthesizing research into presentations
- @layout-architect — When: print formatting critical

### Struggles With
- Complex interactive elements (keep it simple for print)
- Content that doesn't fit standard slide dimensions (split into more slides)

---

## 📝 Project-Specific Notes

### MECE Workshop (2026-01-13)
- **Context:** 60-minute workshop for food delivery professionals
- **Deliverables:** 14 slides, exercises, cheatsheet, facilitator guide
- **What Worked:** 
  - Pure SVG diagrams for ME/CE concepts
  - Fixed content areas preventing footer overlap
  - Print instructions banner
- **What to Improve:** 
  - Start with fewer words per slide
  - Always include print instructions from the start
  - Validate content fits before first delivery

### AIDA Workshop (2026-01-14)
- **Context:** 60-minute AIDA copywriting workshop for food delivery professionals
- **Brand:** Bolt (green #34D399)
- **Deliverables:** 25 slides, exercises (6 pages), A4 + A5 cheatsheets, Gamma export
- **What Worked:**
  - Bolt brand colors looked professional
  - Print button with options (1 slide/page landscape)
  - Gamma-ready markdown with `[VISUAL: ...]` hints
  - Exercise worksheets with explicit page boundaries
- **What DIDN'T Work (Fixed):**
  - Content density question was not asked
  - Page breaks were broken in print
  - Browser added timestamp/URL headers
- **Critical Fixes Applied:**
  ```css
  @page { margin: 0 !important; }  /* Removes browser chrome */
  .slide { max-height: 210mm; page-break-after: always; overflow: hidden; }
  ```
- **Protocol Updates:**
  - PDF-ready HTML is now MANDATORY output
  - Gamma-ready markdown is now MANDATORY output
  - Content density question added to first response

---

## 🎨 Style Preferences Discovered

| Project | Preferred Style | Notes |
|---------|-----------------|-------|
| MECE Workshop | McKinsey: minimal text, bold headers, SVG diagrams | Navy/blue color scheme, 40-60 words/slide |

---

## 📋 Mandatory Protocols

All presentation outputs MUST follow:
- `_output-validation-protocol.md` — Content fit, print validation
- `_print-output-standards.md` — CSS rules, page breaks, colors
- `_shared/_aida-workshop-learnings.md` — Print CSS template, mandatory outputs
- `_content-density-guidelines.md` — Ask user preference

### Mandatory Outputs (as of v2.0)
1. ✅ Interactive HTML slides (with print button)
2. ✅ PDF-ready HTML (`@page { margin: 0 }`, proper page breaks)
3. ✅ Gamma-ready Markdown (with `[VISUAL: ...]` hints)

---

*Auto-updated after each agent invocation*
*Last updated: 2026-01-14*
