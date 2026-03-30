# Universal Chart Quality Rules

**Version:** 4.0  
**Status:** MANDATORY for all visualization-generating agents  
**Referenced by:** @data-analyst, @data-visualization-expert, @presentation-maker  
**Last Updated:** January 14, 2026 (v8 dashboard learnings)  

---

## 🏆 Standard: World Championship-Winning Visualizations

These rules are based on:
- Information is Beautiful Awards winning entries
- McKinsey & BCG visualization standards
- Edward Tufte's principles
- Stephen Few's dashboard design guidelines
- Google Material Design data visualization

---

## 📐 RULE 1: All Charts Start From Zero

### Why
Starting from non-zero exaggerates differences and misleads viewers.

### Application

| Chart Type | Rule | Exception |
|------------|------|-----------|
| Bar (horizontal) | Y-axis = 0 | Never |
| Column (vertical) | Y-axis = 0 | Never |
| Line chart | Y-axis = 0 | Log scale (must label) |
| Area chart | Y-axis = 0 | Never |
| Waterfall | Starts from absolute value | By design |
| Scatter | Can start non-zero | When 0 is meaningless (e.g., year) |

### Implementation (Plotly)
```javascript
yaxis: {
    rangemode: 'tozero',  // Forces start from 0
    range: [0, maxValue * 1.15]  // 15% headroom for labels
}
```

### Validation Check
```
□ Does the axis start at 0?
□ If not, is there explicit justification?
□ Is the non-zero start clearly labeled?
```

---

## 📐 RULE 2: Axis Ticks = Round Numbers ONLY

### Why
Data values as ticks (417, 1266, -59) look unprofessional and are hard to read.

### The Rule
Ticks must be evenly spaced round numbers:
- **Powers of 10:** 0, 10, 100, 1000, 10000...
- **Fives:** 0, 5, 50, 500, 5000...
- **Twos:** 0, 2, 20, 200, 2000... (for small ranges)
- **Percentages:** -60%, -40%, -20%, 0%, 20%, 40%, 60%

### Implementation (Plotly)
```javascript
// For values 0-6000:
xaxis: { dtick: 1000 }  // Shows 0, 1k, 2k, 3k, 4k, 5k, 6k

// For percentages -70% to +60%:
xaxis: { dtick: 20, range: [-80, 80] }  // Shows -80, -60, -40, -20, 0, 20, 40, 60, 80

// For large numbers with K/M suffix:
yaxis: { dtick: 10000, tickformat: '~s' }  // Shows 10K, 20K, 30K...
```

### Common dtick Values

| Value Range | Recommended dtick |
|-------------|-------------------|
| 0-10 | 2 |
| 0-50 | 10 |
| 0-100 | 20 |
| 0-500 | 100 |
| 0-1000 | 200 |
| 0-5000 | 1000 |
| 0-10000 | 2000 |
| 0-50000 | 10000 |
| 0-100000 | 20000 |

### Validation Check
```
□ Are all tick values round numbers?
□ Are ticks evenly spaced?
□ Is the tick interval appropriate for the range?
```

---

## 📐 RULE 3: All Labels Must Fit (No Truncation)

### Why
Truncated labels ("€47.7..." or "€5,0") are unacceptable in professional visualizations.

### The Rule
- Add 15-20% headroom above highest value
- Use `automargin: true` for axis labels
- Test with longest expected label

### Implementation (Plotly)
```javascript
layout: {
    margin: { t: 60, r: 60, b: 60, l: 100 },  // Generous margins
    yaxis: {
        automargin: true,  // Auto-adjust for long labels
        range: [0, maxValue * 1.2]  // 20% headroom
    }
},
trace: {
    textposition: 'outside',  // Labels outside bars
    cliponaxis: false  // Don't clip labels at axis
}
```

### Validation Check
```
□ Is every label fully visible?
□ Is there headroom above the tallest bar/column?
□ Are axis labels not cut off?
□ Do multi-line labels have space?
```

---

## 📐 RULE 4: Diverging Data Needs Special Treatment

### What is Diverging Data?
Data with both positive AND negative values (e.g., +43%, -59%, +27%, -7%)

