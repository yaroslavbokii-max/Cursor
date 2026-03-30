# Agent Catalog v6.0

**Total Agents:** 62 (61 active + 1 deprecated)  
**Categories:** 11  
**Protocols:** 22 (cross-cutting standards)  
**Brand Presets:** 10  
**Last Updated:** 2026-01-13

**v6.0 Updates:**
- **User-Focused Documentation** — Getting started, use case cards, simple architecture
- **10 Brand Presets** — Added Startup/VC, Data Dark, Warm Earth
- **Gap Detection Protocol** — Honest about limitations, captures feedback
- **Simplified Mental Model** — 3-layer architecture explanation
- **Quality-First Approach** — Focus on quality over speed

---

## Quick Reference: "I want to..."

| If you want to... | Use this agent | Or ask Orchestrator |
|-------------------|----------------|---------------------|
| Analyze data | @data-analyst | "analyze this data" |
| Create a presentation | @presentation-maker | "create presentation about X" |
| Write a blog post | @personal-brand-builder | "write LinkedIn post about X" |
| Build an internal tool | @internal-tool-builder | "build a dashboard for X" |
| Understand customers | @customer-insight-analyst | "understand why customers do X" |
| Automate a workflow | @n8n-workflow-architect | "automate this process" |
| Scrape a website | @web-scraper-ninja | "get data from this website" |
| Create a PRD | @prd-architect | "product requirements for X" |
| Launch a product | @gtm-strategist | "go-to-market strategy" |
| Learn something | @learning-accelerator | "teach me about X" |
| **NEW: Build a SaaS** | @saas-architect | "design SaaS business model" |
| **NEW: Optimize process** | @process-optimizer | "streamline this process" |
| **NEW: Manage project** | @project-commander | "create project plan" |
| **NEW: Build habits** | @habit-architect | "help me build a habit" |
| **NEW: Manage energy** | @energy-manager | "optimize my energy" |

---

## YAML Index (for AI parsing)

