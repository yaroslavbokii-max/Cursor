# 🔄 Agent Consolidation Plan

**Goal:** Reduce 62 agents → ~35 agents
**Reason:** Too many agents creates confusion. Consolidate overlapping functionality.

---

## 📊 Current State

### Agents by Category (62 total)

| Category | Count | Agents |
|----------|-------|--------|
| **Analysis** | 9 | data-analyst, data-visualization-expert, knowledge-extractor, context-builder, financial-modeler, customer-insight-analyst, contract-reviewer, document-processor, data-enrichment-agent |
| **Automation** | 3 | web-scraper-ninja, n8n-workflow-architect, devops-setup-agent |
| **Content** | 5 | copywriter, email-composer, brand-architect, personal-brand-builder, seo-optimizer |
| **Creation** | 10 | presentation-maker, layout-architect, workshop-exercise-designer, visual-designer, gamma-optimizer, pitch-deck-creator, form-generator, facilitation-guide-generator, interactive-content-compiler, personalized-plan-generator |
| **Knowledge** | 2 | learning-accelerator, knowledge-base-architect |
| **Meta** | 7 | orchestration-agent, prompt-architect, quality-assurance-reviewer, agent-architect, style-guardian, user-manual-generator, workflow-showcase-builder |
| **People** | 2 | people-leader-coach, account-manager-helper |
| **Product** | 5 | prd-architect, operations-dashboard-builder, code-generator, internal-tool-builder, database-architect |
| **Productivity** | 7 | report-automator, meeting-commander, okr-coach, team-template-generator, process-optimizer, project-commander, productivity-system-designer |
| **Strategy** | 8 | expert-panel, idea-forge, gtm-strategist, saas-architect, product-architect, competitive-analyst, market-researcher, decision-framework-builder |
| **Wellness** | 4 | habit-architect, energy-manager, reflection-facilitator, (research-to-prompt - deprecated) |

---

## 🎯 Consolidation Strategy

### Principle 1: Merge Overlapping Functionality
Combine agents that do similar things with slightly different focus.

### Principle 2: Keep Specialized Experts
Keep agents that have deep, specialized knowledge (e.g., data-analyst, web-scraper).

### Principle 3: Simplify for Users
User shouldn't need to know 62 agents. They should be able to describe their need and get routed correctly.

---

## 🔀 Proposed Mergers

### Analysis (9 → 5)

| Keep | Merge Into It | Reason |
|------|---------------|--------|
| `data-analyst` | - | Core, specialized |
| `data-visualization-expert` | - | Deep chart expertise |
| `knowledge-extractor` | `research-to-prompt` (deprecated), `context-builder` | Same function: extract knowledge |
| `financial-modeler` | - | Specialized |
| `document-processor` | `contract-reviewer`, `data-enrichment-agent` | All process documents |

### Content (5 → 3)

| Keep | Merge Into It | Reason |
|------|---------------|--------|
| `copywriter` | `seo-optimizer` | Both write copy, SEO is a technique |
| `email-composer` | - | Specialized format |
| `brand-architect` | `personal-brand-builder` | Personal brand is subset of brand |

### Creation (10 → 6)

| Keep | Merge Into It | Reason |
|------|---------------|--------|
| `presentation-maker` | `pitch-deck-creator`, `gamma-optimizer` | All make presentations |
| `layout-architect` | - | Specialized for print |
| `workshop-exercise-designer` | `facilitation-guide-generator`, `interactive-content-compiler` | All workshop materials |
| `visual-designer` | - | Visual assets |
| `form-generator` | - | Specialized |
| `personalized-plan-generator` | - | Unique function |

### Meta (7 → 5)

| Keep | Merge Into It | Reason |
|------|---------------|--------|
| `orchestration-agent` | - | Core |
| `prompt-architect` | - | Core |
| `quality-assurance-reviewer` | `style-guardian` | Both review quality |
| `agent-architect` | - | Core |
| `workflow-showcase-builder` | `user-manual-generator` | Both document the system |

### Productivity (7 → 4)

| Keep | Merge Into It | Reason |
|------|---------------|--------|
| `report-automator` | - | Specialized |
| `meeting-commander` | - | Specialized |
| `project-commander` | `okr-coach`, `process-optimizer` | All manage work |
| `team-template-generator` | `productivity-system-designer` | Both create structures |

