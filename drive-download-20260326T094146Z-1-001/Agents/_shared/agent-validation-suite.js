/**
 * Agent Validation Suite
 * 
 * Automated testing for agent protocol compliance
 * Run: node agent-validation-suite.js
 * 
 * Version: 1.0
 * Source: v8 Dashboard Learnings
 */

const fs = require('fs');
const path = require('path');

// Configuration
const AGENTS_ROOT = path.join(__dirname, '..');
const REQUIRED_PROTOCOLS = {
  'MANDATORY_CHECKPOINT': {
    patterns: [
      /⛔.*MANDATORY.*CHECKPOINT/i,
      /HARD STOP/i,
      /CANNOT SKIP/i
    ],
    errorLevel: 'critical',
    description: 'Agent must have mandatory intake checkpoint'
  },
  'PRE_DELIVERY_VALIDATION': {
    patterns: [
      /PRE-DELIVERY VALIDATION/i,
      /Before delivering.*validate/i,
      /Validation.*before delivery/i
    ],
    errorLevel: 'high',
    description: 'Agent must validate outputs before delivery'
  },
  'FALLBACK_PROTOCOL': {
    patterns: [
      /Fallback/i,
      /Alternative.*approach/i,
      /If.*fails.*switch/i
    ],
    errorLevel: 'medium',
    description: 'Agent should have fallback strategies'
  },
  'MEMORY_PROTOCOL': {
    patterns: [
      /MEMORY\.md/i,
      /Update.*memory/i,
      /Learning.*capture/i
    ],
    errorLevel: 'medium',
    description: 'Agent should reference MEMORY.md'
  },
  'CHART_RULES_REFERENCE': {
    patterns: [
      /_universal-chart-rules\.md/i,
      /chart.*rules/i
    ],
    errorLevel: 'high',
    applicableTo: ['data-analyst', 'data-visualization-expert', 'operations-dashboard-builder', 'presentation-maker'],
    description: 'Visualization agents must reference chart rules'
  }
};

// Agent categories
const AGENT_CATEGORIES = {
  'analysis': ['data-analyst', 'data-visualization-expert', 'knowledge-extractor', 'customer-insight-analyst', 'financial-modeler'],
  'creation': ['presentation-maker', 'workshop-exercise-designer', 'layout-architect', 'visual-designer', 'gamma-optimizer'],
  'content': ['copywriter', 'email-composer', 'brand-architect', 'personal-brand-builder'],
  'automation': ['n8n-workflow-architect', 'web-scraper-ninja', 'devops-setup-agent'],
  'meta': ['orchestration-agent', 'prompt-architect', 'quality-assurance-reviewer', 'agent-architect'],
  'productivity': ['meeting-commander', 'okr-coach', 'process-optimizer', 'project-commander', 'report-automator'],
  'strategy': ['competitive-analyst', 'decision-framework-builder', 'expert-panel', 'gtm-strategist', 'idea-forge'],
  'product': ['code-generator', 'database-architect', 'internal-tool-builder', 'operations-dashboard-builder', 'prd-architect']
};

// Results storage
const results = {
  totalAgents: 0,
  compliant: 0,
  partial: 0,
  nonCompliant: 0,
  agents: [],
  criticalIssues: [],
  timestamp: new Date().toISOString()
};

/**
 * Read agent markdown file
 */
function readAgentFile(agentPath) {
  const mdFiles = fs.readdirSync(agentPath).filter(f => f.endsWith('.md') && f !== 'MEMORY.md' && f !== 'changelog.md');
  if (mdFiles.length === 0) return null;
  
  const mainFile = mdFiles[0];
  return fs.readFileSync(path.join(agentPath, mainFile), 'utf-8');
}

/**
 * Check if agent content matches protocol patterns
 */
function checkProtocol(content, protocol, agentName) {
  // Check if protocol is applicable to this agent
  if (protocol.applicableTo && !protocol.applicableTo.includes(agentName)) {
    return { status: 'not_applicable', protocol };
  }
  
  for (const pattern of protocol.patterns) {
    if (pattern.test(content)) {
      return { status: 'pass', protocol };
    }
  }
  
  return { status: 'fail', protocol };
}

/**
 * Validate single agent
 */
function validateAgent(agentName, agentPath) {
  const content = readAgentFile(agentPath);
  if (!content) {
    return {
      name: agentName,
      status: 'error',
      message: 'Could not read agent file',
      checks: []
    };
  }
  
  const checks = [];
  let criticalFails = 0;
  let highFails = 0;
  let passes = 0;
  
  for (const [protocolName, protocol] of Object.entries(REQUIRED_PROTOCOLS)) {
    const result = checkProtocol(content, protocol, agentName);
    
    checks.push({
      protocol: protocolName,
      status: result.status,
      errorLevel: protocol.errorLevel,
      description: protocol.description
    });
    
    if (result.status === 'fail') {
      if (protocol.errorLevel === 'critical') criticalFails++;
      if (protocol.errorLevel === 'high') highFails++;
    } else if (result.status === 'pass') {
      passes++;
    }
  }
  
  // Determine overall status
  let status = 'compliant';
  let score = 100;
  
  if (criticalFails > 0) {
    status = 'non-compliant';
    score = Math.max(0, 100 - (criticalFails * 30) - (highFails * 15));
  } else if (highFails > 0) {
    status = 'partial';
    score = Math.max(20, 100 - (highFails * 20));
  }
  
  return {
    name: agentName,
    status,
    score,
    checks,
    criticalFails,
    highFails,
    passes
  };
}