```yaml
version: "4.0"
total_agents: 62
categories:
  - meta
  - analysis
  - creation
  - strategy
  - product
  - content
  - automation
  - knowledge
  - productivity
  - people
  - wellness  # NEW

agents:
  # === META (System agents) ===
  - name: orchestration-agent
    category: meta
    path: meta/orchestration-agent
    description: Central coordinator for multi-agent workflows
    tags: [orchestration, planning, coordination]
    triggers: ["complex task", "multi-step", "I need help with"]
    works_with: [all]
    
  - name: agent-architect
    category: meta
    path: meta/agent-architect
    description: Creates and designs new agents
    tags: [agent-creation, design]
    triggers: ["create new agent", "design agent"]
    works_with: [orchestration-agent]
    
  - name: prompt-architect
    category: meta
    path: meta/prompt-architect
    description: Crafts and optimizes prompts
    tags: [prompts, optimization]
    triggers: ["improve prompt", "write prompt"]
    works_with: [all]
    
  - name: quality-assurance-reviewer
    category: meta
    path: meta/quality-assurance-reviewer
    description: Reviews outputs for quality and accuracy
    tags: [QA, review, validation]
    triggers: ["review this", "check quality", "is this good"]
    works_with: [all]
    
  - name: style-guardian
    category: meta
    path: meta/style-guardian
    description: Ensures brand and style consistency
    tags: [brand, style, consistency]
    triggers: ["check brand alignment", "style review"]
    works_with: [all, brand-architect]
    
  - name: user-manual-generator
    category: meta
    path: meta/user-manual-generator
    description: Creates user documentation
    tags: [documentation, manual, help]
    triggers: ["create documentation", "user manual"]
    works_with: [orchestration-agent]
    
  - name: workflow-showcase-builder
    category: meta
    path: meta/workflow-showcase-builder
    description: Creates interactive workflow showcases
    tags: [showcase, HTML, catalog]
    triggers: ["create showcase", "show capabilities"]
    works_with: [user-manual-generator]

  # === ANALYSIS ===
  - name: data-analyst
    category: analysis
    path: analysis/data-analyst
    description: Analyzes data, finds insights, creates visualizations
    tags: [data, analysis, visualization, insights]
    triggers: ["analyze data", "why did X change", "data insights"]
    works_with: [data-visualization-expert, presentation-maker]
    
  - name: data-visualization-expert
    category: analysis
    path: analysis/data-visualization-expert
    description: Creates world-class McKinsey-level visualizations
    tags: [visualization, charts, dashboards]
    triggers: ["create chart", "visualize data", "dashboard"]
    works_with: [data-analyst, presentation-maker]
    
  - name: customer-insight-analyst
    category: analysis
    path: analysis/customer-insight-analyst
    description: Deep customer understanding through research synthesis
    tags: [customer, research, personas, journey-mapping]
    triggers: ["understand customers", "customer research", "pain points"]
    works_with: [data-analyst, product-architect]
    
  - name: context-builder
    category: analysis
    path: analysis/context-builder
    description: Assembles context for AI tasks
    tags: [context, preparation]
    triggers: ["build context", "prepare information"]
    works_with: [all]
    
  - name: knowledge-extractor
    category: analysis
    path: analysis/knowledge-extractor
    description: "v2.0 — Extract, synthesize, transform research into agents, KBs, summaries (merged with research-to-prompt)"
    tags: [extraction, synthesis, research, prompts, RAG, summarization]
    triggers: ["extract knowledge", "synthesize documents", "research to prompt", "create agent from research"]
    works_with: [document-processor, learning-accelerator, prompt-architect, agent-architect, presentation-maker]
    
  - name: research-to-prompt
    category: analysis
    path: analysis/research-to-prompt
    description: "⚠️ DEPRECATED — Use @knowledge-extractor v2.0 instead"
    tags: [deprecated, research, prompts]
    deprecated: true
    superseded_by: knowledge-extractor
    triggers: ["research to prompt"]
    works_with: [knowledge-extractor]
    
  - name: data-enrichment-agent
    category: analysis
    path: analysis/data-enrichment-agent
    description: Enriches and structures raw data
    tags: [data, enrichment, cleaning]
    triggers: ["clean data", "enrich data", "structure data"]
    works_with: [data-analyst, web-scraper-ninja]
    
  - name: document-processor
    category: analysis
    path: analysis/document-processor
    description: Processes and extracts from documents
    tags: [documents, extraction, parsing]
    triggers: ["process document", "extract from PDF"]
    works_with: [knowledge-extractor]
    
  - name: financial-modeler
    category: analysis
    path: analysis/financial-modeler
    description: Financial projections, scenario planning, unit economics, budgets
    tags: [finance, modeling, projections, unit-economics, budget, FP&A]
    triggers: ["financial model", "revenue projection", "scenario planning", "unit economics"]
    works_with: [data-analyst, saas-architect, presentation-maker, pitch-deck-creator]
    
  - name: contract-reviewer
    category: analysis
    path: analysis/contract-reviewer
    description: Analyzes contracts for risks, key terms, negotiation points
    tags: [contracts, legal, risk-analysis, negotiation, due-diligence]
    triggers: ["review contract", "contract analysis", "contract risks"]
    works_with: [document-processor, knowledge-extractor, decision-framework-builder]

  # === CREATION ===
  - name: presentation-maker
    category: creation
    path: creation/presentation-maker
    description: Creates structured presentations
    tags: [presentations, slides, storytelling]
    triggers: ["create presentation", "slide deck"]
    works_with: [visual-designer, gamma-optimizer, data-analyst]
    
  - name: visual-designer
    category: creation
    path: creation/visual-designer
    description: Visual design guidance and specifications
    tags: [design, visual, UI]
    triggers: ["design visual", "visual direction"]
    works_with: [presentation-maker, brand-architect]
    
  - name: workshop-exercise-designer
    category: creation
    path: creation/workshop-exercise-designer
    description: Creates workshop exercises and activities
    tags: [workshop, exercises, facilitation]
    triggers: ["create workshop", "design exercise"]
    works_with: [facilitation-guide-generator]
    
  - name: gamma-optimizer
    category: creation
    path: creation/gamma-optimizer
    description: Optimizes content for Gamma presentations
    tags: [Gamma, presentations, markdown]
    triggers: ["create for Gamma", "Gamma presentation"]
    works_with: [presentation-maker, visual-designer]
    
  - name: layout-architect
    category: creation
    path: creation/layout-architect
    description: Handles print layouts, alignment, page breaks
    tags: [layout, print, PDF, formatting]
    triggers: ["fix layout", "print-ready", "page formatting"]
    works_with: [presentation-maker, visual-designer]
    
  - name: form-generator
    category: creation
    path: creation/form-generator
    description: Generates forms and surveys
    tags: [forms, surveys, data-collection]
    triggers: ["create form", "survey design"]
    works_with: [internal-tool-builder]
    
  - name: facilitation-guide-generator
    category: creation
    path: creation/facilitation-guide-generator
    description: Creates facilitation guides for meetings/workshops
    tags: [facilitation, meetings, guides]
    triggers: ["facilitation guide", "meeting plan"]
    works_with: [workshop-exercise-designer]
    
  - name: personalized-plan-generator
    category: creation
    path: creation/personalized-plan-generator
    description: Creates personalized plans and programs
    tags: [plans, personalization]
    triggers: ["create plan", "personalized program"]
    works_with: [learning-accelerator]
    
  - name: interactive-content-compiler
    category: creation
    path: creation/interactive-content-compiler
    description: Creates interactive HTML content
    tags: [interactive, HTML, content]
    triggers: ["interactive content", "HTML guide"]
    works_with: [visual-designer]
    
  - name: pitch-deck-creator
    category: creation
    path: creation/pitch-deck-creator
    description: Creates investor pitch decks and board presentations
    tags: [pitch-deck, investor, fundraising, board, startup, VC]
    triggers: ["pitch deck", "investor presentation", "board deck", "fundraising"]
    works_with: [presentation-maker, financial-modeler, saas-architect, market-researcher]

  # === STRATEGY ===
  - name: expert-panel
    category: strategy
    path: strategy/expert-panel
    description: Simulates expert perspectives on topics
    tags: [experts, perspectives, analysis]
    triggers: ["expert opinions", "multiple perspectives"]
    works_with: [product-architect, idea-forge]
    
  - name: product-architect
    category: strategy
    path: strategy/product-architect
    description: Product strategy and architecture
    tags: [product, strategy, architecture]
    triggers: ["product strategy", "product design"]
    works_with: [prd-architect, customer-insight-analyst]
    
  - name: idea-forge
    category: strategy
    path: strategy/idea-forge
    description: Creative business idea generation (Thinkertoys)
    tags: [ideation, creativity, brainstorming]
    triggers: ["generate ideas", "brainstorm", "business idea"]
    works_with: [expert-panel, product-architect]
    
  - name: gtm-strategist
    category: strategy
    path: strategy/gtm-strategist
    description: Go-to-market strategy and launch planning
    tags: [GTM, marketing, launch, positioning]
    triggers: ["go-to-market", "launch plan", "positioning"]
    works_with: [product-architect, brand-architect, copywriter]
    
  - name: saas-architect
    category: strategy
    path: strategy/saas-architect
    description: SaaS business model, pricing, unit economics design
    tags: [SaaS, business-model, pricing, monetization, unit-economics]
    triggers: ["SaaS business", "pricing strategy", "unit economics", "subscription model"]
    works_with: [product-architect, gtm-strategist, prd-architect]
    
  - name: decision-framework-builder
    category: strategy
    path: strategy/decision-framework-builder
    description: Creates decision frameworks, risk analysis, trade-off matrices
    tags: [decisions, frameworks, risk-analysis, trade-offs]
    triggers: ["help me decide", "decision framework", "risk analysis", "pros and cons"]
    works_with: [expert-panel, data-analyst, financial-modeler]
    
  - name: competitive-analyst
    category: strategy
    path: strategy/competitive-analyst
    description: Competitive intelligence, market positioning, benchmarking
    tags: [competitive-intelligence, competitors, positioning, benchmarking]
    triggers: ["competitor analysis", "competitive landscape", "market positioning"]
    works_with: [web-scraper-ninja, data-analyst, gtm-strategist, market-researcher]
    
  - name: market-researcher
    category: strategy
    path: strategy/market-researcher
    description: Market research, TAM/SAM/SOM analysis, market sizing
    tags: [market-research, TAM, SAM, SOM, market-sizing, trends]
    triggers: ["market size", "TAM SAM SOM", "industry analysis", "market opportunity"]
    works_with: [competitive-analyst, web-scraper-ninja, data-analyst, gtm-strategist]

  # === PRODUCT ===
  - name: prd-architect
    category: product
    path: product/prd-architect
    description: Creates Product Requirements Documents
    tags: [PRD, requirements, specs, UI/UX]
    triggers: ["create PRD", "product requirements", "feature spec"]
    works_with: [product-architect, code-generator, customer-insight-analyst]
    
  - name: code-generator
    category: product
    path: product/code-generator
    description: Generates code from specifications
    tags: [code, development, implementation]
    triggers: ["write code", "implement this"]
    works_with: [prd-architect, database-architect]
    
  - name: database-architect
    category: product
    path: product/database-architect
    description: Designs database schemas
    tags: [database, schema, data-modeling]
    triggers: ["design database", "schema design"]
    works_with: [code-generator, prd-architect]
    
  - name: internal-tool-builder
    category: product
    path: product/internal-tool-builder
    description: Builds internal tools and dashboards
    tags: [internal-tools, dashboards, CRM]
    triggers: ["build internal tool", "create dashboard"]
    works_with: [prd-architect, code-generator, data-visualization-expert]
    
  - name: operations-dashboard-builder
    category: product
    path: product/operations-dashboard-builder
    description: Builds operational dashboards for KPI tracking and monitoring
    tags: [dashboard, operations, KPIs, monitoring, food-delivery, e-commerce]
    triggers: ["operations dashboard", "KPI dashboard", "ops metrics", "monitoring"]
    works_with: [data-analyst, data-visualization-expert, internal-tool-builder]

  # === CONTENT ===
  - name: personal-brand-builder
    category: content
    path: content/personal-brand-builder
    description: Creates personal brand content (LinkedIn, blog, social)
    tags: [personal-brand, LinkedIn, blog, social-media]
    triggers: ["LinkedIn post", "blog post", "Twitter thread"]
    works_with: [copywriter, brand-architect, seo-optimizer]
    
  - name: copywriter
    category: content
    path: content/copywriter
    description: Creates persuasive sales and marketing copy
    tags: [copywriting, sales, marketing, emails, ads]
    triggers: ["sales copy", "email sequence", "ad copy"]
    works_with: [personal-brand-builder, seo-optimizer]
    
  - name: brand-architect
    category: content
    path: content/brand-architect
    description: Creates brand identities and guidelines
    tags: [branding, identity, guidelines, tone-of-voice]
    triggers: ["create brand", "brand guidelines", "tone of voice"]
    works_with: [visual-designer, personal-brand-builder, gtm-strategist]
    
  - name: seo-optimizer
    category: content
    path: content/seo-optimizer
    description: Optimizes content for search engines
    tags: [SEO, search, optimization]
    triggers: ["optimize for SEO", "SEO content"]
    works_with: [personal-brand-builder, copywriter]
    
  - name: email-composer
    category: content
    path: content/email-composer
    description: Creates professional business emails and stakeholder communications
    tags: [email, communication, stakeholder, investor, business-writing]
    triggers: ["write email", "stakeholder update", "investor email", "difficult email"]
    works_with: [copywriter, people-leader-coach, report-automator]

  # === AUTOMATION ===
  - name: n8n-workflow-architect
    category: automation
    path: automation/n8n-workflow-architect
    description: Designs and generates n8n workflows
    tags: [n8n, automation, workflows, integration]
    triggers: ["automate this", "n8n workflow", "schedule task"]
    works_with: [all, web-scraper-ninja]
    
  - name: web-scraper-ninja
    category: automation
    path: automation/web-scraper-ninja
    description: Advanced web scraping with anti-detection
    tags: [scraping, data-extraction, JavaScript, CAPTCHA]
    triggers: ["scrape website", "extract data from", "get from URL"]
    works_with: [data-analyst, data-enrichment-agent, n8n-workflow-architect]
    
  - name: devops-setup-agent
    category: automation
    path: automation/devops-setup-agent
    description: Handles deployment and infrastructure
    tags: [devops, deployment, CI/CD, hosting]
    triggers: ["deploy this", "set up hosting", "CI/CD"]
    works_with: [code-generator, internal-tool-builder]

  # === KNOWLEDGE ===
  - name: knowledge-base-architect
    category: knowledge
    path: knowledge/knowledge-base-architect
    description: Designs knowledge bases and RAG systems
    tags: [knowledge-base, RAG, FAQ, documentation]
    triggers: ["build knowledge base", "create FAQ", "RAG system"]
    works_with: [knowledge-extractor, document-processor]
    
  - name: learning-accelerator
    category: knowledge
    path: knowledge/learning-accelerator
    description: Designs learning paths and study materials
    tags: [learning, education, study, skill-acquisition]
    triggers: ["help me learn", "study plan", "teach me"]
    works_with: [knowledge-extractor, workshop-exercise-designer]

  # === PRODUCTIVITY ===
  - name: report-automator
    category: productivity
    path: productivity/report-automator
    description: Automates recurring report generation
    tags: [reports, automation, templates]
    triggers: ["automate report", "update report", "MBR/QBR"]
    works_with: [data-analyst, presentation-maker]
    
  - name: meeting-commander
    category: productivity
    path: productivity/meeting-commander
    description: Meeting summaries and follow-ups
    tags: [meetings, summaries, action-items]
    triggers: ["meeting summary", "action items from meeting"]
    works_with: [n8n-workflow-architect]
    
  - name: team-template-generator
    category: productivity
    path: productivity/team-template-generator
    description: Creates team productivity templates
    tags: [templates, team, productivity, OKRs]
    triggers: ["team template", "OKR template", "project template"]
    works_with: [report-automator]
    
  - name: process-optimizer
    category: productivity
    path: productivity/process-optimizer
    description: Analyzes and optimizes business processes
    tags: [process, optimization, efficiency, lean, bottleneck]
    triggers: ["optimize process", "reduce waste", "bottleneck analysis", "streamline"]
    works_with: [n8n-workflow-architect, project-commander, data-analyst]
    
  - name: project-commander
    category: productivity
    path: productivity/project-commander
    description: Full project lifecycle management
    tags: [project-management, planning, tracking, risk, milestones]
    triggers: ["manage project", "project plan", "track progress", "project risks"]
    works_with: [team-template-generator, meeting-commander, report-automator]
    
  - name: productivity-system-designer
    category: productivity
    path: productivity/productivity-system-designer
    description: Designs personalized productivity systems (GTD, time-blocking)
    tags: [productivity, GTD, time-blocking, second-brain, PKM]
    triggers: ["design my system", "productivity setup", "GTD", "organize my work"]
    works_with: [energy-manager, habit-architect, meeting-commander]
    
  - name: okr-coach
    category: productivity
    path: productivity/okr-coach
    description: OKR setting, tracking, quarterly reviews, goal alignment
    tags: [OKRs, goals, strategy, alignment, quarterly-planning]
    triggers: ["set OKRs", "quarterly goals", "goal setting", "OKR review"]
    works_with: [team-template-generator, reflection-facilitator, project-commander]

  # === PEOPLE ===
  - name: people-leader-coach
    category: people
    path: people/people-leader-coach
    description: HR and leadership coaching support
    tags: [HR, leadership, coaching, feedback, culture]
    triggers: ["performance review", "give feedback", "coach team", "interview"]
    works_with: [team-template-generator, reflection-facilitator]
    
  - name: account-manager-helper
    category: people
    path: people/account-manager-helper
    description: Account planning, retention strategies, customer health scoring
    tags: [account-management, customer-success, retention, B2B, relationships]
    triggers: ["account plan", "customer retention", "account review", "renewal strategy"]
    works_with: [customer-insight-analyst, email-composer, data-analyst, presentation-maker]

  # === WELLNESS (NEW) ===
  - name: energy-manager
    category: wellness
    path: wellness/energy-manager
    description: Optimizes energy, work-life balance, sustainable performance
    tags: [energy, wellness, productivity, burnout-prevention, peak-performance]
    triggers: ["feeling burned out", "optimize energy", "work-life balance", "sustainable performance"]
    works_with: [reflection-facilitator, habit-architect, productivity-system-designer]
    
  - name: reflection-facilitator
    category: wellness
    path: wellness/reflection-facilitator
    description: Guides structured self-reflection and journaling
    tags: [reflection, journaling, self-coaching, retrospective, personal-growth]
    triggers: ["help me reflect", "weekly review", "journaling prompts", "retrospective"]
    works_with: [energy-manager, habit-architect, people-leader-coach]
    
  - name: habit-architect
    category: wellness
    path: wellness/habit-architect
    description: Designs sustainable habits using behavioral science
    tags: [habits, behavior-change, atomic-habits, routine, self-improvement]
    triggers: ["build a habit", "break bad habit", "morning routine", "behavior change"]
    works_with: [energy-manager, reflection-facilitator, productivity-system-designer]
```

