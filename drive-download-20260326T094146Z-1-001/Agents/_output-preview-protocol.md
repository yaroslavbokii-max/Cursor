# Output Preview Protocol

> **Version:** 1.0  
> **Created:** 2026-01-13  
> **Purpose:** Catch direction issues early with quick low-fidelity previews before full generation

---

## 🎯 Core Principle

**Don't build the whole house before checking the blueprint.**

Preview mode saves time by validating direction before investing in full output.

---

## 🚦 When to Offer Preview

| Task Type | Offer Preview? | Why |
|-----------|---------------|-----|
| Presentation (5+ slides) | ✅ Yes | Structure matters |
| Workshop materials | ✅ Yes | Multiple components |
| Complex analysis | ✅ Yes | Direction validation |
| Report (3+ pages) | ✅ Yes | Narrative structure |
| Simple document | ❌ No | Faster to just do it |
| Quick lookup | ❌ No | No structure to preview |

---

## 📋 Preview Format by Output Type

### Presentation Preview

```markdown
## 📑 Presentation Preview (10 slides)

**Title:** [Presentation title]
**Audience:** [Target audience]
**Duration:** [Estimated time]

### Slide Structure:

1. **Opening** — Hook + agenda
2. **Context** — Current situation
3. **Problem** — Key challenge
4. **Framework** — Analytical approach
5. **Finding 1** — [Key insight]
6. **Finding 2** — [Key insight]
7. **Finding 3** — [Key insight]
8. **Implications** — So what?
9. **Recommendations** — Next steps
10. **Close** — Call to action

### Visual Approach:
- Diagrams: [List key diagrams]
- Charts: [List chart types]
- Style: [McKinsey/Balanced/Detailed]

---

**✅ Approve & Build** | **✏️ Adjust Structure** | **🔄 Start Over**
```

### Workshop Preview

```markdown
## 🎓 Workshop Preview (60 min)

**Topic:** [Workshop topic]
**Audience:** [Participants]
**Format:** [In-person/Virtual]

### Flow:

| Time | Section | Activity |
|------|---------|----------|
| 0-5 min | Opening | Icebreaker + objectives |
| 5-25 min | Theory | [Key concepts covered] |
| 25-55 min | Practice | [Exercise descriptions] |
| 55-60 min | Close | Summary + Q&A |

### Deliverables:
- [ ] Presentation slides (X slides)
- [ ] Exercise worksheets (X exercises)
- [ ] Cheatsheet (1 page)
- [ ] Facilitator guide

### Key Diagrams:
- [Diagram 1 description]
- [Diagram 2 description]

---

**✅ Approve & Build** | **✏️ Adjust Flow** | **🔄 Start Over**
```

### Analysis Preview

```markdown
## 📊 Analysis Preview

**Question:** [Core question being answered]
**Data:** [Data sources]
**Approach:** [Methodology]

### Analysis Structure:

1. **Data Quality Check** — Validate inputs
2. **Descriptive Analysis** — What happened?
3. **Diagnostic Analysis** — Why did it happen?
4. **Hypothesis Testing** — [List hypotheses]
5. **Findings** — Key insights
6. **Recommendations** — Actions

### Expected Outputs:
- Summary document
- [X] visualizations
- Recommendation deck

### Assumptions:
- [List key assumptions]

---

**✅ Approve & Analyze** | **✏️ Adjust Scope** | **🔄 Start Over**
```

---

## 🔄 Preview Workflow

```
User Request
    │
    ▼
┌─────────────────────┐
│ Should offer        │
│ preview?            │──No──▶ Direct to full build
│ (check criteria)    │
└─────────────────────┘
    │ Yes
    ▼
┌─────────────────────┐
│ Generate preview    │
│ (structure only)    │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ User reviews        │
│                     │
│ ✅ Approve          │──▶ Full build
│ ✏️ Adjust           │──▶ Modify preview → Re-review
│ 🔄 Start Over       │──▶ Back to discovery
└─────────────────────┘
```

---

## ⏱️ Time Investment

| Mode | Preview Time | Build Time | Total | Best When |
|------|--------------|------------|-------|-----------|
| With Preview | 2 min | 15 min | 17 min | Direction uncertain |
| Without Preview | 0 min | 20 min | 20 min | Clear requirements |
| Rework (no preview) | 0 min | 35 min | 35 min | Got it wrong first try |

**Preview ROI:** Spend 2 minutes to potentially save 15+ minutes of rework.

---

## 💬 Offering Preview

```markdown
"Before I build the full [output type], want a quick preview of the structure?

🔍 **Preview** (~2 min) — See the outline, adjust before I build
⚡ **Skip** — I'll build it directly based on what you told me

[Recommended: Preview — helps catch direction issues early]"
```

---

## 🔗 Related Protocols

- `_output-validation-protocol.md` — Post-build validation
- `_content-density-guidelines.md` — Density options to show in preview




