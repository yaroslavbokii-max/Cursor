/**
 * AUTOMATED VALIDATION SUITE v1.0
 * 
 * Runs before ANY output is delivered to user.
 * Catches issues that humans miss.
 * 
 * Usage: Include in any HTML output, or run via Node.js
 */

const ValidationSuite = {
    
    // ============================================
    // PRINT VALIDATION
    // ============================================
    
    validatePrintCSS: function(html) {
        const errors = [];
        const warnings = [];
        
        // CRITICAL: @page margin must be 0
        if (!html.includes('@page') || !html.includes('margin: 0')) {
            errors.push({
                type: 'PRINT_CSS',
                severity: 'CRITICAL',
                message: 'Missing @page { margin: 0 } — Browser will add headers/footers',
                fix: 'Add: @media print { @page { margin: 0 !important; } }'
            });
        }
        
        // CRITICAL: page-break-after on pages/slides
        if (!html.includes('page-break-after')) {
            errors.push({
                type: 'PRINT_CSS',
                severity: 'CRITICAL',
                message: 'Missing page-break-after — Pages will merge when printing',
                fix: 'Add: .page, .slide { page-break-after: always !important; }'
            });
        }
        
        // CRITICAL: page-break-inside avoid on key elements
        if (!html.includes('page-break-inside: avoid')) {
            warnings.push({
                type: 'PRINT_CSS',
                severity: 'HIGH',
                message: 'Missing page-break-inside: avoid — Tables/cards may break across pages',
                fix: 'Add: table, .card, .box { page-break-inside: avoid !important; }'
            });
        }
        
        // CRITICAL: print-color-adjust for backgrounds
        if (!html.includes('print-color-adjust') && !html.includes('-webkit-print-color-adjust')) {
            warnings.push({
                type: 'PRINT_CSS',
                severity: 'MEDIUM',
                message: 'Missing print-color-adjust — Backgrounds may not print',
                fix: 'Add: * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }'
            });
        }
        
        // Check for explicit page dimensions
        if (!html.includes('297mm') && !html.includes('210mm')) {
            warnings.push({
                type: 'PRINT_CSS',
                severity: 'MEDIUM',
                message: 'No explicit A4 dimensions (210mm × 297mm) — Layout may shift',
                fix: 'Add explicit width/height in mm for print containers'
            });
        }
        
        return { errors, warnings, valid: errors.length === 0 };
    },
    
    // ============================================
    // CHART VALIDATION
    // ============================================
    
    validateCharts: function(chartConfigs) {
        const errors = [];
        const warnings = [];
        
        chartConfigs.forEach((config, index) => {
            const chartId = config.id || `Chart ${index + 1}`;
            
            // Rule 1: Y-axis must start from zero for bar/column charts
            if (['bar', 'column'].includes(config.type)) {
                if (config.yAxis && config.yAxis.min !== 0 && config.yAxis.min !== undefined) {
                    errors.push({
                        type: 'CHART_AXIS',
                        severity: 'CRITICAL',
                        chart: chartId,
                        message: `Y-axis does not start from 0 (starts at ${config.yAxis.min})`,
                        fix: 'Set yAxis.min = 0 or remove min constraint'
                    });
                }
            }
            
            // Rule 2: Check for round number ticks
            if (config.yAxis && config.yAxis.tickValues) {
                const hasNonRound = config.yAxis.tickValues.some(v => !isRoundNumber(v));
                if (hasNonRound) {
                    warnings.push({
                        type: 'CHART_AXIS',
                        severity: 'MEDIUM',
                        chart: chartId,
                        message: 'Y-axis has non-round tick values',
                        fix: 'Use round numbers: 0, 5K, 10K, 15K etc.'
                    });
                }
            }
            
            // Rule 3: Pie charts should have outside labels or legend
            if (config.type === 'pie' || config.type === 'donut') {
                if (config.labels && config.labels.position === 'inside') {
                    warnings.push({
                        type: 'CHART_LABELS',
                        severity: 'HIGH',
                        chart: chartId,
                        message: 'Pie chart has inside labels — may overlap',
                        fix: 'Use outside labels with leader lines, or horizontal legend below'
                    });
                }
            }
            
            // Rule 4: Check for data label visibility
            if (config.dataLabels === false) {
                warnings.push({
                    type: 'CHART_LABELS',
                    severity: 'LOW',
                    chart: chartId,
                    message: 'Data labels disabled — values not visible',
                    fix: 'Enable dataLabels for key values'
                });
            }
            
            // Rule 5: Baseline validation
            if (config.baseline) {
                // Check if any data point is within 10% of baseline
                const nearBaseline = config.data.some(d => 
                    Math.abs(d.value - config.baseline.value) / config.baseline.value < 0.1
                );
                if (nearBaseline) {
                    warnings.push({
                        type: 'CHART_BASELINE',
                        severity: 'HIGH',
                        chart: chartId,
                        message: 'Data point near baseline — label may overlap',
                        fix: 'Use conditional label positioning (inside bar if below baseline)'
                    });
                }
            }
        });
        
        return { errors, warnings, valid: errors.length === 0 };
    },
    
    // ============================================
    // CONTENT VALIDATION
    // ============================================
    
    validateContent: function(html, options = {}) {
        const errors = [];
        const warnings = [];
        
        const maxWordsPerSlide = options.maxWordsPerSlide || 100;
        const slides = html.match(/<div class="slide[^"]*"[^>]*>[\s\S]*?<\/div>/gi) || [];
        
        slides.forEach((slide, index) => {
            // Strip HTML tags and count words
            const text = slide.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
            const wordCount = text.split(' ').filter(w => w.length > 0).length;
            
            if (wordCount > maxWordsPerSlide) {
                warnings.push({
                    type: 'CONTENT_DENSITY',
                    severity: 'HIGH',
                    slide: index + 1,
                    message: `Slide has ${wordCount} words (max: ${maxWordsPerSlide})`,
                    fix: `Reduce content or split into multiple slides`
                });
            }
        });
        
        // Check for overflow: hidden on slides
        if (slides.length > 0 && !html.includes('overflow: hidden')) {
            warnings.push({
                type: 'CONTENT_OVERFLOW',
                severity: 'MEDIUM',
                message: 'Slides missing overflow: hidden — content may bleed',
                fix: 'Add: .slide { overflow: hidden !important; }'
            });
        }
        
        return { errors, warnings, valid: errors.length === 0 };
    },
    
    // ============================================
    // ACCESSIBILITY VALIDATION
    // ============================================
    
    validateAccessibility: function(html) {
        const errors = [];
        const warnings = [];
        
        // Check for alt text on images
        const images = html.match(/<img[^>]*>/gi) || [];
        images.forEach((img, index) => {
            if (!img.includes('alt=')) {
                warnings.push({
                    type: 'ACCESSIBILITY',
                    severity: 'MEDIUM',
                    message: `Image ${index + 1} missing alt text`,
                    fix: 'Add alt attribute to all images'
                });
            }
        });
        
        // Check for color contrast (basic check)
        if (html.includes('color: #999') || html.includes('color: #aaa') || html.includes('color: #bbb')) {
            warnings.push({
                type: 'ACCESSIBILITY',
                severity: 'MEDIUM',
                message: 'Low contrast text detected (gray on white)',
                fix: 'Use minimum #666 for body text, #333 for headers'
            });
        }
        
        // Check for semantic headings
        const hasH1 = html.includes('<h1');
        const hasH2 = html.includes('<h2');
        if (!hasH1 && hasH2) {
            warnings.push({
                type: 'ACCESSIBILITY',
                severity: 'LOW',
                message: 'Document has H2 but no H1 — improper heading hierarchy',
                fix: 'Start with H1, then H2, H3, etc.'
            });
        }
        
        return { errors, warnings, valid: errors.length === 0 };
    },
    
    // ============================================
    // DATA CONSISTENCY VALIDATION
    // ============================================
    
    validateDataConsistency: function(data) {
        const errors = [];
        const warnings = [];
        
        // Check if percentages sum to 100%
        if (data.percentages) {
            const sum = data.percentages.reduce((a, b) => a + b, 0);
            if (Math.abs(sum - 100) > 0.5) {
                errors.push({
                    type: 'DATA_CONSISTENCY',
                    severity: 'CRITICAL',
                    message: `Percentages sum to ${sum.toFixed(1)}%, not 100%`,
                    fix: 'Verify data source and recalculate percentages'
                });
            }
        }
        
        // Check if parts sum to total
        if (data.total && data.parts) {
            const partsSum = data.parts.reduce((a, b) => a + b, 0);
            const diff = Math.abs(partsSum - data.total);
            const tolerance = data.total * 0.01; // 1% tolerance
            if (diff > tolerance) {
                errors.push({
                    type: 'DATA_CONSISTENCY',
                    severity: 'CRITICAL',
                    message: `Parts (${partsSum}) don't sum to total (${data.total})`,
                    fix: 'Verify data source — parts must equal total'
                });
            }
        }
        
        return { errors, warnings, valid: errors.length === 0 };
    },
    
    // ============================================
    // FULL VALIDATION RUN
    // ============================================
    
    runFullValidation: function(html, options = {}) {
        const results = {
            print: this.validatePrintCSS(html),
            content: this.validateContent(html, options),
            accessibility: this.validateAccessibility(html),
            timestamp: new Date().toISOString(),
            overallValid: true,
            totalErrors: 0,
            totalWarnings: 0
        };
        
        // Aggregate results
        Object.keys(results).forEach(key => {
            if (results[key].errors) {
                results.totalErrors += results[key].errors.length;
                if (results[key].errors.length > 0) {
                    results.overallValid = false;
                }
            }
            if (results[key].warnings) {
                results.totalWarnings += results[key].warnings.length;
            }
        });
        
        return results;
    },
    
    // ============================================
    // GENERATE VALIDATION REPORT
    // ============================================
    
    generateReport: function(results) {
        let report = `
╔══════════════════════════════════════════════════════════════╗
║              AUTOMATED VALIDATION REPORT                     ║
║              ${results.timestamp}                            ║
╠══════════════════════════════════════════════════════════════╣
║  STATUS: ${results.overallValid ? '✅ PASSED' : '❌ FAILED'}                                      ║
║  Errors: ${results.totalErrors}  |  Warnings: ${results.totalWarnings}                              ║
╚══════════════════════════════════════════════════════════════╝
`;
        
        // List all errors
        if (results.totalErrors > 0) {
            report += '\n🔴 ERRORS (Must Fix Before Delivery):\n';
            report += '─'.repeat(60) + '\n';
            
            Object.keys(results).forEach(category => {
                if (results[category].errors && results[category].errors.length > 0) {
                    results[category].errors.forEach(err => {
                        report += `\n[${err.severity}] ${err.type}\n`;
                        report += `  Message: ${err.message}\n`;
                        report += `  Fix: ${err.fix}\n`;
                    });
                }
            });
        }
        
        // List warnings
        if (results.totalWarnings > 0) {
            report += '\n🟡 WARNINGS (Should Fix):\n';
            report += '─'.repeat(60) + '\n';
            
            Object.keys(results).forEach(category => {
                if (results[category].warnings && results[category].warnings.length > 0) {
                    results[category].warnings.forEach(warn => {
                        report += `\n[${warn.severity}] ${warn.type}\n`;
                        report += `  Message: ${warn.message}\n`;
                        report += `  Fix: ${warn.fix}\n`;
                    });
                }
            });
        }
        
        if (results.overallValid && results.totalWarnings === 0) {
            report += '\n✅ All checks passed! Ready for delivery.\n';
        }
        
        return report;
    }
};

// Helper function
function isRoundNumber(n) {
    if (n === 0) return true;
    const abs = Math.abs(n);
    if (abs >= 1000) return abs % 1000 === 0;
    if (abs >= 100) return abs % 100 === 0;
    if (abs >= 10) return abs % 5 === 0;
    return Number.isInteger(n);
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ValidationSuite;
}

// Browser usage
if (typeof window !== 'undefined') {
    window.ValidationSuite = ValidationSuite;
}