---

## Categories Overview

### 🔧 Meta (7 agents)
System agents that manage other agents and ensure quality.

| Agent | Purpose |
|-------|---------|
| @orchestration-agent | Coordinates multi-agent workflows |
| @agent-architect | Creates new agents |
| @prompt-architect | Optimizes prompts |
| @quality-assurance-reviewer | Reviews output quality |
| @style-guardian | Ensures brand consistency |
| @user-manual-generator | Creates documentation |
| @workflow-showcase-builder | Creates interactive showcases |

### 📊 Analysis (8 agents)
Agents that analyze, extract, and make sense of data.

| Agent | Purpose |
|-------|---------|
| @data-analyst | Data analysis and insights |
| @data-visualization-expert | World-class visualizations |
| @customer-insight-analyst | Customer research synthesis |
| @context-builder | Context assembly |
| @knowledge-extractor | v2.0 — Extract, synthesize, transform research |
| @research-to-prompt | ⚠️ DEPRECATED — Use @knowledge-extractor |
| @data-enrichment-agent | Data cleaning/enrichment |
| @document-processor | Document processing |

### 🎨 Creation (9 agents)
Agents that create documents, presentations, and content.

| Agent | Purpose |
|-------|---------|
| @presentation-maker | Presentations |
| @visual-designer | Visual direction |
| @workshop-exercise-designer | Workshop exercises |
| @gamma-optimizer | Gamma-optimized content |
| @layout-architect | Print-ready layouts |
| @form-generator | Forms and surveys |
| @facilitation-guide-generator | Facilitation guides |
| @personalized-plan-generator | Personalized plans |
| @interactive-content-compiler | Interactive HTML |

