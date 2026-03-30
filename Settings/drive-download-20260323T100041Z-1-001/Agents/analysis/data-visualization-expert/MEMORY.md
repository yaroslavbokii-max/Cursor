# Agent Memory — Data Visualization Expert

**Last Updated:** 2026-01-13
**Total Learnings:** 9
**Projects Contributed To:** [MECE Workshop 2026-01-13]

---

## 🧠 Core Learnings

### What Works Well
1. **Pure SVG for diagrams** — Most reliable, scales perfectly, prints cleanly
2. **Semantic accuracy** — Diagram MUST visually represent its stated meaning
3. **Print-safe colors** — Navy (#1e3a5f), Blue (#0066cc), Green (#28a745), Red (#dc3545)
4. **Fixed viewBox** — Use `viewBox` attribute for responsive SVG scaling
5. **Inline SVG** — Embedding SVG directly in HTML ensures it renders and prints

### What Doesn't Work
1. **JavaScript-dependent diagrams** — Mermaid.js, Chart.js can fail in print
2. **Overlapping ME circles** — Mutually Exclusive diagrams MUST show SEPARATE shapes with gaps
3. **CE diagrams with gaps** — Collectively Exhaustive diagrams MUST fill their container completely
4. **Light colors** — Yellows/light grays may not print visibly
5. **External image dependencies** — SVG links to external images may fail

### User Visualization Preferences
- **Preferred chart types:** McKinsey standards (bar, line, waterfall, bridge)
- **Color palette:** Navy/Blue primary, Green for success, Red for danger
- **Style:** Minimal, spotlight-focused, BLUF titles
- **Diagram tech:** Pure SVG (NOT Mermaid, NOT Chart.js for print)

---

## 📊 Usage Statistics

| Metric | Value |
|--------|-------|
| Times Invoked | 1 |
| Charts/Diagrams Created | 8 |
| Most Common Diagram Type | Concept diagram (ME/CE) |
| Avg Output Quality | Excellent (after semantic corrections) |

---

## 🔴 Critical: Semantic Accuracy Rules

### Mutually Exclusive (ME) Diagrams
```
CORRECT: Two shapes with VISIBLE GAP between them
         ○     ○  (circles NOT touching)
         
WRONG:   ○○  or (●) (overlapping or touching)
```

**SVG Example:**
```svg
<circle cx="80" cy="50" r="40"/>   <!-- Left -->
<circle cx="200" cy="50" r="40"/> <!-- Right - GAP of 80px -->
```

### Collectively Exhaustive (CE) Diagrams
```
CORRECT: Shapes that FILL container with NO gaps
         [███|███|███] (segments fill rectangle)
         
WRONG:   [ █  █  █ ] (gaps between or around)
```

**SVG Example:**
```svg
<rect x="0" y="0" width="300" height="100"/>  <!-- Container -->
<rect x="2" y="2" width="98" height="96"/>    <!-- Fills left -->
<rect x="102" y="2" width="98" height="96"/>  <!-- Fills middle -->
<rect x="202" y="2" width="96" height="96"/>  <!-- Fills right -->
```

---

## 🎨 Print-Safe Color Palette

| Color | Hex | Use | Print Safety |
|-------|-----|-----|--------------|
| Navy | `#1e3a5f` | Headers, primary | ✅ Excellent |
| Blue | `#0066cc` | Accent, ME concept | ✅ Excellent |
| Green | `#28a745` | Success, CE concept | ✅ Excellent |
| Red | `#dc3545` | Danger, bad examples | ✅ Excellent |
| Dark Gray | `#333`, `#666` | Body text | ✅ Good |
| Light Blue BG | `#e7f3ff` | ME shape fill | ✅ Good |
| Light Green BG | `#e8f5e9` | CE shape fill | ✅ Good |
| Light Yellow BG | `#fff8e1` | Callouts | ⚠️ Needs dark text |

### Colors to Avoid
- `#f0f0f0` and lighter grays — may not print
- Pure yellow (`#ffff00`) — invisible on white paper
- Subtle gradients — may band when printed

---

## 🔗 Context Connections

### Works Best With
- @data-analyst — When: Data needs visualization
- @presentation-maker — When: Diagrams for slides
- @report-automator — When: Visuals for automated reports
- @layout-architect — When: Diagram sizing and placement

### Common Workflows
1. Concept explanation → SVG diagram → Embed in HTML → Print validation
2. Data → Chart type selection → SVG/Canvas → Print-safe colors

---

## 📝 Project-Specific Notes

### MECE Workshop (2026-01-13)
- **Context:** Teaching ME and CE concepts visually
- **Diagrams Created:** ME (separate circles), CE (filled rectangle), tree structures, funnel
- **What Worked:** 
  - Pure inline SVG for all diagrams
  - Semantic accuracy (ME = gap, CE = filled)
  - Print-safe colors
- **What to Improve:** 
  - Always validate semantic meaning before delivery
  - Include viewBox for responsive scaling
  - Test print preview for color visibility

---

## 🎯 Improvement Queue

### Lessons Implemented
- ✅ Pure SVG as default (no JS dependencies)
- ✅ Semantic accuracy checks for concept diagrams
- ✅ Print-safe color palette
- ✅ Inline SVG embedding

### Known Limitations
- Interactive charts (hover, filter) don't work in print
- Complex animations should be avoided for print outputs

---

## 📋 Mandatory Protocols

All visualization outputs MUST follow:
- `_output-validation-protocol.md` — Semantic accuracy, print validation
- `_print-output-standards.md` — Print-safe colors, CSS rules

---

*Auto-updated after each agent invocation*
