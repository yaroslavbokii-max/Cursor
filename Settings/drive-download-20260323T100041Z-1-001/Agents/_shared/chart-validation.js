/**
 * Chart Pre-Render Validation System
 * Version: 1.0 (v8)
 * 
 * Validates chart configurations against universal rules BEFORE rendering.
 * Catches common errors: non-zero start, non-round ticks, label overflow, etc.
 */

const ChartValidator = {
    errors: [],
    warnings: [],
    
    /**
     * Main validation entry point
     * @param {string} chartName - Name/ID of chart for logging
     * @param {object} config - Plotly layout configuration
     * @param {Array} data - Plotly trace data
     * @returns {object} { valid: boolean, errors: [], warnings: [] }
     */
    validate(chartName, config, data) {
        this.errors = [];
        this.warnings = [];
        
        // Rule 1: Axis starts from zero
        this.checkAxisStartsFromZero(chartName, config);
        
        // Rule 2: Round tick values
        this.checkRoundTicks(chartName, config);
        
        // Rule 3: Label headroom
        this.checkLabelHeadroom(chartName, config, data);
        
        // Rule 6: Grid configuration
        this.checkGridConfig(chartName, config);
        
        // Rule 9: Element crossing prevention
        this.checkLabelBaseline(chartName, config, data);
        
        // Rule 13: Pie chart configuration
        if (data && data[0] && data[0].type === 'pie') {
            this.checkPieConfig(chartName, config, data);
        }
        
        return {
            valid: this.errors.length === 0,
            errors: [...this.errors],
            warnings: [...this.warnings]
        };
    },
    
    /**
     * Rule 1: Check if axis starts from zero
     */
    checkAxisStartsFromZero(chartName, config) {
        const axes = ['xaxis', 'yaxis'];
        
        axes.forEach(axis => {
            if (config[axis] && config[axis].range) {
                const startValue = config[axis].range[0];
                if (startValue !== 0 && startValue !== '0') {
                    // Allow negative start for diverging data
                    if (startValue < 0) {
                        // Check if it's symmetric around zero (diverging)
                        const endValue = config[axis].range[1];
                        if (Math.abs(startValue) !== endValue) {
                            this.warnings.push(`${chartName}: ${axis} range [${startValue}, ${endValue}] is not symmetric for diverging data`);
                        }
                    } else {
                        this.errors.push(`${chartName}: ${axis} should start from 0, currently starts from ${startValue}`);
                    }
                }
            }
        });
    },
    
    /**
     * Rule 2: Check if dtick is a round number
     */
    checkRoundTicks(chartName, config) {
        const roundNumbers = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000];
        const axes = ['xaxis', 'yaxis'];
        
        axes.forEach(axis => {
            if (config[axis] && config[axis].dtick) {
                const dtick = config[axis].dtick;
                if (typeof dtick === 'number' && !roundNumbers.includes(dtick)) {
                    this.errors.push(`${chartName}: ${axis} dtick (${dtick}) is not a round number. Use: ${roundNumbers.filter(n => n < dtick * 5 && n > dtick / 5).join(', ')}`);
                }
            }
        });
    },
    
    /**
     * Rule 3: Check for label headroom
     */
    checkLabelHeadroom(chartName, config, data) {
        if (!data || !data[0]) return;
        
        const trace = data[0];
        const values = trace.y || trace.x || trace.values;
        
        if (values && Array.isArray(values)) {
            const maxValue = Math.max(...values.filter(v => typeof v === 'number'));
            
            // Check Y-axis range
            if (config.yaxis && config.yaxis.range) {
                const maxRange = config.yaxis.range[1];
                const headroomPercent = ((maxRange - maxValue) / maxValue) * 100;
                
                if (headroomPercent < 10) {
                    this.warnings.push(`${chartName}: Only ${headroomPercent.toFixed(0)}% headroom above max value. Consider 15-20% for labels.`);
                }
            }
        }
    },
    
    /**
     * Rule 6: Check grid configuration
     */
    checkGridConfig(chartName, config) {
        // Vertical grid should generally be off
        if (config.xaxis && config.xaxis.showgrid === true) {
            this.warnings.push(`${chartName}: Vertical grid lines are enabled. Consider removing for cleaner look.`);
        }
        
        // Check grid color is light enough
        if (config.yaxis && config.yaxis.gridcolor) {
            const color = config.yaxis.gridcolor.toLowerCase();
            // Check if it's a dark color (crude check)
            if (color.includes('#') && !['#f', '#e', '#d'].some(c => color.startsWith(c.toLowerCase()))) {
                this.warnings.push(`${chartName}: Grid color (${color}) may be too dark. Use #F3F4F6 or lighter.`);
            }
        }
    },
    
    /**
     * Rule 9: Check for potential label/baseline crossing
     */
    checkLabelBaseline(chartName, config, data) {
        if (!config.shapes || !data || !data[0]) return;
        
        const trace = data[0];
        const values = trace.x || trace.y || [];
        
        config.shapes.forEach(shape => {
            if (shape.type === 'line') {
                const baselineValue = shape.y0 || shape.x0;
                
                // Check if any values are close to baseline
                const closeValues = values.filter(v => {
                    if (typeof v !== 'number') return false;
                    const diff = Math.abs(v - baselineValue);
                    return diff < baselineValue * 0.15; // Within 15%
                });
                
                if (closeValues.length > 0 && trace.textposition === 'outside') {
                    this.errors.push(`${chartName}: Values [${closeValues.join(', ')}] are close to baseline (${baselineValue}). Labels may cross. Use textposition 'inside' for these.`);
                }
            }
        });
    },
    
    /**
     * Rule 13: Check pie chart configuration
     */
    checkPieConfig(chartName, config, data) {
        const trace = data[0];
        
        // Best practice: use HTML legend instead of inline labels
        if (trace.textinfo && trace.textinfo !== 'none') {
            this.warnings.push(`${chartName}: Pie chart has inline labels. Consider textinfo='none' + HTML legend for reliable positioning.`);
        }
        
        // Check for small segments
        if (trace.values) {
            const total = trace.values.reduce((a, b) => a + b, 0);
            const smallSegments = trace.values.filter(v => (v / total) < 0.05);
            
            if (smallSegments.length > 2) {
                this.warnings.push(`${chartName}: ${smallSegments.length} segments are <5%. Consider combining into "Other" or using HTML legend.`);
            }
        }
    },
    
    /**
     * Log results to console with formatting
     */
    logResults(chartName, results) {
        if (results.errors.length > 0) {
            console.error(`❌ ${chartName} validation FAILED:`);
            results.errors.forEach(e => console.error(`  • ${e}`));
        }
        
        if (results.warnings.length > 0) {
            console.warn(`⚠️ ${chartName} warnings:`);
            results.warnings.forEach(w => console.warn(`  • ${w}`));
        }
        
        if (results.valid && results.warnings.length === 0) {
            console.log(`✅ ${chartName} validation passed`);
        }
    },
    
    /**
     * Update validation badge in DOM
     */
    updateBadge(totalErrors) {
        const badge = document.getElementById('validationBadge');
        if (!badge) return;
        
        if (totalErrors > 0) {
            badge.textContent = `⚠️ ${totalErrors} Validation Error${totalErrors > 1 ? 's' : ''}`;
            badge.classList.add('error');
        } else {
            badge.textContent = '✅ All Charts Validated';
            badge.classList.remove('error');
        }
    }
};

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChartValidator;
}




