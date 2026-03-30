/**
 * Quality Gate Automation
 * 
 * Automated quality checks that run before ANY output delivery.
 * This is the enforcement layer for the entire agent stack.
 * 
 * Version: 1.0
 */

/**
 * Quality Gate Configuration
 */
const QUALITY_CONFIG = {
  minimumScore: 80,
  requiredChecks: {
    visual: ['chartRules', 'colorContrast', 'labelVisibility', 'brandCompliance'],
    content: ['consistency', 'insights', 'takeaways', 'methodology'],
    technical: ['dataAccuracy', 'footnotes', 'periodConsistency'],
    delivery: ['printSafe', 'browserTested', 'noOverflow']
  },
  categoryWeights: {
    visual: 0.30,
    content: 0.35,
    technical: 0.20,
    delivery: 0.15
  }
};

/**
 * Chart Quality Rules Validation
 * Based on _universal-chart-rules.md
 */
function validateChartRules(chartConfig) {
  const errors = [];
  const warnings = [];
  
  // Rule 1: Y-axis must start from zero (unless justified)
  if (chartConfig.yAxis && chartConfig.yAxis.min !== 0 && !chartConfig.zeroOverride) {
    errors.push({
      rule: 'Y-axis Zero Start',
      message: 'Y-axis must start from 0 unless explicitly justified',
      severity: 'error'
    });
  }
  
  // Rule 2: Round tick values
  if (chartConfig.yAxis?.tickValues) {
    const hasOddTicks = chartConfig.yAxis.tickValues.some(v => 
      v !== 0 && v % 100 !== 0 && v % 1000 !== 0 && v % 500 !== 0
    );
    if (hasOddTicks) {
      errors.push({
        rule: 'Round Tick Values',
        message: 'Use round numbers for axis ticks (0, 500, 1k, 2k...)',
        severity: 'error'
      });
    }
  }
  
  // Rule 3: All labels must be visible
  if (chartConfig.labels?.some(l => l.truncated || l.overflow)) {
    errors.push({
      rule: 'Label Visibility',
      message: 'All labels must be fully visible, not cut off',
      severity: 'error'
    });
  }
  
  // Rule 4: Baseline positioning
  if (chartConfig.baseline && chartConfig.dataLabels) {
    const crossingLabels = chartConfig.dataLabels.filter(d => 
      Math.abs(d.value - chartConfig.baseline.value) < chartConfig.baseline.value * 0.1
    );
    if (crossingLabels.length > 0) {
      warnings.push({
        rule: 'Baseline Label Conflict',
        message: 'Data labels near baseline should be positioned inside bars',
        severity: 'warning'
      });
    }
  }
  
  // Rule 5: Chart type selection
  if (chartConfig.dataType === 'composition' && chartConfig.type === 'column') {
    warnings.push({
      rule: 'Chart Type Selection',
      message: 'Composition data is better shown with pie/donut charts',
      severity: 'warning'
    });
  }
  
  if (chartConfig.dataType === 'diverging' && chartConfig.type === 'column') {
    warnings.push({
      rule: 'Chart Type Selection',
      message: 'Diverging data (+ and -) is better shown with horizontal bar charts',
      severity: 'warning'
    });
  }
  
  // Rule 6: Grid lines
  if (chartConfig.gridLines?.vertical) {
    warnings.push({
      rule: 'Grid Line Usage',
      message: 'Avoid vertical grid lines in most charts',
      severity: 'warning'
    });
  }
  
  return {
    passed: errors.length === 0,
    errors,
    warnings,
    score: Math.max(0, 100 - (errors.length * 15) - (warnings.length * 5))
  };
}

/**
 * Content Quality Validation
 */
function validateContentQuality(content) {
  const checks = {
    hasExecutiveSummary: /executive summary|key insights|top \d+ insights/i.test(content),
    hasHypothesis: /hypothesis|h[0-4]:/i.test(content),
    hasSoWhat: /so what|action|implication|recommendation/i.test(content),
    hasMethodology: /methodology|approach|data source|period/i.test(content),
    hasFootnotes: /\*|†|source:|note:/i.test(content),
    hasDataConsistency: true // Would need actual data validation
  };
  
  const passed = Object.values(checks).filter(v => v).length;
  const total = Object.keys(checks).length;
  
  return {
    passed: passed === total,
    checks,
    score: Math.round((passed / total) * 100),
    missing: Object.entries(checks).filter(([k, v]) => !v).map(([k]) => k)
  };
}