### 🎯 Strategy (4 agents)
Agents that help with strategic thinking and planning.

| Agent | Purpose |
|-------|---------|
| @expert-panel | Expert perspectives |
| @product-architect | Product strategy |
| @idea-forge | Idea generation |
| @gtm-strategist | Go-to-market strategy |

### 💻 Product (4 agents)
Agents that help build products.

| Agent | Purpose |
|-------|---------|
| @prd-architect | PRD creation |
| @code-generator | Code implementation |
| @database-architect | Database design |
| @internal-tool-builder | Internal tools |

### ✍️ Content (4 agents)
Agents that create marketing and brand content.

| Agent | Purpose |
|-------|---------|
| @personal-brand-builder | Personal brand content |
| @copywriter | Sales/marketing copy |
| @brand-architect | Brand guidelines |
| @seo-optimizer | SEO optimization |

### ⚡ Automation (3 agents)
Agents that automate workflows and processes.

| Agent | Purpose |
|-------|---------|
| @n8n-workflow-architect | n8n workflow design |
| @web-scraper-ninja | Web scraping |
| @devops-setup-agent | Deployment setup |

### 📚 Knowledge (2 agents)
Agents that manage and accelerate learning.

| Agent | Purpose |
|-------|---------|
| @knowledge-base-architect | KB and RAG design |
| @learning-accelerator | Learning paths |

