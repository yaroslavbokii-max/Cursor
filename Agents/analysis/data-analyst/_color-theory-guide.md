# 🎨 Color Theory for Data Visualization

## Core Principle: Contrast is King

The #1 rule: **Every element must have sufficient contrast against its background.**

---

## High-Contrast Combinations (USE THESE)

### On White/Light Background (#FFFFFF, #FAFAFB)
| Element | Recommended Color | Hex | Why |
|---------|------------------|-----|-----|
| Primary text | Dark gray | `#1F2937` | High contrast, easier than pure black |
| Secondary text | Medium gray | `#6B7280` | Clearly subordinate |
| Positive values | Green | `#10B981` | Strong contrast, universally "good" |
| Negative values | Red | `#EF4444` | High contrast, universally "bad" |
| Neutral bars | Gray | `#6B7280` | Doesn't compete for attention |
| Highlight/accent | Blue | `#3B82F6` | Distinct from pos/neg |
| Baseline/reference | Dark gray | `#374151` | Visible but not dominant |
| Grid lines | Light gray | `#E5E7EB` | Subtle, doesn't distract |

### On Dark Background (IF user explicitly requests)
| Element | Recommended Color | Hex | Why |
|---------|------------------|-----|-----|
| Primary text | White | `#F8FAFC` | Maximum contrast |
| Secondary text | Light gray | `#9CA3AF` | Readable but subordinate |
| Positive values | Bright green | `#34D399` | Pops on dark |
| Negative values | Bright red | `#F87171` | Pops on dark |
| Neutral bars | Medium gray | `#9CA3AF` | Visible |
| Baseline/reference | White or bright | `#F8FAFC` | Must be visible! |

---

## Low-Contrast Combinations (AVOID)

| Combination | Problem |
|-------------|---------|
| Orange on dark (#F59E0B on #1a1a2e) | Low contrast, hard to read |
| Light gray on white (#E5E7EB on #FFFFFF) | Nearly invisible |
| Yellow anywhere | Generally low contrast |
| Red on dark (#EF4444 on #1a1a2e) | Vibrates, hard to read |
| Light green on white (#A7F3D0 on #FFFFFF) | Too subtle |

---

## Reference Lines & Baselines

**CRITICAL: Reference lines must be highly visible.**

### Good Practice
```javascript
shapes: [{
    line: { 
        color: '#374151',  // Dark gray - visible on white
        width: 2,
        dash: 'dash'
    }
}],
annotations: [{
    y: baselineValue + 0.3,  // ABOVE the line
    text: 'Target',
    font: { color: '#374151' }
}]
```

### Bad Practice
- Orange dashed line on dark background (invisible)
- Thin 1px lines (too subtle)
- Annotation text ON the line (crossing data)

---

## Bar Chart Colors

### Principle: Color = Meaning

```javascript
// Color by performance, not arbitrary
marker: {
    color: data.map(d => {
        if (d.change > 20) return '#10B981';      // Strong positive = green
        if (d.change > 0) return '#6EE7B7';       // Mild positive = light green
        if (d.change > -20) return '#FCA5A5';     // Mild negative = light red
        return '#EF4444';                          // Strong negative = red
    })
}
```

### Highlight Strategy
- **One standout item:** Make it green/blue, rest gray
- **Comparison:** Green for above target, red for below
- **Ranking:** Gradient from dark to light (not rainbow)

---

## Typography Contrast

| Use Case | Font Weight | Size | Color |
|----------|-------------|------|-------|
| Card title | 700 (bold) | 18px | #1F2937 |
| Subtitle/insight | 500 | 14px | #10B981 (accent) |
| Body text | 400 | 14px | #1F2937 |
| Muted/secondary | 400 | 13px | #6B7280 |
| Labels (axis) | 400 | 11-12px | #6B7280 |
| Data labels | 500-600 | 11-12px | #1F2937 |

---

## Accessibility Checklist

- [ ] Contrast ratio ≥ 4.5:1 for text
- [ ] Contrast ratio ≥ 3:1 for large text/graphics
- [ ] Don't rely on color alone (add patterns/labels)
- [ ] Test with colorblind simulation

### Tools
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Colorblind Simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/)

---

## Quick Reference: Bolt Brand on White

```css
:root {
    --bg-page: #FAFAFB;
    --bg-card: #FFFFFF;
    --text-primary: #1F2937;
    --text-secondary: #6B7280;
    --accent-green: #10B981;
    --accent-red: #EF4444;
    --accent-blue: #3B82F6;
    --accent-amber: #F59E0B;
    --border: #E5E7EB;
    --baseline: #374151;
}
```

---

*Last updated: January 2026 | Based on dashboard feedback*




