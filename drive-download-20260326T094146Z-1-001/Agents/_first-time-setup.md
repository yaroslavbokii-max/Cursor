# First-Time User Setup Protocol

> **Version:** 1.0  
> **Created:** 2026-01-13  
> **Purpose:** Onboard new users gracefully and learn their preferences

---

## 🎯 Core Principle

**Learn once, apply forever.** Capture preferences early so users never repeat themselves.

---

## 🔍 Detection: Is This a New User?

Check for these indicators:

```yaml
new_user_indicators:
  - No MEMORY.md entries for this user
  - No saved brand preference
  - No saved output format preference
  - No saved involvement level preference
  - First interaction with orchestrator
```

---

## 👋 Welcome Flow

### Initial Greeting

```markdown
"👋 **Welcome to the Agent Stack!**

I'm your AI productivity system with 62 specialized agents that work together. 
You don't need to know them all — just tell me what you need.

**Quick setup (2 minutes) will make everything work better for you.**

Ready? Let's go! [▶️ Start Setup] [⏭️ Skip, use defaults]"
```

---

## 📋 Setup Questions (5 total)

### Question 1: Visual Style

```markdown
"**1/5 — What's your visual style?**

🟢 **A) Bolt Corporate** — Modern tech, green accent
🌟 **B) Radiant Operator** — Gold spotlight, consulting precision ← RECOMMENDED
🔵 **C) McKinsey Classic** — Traditional blue, authoritative
⬛ **D) Minimal Modern** — Black/white, clean
🟣 **E) Creative Studio** — Bold colors, creative
🌊 **F) Ocean Professional** — Teal, enterprise
🎯 **G) Custom** — I'll specify

[Most users pick B — works great for business content]"
```

### Question 2: Output Formats

```markdown
"**2/5 — How do you typically use outputs?**

📺 **A) Screen only** — View on computer, share digitally
🖨️ **B) Print** — I print documents and handouts
🎨 **C) Gamma/Slides** — I use Gamma.app for presentations
📦 **D) All of the above** ← RECOMMENDED

[Choosing D ensures you get all formats automatically]"
```

### Question 3: Content Density

```markdown
"**3/5 — How much content per slide/page?**

📊 **A) Executive** — Minimal text, big impact (40-60 words/slide)
   *Best for senior audiences, keynotes*

📋 **B) Balanced** — Key info with context (80-100 words/slide) ← RECOMMENDED
   *Best for most business situations*

📝 **C) Detailed** — Comprehensive, standalone (120-150 words/slide)
   *Best for handouts, self-study materials*

🎯 **D) Ask me each time** — I'll decide per project"
```

### Question 4: Involvement Level

```markdown
"**4/5 — How involved do you want to be?**

🚀 **A) Fast** — Make smart assumptions, show me results
   *~5-10 min, minimal questions*

🤝 **B) Balanced** — Check with me on key decisions ← RECOMMENDED
   *~15-25 min, 3-5 questions*

🎓 **C) Detailed** — Walk me through everything
   *~30-45 min, comprehensive discovery*

🎯 **D) Adaptive** — Decide based on task complexity"
```

### Question 5: Industry/Context

```markdown
"**5/5 — What's your primary work context?**

🍔 **A) Food Delivery / Logistics** — I'll load Bolt Food metrics
🏢 **B) Consulting / Strategy** — McKinsey-style frameworks
💻 **C) Tech / Product** — Product management focus
📊 **D) Finance / Analytics** — Data-heavy outputs
🎨 **E) Marketing / Creative** — Brand and content focus
📚 **F) General Business** — Bit of everything

[This helps me load the right context files automatically]"
```

---

## 💾 Save Preferences

After setup, save to orchestrator MEMORY:

```yaml
# Append to orchestration-agent/MEMORY.md

user_profile:
  setup_completed: true
  setup_date: "2026-01-13"
  
  preferences:
    brand_preset: "radiant-operator"
    output_formats: "all"
    content_density: "balanced"
    involvement_level: "balanced"
    industry_context: "food-delivery"
  
  context_files_to_load:
    - /Context/personal_brand_guideline.md
    - /Context/personal_tone_of_voice.md
    - /Context/Bolt_Food_Metrics_Glossary.md
    - /Context/Looker_Explores_Datasources_Guide.md
```

---

## ✅ Setup Confirmation

```markdown
"🎉 **All set!**

**Your preferences:**
- Style: Radiant Operator (gold/white)
- Outputs: All formats (screen + print + Gamma)
- Density: Balanced (80-100 words/slide)
- Involvement: Balanced (check on key decisions)
- Context: Food Delivery (Bolt metrics loaded)

**These are saved and will apply to all future sessions.**

You can change anytime by saying "update my preferences."

**Now, what can I help you with?** 🚀"
```

---

## ⏭️ Skip Setup (Use Defaults)

If user skips:

```yaml
default_preferences:
  brand_preset: "radiant-operator"
  output_formats: "all"
  content_density: "balanced"
  involvement_level: "balanced"
  industry_context: "general-business"
```

```markdown
"No problem! Using smart defaults:
- Professional gold/white style
- All output formats
- Balanced content density
- I'll check with you on key decisions

You can customize anytime. What can I help you with?"
```

---

## 🔄 Preference Update Flow

When user says "update my preferences" or "change settings":

```markdown
"**Current preferences:**

| Setting | Current | Change? |
|---------|---------|---------|
| Visual style | Radiant Operator | [Change] |
| Output formats | All | [Change] |
| Content density | Balanced | [Change] |
| Involvement | Balanced | [Change] |
| Industry | Food Delivery | [Change] |

**What would you like to update?**
Or say 'reset all' to start fresh."
```

---

## 📊 Learning From Usage

After each workflow, silently track:

```yaml
usage_patterns:
  most_used_agents:
    - presentation-maker: 5
    - data-analyst: 3
    - workshop-exercise-designer: 2
  
  common_outputs:
    - presentations: 8
    - workshops: 2
    - reports: 1
  
  feedback_sentiment:
    positive: 7
    neutral: 3
    negative: 1
  
  average_iterations_needed: 1.5
```

Use this to:
- Proactively suggest workflows
- Identify common pain points
- Improve default recommendations

---

## 🔗 Related Protocols

- `_brand-auto-load-protocol.md` — Brand handling
- `_brand-presets.md` — Available style presets
- `_output-preview-protocol.md` — Preview before building




