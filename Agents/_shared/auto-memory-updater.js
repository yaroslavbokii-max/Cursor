/**
 * Auto-Memory Updater
 * 
 * Automatically updates agent MEMORY.md files after task completion.
 * Designed to be called by the orchestrator or individual agents.
 * 
 * Version: 1.0
 */

const fs = require('fs');
const path = require('path');

// Configuration
const AGENTS_ROOT = path.join(__dirname, '..');
const MEMORY_FILE = 'MEMORY.md';

/**
 * Parse existing MEMORY.md to extract structured data
 */
function parseMemory(memoryPath) {
  if (!fs.existsSync(memoryPath)) {
    return {
      version: '1.0',
      learnings: [],
      antiPatterns: [],
      stats: { totalTasks: 0, successRate: 0 }
    };
  }

  const content = fs.readFileSync(memoryPath, 'utf-8');
  
  // Basic parsing - count learnings and antipatterns
  const learnings = (content.match(/## Learning \d+/g) || []).length;
  const antiPatterns = (content.match(/🔴|Anti-pattern/g) || []).length;
  
  return {
    content,
    learningCount: learnings,
    antiPatternCount: antiPatterns
  };
}

/**
 * Generate a new learning entry
 */
function generateLearningEntry(learning) {
  const date = new Date().toISOString().split('T')[0];
  const id = Date.now();
  
  return `
## Learning ${id} | ${date}

**Category:** ${learning.category || 'General'}
**Source:** ${learning.source || 'Task completion'}

### What Happened
${learning.what}

### Why It Matters
${learning.why || 'Improves future task execution'}

### Rule/Pattern
${learning.rule}

### Tags
${(learning.tags || ['general']).map(t => `#${t}`).join(' ')}

---
`;
}

/**
 * Generate an anti-pattern entry
 */
function generateAntiPatternEntry(antiPattern) {
  const date = new Date().toISOString().split('T')[0];
  
  return `
## 🔴 Anti-Pattern | ${date}

**Error:** ${antiPattern.error}
**Impact:** ${antiPattern.impact}
**Fix:** ${antiPattern.fix}
**Prevention:** ${antiPattern.prevention}

---
`;
}

/**
 * Update an agent's MEMORY.md file
 */
function updateAgentMemory(agentPath, updates) {
  const memoryPath = path.join(agentPath, MEMORY_FILE);
  const existing = parseMemory(memoryPath);
  
  let newContent = existing.content || '';
  
  // Add new learnings
  if (updates.learnings && updates.learnings.length > 0) {
    for (const learning of updates.learnings) {
      newContent += generateLearningEntry(learning);
    }
  }
  
  // Add new anti-patterns
  if (updates.antiPatterns && updates.antiPatterns.length > 0) {
    for (const ap of updates.antiPatterns) {
      newContent += generateAntiPatternEntry(ap);
    }
  }
  
  // Update stats section if exists
  const statsMatch = newContent.match(/Total Learnings:\s*(\d+)/);
  if (statsMatch) {
    const currentCount = parseInt(statsMatch[1]);
    const newCount = currentCount + (updates.learnings?.length || 0);
    newContent = newContent.replace(
      /Total Learnings:\s*\d+/,
      `Total Learnings: ${newCount}`
    );
  }
  
  fs.writeFileSync(memoryPath, newContent);
  
  return {
    success: true,
    path: memoryPath,
    learningsAdded: updates.learnings?.length || 0,
    antiPatternsAdded: updates.antiPatterns?.length || 0
  };
}

/**
 * Cross-agent memory sync
 * When one agent learns something, propagate to related agents
 */
function syncCrossAgentLearning(sourceAgent, learning, targetAgents) {
  const results = [];
  
  for (const target of targetAgents) {
    const targetPath = path.join(AGENTS_ROOT, target);
    if (fs.existsSync(targetPath)) {
      const crossLearning = {
        ...learning,
        source: `Cross-agent from @${sourceAgent}`,
        category: `Cross-Agent: ${learning.category}`
      };
      
      const result = updateAgentMemory(targetPath, { learnings: [crossLearning] });
      results.push({ agent: target, ...result });
    }
  }
  
  return results;
}

/**
 * Generate task completion summary
 */
function generateTaskSummary(taskData) {
  return {
    taskId: taskData.id || Date.now(),
    agent: taskData.agent,
    timestamp: new Date().toISOString(),
    duration: taskData.duration,
    success: taskData.success,
    qualityScore: taskData.qualityScore,
    feedbackReceived: taskData.feedback || null,
    learnings: taskData.learnings || [],
    issues: taskData.issues || []
  };
}

/**
 * Log task to agent's memory
 */
function logTaskToMemory(agentPath, taskSummary) {
  const memoryPath = path.join(agentPath, MEMORY_FILE);
  
  // Convert task summary to learning if successful
  const updates = {
    learnings: []
  };
  
  if (taskSummary.success && taskSummary.learnings.length > 0) {
    for (const learning of taskSummary.learnings) {
      updates.learnings.push({
        category: 'Task Completion',
        what: learning.description,
        why: 'Successful task execution',
        rule: learning.rule || learning.description,
        tags: learning.tags || ['task', 'success']
      });
    }
  }
  
  if (taskSummary.issues.length > 0) {
    updates.antiPatterns = taskSummary.issues.map(issue => ({
      error: issue.description,
      impact: issue.impact || 'Task quality affected',
      fix: issue.fix || 'Review and adjust',
      prevention: issue.prevention || 'Check before delivery'
    }));
  }
  
  return updateAgentMemory(agentPath, updates);
}

// Export functions
module.exports = {
  parseMemory,
  updateAgentMemory,
  syncCrossAgentLearning,
  generateTaskSummary,
  logTaskToMemory,
  generateLearningEntry,
  generateAntiPatternEntry
};

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args[0] === 'update' && args[1]) {
    const agentPath = args[1];
    const learning = {
      category: args[2] || 'Manual Entry',
      what: args[3] || 'Learning from CLI',
      why: args[4] || 'Manual documentation',
      rule: args[5] || 'N/A',
      tags: ['manual']
    };
    
    const result = updateAgentMemory(agentPath, { learnings: [learning] });
    console.log('Memory updated:', result);
  } else {
    console.log('Usage: node auto-memory-updater.js update <agent-path> [category] [what] [why] [rule]');
  }
}