/**
 * Find all agents in directory structure
 */
function findAgents(rootDir) {
  const agents = [];
  const categories = fs.readdirSync(rootDir).filter(f => {
    const fullPath = path.join(rootDir, f);
    return fs.statSync(fullPath).isDirectory() && !f.startsWith('_') && !f.startsWith('.');
  });
  
  for (const category of categories) {
    const categoryPath = path.join(rootDir, category);
    const agentDirs = fs.readdirSync(categoryPath).filter(f => {
      const fullPath = path.join(categoryPath, f);
      return fs.statSync(fullPath).isDirectory();
    });
    
    for (const agentDir of agentDirs) {
      agents.push({
        name: agentDir,
        category,
        path: path.join(categoryPath, agentDir)
      });
    }
  }
  
  return agents;
}

/**
 * Main validation function
 */
function runValidation() {
  console.log('🔍 Agent Validation Suite v1.0');
  console.log('=' .repeat(50));
  console.log('');
  
  const agents = findAgents(AGENTS_ROOT);
  results.totalAgents = agents.length;
  
  console.log(`Found ${agents.length} agents to validate\n`);
  
  for (const agent of agents) {
    const validation = validateAgent(agent.name, agent.path);
    validation.category = agent.category;
    results.agents.push(validation);
    
    // Track critical issues
    if (validation.criticalFails > 0) {
      results.criticalIssues.push({
        agent: agent.name,
        category: agent.category,
        fails: validation.checks.filter(c => c.status === 'fail' && c.errorLevel === 'critical')
      });
    }
    
    // Update counters
    if (validation.status === 'compliant') results.compliant++;
    else if (validation.status === 'partial') results.partial++;
    else results.nonCompliant++;
    
    // Print status
    const statusIcon = validation.status === 'compliant' ? '✅' : 
                       validation.status === 'partial' ? '🟡' : '❌';
    console.log(`${statusIcon} ${agent.name.padEnd(35)} [${validation.score}%] ${validation.status}`);
  }
  
  // Print summary
  console.log('');
  console.log('=' .repeat(50));
  console.log('SUMMARY');
  console.log('=' .repeat(50));
  console.log(`Total Agents:    ${results.totalAgents}`);
  console.log(`Compliant:       ${results.compliant} (${Math.round(results.compliant/results.totalAgents*100)}%)`);
  console.log(`Partial:         ${results.partial} (${Math.round(results.partial/results.totalAgents*100)}%)`);
  console.log(`Non-Compliant:   ${results.nonCompliant} (${Math.round(results.nonCompliant/results.totalAgents*100)}%)`);
  console.log('');
  
  if (results.criticalIssues.length > 0) {
    console.log('🚨 CRITICAL ISSUES:');
    for (const issue of results.criticalIssues) {
      console.log(`   - ${issue.agent}: Missing ${issue.fails.map(f => f.protocol).join(', ')}`);
    }
  }
  
  // Save results
  const outputPath = path.join(__dirname, 'validation-results.json');
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`\nResults saved to: ${outputPath}`);
  
  return results;
}

/**
 * Generate compliance report
 */
function generateReport() {
  const results = runValidation();
  
  let report = `# Agent Compliance Report

**Generated:** ${new Date().toLocaleString()}
**Total Agents:** ${results.totalAgents}

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Compliant | ${results.compliant} | ${Math.round(results.compliant/results.totalAgents*100)}% |
| 🟡 Partial | ${results.partial} | ${Math.round(results.partial/results.totalAgents*100)}% |
| ❌ Non-Compliant | ${results.nonCompliant} | ${Math.round(results.nonCompliant/results.totalAgents*100)}% |

## Critical Issues

`;

  if (results.criticalIssues.length > 0) {
    for (const issue of results.criticalIssues) {
      report += `### ${issue.agent}\n`;
      report += `**Category:** ${issue.category}\n`;
      report += `**Missing:**\n`;
      for (const fail of issue.fails) {
        report += `- ${fail.description}\n`;
      }
      report += '\n';
    }
  } else {
    report += 'No critical issues found.\n';
  }

  report += `\n## Agent Details\n\n`;
  
  // Group by status
  const grouped = {
    compliant: results.agents.filter(a => a.status === 'compliant'),
    partial: results.agents.filter(a => a.status === 'partial'),
    nonCompliant: results.agents.filter(a => a.status === 'non-compliant')
  };
  
  report += `### ✅ Compliant Agents (${grouped.compliant.length})\n\n`;
  for (const agent of grouped.compliant) {
    report += `- **${agent.name}** [${agent.score}%]\n`;
  }
  
  report += `\n### 🟡 Partially Compliant (${grouped.partial.length})\n\n`;
  for (const agent of grouped.partial) {
    report += `- **${agent.name}** [${agent.score}%]\n`;
  }
  
  report += `\n### ❌ Non-Compliant (${grouped.nonCompliant.length})\n\n`;
  for (const agent of grouped.nonCompliant) {
    report += `- **${agent.name}** [${agent.score}%]\n`;
  }
  
  const reportPath = path.join(__dirname, 'compliance-report.md');
  fs.writeFileSync(reportPath, report);
  console.log(`\nReport saved to: ${reportPath}`);
  
  return report;
}

// Export functions
module.exports = { runValidation, generateReport, validateAgent };

// Run if called directly
if (require.main === module) {
  generateReport();
}




