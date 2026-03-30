# Agent Memory — Expert Panel

**Last Updated:** 2026-01-13
**Total Learnings:** 5
**Projects Contributed To:** [MECE Workshop 2026-01-13]

---

## 🧠 Core Learnings

### What Works Well
1. **Quality Gate Mode** — Using panel to challenge/validate other agents' outputs
2. **Role-specific experts** — Matching expert profiles to the review task improves relevance
3. **Auto-trigger recommendation** — Orchestrator suggesting panel after knowledge extraction
4. **Offering role options** — Let user choose from predefined expert profiles with recommendations
5. **Industry-specific context** — Including domain knowledge (food delivery) makes insights actionable

### What Doesn't Work
1. **Too many experts at once** — 3-4 focused experts better than 6+ unfocused
2. **Generic expert profiles** — Industry-specific expertise produces better insights
3. **Skipping the panel** — Outputs benefit from expert review before delivery

### User Preferences Discovered
- **Trigger:** Appreciates auto-trigger recommendation after knowledge extraction
- **Expert selection:** Wants options with recommendations, not forced choice
- **Output:** Values actionable critique over theoretical discussion

---

## 📊 Usage Statistics

| Metric | Value |
|--------|-------|
| Times Invoked | 1 |
| Panel Discussions Generated | 1 |
| Avg Output Quality | High |
| Most Common Task Type | Quality Gate review |

---

## 🔗 Context Connections

### Works Best With
- @knowledge-extractor — When: validating extracted knowledge
- @data-analyst — When: strategic decisions need data validation
- @product-architect — When: product decisions need expert perspectives
- @presentation-maker — When: presenting expert findings
- @orchestration-agent — When: coordinating multi-agent workflows

### Struggles With
- Very narrow technical topics (may need specialized SME instead)
- Time-sensitive decisions (panel discussion takes time)

---

## 📝 Project-Specific Notes

### MECE Workshop (2026-01-13)
- **Context:** Quality review of MECE framework teaching materials
- **Mode:** Quality Gate (validating content before delivery)
- **Expert Profiles Used:**
  1. Critical Reviewer — Identified logical gaps
  2. Relevance Assessor — Ensured industry fit
  3. Bias Detector — Checked for oversimplification
- **What Worked:** 
  - Auto-trigger after knowledge extraction
  - Industry-specific (food delivery) context improved relevance
  - Expert discussion format made critique constructive
- **What to Improve:** 
  - Could add "Learning Expert" profile for educational content
  - Consider timing within workflow (earlier = less rework)

---

## 👥 Expert Panel Profiles

### Quality Gate Profiles (v1.2)

| Profile | Purpose | Best For |
|---------|---------|----------|
| 🔍 Critical Reviewer | Identify flaws, biases, gaps | Any output needing scrutiny |
| 📊 Data Validator | Verify accuracy, consistency | Data-driven outputs |
| 🎯 Relevance Assessor | Check if output addresses need | Task-specific deliverables |
| ⚖️ Bias Detector | Find implicit biases, assumptions | Analysis, recommendations |
| 🔗 Connection Mapper | Explore implications, interdependencies | Strategic decisions |

### Workshop-Specific Profiles (NEW)

| Profile | Purpose | Best For |
|---------|---------|----------|
| 🎓 Learning Expert | Validate pedagogical effectiveness | Training materials |
| 🏭 Industry SME | Check domain accuracy | Industry-specific content |
| 👥 Audience Advocate | Ensure accessibility for target audience | Any presentation/workshop |

---

## 🎯 Auto-Trigger Rules

### When to Auto-Recommend Panel

| After Agent | Recommended Profile | Reason |
|-------------|---------------------|--------|
| @knowledge-extractor | Critical Reviewer | Validate extracted knowledge |
| @data-analyst | Data Validator | Verify analysis accuracy |
| @presentation-maker | Relevance Assessor | Check message clarity |
| @workshop-exercise-designer | Learning Expert | Validate pedagogical approach |

---

*Auto-updated after each agent invocation*