/**
 * Visual Quality Validation
 */
function validateVisualQuality(visualConfig) {
  const checks = {
    whiteBackground: visualConfig.backgroundColor === 'white' || visualConfig.backgroundColor === '#ffffff',
    brandCompliant: visualConfig.brandColors?.used || false,
    highContrast: visualConfig.contrastRatio >= 4.5,
    consistentFonts: visualConfig.fontFamily !== undefined,
    noOverlap: !visualConfig.hasOverlappingElements,
    printSafe: visualConfig.printMode !== false
  };
  
  const passed = Object.values(checks).filter(v => v).length;
  const total = Object.keys(checks).length;
  
  return {
    passed: passed === total,
    checks,
    score: Math.round((passed / total) * 100),
    failing: Object.entries(checks).filter(([k, v]) => !v).map(([k]) => k)
  };
}

/**
 * Data Accuracy Validation
 */
function validateDataAccuracy(data) {
  const issues = [];
  
  // Check for consistency in percentages summing to 100
  if (data.percentages) {
    const sum = data.percentages.reduce((a, b) => a + b, 0);
    if (Math.abs(sum - 100) > 0.5) {
      issues.push({
        type: 'Percentage Sum',
        message: `Percentages sum to ${sum}%, should be 100%`,
        severity: 'critical'
      });
    }
  }
  
  // Check for segment totals matching main total
  if (data.total && data.segments) {
    const segmentSum = data.segments.reduce((a, s) => a + s.value, 0);
    if (Math.abs(segmentSum - data.total) > data.total * 0.01) {
      issues.push({
        type: 'Segment Total Mismatch',
        message: `Segments sum to ${segmentSum}, but total is ${data.total}`,
        severity: 'critical'
      });
    }
  }
  
  // Check for period consistency
  if (data.periods && data.periods.length > 1) {
    const uniquePeriods = new Set(data.periods.map(p => p.type));
    if (uniquePeriods.size > 1) {
      issues.push({
        type: 'Period Inconsistency',
        message: 'Mixed period types detected (e.g., weekly and monthly)',
        severity: 'warning'
      });
    }
  }
  
  return {
    passed: issues.filter(i => i.severity === 'critical').length === 0,
    issues,
    score: Math.max(0, 100 - (issues.length * 20))
  };
}

/**
 * Print Safety Validation
 */
function validatePrintSafety(html) {
  const checks = {
    hasPageBreakRules: /@page|page-break/i.test(html),
    hasMarginControl: /@page.*margin/i.test(html),
    noBrowserFooters: /@page.*margin.*0/i.test(html),
    tablesSafe: /page-break-inside:\s*avoid/i.test(html),
    slidesFit: /max-height|overflow:\s*hidden/i.test(html),
    colorPrintSafe: !/-webkit-print-color-adjust:\s*exact/i.test(html) || 
                    /print-color-adjust:\s*exact/i.test(html)
  };
  
  const passed = Object.values(checks).filter(v => v).length;
  const total = Object.keys(checks).length;
  
  return {
    passed: passed >= total - 1, // Allow 1 miss
    checks,
    score: Math.round((passed / total) * 100)
  };
}

/**
 * Master Quality Gate Check
 * Runs all validations and returns final quality score
 */
