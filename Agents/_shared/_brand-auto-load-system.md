# 🎨 Brand Auto-Load System v1.0

## Purpose
Automatically detect and apply user's brand preferences without asking every time.

---

## 🔄 How It Works

### 1. Detection Priority
When starting a task, check for brand context in this order:

```
1. User explicitly specifies → Use that
2. User brand files exist → Load from files
3. Recent task used a brand → Suggest that brand
4. Unknown user → Ask (then save preference)
```

### 2. User Brand File Locations
Check these paths for user brand configuration:

```
/Users/[username]/Desktop/PACT/Context/
├── personal_brand_guideline.md    # Brand colors, style
├── personal_tone_of_voice.md      # Writing style
└── brand_config.yaml              # Quick settings (if exists)
```

### 3. Saved Preferences Location
Store learned preferences:

```
/Users/[username]/Desktop/PACT/Agents/NEW/_user-preferences/
├── brand.yaml                     # Brand settings
├── defaults.yaml                  # Default choices
└── history.yaml                   # Past selections
```

---

## 📦 Brand Presets

### Preset Definitions

```yaml
# Built-in brand presets
presets:
  bolt:
    name: "Bolt"
    colors:
      primary: "#34D399"
      secondary: "#059669"
      background: "#FFFFFF"
      text: "#1F2937"
      accent: "#F59E0B"
    typography:
      headers: "Inter, Bold"
      body: "Inter, Regular"
      code: "JetBrains Mono"
    style:
      corners: "rounded-lg (8px)"
      shadows: "subtle"
      spacing: "generous"
    
  mckinsey:
    name: "McKinsey"
    colors:
      primary: "#1E3A8A"
      secondary: "#3B82F6"
      background: "#FFFFFF"
      text: "#1F2937"
      accent: "#DC2626"
    typography:
      headers: "Georgia, Bold"
      body: "Arial, Regular"
    style:
      corners: "sharp"
      shadows: "minimal"
      spacing: "tight"
      
  minimal:
    name: "Minimal"
    colors:
      primary: "#000000"
      secondary: "#666666"
      background: "#FFFFFF"
      text: "#333333"
      accent: "#000000"
    typography:
      headers: "Helvetica, Bold"
      body: "Helvetica, Regular"
    style:
      corners: "sharp"
      shadows: "none"
      spacing: "balanced"
      
  radiant:
    name: "Radiant Operator"
    colors:
      primary: "#FFD700"
      secondary: "#E1E1E1"
      background: "#F9F9F9"
      text: "#333333"
      accent: "#FFD700"
    typography:
      headers: "Inter, Extra Bold, ALL CAPS"
      body: "Inter, Regular"
    style:
      corners: "sharp"
      shadows: "subtle"
      whitespace: "80%"
      
  data_dark:
    name: "Data Dark"
    colors:
      primary: "#60A5FA"
      secondary: "#34D399"
      background: "#111827"
      text: "#F9FAFB"
      accent: "#F59E0B"
    typography:
      headers: "Inter, Bold"
      body: "Inter, Regular"
      code: "Fira Code"
    style:
      corners: "rounded"
      shadows: "glow"
      
  warm_earth:
    name: "Warm Earth"
    colors:
      primary: "#92400E"
      secondary: "#059669"
      background: "#FFFBEB"
      text: "#451A03"
      accent: "#D97706"
    typography:
      headers: "Merriweather, Bold"
      body: "Source Sans Pro, Regular"
    style:
      corners: "soft"
      shadows: "warm"
      
  startup_vc:
    name: "Startup/VC"
    colors:
      primary: "#7C3AED"
      secondary: "#EC4899"
      background: "#FFFFFF"
      text: "#1F2937"
      accent: "#F59E0B"
    typography:
      headers: "Poppins, Bold"
      body: "Inter, Regular"
    style:
      corners: "rounded-xl"
      shadows: "modern"
```

---

## 🔧 Implementation

### Auto-Load Function