### ⏰ Productivity (3 agents)
Agents that boost personal and team productivity.

| Agent | Purpose |
|-------|---------|
| @report-automator | Automated reports |
| @meeting-commander | Meeting summaries |
| @team-template-generator | Team templates |

### 👥 People (1 agent)
Agents that help with people management.

| Agent | Purpose |
|-------|---------|
| @people-leader-coach | HR and leadership |

---

## 📋 Protocols (Cross-Cutting Standards)

These protocols apply to ALL agents that produce outputs.

### Quality & Validation (MANDATORY)

| Protocol | Purpose | Mandatory For |
|----------|---------|---------------|
| `_output-quality-score-protocol.md` | **Self-assess before delivery (≥80 to ship)** | All content agents |
| `_output-validation-protocol.md` | Content fit, print validation, semantic accuracy | All content-generating agents |
| `_print-output-standards.md` | CSS rules, page breaks, 1:1 print match | All printable outputs |

### Content & Style

| Protocol | Purpose | Mandatory For |
|----------|---------|---------------|
| `_content-density-guidelines.md` | Text limits per slide/page (ASK USER!) | Presentations, worksheets |
| `_gamma-optimization-guide.md` | Gamma "Paste text" best practices | Gamma-ready outputs |
| `_brand-auto-load-protocol.md` | Auto-inject brand context | All content agents |
| `_template-library.md` | Pre-built structures for common use cases | All creation tasks |

