# 📊 Chart Implementation Guide

## Advanced Chart Types for Business Analysis

This guide covers implementation of specialized charts commonly used in McKinsey-style presentations.

---

## 🌊 Waterfall Charts (Bridge Charts)

### When to Use ✅
- **Revenue/Profit bridges**: "What drove the change from Period A to Period B?"
- **Variance analysis**: Breaking down differences between actual vs budget
- **Contribution analysis**: 3-7 clearly distinct factors contributing to change
- **Story is "bridge"**: When you need to explain A → B with intermediate steps

### When NOT to Use ❌
- **Too many factors**: >7 components become unreadable
- **No clear story**: Just showing random numbers doesn't justify waterfall
- **Forced decomposition**: If breakdown isn't natural (e.g., arbitrary buckets)
- **Simple comparison**: Regular bar chart is clearer for 2-3 values
- **Trend data**: Line chart is better for time series

### Rule: Only Use Waterfall When It Serves the Narrative

**Ask yourself**: Does the "bridge" from A to B tell a compelling story?
- ✅ "Revenue grew from €1M to €1.2M — Price (+€150k) offset by Volume (-€50k) and Mix (+€100k)"
- ❌ "Here are 15 countries and their contributions" → Use bar chart instead

### Implementation with Plotly.js

```javascript
Plotly.newPlot('waterfall-chart', [{
    type: 'waterfall',
    orientation: 'v',  // Use 'h' for horizontal
    x: ['Starting Value', 'Factor A', 'Factor B', 'Factor C', 'Factor D', 'Ending Value'],
    y: [1000, 200, -100, 150, -50, null],  // null for totals
    measure: ['absolute', 'relative', 'relative', 'relative', 'relative', 'total'],
    text: ['€1,000', '+€200', '-€100', '+€150', '-€50', '€1,200'],
    textposition: 'outside',
    connector: { 
        line: { color: 'rgba(255,255,255,0.3)', width: 1 } 
    },
    increasing: { marker: { color: '#34D399' } },  // Green for positive
    decreasing: { marker: { color: '#ef4444' } },  // Red for negative
    totals: { marker: { color: '#3b82f6' } }       // Blue for totals
}], {
    yaxis: { title: 'Value (€)' }
});
```

### Best Practices
1. **Order factors by magnitude** (largest impact first)
2. **Color code**: Green = positive, Red = negative, Blue/Gray = totals
3. **Always show starting and ending values** as anchors
4. **Add annotations** to highlight surprising or critical changes

---

## 📊 Gantt Charts (Timeline Charts)

### When to Use
- **Project timelines**: Campaign schedules, launch plans
- **Resource allocation**: When different activities overlap
- **Historical analysis**: When did different events occur?

### Implementation with Plotly.js

```javascript
// Gantt chart using horizontal bars with offsets
const tasks = [
    { task: 'Campaign A', start: '2026-01-01', end: '2026-01-15', status: 'completed' },
    { task: 'Campaign B', start: '2026-01-10', end: '2026-01-25', status: 'in_progress' },
    { task: 'Campaign C', start: '2026-01-20', end: '2026-02-05', status: 'planned' }
];

const statusColors = {
    completed: '#34D399',
    in_progress: '#f59e0b',
    planned: '#64748b'
};

// Convert to Plotly format
const data = tasks.map(t => ({
    type: 'bar',
    orientation: 'h',
    y: [t.task],
    x: [new Date(t.end) - new Date(t.start)],  // Duration in ms
    base: [new Date(t.start)],
    marker: { color: statusColors[t.status] },
    name: t.task,
    hovertemplate: `<b>${t.task}</b><br>Start: ${t.start}<br>End: ${t.end}<extra></extra>`
}));

Plotly.newPlot('gantt-chart', data, {
    barmode: 'overlay',
    xaxis: { type: 'date', title: 'Timeline' },
    yaxis: { autorange: 'reversed' },  // Top-to-bottom order
    showlegend: false
});
```

### Alternative: Using Shapes for Cleaner Gantt

```javascript
const layout = {
    shapes: tasks.map((t, i) => ({
        type: 'rect',
        x0: t.start,
        x1: t.end,
        y0: i - 0.3,
        y1: i + 0.3,
        fillcolor: statusColors[t.status],
        line: { width: 0 }
    })),
    yaxis: {
        tickvals: tasks.map((_, i) => i),
        ticktext: tasks.map(t => t.task)
    },
    xaxis: { type: 'date' }
};
```

---

## ⚠️ Chart Alignment Rules (CRITICAL)

### Axis Tick Values — ROUND NUMBERS ONLY

**CRITICAL RULE**: Axis ticks must use round, evenly-spaced numbers. NEVER use actual data values as ticks.

**BAD Example** (actual data values as ticks):
```javascript
// X-axis shows: 30, 417, 491, 1098, 1484...
// This looks terrible and unprofessional!
xaxis: { tickmode: 'linear' }  // Don't use without dtick!
```

**GOOD Example** (round numbers):
```javascript
xaxis: {
    dtick: 1000,           // Ticks at 0, 1000, 2000, 3000...
    tickformat: ',d',      // Adds thousand separators
    range: [0, 6000]       // Clean bounds
}

// For percentages:
xaxis: {
    dtick: 20,             // Ticks at -60, -40, -20, 0, 20, 40
    range: [-70, 60]       // Symmetric for diverging data
}

// For large numbers, use K/M suffix:
yaxis: {
    dtick: 10000,
    tickformat: '~s'       // Shows 10K, 20K, 30K...
}
```

