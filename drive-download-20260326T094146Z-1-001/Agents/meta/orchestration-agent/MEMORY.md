# Agent Memory — Orchestration Agent

**Last Updated:** 2026-01-14
**Total Learnings:** 32
**Projects Contributed To:** [MECE Workshop 2026-01-13, AIDA Workshop 2026-01-14]

---

## 🧠 Core Learnings

### What Works Well
1. **Multi-agent coordination** — Complex deliverables benefit from specialized agents working together
2. **Clarifying questions flow** — Iterative Q&A produces much better outputs than assumptions
3. **Expert Panel as Quality Gate** — Auto-triggering review after knowledge extraction improves quality
4. **Standard workshop package** — Consistent deliverable set (slides, exercises, cheatsheet, guide)
5. **Output validation protocol** — Always validate before delivery prevents rework
6. **Project folder structure** — Outputs to `/Projects/[project-name]/` keeps workspace clean
7. **First-time user setup** — Capturing preferences early saves time on every future interaction
8. **Brand presets** — 7 options cover most use cases, custom handles edge cases
9. **Protocol enforcement** — Quality gates catch issues BEFORE user sees them
10. **Preview mode** — Direction validation saves rebuild time

### What Doesn't Work
1. **Assuming output will be correct on first try** — Always iterate and validate
2. **Skipping print preview** — Browser print settings can break layout
3. **JavaScript-dependent components in print outputs** — Keep it simple (HTML/CSS/SVG only)
4. **Dense content** — McKinsey style (breathing room) is always better
5. **Not providing print instructions** — Users don't know to change Chrome settings
6. **Protocols as "reference docs"** — Must be ENFORCED, not optional
7. **Assuming brand context** — Ask or detect, don't assume

### Edge Cases & Special Handling
- **Gamma outputs:** Need `[VISUAL: description]` hints for diagram generation
- **Print outputs:** Require embedded print instructions + `@page { margin: 0 }`
- **Cheatsheets:** If content doesn't fit A5, use A4 (more pages > smaller text)
- **Complex diagrams:** Use pure SVG, NOT JavaScript libraries
- **New users:** Run first-time setup before first task

---

## 👤 User Preferences Discovered

### Output Preferences
- **Brand Preset:** Radiant Operator (gold/white)
- **Content Density:** Balanced (80-100 words/slide) — can override per project
- **Print:** 1:1 match between screen and printed output is essential
- **Gamma:** Uses "Paste text" workflow, needs visual hints
- **Location:** All outputs go to `/Projects/[project-name]/`
- **Output Formats:** All formats (Screen + Print + Gamma)

### Communication Preferences
- **Clarifying questions:** Appreciated, adaptive depth preferred
- **Options:** Likes multiple options with recommendations
- **Iteration:** Happy to provide feedback and iterate
- **Control:** Prefers Balanced involvement level

### Quality Standards
- **Visual:** Neat, professional, McKinsey-level
- **Print:** Must work with Chrome print settings (None margins, no headers)
- **Diagrams:** Semantically accurate (ME = gap, CE = no gap)
- **Density:** Flexible — ask user each time

---

## 📊 Usage Statistics

| Metric | Value |
|--------|-------|
| Times Invoked | 1 |
| Projects Contributed | 1 |
| Most Common Task Type | Workshop creation |
| Avg Satisfaction Score | High (after iterations) |
| Avg Quality Score | 89 (after fixes) |
| Avg Iterations Needed | 4 (target: 1-2) |

---

## 🔗 Agent Collaboration Insights

### Works Best With
| Agent | When to Use | Notes |
|-------|-------------|-------|
| @presentation-maker | Slides needed | Always validate print/Gamma compatibility |
| @data-visualization-expert | Diagrams needed | Use SVG, check semantic accuracy |
| @workshop-exercise-designer | Exercises needed | Apply page break rules |
| @layout-architect | Print formatting | Apply print standards protocol |
| @expert-panel | Quality review | Auto-trigger after knowledge extraction |
| @knowledge-extractor | Research/synthesis | Feeds into presentations |

### Successful Workflow: MECE Workshop
```
1. First-time setup (if new user)
2. Brand selection/confirmation
3. Content density preference
4. Knowledge extraction → MECE framework
5. Expert Panel (optional) → Validate content  
6. Preview structure → User approval
7. Presentation maker → Slides + Gamma input
8. Data visualization → SVG diagrams
9. Workshop exercise designer → Exercises
10. Layout architect → Print formatting
11. Quality Score check → ≥80 required
12. Output validation → All checks pass
13. Delivery
```

