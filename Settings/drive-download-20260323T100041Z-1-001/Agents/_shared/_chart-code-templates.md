# 📊 Chart Code Templates

**Purpose:** Generate RUNNABLE chart code, not descriptions.
**Supported Libraries:** Plotly.js, Chart.js, Google Sheets formulas

---

## 🎯 RULE: Every Chart = Runnable Code

When the agent recommends a chart, it MUST output:
1. Complete JavaScript code (Plotly.js preferred)
2. Embed-ready HTML snippet
3. Data structure for the chart

---

## 📈 CHART TEMPLATES

### 1. Bar Chart (Horizontal — for comparisons)

```javascript
// BAR CHART: [Title here]
const barChartConfig = {
    data: [{
        type: 'bar',
        orientation: 'h',
        x: [/* values */],
        y: [/* categories */],
        text: [/* formatted labels */],
        textposition: 'outside',
        marker: {
            color: '#34D399',  // Bolt green
            line: { color: '#059669', width: 1 }
        },
        hovertemplate: '%{y}: %{x:,.0f}<extra></extra>'
    }],
    layout: {
        title: {
            text: '<b>[INSIGHT AS TITLE]</b>',
            font: { size: 16, color: '#1F2937' }
        },
        xaxis: {
            title: '[Metric]',
            tickformat: ',.0f',
            tickprefix: '€',  // or '$', '%' etc.
            zeroline: true,
            zerolinecolor: '#E5E7EB',
            gridcolor: '#F3F4F6'
        },
        yaxis: {
            title: '',
            automargin: true
        },
        margin: { l: 120, r: 40, t: 60, b: 40 },
        plot_bgcolor: '#FFFFFF',
        paper_bgcolor: '#FFFFFF'
    },
    config: { responsive: true, displayModeBar: false }
};

Plotly.newPlot('bar-chart-div', barChartConfig.data, barChartConfig.layout, barChartConfig.config);
```

### 2. Column Chart (Vertical — for time series)

```javascript
// COLUMN CHART: [Title here]
const columnChartConfig = {
    data: [{
        type: 'bar',
        x: [/* time periods */],
        y: [/* values */],
        text: [/* formatted labels */],
        textposition: 'outside',
        marker: {
            color: '#34D399'
        }
    }],
    layout: {
        title: {
            text: '<b>[INSIGHT AS TITLE]</b>',
            font: { size: 16, color: '#1F2937' }
        },
        xaxis: {
            title: '',
            type: 'category'
        },
        yaxis: {
            title: '[Metric]',
            tickformat: ',.0f',
            tickprefix: '€',
            rangemode: 'tozero',  // ALWAYS start from zero
            gridcolor: '#F3F4F6'
        },
        margin: { l: 60, r: 20, t: 60, b: 40 },
        plot_bgcolor: '#FFFFFF',
        paper_bgcolor: '#FFFFFF'
    },
    config: { responsive: true, displayModeBar: false }
};

Plotly.newPlot('column-chart-div', columnChartConfig.data, columnChartConfig.layout, columnChartConfig.config);
```

### 3. Line Chart (for trends)

```javascript
// LINE CHART: [Title here]
const lineChartConfig = {
    data: [{
        type: 'scatter',
        mode: 'lines+markers',
        x: [/* dates or periods */],
        y: [/* values */],
        line: { color: '#34D399', width: 2 },
        marker: { size: 6, color: '#34D399' },
        hovertemplate: '%{x}: %{y:,.0f}<extra></extra>'
    }],
    layout: {
        title: {
            text: '<b>[INSIGHT AS TITLE]</b>',
            font: { size: 16, color: '#1F2937' }
        },
        xaxis: {
            title: '',
            showgrid: false
        },
        yaxis: {
            title: '[Metric]',
            tickformat: ',.0f',
            gridcolor: '#F3F4F6',
            rangemode: 'tozero'
        },
        margin: { l: 60, r: 20, t: 60, b: 40 },
        plot_bgcolor: '#FFFFFF',
        paper_bgcolor: '#FFFFFF'
    },
    config: { responsive: true, displayModeBar: false }
};

Plotly.newPlot('line-chart-div', lineChartConfig.data, lineChartConfig.layout, lineChartConfig.config);
```

### 4. Donut Chart (for composition)