### Bar Chart Starting Position — ALWAYS FROM ZERO

**Problem**: Bars don't start from zero, creating weird gaps.

**Solution**: Ensure x-axis range starts at 0 for horizontal bars:
```javascript
xaxis: {
    range: [0, maxValue * 1.1],  // Start at zero, add 10% for labels
    zeroline: true
}
```

### Y-Axis Title Positioning

**Problem**: Rotated 90° Y-axis titles are hard to read.

**Solution**: Use horizontal titles above the axis or with standoff:

```javascript
yaxis: {
    title: {
        text: 'Revenue (€)',
        standoff: 20,  // Adds padding between title and axis
        font: { size: 13 }
    }
}
```

### Baseline/Reference Lines

**Problem**: Reference lines crossing through data labels.

**Solution**: Position annotation labels ABOVE the line, not on it:

```javascript
shapes: [{
    type: 'line',
    x0: -0.5, x1: 10.5,
    y0: 3, y1: 3,
    line: { color: '#f59e0b', width: 2, dash: 'dash' }
}],
annotations: [{
    x: 10,
    y: 3.5,  // Position ABOVE the line value (3)
    text: 'Target: 3.0x',
    showarrow: false,
    font: { color: '#f59e0b' },
    xanchor: 'right'  // Align to right edge
}]
```

### Data Labels Positioning

**Problem**: Labels overlapping with bars or axes.

**Solution**: Use `textposition: 'outside'` and ensure sufficient range:

```javascript
{
    text: values.map(v => `€${v.toLocaleString()}`),
    textposition: 'outside',
    textfont: { size: 12 }
},
// In layout:
yaxis: {
    range: [0, maxValue * 1.15]  // Add 15% headroom for labels
}
```

### Bar-Axis Spacing

**Problem**: Bar labels touching or merging with axis.

**Solution**: Add margins and auto-margin:

```javascript
margin: { l: 120, r: 40, t: 40, b: 60 },
yaxis: {
    automargin: true  // Plotly auto-adjusts for long labels
}
```

---

## 🎨 Chart Type Selection Framework

| Question Type | Best Chart | Why |
|--------------|------------|-----|
| What changed? (A→B) | **Waterfall** | Shows contribution of each factor |
| When did things happen? | **Gantt/Timeline** | Visualizes duration and overlap |
| How much of each? | **Bar/Column** | Direct comparison |
| What's the trend? | **Line** | Shows direction over time |
| What's the composition? | **Stacked Bar** | Shows parts of whole |
| How do things compare? | **Horizontal Bar** | Easy label reading |
| What's the distribution? | **Histogram/Box** | Shows spread and outliers |
| What's the relationship? | **Scatter** | Correlation between variables |

---

## 📱 Responsive & Print Considerations

### For Interactive HTML
```javascript
Plotly.newPlot('chart', data, layout, {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ['lasso2d', 'select2d']
});
```

### For Print/PDF
```javascript
// Add print-specific layout
const printLayout = {
    ...layout,
    paper_bgcolor: 'white',
    plot_bgcolor: 'white',
    font: { color: 'black' }
};
```

---

## 🚫 Annotation Anti-Patterns — ARROWS & OVERLAPS

### NEVER Let Arrows Cross Chart Elements

**Problem**: Arrows highlighting trends cross bars, text, or other elements.

**Bad Practice**:
```javascript
// Arrow crosses through bars to reach target
annotations: [{
    x: 3, y: 32000,
    ax: -100, ay: 0,  // This line may cross bars!
    text: '↑ Growing!',
    arrowhead: 2
}]
```

**Good Practice**: Position annotations in CLEAR SPACE only:
```javascript
// Position annotation entirely above/beside chart elements
annotations: [{
    x: 3, 
    y: 35000,           // Above the highest bar
    xanchor: 'center',
    yanchor: 'bottom',
    text: '<b>+10% Growth</b>',
    showarrow: false,   // No arrow if it would cross elements
    font: { size: 12, color: '#10B981' }
}]
```

### Rule: If No Clean Space, Skip the Annotation

**Decision tree**:
1. Is there clear space near the element to annotate? → Add annotation
2. Would arrow/line cross other data? → **SKIP IT** or use text-only annotation
3. Multiple elements to highlight? → Use color coding instead of multiple arrows

### Better Alternatives to Arrows

| Instead of... | Use... |
|---------------|--------|
| Arrow crossing bars | Color the bar + text label above |
| Arrow to highlight trend | Bold text annotation in clear space |
| Multiple arrows | Conditional bar coloring (green/red) |
| Arrow pointing at number | Put number in bold/larger font |

---

## 🔧 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Y-axis title cut off | Insufficient margin | Increase `margin.l` |
| Labels overlap bars | Range too tight | Add 15% to `yaxis.range` |
| Reference line crosses labels | Label at line level | Position label above/below line |
| Bars touch axis labels | No margin | Set `automargin: true` |
| Colors inconsistent | Hardcoded per chart | Use CSS variables or color object |
| Hover text ugly | Default template | Customize `hovertemplate` |
| **Axis shows data values** | Missing dtick | Set `dtick` to round number (100, 1000, etc.) |
| **Bars don't start at zero** | Wrong range | Set `range: [0, max * 1.1]` |
| **Arrows cross bars** | Poor positioning | Skip arrow, use color/text instead |

---

*Last updated: January 2026 | Based on ad revenue analysis learnings*

