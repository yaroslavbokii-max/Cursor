# General Agent Orchestration Prompt Template

**Purpose:** Reusable template for creating agent orchestration prompts with best practices  
**Version:** 2.1  
**Date:** December 2025  
**Used by:** @orchestration-agent

---

## 🎯 How This Template Works

This template is used by `@orchestration-agent` to automatically generate comprehensive orchestration prompts from user's initial requests.

**Workflow:**
1. User provides initial prompt (e.g., "I want 10-slide presentation about MECE for 60 min")
2. @orchestration-agent uses this template to generate comprehensive prompt
3. Generated prompt includes all phases, checkpoints, and gap analysis
4. Orchestration agent executes the generated prompt automatically

---

## 📋 Template Structure

### Section 1: Task Overview
- Clear description of what needs to be accomplished
- Key requirements and constraints
- Output specifications

### Section 2: Pre-Workflow Clarifying Questions
- **CRITICAL:** Ask these BEFORE any agent starts working
- Gather all necessary context
- Identify constraints and preferences

### Section 3: Agent Orchestration Workflow
- Sequential phases with specific agents
- Clear prompts for each agent
- Checkpoints between phases

### Section 4: Quality Checkpoints
- Validation points throughout the workflow
- Quality criteria for each phase

### Section 5: Critical Decision Points & Checkpoint Questions
- When agents should pause and ask user
- What decisions need user input
- Checkpoint questioning framework (standard + dynamic)

---

## 📝 Template Content

```markdown
# Agent Orchestration Prompt: [TASK NAME]

**Task:** [Clear description of what needs to be accomplished]

**Date:** [Date]  
**Output Folder:** `[path/to/output/folder]`

---

## 🎯 Pre-Workflow Clarifying Questions

**BEFORE starting any agent workflow, ask these questions:**

### 1. Objective & Scope
- **Primary goal:** [ASK] What is the main objective?
- **Success criteria:** [ASK] How will you know it's successful?
- **Scope boundaries:** [ASK] What's in scope? What's out of scope?
- **Constraints:** [ASK] Any time, budget, or resource constraints?

### 2. Audience & Context
- **Target audience:** [ASK] Who is this for?
- **Audience knowledge level:** [ASK] What do they already know?
- **Delivery context:** [ASK] How will this be used/delivered?
- **Business context:** [ASK] Any specific industry or company context?

### 3. Content Requirements
- **Topic/framework:** [Specify or ASK]
- **Depth level:** [ASK] Introductory, intermediate, or advanced?
- **Examples needed:** [ASK] Any specific examples or scenarios?
- **Research materials:** [ASK] Do you have research materials to provide?

### 4. Context Files & Knowledge Base ⚠️ **SIGNIFICANTLY HELPS OUTPUT QUALITY**
- **Do you have existing knowledge base or content files?** [ASK] (e.g., previous extracts, research documents, internal materials)
- **Do you have specific content you want to use?** [ASK] (e.g., company documents, case studies, examples)
- **Do you have any reference materials?** [ASK] (e.g., articles, books, frameworks)
- **Note:** Providing context files significantly improves output quality and relevance. If you have any relevant materials, please share them now.

### 5. Output Requirements
- **Primary output:** [Specify format and purpose]
- **Secondary outputs:** [ASK] What else is needed?
- **Format preferences:** [ASK] Any specific format requirements?
- **Branding:** [ASK] Any brand guidelines or style preferences?

### 6. Quality & Validation
- **Quality standards:** [ASK] Any specific quality requirements?
- **Review process:** [ASK] Who will review? When?
- **Iteration expected:** [ASK] How many rounds of feedback?

---

## 🔄 Agent Orchestration Workflow

### Phase 0: Pre-Workflow Validation
**Action:** Ask all clarifying questions above. **DO NOT PROCEED** until user confirms or provides answers.

**Checkpoint:** User confirms understanding and answers clarifying questions.

---

### Phase 1: [Phase Name]

**Agent:** `@[agent-name]`

**Prompt:**
```
[Specific instructions for this agent]