```javascript
// DONUT CHART: [Title here]
const donutChartConfig = {
    data: [{
        type: 'pie',
        hole: 0.5,
        values: [/* percentages or values */],
        labels: [/* categories */],
        textinfo: 'none',  // Use legend instead
        marker: {
            colors: ['#34D399', '#059669', '#10B981', '#6EE7B7', '#A7F3D0']
        },
        hovertemplate: '%{label}: %{percent:.1%}<extra></extra>'
    }],
    layout: {
        title: {
            text: '<b>[INSIGHT AS TITLE]</b>',
            font: { size: 16, color: '#1F2937' }
        },
        showlegend: true,
        legend: {
            orientation: 'h',
            y: -0.1,
            x: 0.5,
            xanchor: 'center'
        },
        margin: { l: 20, r: 20, t: 60, b: 60 },
        paper_bgcolor: '#FFFFFF'
    },
    config: { responsive: true, displayModeBar: false }
};

Plotly.newPlot('donut-chart-div', donutChartConfig.data, donutChartConfig.layout, donutChartConfig.config);
```

### 5. Waterfall Chart (for decomposition)

```javascript
// WATERFALL CHART: [Title here]
const waterfallChartConfig = {
    data: [{
        type: 'waterfall',
        orientation: 'v',
        x: [/* categories: 'Start', 'Factor1', 'Factor2', ..., 'End' */],
        y: [/* values: positive for increase, negative for decrease */],
        measure: [/* 'absolute', 'relative', 'relative', ..., 'total' */],
        text: [/* formatted labels */],
        textposition: 'outside',
        connector: { line: { color: '#E5E7EB' } },
        increasing: { marker: { color: '#34D399' } },
        decreasing: { marker: { color: '#EF4444' } },
        totals: { marker: { color: '#3B82F6' } }
    }],
    layout: {
        title: {
            text: '<b>[INSIGHT AS TITLE]</b>',
            font: { size: 16, color: '#1F2937' }
        },
        xaxis: { title: '' },
        yaxis: {
            title: '[Metric]',
            tickformat: ',.0f',
            tickprefix: '€'
        },
        margin: { l: 60, r: 20, t: 60, b: 40 },
        plot_bgcolor: '#FFFFFF',
        paper_bgcolor: '#FFFFFF'
    },
    config: { responsive: true, displayModeBar: false }
};

Plotly.newPlot('waterfall-chart-div', waterfallChartConfig.data, waterfallChartConfig.layout, waterfallChartConfig.config);
```

### 6. KPI Card (for single metrics)

```html
<!-- KPI CARD: [Metric Name] -->
<div class="kpi-card" style="
    background: #FFFFFF;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    text-align: center;
    min-width: 150px;
">
    <div class="kpi-label" style="
        font-size: 12px;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    ">[METRIC NAME]</div>
    <div class="kpi-value" style="
        font-size: 32px;
        font-weight: 700;
        color: #1F2937;
    ">[VALUE]</div>
    <div class="kpi-change" style="
        font-size: 14px;
        color: #34D399;  /* Green for positive, #EF4444 for negative */
        margin-top: 4px;
    ">↑ [CHANGE]% vs [PERIOD]</div>
</div>
```

### 7. Diverging Bar Chart (for positive/negative comparisons)

```javascript
// DIVERGING BAR: [Title here]
const divergingBarConfig = {
    data: [{
        type: 'bar',
        orientation: 'h',
        x: [/* values: negative and positive */],
        y: [/* categories */],
        text: [/* formatted labels */],
        textposition: 'outside',
        marker: {
            color: [/* values */].map(v => v >= 0 ? '#34D399' : '#EF4444')
        }
    }],
    layout: {
        title: {
            text: '<b>[INSIGHT AS TITLE]</b>',
            font: { size: 16, color: '#1F2937' }
        },
        xaxis: {
            title: '[Metric]',
            zeroline: true,
            zerolinewidth: 2,
            zerolinecolor: '#1F2937',
            tickformat: '+,.0f'
        },
        yaxis: {
            title: '',
            automargin: true
        },
        margin: { l: 120, r: 40, t: 60, b: 40 },
        plot_bgcolor: '#FFFFFF',
        paper_bgcolor: '#FFFFFF'
    },
    config: { responsive: true, displayModeBar: false }
};

Plotly.newPlot('diverging-bar-div', divergingBarConfig.data, divergingBarConfig.layout, divergingBarConfig.config);
```

---

