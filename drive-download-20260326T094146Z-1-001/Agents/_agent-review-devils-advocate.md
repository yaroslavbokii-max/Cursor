# 🔥 Devil's Advocate Agent Review

**Date:** 2026-01-12  
**Total Agents:** 45  
**Review Type:** Quick Scan + Improvement Urgency Ranking

---

## 📊 Improvement Urgency Ranking

### 🔴 HIGH PRIORITY (Critical Gaps)

| Rank | Agent | Version | Top 3 Improvements | Why Urgent |
|------|-------|---------|-------------------|------------|
| **1** | `@data-analyst` | v6.1 | 1. **No Bolt Food context integration** — Should auto-load `/Context/Bolt_Food_Metrics_Glossary.md`<br>2. **Missing statistical rigor** — No hypothesis testing, confidence intervals<br>3. **No anomaly detection patterns** — Can't auto-flag outliers | Most-used agent, high impact |
| **2** | `@presentation-maker` | v1.3 | 1. **No Gamma optimization** — Should integrate with `@gamma-optimizer`<br>2. **Missing McKinsey slide templates** — Waterfalls, bridges, guns<br>3. **No data visualization handoff** — Should call `@data-visualization-expert` | Core output agent |
| **3** | `@report-automator` | v1.0 | 1. **No template learning** — Can't extract structure from examples<br>2. **Missing data source connectors** — Only CSV, no Looker/Sheets<br>3. **No narrative generation** — Just data replacement, no insights | User's #1 use case |
| **4** | `@orchestration-agent` | v3.0 | 1. **No agent capability index** — Doesn't know agent strengths/limits<br>2. **Missing workflow templates** — Should suggest proven flows<br>3. **No execution monitoring** — Can't track multi-agent progress | Central coordinator |
| **5** | `@product-architect` | v1.1 | 1. **No customer validation** — Should integrate `@customer-insight-analyst`<br>2. **Missing competitive analysis** — No market context<br>3. **No MVP scoping** — Full PRD only, no lean version | Strategy agent |

### 🟡 MEDIUM PRIORITY (Significant Improvements Needed)

| Rank | Agent | Version | Top 3 Improvements | Why Medium |
|------|-------|---------|-------------------|------------|
| **6** | `@prd-architect` | v1.0 | 1. **No UI/UX wireframe generation** — Just text specs<br>2. **Missing user story mapping** — No journey integration<br>3. **No technical feasibility check** — Doesn't validate with `@code-generator` | New agent, needs depth |
| **7** | `@copywriter` | v1.0 | 1. **No A/B variant generation** — Single version only<br>2. **Missing conversion frameworks** — AIDA, PAS not explicit<br>3. **No brand voice integration** — Should auto-load tone files | Content quality |
| **8** | `@personal-brand-builder` | v1.0 | 1. **No content calendar generation** — Just individual posts<br>2. **Missing engagement analytics** — Can't learn what works<br>3. **No cross-platform adaptation** — Same content everywhere | User priority |
| **9** | `@meeting-commander` | v1.0 | 1. **No transcript processing** — Manual input only<br>2. **Missing action item tracking** — No follow-up system<br>3. **No meeting type templates** — Generic format only | Productivity core |
| **10** | `@team-template-generator` | v1.0 | 1. **No template customization** — Static templates<br>2. **Missing context injection** — Doesn't personalize<br>3. **No version control** — Can't track template evolution | Manager tool |
| **11** | `@people-leader-coach` | v1.0 | 1. **No conversation simulation** — Just advice, no practice<br>2. **Missing personality adaptation** — One-size-fits-all<br>3. **No progress tracking** — Can't measure coaching impact | HR critical |
| **12** | `@data-visualization-expert` | v1.0 | 1. **No code generation** — Just recommendations<br>2. **Missing interactive charts** — Static only<br>3. **No accessibility validation** — Color blindness not checked | Visual quality |
| **13** | `@layout-architect` | v1.0 | 1. **No preview generation** — Can't show before print<br>2. **Missing responsive rules** — Fixed dimensions only<br>3. **No template library** — Starts from scratch | Print quality |
| **14** | `@customer-insight-analyst` | v1.0 | 1. **No data source integration** — Manual input only<br>2. **Missing sentiment analysis** — No NLP patterns<br>3. **No persona generation** — Just insights, no profiles | Strategy input |
| **15** | `@n8n-workflow-architect` | v1.0 | 1. **No workflow validation** — Should use n8n-mcp tools<br>2. **Missing error handling patterns** — Happy path only<br>3. **No credential management** — Security gaps | Automation core |

### 🟢 LOWER PRIORITY (Polish & Enhancement)

