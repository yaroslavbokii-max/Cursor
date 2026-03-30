# 📊 Quality Score Rubric v1.0

## Purpose
Provide an **objective, measurable** quality score for every output.
Target: **≥80/100** to deliver. Below 80 = iterate.

---

## 🎯 Scoring Categories

| Category | Weight | Max Points |
|----------|--------|------------|
| **Technical Correctness** | 30% | 30 |
| **Visual Quality** | 25% | 25 |
| **Content Quality** | 25% | 25 |
| **User Requirements** | 20% | 20 |
| **TOTAL** | 100% | **100** |

---

## 📋 Detailed Rubric

### 1. Technical Correctness (30 points)

| Criterion | Points | How to Score |
|-----------|--------|--------------|
| **Print CSS Complete** | 10 | `@page { margin: 0 }` + page-break rules + print-color-adjust |
| | | 10 = All present, 5 = Partial, 0 = Missing critical |
| **No Validation Errors** | 10 | Zero critical errors from validation suite |
| | | 10 = 0 errors, 5 = 1-2 errors, 0 = 3+ errors |
| **Data Consistency** | 5 | Percentages sum to 100%, parts sum to totals |
| | | 5 = All consistent, 0 = Any inconsistency |
| **Cross-Browser** | 5 | Works in Chrome, Safari, Firefox |
| | | 5 = All work, 3 = Minor issues, 0 = Broken |

### 2. Visual Quality (25 points)

| Criterion | Points | How to Score |
|-----------|--------|--------------|
| **Layout Consistency** | 8 | Alignment, spacing, margins consistent |
| | | 8 = Perfect, 5 = Minor issues, 2 = Noticeable problems |
| **Typography Hierarchy** | 5 | Clear H1 > H2 > H3 > body distinction |
| | | 5 = Clear hierarchy, 3 = Somewhat clear, 0 = Confusing |
| **Color Usage** | 5 | Brand colors applied correctly, sufficient contrast |
| | | 5 = Perfect, 3 = Minor deviations, 0 = Wrong colors |
| **Chart Quality** | 7 | Follows universal chart rules, labels visible, no overlap |
| | | 7 = Perfect, 4 = Minor issues, 0 = Major problems |

### 3. Content Quality (25 points)

| Criterion | Points | How to Score |
|-----------|--------|--------------|
| **Density Appropriate** | 8 | Within specified words/slide limit |
| | | 8 = Within limit, 4 = Slightly over, 0 = Way over |
| **Actionable Insights** | 7 | "So what" sections present, recommendations clear |
| | | 7 = Strong insights, 4 = Present but weak, 0 = Missing |
| **Structure Logical** | 5 | MECE, flows well, easy to follow |
| | | 5 = Excellent flow, 3 = Okay, 0 = Confusing |
| **Accuracy** | 5 | Facts correct, calculations accurate |
| | | 5 = All accurate, 3 = Minor errors, 0 = Major errors |

### 4. User Requirements (20 points)

| Criterion | Points | How to Score |
|-----------|--------|--------------|
| **All Deliverables Present** | 8 | Every requested output delivered |
| | | 8 = All present, 4 = Missing some, 0 = Missing critical |
| **Audience Appropriate** | 6 | Content matches specified audience level |
| | | 6 = Perfect match, 3 = Somewhat off, 0 = Wrong audience |
| **Format Correct** | 6 | Correct page size, orientation, file type |
| | | 6 = All correct, 3 = Minor issues, 0 = Wrong format |

---

## 📈 Score Interpretation

| Score | Rating | Action |
|-------|--------|--------|
| **90-100** | ⭐⭐⭐⭐⭐ Excellent | Deliver immediately |
| **80-89** | ⭐⭐⭐⭐ Good | Deliver (acceptable) |
| **70-79** | ⭐⭐⭐ Acceptable | Iterate — fix major issues |
| **60-69** | ⭐⭐ Needs Work | Significant revision needed |
| **Below 60** | ⭐ Poor | Major rework required |

---

## 🧮 Quick Score Calculator

```javascript
function calculateQualityScore(output) {
    const scores = {
        technical: {
            printCSS: 0,        // 0-10
            validation: 0,      // 0-10
            dataConsistency: 0, // 0-5
            crossBrowser: 0     // 0-5
        },
        visual: {
            layout: 0,          // 0-8
            typography: 0,      // 0-5
            color: 0,           // 0-5
            charts: 0           // 0-7
        },
        content: {
            density: 0,         // 0-8
            insights: 0,        // 0-7
            structure: 0,       // 0-5
            accuracy: 0         // 0-5
        },
        requirements: {
            deliverables: 0,    // 0-8
            audience: 0,        // 0-6
            format: 0           // 0-6
        }
    };
    
    const technicalTotal = Object.values(scores.technical).reduce((a, b) => a + b, 0);
    const visualTotal = Object.values(scores.visual).reduce((a, b) => a + b, 0);
    const contentTotal = Object.values(scores.content).reduce((a, b) => a + b, 0);
    const requirementsTotal = Object.values(scores.requirements).reduce((a, b) => a + b, 0);
    
    return technicalTotal + visualTotal + contentTotal + requirementsTotal;
}
```

---

## 📝 Score Card Template

Use this template to score any output:

```markdown
## Quality Score Card

**Output:** [filename]
**Date:** [date]
**Agent:** [@agent]

### Technical Correctness (30 pts)
- [ ] Print CSS: __/10
- [ ] Validation: __/10
- [ ] Data Consistency: __/5
- [ ] Cross-Browser: __/5
**Subtotal:** __/30

### Visual Quality (25 pts)
- [ ] Layout: __/8
- [ ] Typography: __/5
- [ ] Color: __/5
- [ ] Charts: __/7
**Subtotal:** __/25

### Content Quality (25 pts)
- [ ] Density: __/8
- [ ] Insights: __/7
- [ ] Structure: __/5
- [ ] Accuracy: __/5
**Subtotal:** __/25

### User Requirements (20 pts)
- [ ] Deliverables: __/8
- [ ] Audience: __/6
- [ ] Format: __/6
**Subtotal:** __/20

---

## **TOTAL SCORE: __/100**

**Rating:** [⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐ / ⭐⭐ / ⭐]
**Decision:** [Deliver / Iterate / Major Rework]
```

---

## 🔄 Integration

### Display in Output
Every HTML output should show quality score in validation panel:

```html
<div class="quality-score">
    <span class="score">87/100</span>
    <span class="rating">⭐⭐⭐⭐</span>
    <span class="status">Ready to deliver</span>
</div>
```

### Store in MEMORY
After each task, log the quality score:

```markdown
### [Date] — [Task]
- **Quality Score:** 87/100 (⭐⭐⭐⭐)
- **Breakdown:** Tech 28/30, Visual 22/25, Content 20/25, Reqs 17/20
- **Decision:** Delivered
```

---

## 🎯 Improvement Targets

| Current Avg | Target | Timeframe |
|-------------|--------|-----------|
| Unknown | 80+ | Immediate |
| 80 | 85+ | 1 week |
| 85 | 90+ | 1 month |

---

*Quality is measurable. Measure it.*