## 📋 COMPLETE HTML DASHBOARD TEMPLATE

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[DASHBOARD TITLE]</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        :root {
            --bolt-green: #34D399;
            --bolt-green-dark: #059669;
            --text-dark: #1F2937;
            --text-medium: #6B7280;
            --bg-white: #FFFFFF;
            --bg-light: #F9FAFB;
            --border: #E5E7EB;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-light);
            color: var(--text-dark);
            line-height: 1.5;
        }
        
        .dashboard {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
        }
        
        .header {
            background: var(--bg-white);
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
            border-left: 4px solid var(--bolt-green);
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 8px;
        }
        
        .header .period {
            color: var(--text-medium);
            font-size: 14px;
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .chart-section {
            background: var(--bg-white);
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
        }
        
        .chart-section h2 {
            font-size: 16px;
            color: var(--text-medium);
            margin-bottom: 16px;
        }
        
        .insights-box {
            background: #F0FDF4;
            border: 1px solid var(--bolt-green);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 24px;
        }
        
        .insights-box h3 {
            color: var(--bolt-green-dark);
            margin-bottom: 12px;
        }
        
        .insights-box ul {
            list-style: none;
        }
        
        .insights-box li {
            padding: 8px 0;
            border-bottom: 1px solid #D1FAE5;
        }
        
        .insights-box li:last-child {
            border-bottom: none;
        }
        
        @media print {
            @page { size: landscape; margin: 0; }
            body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
            .dashboard { padding: 15mm; }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <!-- HEADER -->
        <div class="header">
            <h1>[DASHBOARD TITLE]</h1>
            <p class="period">Period: [DATE RANGE] | Baseline: [COMPARISON]</p>
        </div>
        
        <!-- TOP INSIGHTS -->
        <div class="insights-box">
            <h3>🎯 Top 3 Insights</h3>
            <ul>
                <li><strong>1.</strong> [INSIGHT + SO WHAT + ACTION]</li>
                <li><strong>2.</strong> [INSIGHT + SO WHAT + ACTION]</li>
                <li><strong>3.</strong> [INSIGHT + SO WHAT + ACTION]</li>
            </ul>
        </div>
        
        <!-- KPI CARDS -->
        <div class="kpi-grid">
            <!-- Insert KPI cards here -->
        </div>
        
        <!-- CHARTS -->
        <div class="chart-section">
            <h2>[Section Title]</h2>
            <div id="chart-1" style="height: 300px;"></div>
        </div>
        
        <div class="chart-section">
            <h2>[Section Title]</h2>
            <div id="chart-2" style="height: 300px;"></div>
        </div>
    </div>
    
    <script>
        // Chart code here
    </script>
</body>
</html>
```

---

## 🔧 DATA TRANSFORMATION HELPERS

```javascript
// Format number with suffix (K, M, B)
function formatNumber(num, prefix = '', decimals = 1) {
    if (num >= 1e9) return prefix + (num / 1e9).toFixed(decimals) + 'B';
    if (num >= 1e6) return prefix + (num / 1e6).toFixed(decimals) + 'M';
    if (num >= 1e3) return prefix + (num / 1e3).toFixed(decimals) + 'K';
    return prefix + num.toFixed(0);
}

// Calculate percent change
function percentChange(current, previous) {
    if (previous === 0) return 0;
    return ((current - previous) / previous) * 100;
}

// Format as currency
function formatCurrency(num, currency = '€') {
    return currency + num.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

// Generate color scale
function getColorScale(values, baseColor = '#34D399') {
    // Returns array of colors from light to dark based on values
    const max = Math.max(...values);
    return values.map(v => {
        const opacity = 0.3 + (v / max) * 0.7;
        return baseColor + Math.round(opacity * 255).toString(16).padStart(2, '0');
    });
}
```

---

## 📊 GOOGLE SHEETS FORMULAS

### Conditional Formatting for KPIs
```
=IF(A1>B1, "🟢", IF(A1<B1*0.9, "🔴", "🟡"))
```

### Percent Change
```
=TEXT((B2-A2)/A2, "+0.0%;-0.0%")
```

### Sparkline
```
=SPARKLINE(A1:A10, {"charttype","line";"color","#34D399"})
```

### Dynamic Range Sum
```
=SUMIFS(Data!C:C, Data!A:A, ">="&$B$1, Data!A:A, "<="&$B$2)
```

---

*Every chart MUST have runnable code. No exceptions.*




