# Brand Presets Library

> **Version:** 1.0  
> **Created:** 2026-01-13  
> **Purpose:** Pre-configured brand styles for quick setup

---

## 🎨 Available Presets

### 1. 🟢 Bolt Corporate

Based on [Bolt's brand](https://bolt.eu) — their signature green mobility aesthetic.

```css
:root {
  --primary: #34D186;      /* Bolt Green */
  --primary-dark: #2AB873; /* Darker green */
  --background: #FFFFFF;   /* Clean white */
  --text: #1A1A1A;         /* Near black */
  --text-muted: #6B7280;   /* Gray */
  --accent: #34D186;       /* Same as primary */
  --surface: #F3F4F6;      /* Light gray */
}
```

**Typography:**
- Headers: Inter, Bold, sentence case
- Body: Inter, Regular
- Style: Modern, clean, tech-forward

**Best for:** Tech products, mobility, modern apps

---

### 2. ☀️ Radiant Operator (Your Personal Brand)

From `/Context/personal_brand_guideline.md` — McKinsey precision meets player-coach energy.

```css
:root {
  --primary: #FFD700;      /* Solstice Gold - spotlight only */
  --background: #F9F9F9;   /* Cloud White */
  --text: #333333;         /* Slate Graphite */
  --text-muted: #666666;   /* Medium gray */
  --accent: #FFD700;       /* Solstice Gold */
  --surface: #E1E1E1;      /* Soft Pebble */
}
```

**Typography:**
- Headers: Inter/Montserrat, Extra Bold, ALL CAPS, tight tracking
- Body: Inter, Regular, line-height 1.6
- Code: JetBrains Mono

**Principles:**
- 80% whitespace
- Gold used ONLY for key insights (spotlight rule)
- Ultra-thin geometric icons

**Best for:** Executive presentations, consulting, thought leadership

---

### 3. 🔵 McKinsey Classic

Traditional consulting aesthetic — authority and trust.

```css
:root {
  --primary: #0066CC;      /* McKinsey Blue */
  --primary-dark: #004C99; /* Darker blue */
  --background: #FFFFFF;   /* White */
  --text: #1A1A1A;         /* Near black */
  --text-muted: #5A6672;   /* Slate */
  --accent: #0066CC;       /* Blue */
  --surface: #F5F7FA;      /* Light blue-gray */
}
```

**Typography:**
- Headers: Georgia or Times, Bold
- Body: Arial or Helvetica, Regular
- Style: Traditional, authoritative

**Principles:**
- Pyramid structure (BLUF)
- Minimal text, maximum impact
- Data-driven visuals

**Best for:** Board presentations, strategy decks, formal reports

---

### 4. ⬛ Minimal Modern

Clean, distraction-free, developer-friendly.

```css
:root {
  --primary: #000000;      /* Pure black */
  --background: #FFFFFF;   /* Pure white */
  --text: #1A1A1A;         /* Near black */
  --text-muted: #9CA3AF;   /* Gray */
  --accent: #000000;       /* Black */
  --surface: #F9FAFB;      /* Off-white */
}
```

**Typography:**
- Headers: SF Pro Display or Inter, Semibold
- Body: SF Pro Text or Inter, Regular
- Code: SF Mono or JetBrains Mono

**Best for:** Documentation, technical content, minimalist presentations

---

### 5. 🟣 Creative Studio

Bold, expressive, attention-grabbing.

```css
:root {
  --primary: #7C3AED;      /* Vibrant purple */
  --primary-light: #A78BFA; /* Light purple */
  --background: #FFFFFF;   /* White */
  --text: #1F2937;         /* Dark gray */
  --text-muted: #6B7280;   /* Gray */
  --accent: #EC4899;       /* Pink accent */
  --surface: #F3E8FF;      /* Light purple */
}
```

**Typography:**
- Headers: Poppins or Outfit, Bold
- Body: Inter, Regular
- Style: Playful, modern, energetic

**Best for:** Marketing, creative pitches, social media content

---

### 6. 🌊 Ocean Professional

Calm, trustworthy, enterprise-ready.

```css
:root {
  --primary: #0891B2;      /* Teal */
  --primary-dark: #0E7490; /* Darker teal */
  --background: #FFFFFF;   /* White */
  --text: #1E293B;         /* Slate */
  --text-muted: #64748B;   /* Muted slate */
  --accent: #06B6D4;       /* Cyan */
  --surface: #F0FDFA;      /* Light teal */
}
```

**Typography:**
- Headers: Plus Jakarta Sans, Semibold
- Body: Inter, Regular

**Best for:** Healthcare, finance, enterprise software

---

### 7. 🚀 Startup/VC

Bold, energetic, investor-ready.

```css
:root {
  --primary: #FF6B6B;      /* Coral Red */
  --primary-dark: #EE5A5A; /* Darker coral */
  --background: #1A1A2E;   /* Dark navy */
  --text: #FFFFFF;         /* White */
  --text-muted: #A0A0B0;   /* Muted gray */
  --accent: #4ECDC4;       /* Teal accent */
  --surface: #16213E;      /* Dark surface */
}
```

**Typography:**
- Headers: Outfit or Space Grotesk, Bold
- Body: Inter, Regular
- Style: Bold, high-contrast, attention-grabbing

**Best for:** Investor pitches, product launches, startup culture decks

---

### 8. 📊 Data Dark

Technical, analytical, developer-friendly dark mode.

```css
:root {
  --primary: #00D9FF;      /* Cyan */
  --primary-dark: #00B8D9; /* Darker cyan */
  --background: #0D1117;   /* GitHub dark */
  --text: #E6EDF3;         /* Light gray */
  --text-muted: #8B949E;   /* Muted */
  --accent: #58A6FF;       /* Blue accent */
  --surface: #161B22;      /* Elevated surface */
  --success: #3FB950;      /* Green */
  --warning: #D29922;      /* Yellow */
  --error: #F85149;        /* Red */
}
```

**Typography:**
- Headers: JetBrains Mono or SF Mono, Medium
- Body: Inter, Regular
- Code: JetBrains Mono

**Best for:** Technical dashboards, analytics reports, developer documentation, data-heavy presentations

---

### 9. 🌿 Warm Earth

Human, approachable, culture-focused.

```css
:root {
  --primary: #E07A5F;      /* Terracotta */
  --primary-dark: #C96A50; /* Darker terracotta */
  --background: #FDF8F3;   /* Warm cream */
  --text: #3D405B;         /* Muted navy */
  --text-muted: #81858F;   /* Soft gray */
  --accent: #81B29A;       /* Sage green */
  --surface: #F4EDDE;      /* Warm surface */
}
```

**Typography:**
- Headers: Libre Baskerville or Playfair Display, Regular
- Body: Source Sans Pro, Regular
- Style: Warm, inviting, human

**Best for:** HR communications, culture decks, team updates, internal newsletters, onboarding materials

---

### 10. 🎯 Custom

User-defined colors and fonts.

**Quick Setup Questions:**
1. What's your primary/accent color? (hex or description)
2. Light or dark background preference?
3. Font style: Modern (Inter) / Traditional (Georgia) / Technical (Mono)?
4. Formal or casual tone?

---

## 📊 Visual Preset Comparison

| Preset | Background | Primary | Accent | Vibe |
|--------|------------|---------|--------|------|
| 🟢 Bolt Corporate | White | Green #34D186 | Green | Modern tech |
| ☀️ Radiant Operator | Off-white #F9F9F9 | Gold #FFD700 | Gold | Executive consulting |
| 🔵 McKinsey Classic | White | Blue #0066CC | Blue | Traditional authority |
| ⬛ Minimal Modern | White | Black #000000 | Black | Clean simplicity |
| 🟣 Creative Studio | White | Purple #7C3AED | Pink #EC4899 | Bold creative |
| 🌊 Ocean Professional | White | Teal #0891B2 | Cyan #06B6D4 | Calm enterprise |
| 🚀 Startup/VC | Dark #1A1A2E | Coral #FF6B6B | Teal #4ECDC4 | Bold pitch |
| 📊 Data Dark | Dark #0D1117 | Cyan #00D9FF | Blue #58A6FF | Technical analytics |
| 🌿 Warm Earth | Cream #FDF8F3 | Terracotta #E07A5F | Sage #81B29A | Human warmth |

---

## 🔄 Selection Flow

```markdown
"**Choose your visual style:**

🟢 **A) Bolt Corporate** — Modern tech, green accent
   *Best for: Product demos, tech content*

☀️ **B) Radiant Operator** — Gold spotlight, McKinsey precision ← YOUR SAVED STYLE
   *Best for: Executive presentations, thought leadership*

🔵 **C) McKinsey Classic** — Traditional blue, authoritative
   *Best for: Board meetings, strategy decks*

⬛ **D) Minimal Modern** — Black/white, clean
   *Best for: Documentation, technical content*

🟣 **E) Creative Studio** — Purple/pink, bold
   *Best for: Marketing, creative pitches*

🌊 **F) Ocean Professional** — Teal, enterprise
   *Best for: Healthcare, finance, enterprise*

🎯 **G) Custom** — Define your own colors

**[Recommended: B - Radiant Operator]** (matches your saved brand)"
```

---

## 💾 Saving User Preference

After selection, save to user profile:

```yaml
# In MEMORY.md or user preferences
brand_preference:
  preset: "radiant-operator"
  custom_overrides: null
  saved_date: "2026-01-13"
  
# Or for custom:
brand_preference:
  preset: "custom"
  custom_overrides:
    primary: "#FF5733"
    background: "#FFFFFF"
    font_headers: "Poppins"
    font_body: "Inter"
```

---

## 🔗 Related Protocols

- `_brand-auto-load-protocol.md` — How to load brand context
- `_output-validation-protocol.md` — Brand consistency checking