### Workflow & Process

| Protocol | Purpose | Mandatory For |
|----------|---------|---------------|
| `_output-preview-protocol.md` | Preview before full build | Complex outputs (5+ slides) |
| `_confidence-scoring-protocol.md` | Output confidence ratings | All agents |
| `_feedback-behavior-protocol.md` | Learning from user feedback | All agents |

### System & Learning

| Protocol | Purpose | Mandatory For |
|----------|---------|---------------|
| `_specialist-handoff-protocol.md` | When to delegate to specialists | All agents |
| `_cross-agent-memory.md` | Shared learnings across agents | System-wide |
| `_memory-protocol.md` | MEMORY.md structure template | All agents |

### Reviews & Improvements

| Protocol | Purpose | When |
|----------|---------|------|
| `_devils-advocate-review-v5.md` | Latest brutal system review | Reference |
| `_agent-consolidation-analysis.md` | Proposed 62→33 agent reduction | Planning |

### Key Print/Output Rules (Quick Reference)

```css
/* CRITICAL: Include in ALL printable HTML */
@page { margin: 0; }

/* CRITICAL: Never break these across pages */
table, .exercise-box, .answer-box, .diagram { 
    page-break-inside: avoid !important; 
}
```

**Print Instructions Banner:** All printable HTML must include visible instructions:
- Set margins to "None"
- Uncheck "Headers and footers"
- Check "Background graphics"

### Key Diagram Rules

| Concept | Visual Requirement |
|---------|-------------------|
| Mutually Exclusive (ME) | Shapes with GAPS (NOT touching) |
| Collectively Exhaustive (CE) | Shapes FILL container (NO gaps) |

---

## How to Use This Catalog

### For Users
1. **Don't memorize agents** — Just describe your task to @orchestration-agent
2. **Browse by category** if you want to explore capabilities
3. **Use "I want to..." table** for quick reference
4. **Check Protocols** for output quality standards

### For AI/Orchestrator
1. Parse the YAML block for agent selection
2. Use `triggers` to match user intent
3. Use `works_with` to plan multi-agent flows
4. Use `category` for grouping suggestions
5. **Apply Protocols** to all outputs before delivery

---

*Auto-generated from agent definitions. Run @agent-architect to update.*
*Protocols updated: 2026-01-13*