### The Rule
- Must show **zero baseline clearly**
- Use **horizontal bar chart** (easier to read + and -)
- Center the zero line
- **Green** for positive, **Red** for negative

### Implementation (Plotly)
```javascript
// Horizontal diverging bar chart
Plotly.newPlot('chart', [{
    type: 'bar',
    orientation: 'h',
    x: [43, 43, 42, 35, 27, 23, 19, 14, -2, -3, -5, -7, -53],
    y: ['Portugal', 'Romania', 'Malta', 'Lithuania', 'Estonia', 'Cyprus', 
        'Slovakia', 'Georgia', 'Bulgaria', 'Kenya', 'Ukraine', 'Azerbaijan', 'Latvia'],
    marker: {
        color: data.map(v => v >= 0 ? '#10B981' : '#EF4444')
    }
}], {
    xaxis: {
        zeroline: true,
        zerolinewidth: 2,
        zerolinecolor: '#374151',
        dtick: 20,
        range: [-70, 60]
    }
});
```

### Wrong Choices for Diverging Data
- ❌ Vertical column chart (hard to scan + and -)
- ❌ Pie chart (can't show negative)
- ❌ Stacked bar (confusing)

### Validation Check
```
□ Is zero baseline clearly visible?
□ Are positive/negative colors consistent (green/red)?
□ Is horizontal orientation used for diverging data?
```

---

## 📐 RULE 5: Reference Lines at Correct Position

### Why
A baseline at 3.0x should visually BE at the 3.0 position, not floating randomly.

### The Rule
- Reference line Y position = the actual value
- Label positioned ABOVE the line (not on it)
- Use high-contrast color (dark gray on white)
- Line should clearly show which bars pass/fail threshold

### Implementation (Plotly)
```javascript
shapes: [{
    type: 'line',
    x0: -0.5, x1: 1.5,  // Span full chart width
    y0: 3.0, y1: 3.0,   // ACTUAL position
    line: { color: '#374151', width: 2, dash: 'dash' }
}],
annotations: [{
    x: 1.5,
    y: 3.3,  // Slightly ABOVE the line
    xanchor: 'right',
    text: 'Target: 3.0x',
    showarrow: false,
    font: { color: '#374151', size: 11 }
}]
```

### Validation Check
```
□ Is the line at the correct Y value?
□ Is the label not overlapping data?
□ Can you clearly see which bars are above/below?
□ Does the baseline make visual sense?
```

---

## 📐 RULE 6: Grid Lines — Minimal by Default

### The Rule
Less is more. Grid should help read values, not add visual noise.

### Grid Line Guidelines

| Chart Type | Horizontal Grid | Vertical Grid |
|------------|-----------------|---------------|
| Line chart | ✅ Light | ❌ None |
| Bar (horizontal) | ❌ None or very light | ❌ None |
| Column (vertical) | ✅ Light | ❌ None |
| Scatter plot | ✅ Light | ✅ Light |
| Pie/Donut | ❌ Never | ❌ Never |
| Heatmap | ❌ None | ❌ None |
| Area chart | ✅ Light | ❌ None |

### Implementation (Plotly)
```javascript
xaxis: {
    showgrid: false,  // No vertical grid
    zeroline: true,
    zerolinecolor: '#E5E7EB'
},
yaxis: {
    showgrid: true,
    gridcolor: '#F3F4F6',  // Very light gray
    gridwidth: 1
}
```

### Validation Check
```
□ Does the grid help or add noise?
□ Is vertical grid removed (unless scatter)?
□ Is grid color light enough to not compete with data?
```

---

## 📐 RULE 7: Readable Y-Axis Labels

### The Rule
- Horizontal text preferred
- If must rotate, add spacing with `standoff`
- Font size ≥ 11px
- Use abbreviations (K, M, B) for large numbers

### Implementation (Plotly)
```javascript
yaxis: {
    title: {
        text: 'Revenue (€)',
        standoff: 20,  // Space between title and axis
        font: { size: 13 }
    },
    tickfont: { size: 11 },
    tickformat: '~s'  // Auto K/M/B suffix
}
```

### Validation Check
```
□ Can the Y-axis title be read without tilting head?
□ Is there enough space between title and numbers?
□ Are tick labels not cramped?
```

---

## 📐 RULE 8: Eye-Tracking Grid for Multi-Item Charts

### Why
When a chart has many bars (10+), the eye loses track connecting a bar to its label. Horizontal grid lines act as "tramlines" guiding the eye.

### The Rule
- **5 or fewer items:** Grid optional
- **6-10 items:** Light horizontal grid recommended
- **10+ items:** Horizontal grid REQUIRED

### Implementation (Plotly)
```javascript
// For horizontal bar charts with many items
yaxis: {
    showgrid: true,
    gridcolor: '#F3F4F6',  // Very light, almost invisible
    gridwidth: 1,
    dtick: 1  // Grid line at each row
}
```

### Alternative: Alternating Row Shading
For very dense charts, consider alternating background:
```javascript
shapes: countries.map((c, i) => ({
    type: 'rect',
    x0: 0, x1: 1, y0: i - 0.5, y1: i + 0.5,
    xref: 'paper', yref: 'y',
    fillcolor: i % 2 === 0 ? '#FAFAFA' : 'white',
    line: { width: 0 }
}))
```

### Validation Check
```
□ Can you easily trace from bar end to label?
□ If 10+ items, is there a grid or shading?
□ Is grid light enough to not compete with data?
```

---

## 📐 RULE 9: No Element Crossing (CRITICAL)

### Why
Elements crossing each other (labels crossing baselines, arrows crossing bars) looks unprofessional and confuses the viewer.

### The Rule
**NEVER allow any element to cross another:**
- ❌ Data labels crossing reference lines
- ❌ Arrows crossing bars or text
- ❌ Annotations overlapping data points
- ❌ Pie chart labels overlapping each other

### Prevention Strategies

**For data labels near reference lines:**
```javascript
// If bar value is close to baseline, position label INSIDE
text: values.map((v, i) => {
    // If value within 15% of baseline, put label inside
    return Math.abs(v - baseline) < baseline * 0.15 ? 'inside' : 'outside';
});
```

**For pie chart labels:**
```javascript
// Use leader lines for small segments
textposition: 'outside',
textinfo: 'label',
pull: [0.02, 0, 0, 0]  // Pull small segments outward
```

**For annotations:**
```javascript
// Position in clear space only
annotations: [{
    x: 1.1,  // Slightly outside chart area
    y: targetValue + offset,  // Above/below, not ON
    xanchor: 'left',
    showarrow: false
}]
```

### Validation Check
```
□ Are ANY elements crossing each other?
□ If data value ≈ baseline, is label repositioned?
□ Are pie chart labels separated with leader lines?
□ Are annotations in clear space?
```

---

## 📐 RULE 10: Data Consistency Protocol (MBB Standard)

### Why
Inconsistent data (showing €32k total but €93k in breakdown) destroys credibility instantly.

### The Rule
1. **Single Source of Truth:** All charts in a report use SAME underlying data
2. **Period Stated Clearly:** Always show analysis period prominently
3. **Totals Must Match:** Sum of breakdown = overall total
4. **Footnotes Required:** Every chart has data source + period

### Implementation

**Dashboard/Report Header:**
```html
<!-- Period banner at top -->
<div class="period-banner">
    📅 Analysis Period: Week 50 (Dec 8-14, 2025) vs Week 49 (Dec 1-7, 2025)
    All figures in this report are for W50 unless otherwise noted
</div>
```

**Chart Footnotes:**
```html
<div class="chart-footnote">
    Source: Ads Dashboard | Period: Week 50 (Dec 8-14, 2025) | n=15 countries | Total: €29,048
</div>
```

**Pre-Generation Consistency Check:**
```javascript
// Before generating visualizations
const total = countries.reduce((sum, c) => sum + c.revenue, 0);
const segmentTotal = segments.reduce((sum, s) => sum + s.revenue, 0);

console.assert(
    Math.abs(total - segmentTotal) < 1,
    `Data inconsistency: Country total (${total}) ≠ Segment total (${segmentTotal})`
);
```

### MBB Footnote Standard
Every professional slide includes:
- **Source:** Where data comes from
- **Period:** Time frame
- **Sample:** n= count
- **Notes:** Any caveats or exclusions

### Validation Check
```
□ Is analysis period stated at top of report?
□ Do all breakdowns sum to the same total?
□ Does every chart have a footnote?
□ Are time periods consistent across all charts?
```

---

## 📐 RULE 11: Consistent Section Headers (v6)

### Why
Inconsistent headers (some with icons, some without) look sloppy and unprofessional.

### The Rule
**ALL sections MUST use identical header structure:**
- Format: `[Icon] [Section Title]`
- Same font size/weight across all section headers
- Same spacing between icon and title

### Validation Check
```
□ Do ALL sections have icons + titles?
□ Is spacing consistent?
□ Same font size/weight across all section headers?
```

---

## 📐 RULE 12: Subtitles = Takeaways (v6)

### Why
Subtitles are prime real estate. Readers often only scan subtitles.

### The Rule
Card/chart subtitles MUST be the main takeaway, NOT a description.

| ❌ Bad Subtitle | ✅ Good Subtitle |
|-----------------|------------------|
| "Revenue by Country (W50)" | "Portugal leads with 17%, but 3 markets = concentration risk" |
| "Week-over-Week Change" | "Latvia's -53% crash nearly erased all gains" |

### Validation Check
```
□ Is every subtitle an insight/takeaway?
□ Could the subtitle stand alone as a finding?
□ NO subtitles that just describe chart content?
```

---

## 📐 RULE 13: Pie/Donut Labels — Smart Legend Fallback (v8)

### Why
Inline labels on pie charts are prone to overlap, cramping, and boundary overflow. After extensive testing, using a **horizontal HTML legend** provides the cleanest, most reliable solution.

### The Rule (Updated v8)
**PREFERRED APPROACH: Hide inline labels, use horizontal legend**

This eliminates ALL label positioning issues permanently:
- ✅ No overlap possible
- ✅ No truncation
- ✅ No boundary overflow
- ✅ Consistent formatting always
- ✅ Works with any number of segments

### Implementation — PRIMARY (v8)
```javascript
// ✅ v8 BEST PRACTICE: No inline labels + HTML legend
Plotly.newPlot('chart', [{
    values: [14831, 12302, 1509, 406],
    labels: ['Mid-Market', 'SMB', 'National Chain', 'Int\'l Chain'],
    type: 'pie',
    hole: 0.5,  // Donut
    
    // ✅ KEY: NO inline labels — use HTML legend
    textinfo: 'none',
    
    hovertemplate: '<b>%{label}</b><br>€%{value:,.0f} (%{percent})<extra></extra>',
    
    marker: {
        colors: ['#3B82F6', '#10B981', '#6B7280', '#EF4444'],
        line: { color: 'white', width: 2 }
    }
}], {
    showlegend: false,  // Using custom HTML legend
    margin: { t: 30, r: 30, b: 30, l: 30 }
});
```

Then add HTML legend below:
```html
<div class="chart-legend">
    <div class="legend-item"><div class="legend-color" style="background: #3B82F6;"></div>Mid-Market: €14,831 (51%)</div>
    <div class="legend-item"><div class="legend-color" style="background: #10B981;"></div>SMB: €12,302 (42%)</div>
    <div class="legend-item"><div class="legend-color" style="background: #6B7280;"></div>National Chain: €1,509 (5%)</div>
    <div class="legend-item"><div class="legend-color" style="background: #EF4444;"></div>Int'l Chain: €406 (1%)</div>
</div>
```

CSS for legend:
```css
.chart-legend {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-top: 16px;
    flex-wrap: wrap;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
}
.legend-color {
    width: 12px;
    height: 12px;
    border-radius: 2px;
}
```

### Alternative: Outside Labels (use only if 2-3 large segments)
Only use this for simple pies with 2-3 large, well-spaced segments:
```javascript
// ⚠️ ONLY for simple pies with 2-3 large segments
textposition: 'outside',
textinfo: 'label',
pull: [0.02, 0.02],  // Pull segments slightly
```

### Legend Format Best Practice
Include category + value + percentage:
- ✅ `"Mid-Market: €14,831 (51%)"`
- ❌ `"Mid-Market 51%"` — Missing absolute value

### Validation Check
```
□ Is pie using HTML legend (preferred)?
□ If using inline labels: only 2-3 large segments?
□ NO overlapping labels?
□ NO truncated labels?
□ NO labels outside boundaries?
□ Legend has color + label + value + percentage?
```

---

## 📐 RULE 14: Section Dividers & Breathing Room (v6)

### Why
Dense reports need visual breathing room.

### The Rule
- Major sections must have visual dividers
- Top of document cannot be too condensed
- Consistent spacing between sections

### Validation Check
```
□ Are major sections visually separated?
□ Is spacing consistent between sections?
□ Is the top of document not too condensed?
```

---

## 📐 RULE 15: Hypothesis Section — Complete (v6)

### Why
Shows analytical rigor and complete hypothesis testing.

### The Rule
Hypothesis section must include ALL tested hypotheses (minimum 4):
- **H0:** User's original hypothesis
- **H1-H3:** Generated alternative hypotheses
- Each with: Text, Evidence, Verdict (Supported/Partial/Rejected)
- Color coded: Green (supported), Amber (partial), Red (rejected)

### Validation Check
```
□ At least 4 hypotheses shown?
□ Each has text, evidence, and verdict?
□ Distinct from Devil's Advocate section?
□ Using color coding for verdicts?
```

---

## 📐 RULE 16: Semantic Header Positioning (v7)

### Why
Header placement follows visual semantics — different content types benefit from different structures.

### The Rule
**Headers are positioned based on content type:**

| Content Type | Header Position | Rationale |
|--------------|-----------------|-----------|
| **Charts/Visualizations** | Header **OUTSIDE** white card | Header labels the data; card contains just the visual |
| **Text/Narrative** (insights, actions, recommendations) | Header **INSIDE** styled container | Header + content form one cohesive message block |

### Visual Language
- 📊 **Data sections** (charts, KPIs, metrics): External header → "Look at this data"
- 💬 **Narrative sections** (hypothesis, insights, actions, devil's advocate): Internal header → "Read this content block"

### Implementation Example

**Chart Section (header OUTSIDE):**
```html
<section class="chart-section">
    <div class="section-header">
        <span class="section-icon">🌍</span>
        <h2 class="section-title">Breakdown by Country</h2>
    </div>
    <div class="card">
        <div class="card-header">
            <h3 class="card-title">Revenue by Country</h3>
            <p class="card-subtitle">Portugal leads with 17%...</p>
        </div>
        <div id="chart"></div>
    </div>
</section>
```

**Text Section (header INSIDE):**
```html
<section class="text-section">
    <div class="insights-box">
        <div class="section-header">
            <span class="section-icon">💡</span>
            <h2 class="section-title">Top 3 Insights</h2>
        </div>
        <div class="content">...</div>
    </div>
</section>
```

### Standard Classifications

| Section | Type | Header Position |
|---------|------|-----------------|
| KPIs | Data | OUTSIDE |
| By Country | Data | OUTSIDE |
| By Segment | Data | OUTSIDE |
| Trends | Data | OUTSIDE |
| Deep Dives | Data | OUTSIDE |
| Hypothesis Testing | Text | INSIDE |
| Top Insights | Text | INSIDE |
| Devil's Advocate | Text | INSIDE (red border) |
| Actions | Text | INSIDE |
| Suggested Next Steps | Text | INSIDE (blue gradient) |

### Validation Check
```
□ Are chart sections using external headers?
□ Are text/narrative sections using internal headers?
□ Is the pattern consistent throughout the document?
□ Does the visual language make semantic sense?
```

---

## 📐 RULE 17: Smart Label Positioning Near Baselines (v8)

### Why
When data labels are positioned OUTSIDE bars but sit near a reference line, they cross the line — looking unprofessional. The label must be repositioned to avoid crossing ANY other element.

### The Rule
**If bar value is BELOW the baseline:**
- Position label **INSIDE** the bar (with white text)
- This prevents the label from crossing the baseline

**If bar value is ABOVE the baseline:**
- Position label **OUTSIDE** the bar (with dark text)
- Label is in clear space, no crossing possible

### Implementation (Plotly) — v8 Fix
```javascript
// Example: ROAS chart with 3.0x baseline
const baseline = 3.0;
const values = [2.7, 5.5];  // Home Screen, Search

Plotly.newPlot('chart', [{
    y: ['Home Screen', 'Search Result'],
    x: values,
    type: 'bar',
    orientation: 'h',
    marker: { color: values.map(v => v < baseline ? '#EF4444' : '#10B981') },
    
    // ✅ KEY: Smart positioning based on value vs baseline
    text: values.map(v => `${v}x`),
    textposition: values.map(v => v < baseline ? 'inside' : 'outside'),
    textfont: {
        size: 14,
        // ✅ White text for inside, dark for outside
        color: values.map(v => v < baseline ? 'white' : '#1F2937')
    },
    insidetextanchor: 'end',  // Align inside text to right edge
    cliponaxis: false
}], {
    shapes: [{
        type: 'line',
        x0: baseline, x1: baseline,
        y0: -0.5, y1: 1.5,
        line: { color: '#374151', width: 2, dash: 'dash' }
    }]
});
```

### Visual Result
- **Bar at 2.7x** (below 3.0 baseline): Label "2.7x" appears **inside** bar in white
- **Bar at 5.5x** (above 3.0 baseline): Label "5.5x" appears **outside** bar in dark gray
- **Baseline at 3.0x**: Clearly visible, no crossings

### Generalized Formula
```javascript
// For any bar chart with reference line
const shouldLabelInside = (value) => {
    // Inside if value is within 20% below baseline
    return value < baseline && value > baseline * 0.5;
};

textposition: values.map(v => shouldLabelInside(v) ? 'inside' : 'outside');
textfont: { color: values.map(v => shouldLabelInside(v) ? 'white' : '#1F2937') };
```

### Validation Check
```
□ Are there data labels near a reference line?
□ If label would cross baseline, is it repositioned INSIDE?
□ Are inside labels using contrasting color (white on dark bar)?
□ Is `insidetextanchor: 'end'` set for inside labels?
□ NO labels crossing ANY reference lines?
```

---

## 🎯 CHART TYPE DECISION TREE

### Step 1: What Question Are You Answering?

```
What's the question?
│
├─► "What's the composition/breakdown?" 
│   └─► How many categories?
│       ├─► 2-5 categories → PIE or DONUT
│       ├─► 6-10 categories → STACKED BAR (horizontal)
│       └─► 10+ categories → TREEMAP
│
├─► "How do items compare?"
│   └─► Is there + and - values?
│       ├─► Yes (diverging) → HORIZONTAL BAR with center zero
│       └─► No (all positive)
│           └─► How many items?
│               ├─► 2-4 items → COLUMN chart
│               ├─► 5-15 items → HORIZONTAL BAR (easier to label)
│               └─► 15+ items → Top N only, or small multiples
│
├─► "What's the trend over time?"
│   └─► How many series?
│       ├─► 1 series → LINE or COLUMN
│       ├─► 2-4 series → MULTI-LINE
│       └─► 5+ series → SMALL MULTIPLES or highlight key series
│
├─► "What changed from A to B?"
│   └─► Want to show contributing factors?
│       ├─► Yes (3-7 factors) → WATERFALL
│       └─► No (just before/after) → PAIRED BAR or BULLET
│
├─► "What's the relationship between X and Y?"
│   └─► SCATTER plot
│       └─► Add size dimension? → BUBBLE chart
│
├─► "What's the distribution?"
│   └─► HISTOGRAM or BOX PLOT
│
├─► "Where is it located?"
│   └─► MAP (choropleth, point, or heat)
│
├─► "What's the flow/journey?"
│   └─► SANKEY or FUNNEL
│
└─► "What's the ranking?"
    └─► HORIZONTAL BAR (sorted)
```

### Step 2: Validate Chart Choice

| If you chose... | Verify... |
|-----------------|-----------|
| Pie chart | ≤5 segments, shows composition |
| Bar chart | Categories are discrete |
| Line chart | X-axis is continuous (time) |
| Waterfall | Clear A→B bridge story |
| Scatter | Looking for correlation |
| Map | Geographic dimension exists |

---

## ✅ PRE-RENDER VALIDATION CHECKLIST

Run this checklist BEFORE generating any chart:

### Structural Checks
```
□ Does Y-axis start at 0? (or explicit justification)
□ Are axis ticks round numbers?
□ Is dtick set appropriately for the range?
□ Is chart type appropriate for the data pattern?
```

### Label Checks
```
□ Is there 15-20% headroom above max value?
□ Are all data labels fully visible (not truncated)?
□ Is Y-axis title readable (horizontal or with standoff)?
□ Are X-axis labels not overlapping?
```

### Color & Contrast Checks
```
□ Is background white/light? (unless dark explicitly requested)
□ Do text colors have sufficient contrast?
□ Are positive/negative values green/red consistently?
□ Is baseline/reference line color visible?
```

### Reference Line Checks (if applicable)
```
□ Is the line at the actual Y value?
□ Is the label positioned above/beside (not crossing data)?
□ Can you clearly see which items pass/fail the threshold?
```

### Diverging Data Checks (if + and - values)
```
□ Is zero baseline clearly marked?
□ Is horizontal bar orientation used?
□ Are bars extending left (negative) and right (positive)?
```

### Grid Checks
```
□ Is grid minimal (horizontal only in most cases)?
□ Is grid color light (#F3F4F6 or lighter)?
□ Is vertical grid removed (unless scatter)?
```

### Eye-Tracking Checks (Rule 8)
```
□ If chart has 10+ items, is there horizontal grid/shading?
□ Can you easily trace from bar end to label?
```

### No Crossing Checks (Rule 9) — CRITICAL
```
□ Are ANY elements crossing each other? (MUST be NO)
□ Are data labels repositioned if near baseline?
□ Are pie chart labels using leader lines if cramped?
□ Are annotations in clear space only?
```

### Data Consistency Checks (Rule 10) — CRITICAL
```
□ Is analysis period clearly stated at top?
□ Do all breakdown totals match overall total?
□ Does every chart have a footnote?
□ Is data source cited?
```

### Final Visual Check
```
□ Would McKinsey put this in a client presentation?
□ Could this win an Information is Beautiful award?
□ Is every element necessary (no chart junk)?
□ If I printed this, would I be proud?
```

---

## 📊 QUICK REFERENCE: Common Mistakes

| Mistake | Fix |
|---------|-----|
| Axis starts at data value (1266) | Set `rangemode: 'tozero'` |
| Ticks are data values | Set `dtick` to round number |
| Labels truncated | Add headroom, use `cliponaxis: false` |
| Baseline in wrong place | Set `y0: actualValue` in shapes |
| Diverging data in columns | Switch to horizontal bar |
| Composition in bar chart | Switch to pie (≤5) or stacked bar |
| Too much grid | Remove vertical, lighten horizontal |
| Y-axis title cramped | Add `standoff: 20` |
| Low contrast colors | Check against `_color-theory-guide.md` |
| Label crosses baseline | Reposition label inside bar or offset |
| No grid on 10+ item chart | Add light horizontal grid |
| Inconsistent totals | Verify all breakdowns sum to same total |
| Missing footnote | Add Source, Period, n= to every chart |
| Pie labels overlapping | Use leader lines, or combine small segments |
| Hard to trace bar to label | Add row grid or alternating shading |
| **v7: Pie labels INSIDE segments** | ~~Move to outside~~ → **v8: Use HTML legend instead** |
| **v7: Inconsistent pie label sizes** | **v8: Use HTML legend (always consistent)** |
| **v7: Angled/curved pie labels** | **v8: Use HTML legend (always horizontal)** |
| **v7: Pie labels outside boundaries** | **v8: Use HTML legend (no boundaries issue)** |
| **v7: Chart header inside white card** | Data sections → external header, text sections → internal |
| **v8: Label crossing baseline** | Use `textposition: 'inside'` for values below baseline |
| **v8: Outside label near reference line** | Smart positioning: inside if < baseline, outside if > |
| **v8: Pie labels still overlapping with pull** | Switch to `textinfo: 'none'` + HTML legend |
| **v8: Condensed adjacent pie labels** | Use HTML legend — eliminates positioning issues entirely |

---

## 🔗 Related Documents

- `_color-theory-guide.md` — Color contrast and palette rules
- `_chart-implementation-guide.md` — Code examples for specific chart types
- `data-analyst.md` — When to use which analytical method
- `data-visualization-expert.md` — Advanced design principles

---

*Version 4.0 | January 2026 | Mandatory for all visualization agents*