### Strategy (8 → 5)

| Keep | Merge Into It | Reason |
|------|---------------|--------|
| `expert-panel` | - | Unique function |
| `idea-forge` | `decision-framework-builder` | Both ideation/decision |
| `gtm-strategist` | `market-researcher` | Both market-focused |
| `saas-architect` | - | Specialized |
| `product-architect` | `competitive-analyst` | Both product strategy |

### Product (5 → 4)

| Keep | Merge Into It | Reason |
|------|---------------|--------|
| `prd-architect` | - | Specialized |
| `code-generator` | `internal-tool-builder` | Both generate code |
| `database-architect` | - | Specialized |
| `operations-dashboard-builder` | - | Specialized |

### Other Categories (Keep as is)

| Category | Agents | Notes |
|----------|--------|-------|
| Automation (3) | Keep all | Each is specialized |
| Knowledge (2) | Keep all | Different purposes |
| People (2) | Keep all | Different purposes |
| Wellness (3) | Keep all | Different purposes |

---

## 📋 Resulting Agent List (~35 agents)

### Analysis (5)
1. `data-analyst`
2. `data-visualization-expert`
3. `knowledge-extractor` ← Merged: context-builder, research-to-prompt
4. `financial-modeler`
5. `document-processor` ← Merged: contract-reviewer, data-enrichment

### Automation (3)
6. `web-scraper-ninja`
7. `n8n-workflow-architect`
8. `devops-setup-agent`

### Content (3)
9. `copywriter` ← Merged: seo-optimizer
10. `email-composer`
11. `brand-architect` ← Merged: personal-brand-builder

### Creation (6)
12. `presentation-maker` ← Merged: pitch-deck, gamma-optimizer
13. `layout-architect`
14. `workshop-exercise-designer` ← Merged: facilitation-guide, interactive-content
15. `visual-designer`
16. `form-generator`
17. `personalized-plan-generator`

### Knowledge (2)
18. `learning-accelerator`
19. `knowledge-base-architect`

### Meta (5)
20. `orchestration-agent`
21. `prompt-architect`
22. `quality-assurance-reviewer` ← Merged: style-guardian
23. `agent-architect`
24. `documentation-generator` ← Merged: user-manual, workflow-showcase

### People (2)
25. `people-leader-coach`
26. `account-manager-helper`

### Product (4)
27. `prd-architect`
28. `code-generator` ← Merged: internal-tool-builder
29. `database-architect`
30. `operations-dashboard-builder`

### Productivity (4)
31. `report-automator`
32. `meeting-commander`
33. `project-commander` ← Merged: okr-coach, process-optimizer
34. `team-template-generator` ← Merged: productivity-system-designer

### Strategy (5)
35. `expert-panel`
36. `idea-forge` ← Merged: decision-framework-builder
37. `gtm-strategist` ← Merged: market-researcher
38. `saas-architect`
39. `product-architect` ← Merged: competitive-analyst

### Wellness (3)
40. `habit-architect`
41. `energy-manager`
42. `reflection-facilitator`

**Total: 42 agents** (reduced from 62)

---

## 🔧 Implementation Steps

### Phase 1: Mark Deprecated (Now)
1. Add deprecation notice to agents being merged
2. Point to new parent agent
3. Keep files for reference

### Phase 2: Merge Capabilities (Next)
1. Update parent agent with merged capabilities
2. Update triggers to capture merged agent triggers
3. Update MEMORY with merged learnings

### Phase 3: Update References (After)
1. Update `_catalog.md`
2. Update orchestration agent
3. Update documentation

### Phase 4: Archive (Later)
1. Move deprecated agents to `_archived/`
2. Keep for historical reference

---

## ⚠️ Risks

| Risk | Mitigation |
|------|------------|
| Lose specialized capability | Merge ALL triggers and capabilities |
| User confusion | Clear deprecation notices |
| Break existing workflows | Keep old agent files with redirect |

---

## ✅ Immediate Actions

1. Update `_catalog.md` with consolidation notes
2. Add deprecation notices to 20 agents being merged
3. Update parent agents with merged capabilities
4. Test that orchestrator routes correctly

---

*This plan reduces cognitive load while preserving all functionality.*