**CRITICAL Checkpoint Questions:**
- If you encounter ambiguity or multiple valid paths → Ask user using checkpoint questioning framework
- If you need to make trade-offs (quality/speed/scope) → Present options with recommendation
- If you discover something unexpected → Explain finding and ask how to proceed
- Use structured format for standard decisions, conversational for context-specific

**CRITICAL:** If you encounter [specific situation], ASK the user before proceeding.

**Output:** [Specify output file and location]
```

**Checkpoint:** [What to validate before proceeding]

---

### Phase 2: [Phase Name]

**Agent:** `@[agent-name]`

**Prompt:**
```
[Specific instructions for this agent]

**Inputs from previous phase:**
- [File/location from Phase 1]

**CRITICAL:** If you need to make decisions about [decision type], ASK the user.

**Output:** [Specify output file and location]
```

**Checkpoint:** [What to validate before proceeding]

---

### Phase 3: [Phase Name]

[Continue pattern...]

---

### Phase N: Final Integration

**Action:** Compile all outputs into final package

**Create:** `[output-folder]/README.md` with:
- Overview of all materials
- Quick start guide
- File descriptions
- Delivery checklist

**Verify:**
- [ ] All required outputs exist
- [ ] Quality standards met
- [ ] All materials in correct location

---

## 📋 Quality Checkpoints

### Before Starting Workflow
- [ ] All clarifying questions answered
- [ ] User confirmed understanding of requirements
- [ ] Output folder created

### After Phase 1: [Phase Name]
- [ ] [Quality criterion 1]
- [ ] [Quality criterion 2]

### After Phase 2: [Phase Name]
- [ ] [Quality criterion 1]
- [ ] [Quality criterion 2]

[Continue for each phase...]

### Final Package
- [ ] All files are in correct location
- [ ] README is complete
- [ ] All outputs meet requirements

---

## 🚨 Critical Decision Points & Checkpoint Questions

**Agents MUST ask user for input at these points:**

1. **Before workflow starts:** All clarifying questions
2. **At checkpoints:** When agents encounter ambiguity or multiple valid paths
3. **[Decision point 1]:** [When this decision is needed]
4. **[Decision point 2]:** [When this decision is needed]
5. **[Decision point 3]:** [When this decision is needed]

### Checkpoint Questioning Framework

**When to Ask:**
- Agent encounters ambiguity or multiple valid paths
- Trade-offs needed (quality vs. speed, depth vs. breadth)
- Content direction decisions required
- Format/style choices affect outcome
- Scope adjustments needed based on findings

**Question Format:**
- **Structured** (tables, checkboxes) for: Multiple clear options, standard decisions
- **Conversational** for: Context-specific findings, nuanced trade-offs

**Standard Checkpoint Question Templates:**

#### Content Direction
```markdown
## 🔍 Checkpoint: Content Direction

Based on my analysis, I found [finding]. I can proceed in [X] ways:

**Option A:** [Approach] — [pros/cons]
**Option B:** [Approach] — [pros/cons]

**My recommendation:** [Option] because [reason]

**Which approach should I use?**
```

#### Quality Trade-off
```markdown
## ⚖️ Checkpoint: Quality Trade-off

I can deliver this in two ways:
- **Comprehensive:** [time, depth, quality]
- **Quick:** [time, depth, quality]

**Which do you prefer?**
```

#### Scope Adjustment
```markdown
## 📏 Checkpoint: Scope Adjustment

I discovered [finding] which means [implication].

**Options:**
- Reduce scope to fit timeline
- Extend timeline to complete full scope
- Prioritize specific items