### Handoff Improvements Implemented
- ✅ Print validation step before delivery
- ✅ All agents reference protocols
- ✅ Quality Score gate (≥80)
- ✅ Expert Panel auto-trigger
- ✅ Preview mode for complex outputs

---

## 📝 Project-Specific Notes

### MECE Workshop (2026-01-13)
- **Request:** 60-minute presentation for food delivery professionals
- **Mode:** Balanced
- **Iterations Required:** 4 (initial → Gamma fix → diagram fix → print fix)
- **Final Quality Score:** 89

**Key Lessons Captured:**
1. Always include print instructions from first delivery
2. Use pure SVG for diagrams (no Mermaid.js)
3. Apply `@page { margin: 0 }` for 1:1 print match
4. `page-break-inside: avoid` on tables and exercise boxes
5. Content density matters (ask user preference)
6. Outputs go to `/Projects/` not agent folders
7. Offer preview before full build

### AIDA Workshop (2026-01-14)
- **Request:** 60-minute AIDA copywriting workshop for food delivery professionals
- **Mode:** Balanced
- **Brand:** Bolt
- **Iterations Required:** 2 (initial → print fix)
- **Final Quality Score:** 94

**Key Lessons Captured:**
1. **Content density question was SKIPPED** — Even though it was in protocol, I didn't ask it
2. **PDF should be MANDATORY output** — Always include PDF-ready HTML + Gamma export
3. **Print CSS template is critical:**
   ```css
   @page { margin: 0 !important; }  /* Removes browser headers/footers */
   .page { max-height: 297mm; page-break-after: always; }
   ```
4. **Explicit page dimensions required** — Each page needs `width: 210mm; height: 297mm`
5. **Gamma-ready export is valuable** — User can paste and get instant slides
6. **Learnings must propagate** — Created `_aida-workshop-learnings.md` for cross-agent use

**Protocol Updates Made:**
- Added content density to `@orchestration-agent` first response template
- Updated references in all visual output agents
- Made PDF output mandatory default

---

## 🎨 Brand Configuration

### Current User Brand
```yaml
preset: "radiant-operator"
colors:
  primary: "#FFD700"      # Solstice Gold
  background: "#F9F9F9"   # Cloud White
  text: "#333333"         # Slate Graphite
  secondary: "#E1E1E1"    # Soft Pebble
typography:
  headers: "Inter, Extra Bold, ALL CAPS"
  body: "Inter, Regular, 1.6 line-height"
  code: "JetBrains Mono"
principles:
  - "80% whitespace"
  - "Gold used ONLY for key insights (spotlight)"
  - "Ultra-thin geometric icons"
```

### Default for Unknown Users
```yaml
preset: "radiant-operator"  # Professional, works for most business content
fallback_behavior: "Ask user to confirm or change"
```

---

## 📋 Protocol Compliance Log

| Protocol | Status | Notes |
|----------|--------|-------|
| `_first-time-setup.md` | ✅ Active | Run for new users |
| `_brand-auto-load-protocol.md` | ✅ Active | 7 presets + custom |
| `_protocol-enforcement-layer.md` | ✅ Active | Mandatory gates |
| `_output-quality-score-protocol.md` | ✅ Active | ≥80 to deliver |
| `_output-preview-protocol.md` | ✅ Active | For complex outputs |
| `_output-validation-protocol.md` | ✅ Active | Post-build checks |
| `_print-output-standards.md` | ✅ Active | Print-specific rules |
| `_content-density-guidelines.md` | ✅ Active | Ask user preference |

---

## 🎯 Improvement Queue

### Implemented This Session
- ✅ First-time user setup
- ✅ Brand presets (7 options)
- ✅ Protocol enforcement layer
- ✅ Quality Score gate
- ✅ Preview mode
- ✅ Content density as user choice

### Pending (Future Work)
- [ ] Agent consolidation (62 → 33)
- [x] PDF generation — Now mandatory default (PDF-ready HTML)
- [ ] Real-time quality feedback during build
- [x] Cross-project learning patterns — `_aida-workshop-learnings.md` created

---

*Memory updated: 2026-01-14*
*Version: 7.0*