| Rank | Agent | Version | Top 3 Improvements | Why Lower |
|------|-------|---------|-------------------|------------|
| **16** | `@prompt-architect` | v2.1 | 1. **No prompt testing** — Can't validate effectiveness<br>2. **Missing prompt library** — Starts fresh each time<br>3. **No version comparison** — Can't A/B prompts | Meta agent |
| **17** | `@agent-architect` | v2.0 | 1. **No agent testing framework** — Can't validate new agents<br>2. **Missing capability gap detection** — Manual only<br>3. **No agent deprecation workflow** — No cleanup process | Meta agent |
| **18** | `@context-builder` | v1.1 | 1. **No auto-discovery** — Manual file specification<br>2. **Missing relevance scoring** — All context equal<br>3. **No context compression** — Token-heavy | Support agent |
| **19** | `@knowledge-extractor` | v1.2 | 1. **Overlap with `@research-to-prompt`** — Should merge<br>2. **No source validation** — Trusts all inputs<br>3. **Missing citation generation** — No attribution | Support agent |
| **20** | `@research-to-prompt` | v1.1 | 1. **Overlap with `@knowledge-extractor`** — Should merge<br>2. **No research quality scoring** — All sources equal<br>3. **Missing synthesis patterns** — Just extraction | Support agent |
| **21** | `@visual-designer` | v1.1 | 1. **No brand guideline enforcement** — Should use `@style-guardian`<br>2. **Missing asset generation** — Just specs<br>3. **No design system integration** — One-off designs | Creation agent |
| **22** | `@workshop-exercise-designer` | v1.2 | 1. **No difficulty calibration** — One level fits all<br>2. **Missing time estimation** — No duration guidance<br>3. **No facilitation tips** — Just exercises | Creation agent |
| **23** | `@expert-panel` | v1.1 | 1. **No expert selection logic** — Random experts<br>2. **Missing debate synthesis** — Just opinions<br>3. **No confidence scoring** — All views equal | Analysis agent |
| **24** | `@gtm-strategist` | v1.0 | 1. **No market data integration** — Theoretical only<br>2. **Missing competitor tracking** — Static analysis<br>3. **No launch timeline generation** — No Gantt | Strategy agent |
| **25** | `@idea-forge` | v1.0 | 1. **No idea validation** — Just generation<br>2. **Missing feasibility scoring** — All ideas equal<br>3. **No idea evolution tracking** — One-shot | Strategy agent |
| **26-45** | *Remaining 20 agents* | v1.0 | Generally solid for v1.0, need real-world usage to identify gaps | New agents |

---

## 🎯 Top 10 Improvements to Implement

Based on impact and user needs:

| # | Improvement | Agent(s) | Impact | Effort |
|---|-------------|----------|--------|--------|
| **1** | Auto-load Bolt Food context | `@data-analyst` | 🔥🔥🔥 | Low |
| **2** | Gamma integration | `@presentation-maker` | 🔥🔥🔥 | Medium |
| **3** | Template learning from examples | `@report-automator` | 🔥🔥🔥 | High |
| **4** | McKinsey slide templates | `@presentation-maker` | 🔥🔥 | Medium |
| **5** | n8n-mcp validation integration | `@n8n-workflow-architect` | 🔥🔥 | Medium |
| **6** | Merge knowledge-extractor + research-to-prompt | Both | 🔥🔥 | Medium |
| **7** | A/B variant generation | `@copywriter` | 🔥🔥 | Low |
| **8** | Content calendar generation | `@personal-brand-builder` | 🔥🔥 | Medium |
| **9** | Conversation simulation | `@people-leader-coach` | 🔥🔥 | High |
| **10** | Chart code generation | `@data-visualization-expert` | 🔥🔥 | Medium |

---

## 🔄 Suggested Agent Mergers

| Merge | Agents | Reason | New Name |
|-------|--------|--------|----------|
| **1** | `@knowledge-extractor` + `@research-to-prompt` | 80% overlap in functionality | `@research-synthesizer` |
| **2** | `@visual-designer` + `@layout-architect` | Both handle visual formatting | Keep separate but integrate |

---

## 🆕 New Agents Needed (Phase 4)

Based on gaps identified:

| Agent | Category | Purpose | Priority |
|-------|----------|---------|----------|
| `@saas-architect` | strategy | Business model design, pricing, monetization | High |
| `@process-optimizer` | productivity | Process analysis, bottleneck identification | High |
| `@project-commander` | productivity | Full project lifecycle management | High |
| `@productivity-system-designer` | productivity | Personal systems (GTD, etc.) | Medium |
| `@energy-manager` | wellness | Work-life balance, energy optimization | Medium |
| `@reflection-facilitator` | wellness | Self-coaching, journaling, reviews | Medium |
| `@habit-architect` | wellness | Behavioral science, habit loops | Medium |

---

## 📋 Implementation Recommendation

### Phase 3A: Quick Wins (This Session)
1. ✅ Add Bolt Food context auto-loading to `@data-analyst`
2. ✅ Add Gamma integration to `@presentation-maker`
3. ✅ Add A/B variants to `@copywriter`
4. ✅ Add n8n-mcp tools to `@n8n-workflow-architect`

### Phase 3B: Medium Effort (Next Session)
5. McKinsey templates for `@presentation-maker`
6. Content calendar for `@personal-brand-builder`
7. Chart code generation for `@data-visualization-expert`
8. Merge `@knowledge-extractor` + `@research-to-prompt`

### Phase 4: New Agents
9. Create wellness category + 3 wellness agents
10. Create remaining strategy/productivity agents

---

**Ready to implement?** Say "proceed" and I'll start with the Quick Wins.