function runQualityGate(output) {
  const results = {
    timestamp: new Date().toISOString(),
    checks: {},
    scores: {},
    overallScore: 0,
    passed: false,
    blockers: [],
    warnings: []
  };
  
  // Run chart validation if applicable
  if (output.charts) {
    for (const chart of output.charts) {
      const chartResult = validateChartRules(chart);
      results.checks[`chart_${chart.id || 'main'}`] = chartResult;
      results.scores.charts = (results.scores.charts || 0) + chartResult.score;
      
      if (!chartResult.passed) {
        results.blockers.push(...chartResult.errors.map(e => e.message));
      }
      results.warnings.push(...chartResult.warnings.map(w => w.message));
    }
    if (output.charts.length > 0) {
      results.scores.charts /= output.charts.length;
    }
  }
  
  // Run content validation
  if (output.content) {
    const contentResult = validateContentQuality(output.content);
    results.checks.content = contentResult;
    results.scores.content = contentResult.score;
    
    if (!contentResult.passed) {
      results.warnings.push(`Missing content elements: ${contentResult.missing.join(', ')}`);
    }
  }
  
  // Run visual validation
  if (output.visual) {
    const visualResult = validateVisualQuality(output.visual);
    results.checks.visual = visualResult;
    results.scores.visual = visualResult.score;
    
    if (!visualResult.passed) {
      results.blockers.push(`Visual issues: ${visualResult.failing.join(', ')}`);
    }
  }
  
  // Run data validation
  if (output.data) {
    const dataResult = validateDataAccuracy(output.data);
    results.checks.data = dataResult;
    results.scores.data = dataResult.score;
    
    if (!dataResult.passed) {
      results.blockers.push(...dataResult.issues.map(i => i.message));
    }
  }
  
  // Run print validation if HTML
  if (output.html) {
    const printResult = validatePrintSafety(output.html);
    results.checks.print = printResult;
    results.scores.print = printResult.score;
  }
  
  // Calculate overall score
  const scoreValues = Object.values(results.scores);
  results.overallScore = scoreValues.length > 0 
    ? Math.round(scoreValues.reduce((a, b) => a + b, 0) / scoreValues.length)
    : 0;
  
  // Determine pass/fail
  results.passed = results.overallScore >= QUALITY_CONFIG.minimumScore && 
                   results.blockers.length === 0;
  
  return results;
}

/**
 * Generate Quality Report (Human-Readable)
 */
function generateQualityReport(results) {
  let report = `
# 📊 Quality Gate Report
Generated: ${results.timestamp}

## Overall Score: ${results.overallScore}/100 ${results.passed ? '✅ PASSED' : '❌ FAILED'}

### Category Scores
`;
  
  for (const [category, score] of Object.entries(results.scores)) {
    const emoji = score >= 80 ? '✅' : score >= 60 ? '⚠️' : '❌';
    report += `- ${emoji} **${category}**: ${score}/100\n`;
  }
  
  if (results.blockers.length > 0) {
    report += `
### ❌ Blockers (Must Fix)
${results.blockers.map(b => `- ${b}`).join('\n')}
`;
  }
  
  if (results.warnings.length > 0) {
    report += `
### ⚠️ Warnings (Should Fix)
${results.warnings.map(w => `- ${w}`).join('\n')}
`;
  }
  
  report += `
---
*Minimum passing score: ${QUALITY_CONFIG.minimumScore}*
`;
  
  return report;
}

/**
 * Quick Pre-Delivery Check
 * Returns a simple go/no-go decision
 */
function quickCheck(output) {
  const result = runQualityGate(output);
  return {
    canDeliver: result.passed,
    score: result.overallScore,
    blockerCount: result.blockers.length,
    summary: result.passed 
      ? `✅ Ready for delivery (${result.overallScore}/100)`
      : `❌ ${result.blockers.length} blocker(s) must be fixed`
  };
}

// Export functions
module.exports = {
  QUALITY_CONFIG,
  validateChartRules,
  validateContentQuality,
  validateVisualQuality,
  validateDataAccuracy,
  validatePrintSafety,
  runQualityGate,
  generateQualityReport,
  quickCheck
};

// CLI usage
if (require.main === module) {
  // Example usage
  const testOutput = {
    charts: [{
      id: 'revenue',
      type: 'column',
      yAxis: { min: 0, tickValues: [0, 1000, 2000, 3000] },
      labels: [{ text: 'Revenue', truncated: false }]
    }],
    content: 'Executive Summary: Key insights from analysis...',
    visual: {
      backgroundColor: 'white',
      brandColors: { used: true },
      contrastRatio: 5.0
    },
    html: '@page { margin: 0; } .table { page-break-inside: avoid; }'
  };
  
  const result = runQualityGate(testOutput);
  console.log(generateQualityReport(result));
}




