# Gamma Optimization Guide

> **Version:** 1.0  
> **Created:** 2026-01-13  
> **Purpose:** Best practices for creating Gamma-ready Markdown that produces professional presentations

---

## 🎯 Core Principle

Gamma's "Paste text" feature works best with **simple, well-structured Markdown** and **explicit visual hints**.

---

## 📋 Input Format

### Basic Structure

```markdown
# Presentation Title

---

## Slide 1 Title

Content for slide 1

[VISUAL: Description of desired image/diagram]

---

## Slide 2 Title

Content for slide 2

---

## 📌 Gamma Tips for Best Results

[Instructions for Gamma at the end]
```

### Key Rules

1. **Use `---` for slide breaks** — One per slide
2. **`## ` for slide titles** — Gamma converts these to slide headings
3. **Keep content simple** — Avoid complex nested structures
4. **Add `[VISUAL:]` hints** — Tell Gamma what images/diagrams to generate

---

## 🖼️ Visual Hints

### Format

```markdown
[VISUAL: Brief, specific description of desired image or diagram]
```

### Good Examples

```markdown
[VISUAL: Two separate circles labeled "Category A" and "Category B" with visible gap between them, blue theme]

[VISUAL: Professional diverse team in modern office workshop setting]

[VISUAL: Three-stage horizontal funnel: Acquisition → Activation → Retention]

[VISUAL: Tree diagram with root "Problem" and three branches]

[VISUAL: Before/after comparison chart showing improvement]
```

### Bad Examples

```markdown
[VISUAL: A picture]  ← Too vague

[VISUAL: Create a complex interactive 3D visualization with animated transitions]  ← Too complex

[VISUAL: image.png]  ← Not descriptive
```

---

## 📊 Diagram Instructions

### For Concept Diagrams

| Concept | Visual Hint |
|---------|-------------|
| Mutually Exclusive | `[VISUAL: Two separate circles NOT touching, with visible gap, labeled A and B]` |
| Collectively Exhaustive | `[VISUAL: Rectangle divided into 3 equal parts filling entire space, no gaps]` |
| Hierarchy/Tree | `[VISUAL: Tree structure with root at top, 3 branches below]` |
| Process/Flow | `[VISUAL: Horizontal arrow flow: Step 1 → Step 2 → Step 3]` |
| Comparison | `[VISUAL: Side-by-side comparison table: Option A vs Option B]` |

### For Data Visualizations

```markdown
[VISUAL: Bar chart showing revenue growth 2023-2025, upward trend]

[VISUAL: Pie chart with 3 segments: Product A (50%), Product B (30%), Other (20%)]

[VISUAL: Line graph comparing two metrics over time, one increasing, one flat]
```

---

## 🎨 Color & Style Guidance

### Include at End of Document

```markdown
---

## 📌 Gamma Tips for Best Results

**Color Scheme:**
- Primary: #1e3a5f (navy)
- Accent: #0066cc (blue)
- Success: #28a745 (green)
- Danger: #dc3545 (red)
- Background: White or light gray

**Style:**
- McKinsey-inspired
- Minimal text, maximum impact
- Professional business aesthetic
- Clean, modern fonts

**Key Diagrams to Generate:**
1. Slide 3: Two separate circles for ME concept (blue)
2. Slide 5: Three connected segments for CE concept (green)
3. Slide 8: Tree hierarchy with 4 levels

**Image Style:**
- Professional business settings
- Diverse teams in modern offices
- High quality, not stock-photo generic
```

---

## ✅ Content Optimization

### What Works Well in Gamma

| Element | Format | Example |
|---------|--------|---------|
| Bullet lists | Simple `-` bullets | `- Point one\n- Point two` |
| Numbered lists | `1.` format | `1. First step\n2. Second step` |
| Headers | `##` for slides | `## Key Takeaway` |
| Bold text | `**text**` | `**Important concept**` |
| Tables | Simple markdown | `| A | B |\n|---|---|\n| 1 | 2 |` |

### What to Avoid

| Element | Why | Alternative |
|---------|-----|-------------|
| Complex nested lists | Gamma may flatten | Keep to 2 levels max |
| Code blocks | May not render well | Use plain text |
| LaTeX/math | Limited support | Use words or images |
| Raw HTML | Won't process | Pure markdown only |
| External links | May break | Include in speaker notes |

---

## 📄 Template

```markdown
# [Presentation Title]

A presentation about [topic] for [audience]

---

## [Opening Hook / Title Slide]

[VISUAL: Compelling image related to main theme]

---

## Agenda

1. [Topic 1]
2. [Topic 2]
3. [Topic 3]

[VISUAL: Simple numbered list with icons]

---

## [Content Slide 1]

**Key Point**

- Supporting detail
- Supporting detail

[VISUAL: Relevant diagram or image]

---

## [Content Slide 2]

**Another Key Point**

| Option A | Option B |
|----------|----------|
| Pro 1 | Pro 1 |
| Con 1 | Con 1 |

[VISUAL: Comparison visual]

---

## Key Takeaway

**[One sentence summary]**

[VISUAL: Memorable image that reinforces the message]

---

## 📌 Gamma Tips for Best Results

**Color Scheme:**
- Primary: [hex]
- Accent: [hex]

**Style:** [Description]

**Key Diagrams:**
- Slide X: [description]

**Images:** [Style guidance]
```

---

## 🔄 Workflow

### Step 1: Create Markdown
Use this guide to create `gamma-input.md`

### Step 2: Paste into Gamma
1. Open Gamma
2. Click "Create" → "Paste text"
3. Paste entire markdown content
4. Click "Generate"

### Step 3: Review & Refine
1. Check visual hints generated correctly
2. Adjust any diagrams manually if needed
3. Fine-tune colors to match brand
4. Add/remove slides as needed

---

## 🔗 Related Protocols

- `_output-validation-protocol.md` — Output quality standards
- `_content-density-guidelines.md` — Text limits per slide

---

*Optimized for Gamma.app "Paste text" workflow*