```javascript
async function autoLoadBrand(userId) {
    // 1. Check user brand files
    const brandGuideline = await readFile(`/Context/personal_brand_guideline.md`);
    const toneOfVoice = await readFile(`/Context/personal_tone_of_voice.md`);
    
    if (brandGuideline) {
        return {
            source: 'user_file',
            brand: parseBrandFromMarkdown(brandGuideline),
            tone: toneOfVoice ? parseToneFromMarkdown(toneOfVoice) : null
        };
    }
    
    // 2. Check saved preferences
    const savedPrefs = await readFile(`/_user-preferences/brand.yaml`);
    if (savedPrefs) {
        return {
            source: 'saved_preference',
            brand: parseYaml(savedPrefs)
        };
    }
    
    // 3. Check recent history
    const history = await readFile(`/_user-preferences/history.yaml`);
    if (history) {
        const recent = parseYaml(history).slice(-3);
        const mostUsed = findMostCommon(recent.map(h => h.brand));
        if (mostUsed) {
            return {
                source: 'history_suggestion',
                brand: presets[mostUsed],
                confidence: 'medium'
            };
        }
    }
    
    // 4. No preference found - ask user
    return {
        source: 'ask_user',
        brand: null,
        prompt: generateBrandQuestion()
    };
}
```

### Brand Question (If Needed)

```markdown
### 🎨 Brand & Style
Which visual style should I use?

| Option | Preview | Best For |
|--------|---------|----------|
| **A) Bolt** | Green, modern | Tech, startups |
| **B) McKinsey** | Blue, classic | Consulting, exec |
| **C) Minimal** | B&W, clean | Professional |
| **D) Radiant** | Gold, premium | Standout |
| **E) Data Dark** | Dark mode | Dashboards |
| **F) Custom** | Your colors | Brand-specific |

Your choice: ___

💡 _I can save this preference so I won't ask again._
```

### Save Preference

```yaml
# _user-preferences/brand.yaml
default_brand: "bolt"
saved_at: "2026-01-14T12:00:00Z"
user_confirmed: true

# Optional overrides
overrides:
  presentations: "mckinsey"
  dashboards: "data_dark"
  workshops: "bolt"
```

---

## 🔄 Integration with Orchestrator

### At Task Start

```python
# Pseudo-code for orchestrator
def start_task(user_request):
    # Auto-load brand
    brand_result = auto_load_brand(user_id)
    
    if brand_result.source == 'user_file':
        # Use directly, mention source
        print(f"Using your brand from personal_brand_guideline.md")
        
    elif brand_result.source == 'saved_preference':
        # Use saved, offer override
        print(f"Using your saved brand: {brand_result.brand.name}")
        print("(Say 'different style' to change)")
        
    elif brand_result.source == 'history_suggestion':
        # Suggest but confirm
        print(f"Based on recent tasks, using {brand_result.brand.name}")
        print("Is this correct? (y/n)")
        
    else:
        # Ask user
        ask_brand_question()
```

### Pass to Sub-Agents

When orchestrator calls sub-agents, include brand context:

```markdown
## Agent Context
Brand: Bolt
Colors: Primary #34D399, Background #FFFFFF, Text #1F2937
Typography: Inter Bold (headers), Inter Regular (body)
Style: Rounded corners, subtle shadows, generous spacing
```

---

## 📊 Brand Usage Tracking

Track which brands are used for future suggestions:

```yaml
# _user-preferences/history.yaml
- date: "2026-01-14"
  task: "AIDA Workshop"
  brand: "bolt"
  satisfaction: "high"
  
- date: "2026-01-13"
  task: "MECE Workshop"
  brand: "radiant"
  satisfaction: "high"
  
- date: "2026-01-12"
  task: "Data Analysis"
  brand: "data_dark"
  satisfaction: "medium"
```

---

## ✅ Implementation Checklist

- [x] Define brand presets (7 presets)
- [x] Create detection priority logic
- [x] Define brand question format
- [ ] Create `_user-preferences/` folder structure
- [ ] Implement auto-load in orchestrator
- [ ] Add brand context passing to sub-agents
- [ ] Add "save preference" option
- [ ] Add brand history tracking

---

*Never ask a question you can answer from context.*




