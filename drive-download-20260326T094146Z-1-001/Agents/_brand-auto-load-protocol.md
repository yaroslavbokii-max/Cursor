# Brand Auto-Load Protocol

> **Version:** 2.0  
> **Created:** 2026-01-13  
> **Purpose:** Flexible brand handling — works for users with guidelines AND without

---

## 🎯 Core Principle

**Be helpful to everyone.** Some users have brand guidelines, some don't. Handle both gracefully.

---

## 🔄 Brand Detection Flow

```
Content Generation Request
    │
    ▼
┌─────────────────────────────────────────────┐
│ STEP 1: Check for existing brand files      │
│                                             │
│ Look for:                                   │
│ - /Context/personal_brand_guideline.md      │
│ - /Context/brand_guidelines.md              │
│ - /Context/style_guide.md                   │
└─────────────────────────────────────────────┘
    │
    ├─── FOUND ──────────────────────────────────┐
    │                                            │
    │    "📎 Found your brand guidelines.        │
    │     Using Radiant Operator style.          │
    │                                            │
    │     [✓ Use this] [↻ Choose different]"     │
    │                                            │
    └────────────────────────────────────────────┘
    │
    └─── NOT FOUND ──────────────────────────────┐
                                                 │
         ┌───────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│ STEP 2: Check user's saved preference       │
│                                             │
│ Look in MEMORY.md for:                      │
│ - brand_preference.preset                   │
│ - brand_preference.custom_overrides         │
└─────────────────────────────────────────────┘
    │
    ├─── FOUND ──────────────────────────────────┐
    │                                            │
    │    "Using your saved style: [preset name]  │
    │     [✓ Continue] [↻ Change]"               │
    │                                            │
    └────────────────────────────────────────────┘
    │
    └─── NOT FOUND ──────────────────────────────┐
                                                 │
         ┌───────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│ STEP 3: Offer brand selection               │
│                                             │
│ Show preset options (see below)             │
└─────────────────────────────────────────────┘
```

---

## 🎨 Brand Selection Message

```markdown
"**Choose your visual style:**

🟢 **A) Bolt Corporate** — Modern tech aesthetic, signature green
   *Best for: Product demos, tech content, modern apps*

☀️ **B) Radiant Operator** — Gold spotlight, McKinsey precision
   *Best for: Executive presentations, consulting, thought leadership*
   **← RECOMMENDED as default**

🔵 **C) McKinsey Classic** — Traditional blue, authoritative
   *Best for: Board meetings, strategy decks, formal reports*

⬛ **D) Minimal Modern** — Black & white, distraction-free
   *Best for: Documentation, technical content, developer audiences*

🟣 **E) Creative Studio** — Bold purple/pink, attention-grabbing
   *Best for: Marketing, creative pitches, social media*

🌊 **F) Ocean Professional** — Calm teal, enterprise-ready
   *Best for: Healthcare, finance, enterprise software*

🎯 **G) Custom** — I'll define my own colors and fonts

💾 **Your choice will be saved for future sessions.**"
```

---

## 🎯 Quick Custom Setup (Option G)

If user chooses Custom, ask 4 simple questions:

```markdown
"**Quick brand setup (4 questions):**

1️⃣ **Primary/accent color?**
   - Provide hex code (e.g., #FF5733)
   - Or describe: "bright orange", "dark blue"
   - Or: "surprise me"

2️⃣ **Background preference?**
   A) Light (white/off-white) ← most common
   B) Dark (dark gray/black)
   C) Colored (subtle tint)

3️⃣ **Typography vibe?**
   A) Modern & clean (Inter, SF Pro)
   B) Traditional & authoritative (Georgia, Times)
   C) Technical & precise (Monospace)
   D) Friendly & approachable (Poppins, Outfit)

4️⃣ **Overall tone?**
   A) Formal/corporate
   B) Professional but approachable ← recommended
   C) Casual/friendly
   D) Bold/creative"
```

---

## 💾 Saving Preferences

### After Selection, Update User's MEMORY

```yaml
# Append to orchestration-agent MEMORY.md

user_brand_preference:
  preset: "radiant-operator"  # or "custom"
  saved_date: "2026-01-13"
  
  # If custom:
  custom_colors:
    primary: "#FF5733"
    background: "#FFFFFF"
    text: "#1A1A1A"
    accent: "#FF5733"
  
  custom_typography:
    headers: "Poppins"
    body: "Inter"
    code: "JetBrains Mono"
  
  custom_tone: "professional-approachable"
```

---

## 🔌 Integration with Agents

### For Content-Generating Agents

Add this to agent prompts when brand is loaded:

```markdown
## Brand Context (Auto-Loaded)

**Preset:** [Preset Name]

**Colors:**
- Primary/Accent: [hex]
- Background: [hex]
- Text: [hex]
- Secondary: [hex]

**Typography:**
- Headers: [font], [weight], [style]
- Body: [font], [weight]

**Principles:**
- [Key principle 1]
- [Key principle 2]

**Apply these consistently to all visual outputs.**
```

---

## 🏢 Default for Unknown Users (No Preference)

If user doesn't select and just wants to proceed:

```markdown
"No preference selected. Using **Radiant Operator** defaults:
- Clean white background (#F9F9F9)
- Gold accents for highlights (#FFD700)
- Professional typography (Inter)

This works well for most business content. You can change anytime."
```

---

## ⚡ Silent Mode (For Returning Users)

When brand is already known, don't ask — just acknowledge:

```markdown
"📎 Using your Radiant Operator brand style."
```

Only show this briefly, don't interrupt the workflow.

---

## 📁 Preset Definitions

See `_brand-presets.md` for full color codes and typography specs for each preset:
- Bolt Corporate
- Radiant Operator
- McKinsey Classic
- Minimal Modern
- Creative Studio
- Ocean Professional

---

## 🔗 Related Protocols

- `_brand-presets.md` — Full preset definitions
- `_output-validation-protocol.md` — Brand consistency checking
- `_first-time-setup.md` — New user onboarding