**Which approach?**
```

**Agent-Specific Checkpoint Patterns:**

- **@data-analyst:** Visualization preferences, deep dive selection, analysis approach when ambiguity detected
- **@presentation-maker:** Slide structure confirmation, visual style, content depth
- **@workshop-exercise-designer:** Exercise type confirmation, timing adjustments
- **@knowledge-extractor:** Depth confirmation, framework interpretation
- **@expert-panel:** Recommendation confirmation, additional perspectives

**Decision Framework:**
- If [condition A] → Ask user about [decision] using [format]
- If [condition B] → Ask user about [decision] using [format]
- If [conflict/ambiguity] → Ask user to resolve with context
- If [multiple valid paths] → Present options with recommendation

---

## 📁 Expected Output Files

```
[output-folder]/
├── README.md                    # Overview and quick start
├── [file-1].md                  # [Description]
├── [file-2].md                  # [Description]
└── [file-n].md                  # [Description]
```

---

## 🎯 Success Criteria

✅ **[Output 1]:**
- [Criterion 1]
- [Criterion 2]

✅ **[Output 2]:**
- [Criterion 1]
- [Criterion 2]

✅ **Quality:**
- [Quality standard 1]
- [Quality standard 2]

---

## 🔧 Best Practices Embedded

### 1. Clarifying Questions Before Workflow
- **Why:** Prevents rework and ensures alignment
- **When:** Before ANY agent starts working
- **How:** Structured questions covering all critical dimensions

### 2. Checkpoints Between Phases
- **Why:** Catch issues early, validate direction
- **When:** After each major phase
- **How:** Explicit validation criteria and user approval points

### 3. Critical Decision Points & Checkpoint Questions
- **Why:** Agents shouldn't make assumptions on critical choices, especially when ambiguity exists
- **When:** When decisions impact quality or direction, or when agents encounter multiple valid paths
- **How:** Explicit "ASK user" instructions + checkpoint questioning framework (standard + dynamic, structured + conversational)

### 4. Quality Gates
- **Why:** Ensure outputs meet standards
- **When:** At each phase completion
- **How:** Checklist of quality criteria

### 5. Context Handoff
- **Why:** Each agent needs full context
- **When:** Between agent phases
- **How:** Explicit file references and context summaries

### 6. Output Organization
- **Why:** Easy to find and use outputs
- **When:** Final phase
- **How:** Structured folder with README

---

## 📚 Common Agent Patterns

### Pattern 1: Research → Analysis → Creation
```
@research-to-prompt → @data-analyst → @presentation-maker
```
**Use when:** Need to research, analyze, then create output

### Pattern 2: Knowledge → Expert → Design
```
@knowledge-extractor → @expert-panel → @workshop-exercise-designer
```
**Use when:** Need expert validation of approach

### Pattern 3: Extract → Design → Present
```
@knowledge-extractor → @workshop-exercise-designer → @presentation-maker
```
**Use when:** Creating workshop or training materials

### Pattern 4: Context → Analysis → Recommendation
```
@context-builder → @data-analyst → @expert-panel
```
**Use when:** Need strategic recommendations

---

## ⚠️ Common Mistakes to Avoid

### ❌ Don't: Start agents without clarifying questions
**Why:** Leads to misaligned outputs and rework  
**Fix:** Always ask clarifying questions first

### ❌ Don't: Skip checkpoints
**Why:** Issues compound and become harder to fix  
**Fix:** Validate at each phase

### ❌ Don't: Let agents make critical decisions
**Why:** User preferences and context matter  
**Fix:** Explicit "ASK user" instructions

### ❌ Don't: Forget context handoff
**Why:** Agents need full context to work effectively  
**Fix:** Explicit file references and summaries

### ❌ Don't: Create outputs without organization
**Why:** Hard to find and use later  
**Fix:** Structured folders with README

---

## 🎓 Customization Guide

### For Simple Tasks (1-2 agents)
- Reduce phases
- Simplify checkpoints
- Focus on core outputs

### For Complex Tasks (4+ agents)
- Add more checkpoints
- Break into sub-phases
- Add integration phases

### For Iterative Tasks
- Add feedback loops
- Include revision phases
- Define iteration criteria

### For Time-Sensitive Tasks
- Prioritize critical checkpoints
- Parallelize where possible
- Define "good enough" criteria

---

*General Orchestration Prompt Template v2.1 — December 2025*

