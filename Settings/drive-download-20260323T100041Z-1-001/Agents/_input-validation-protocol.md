# Input Validation Protocol

**Version:** 1.0  
**Applies To:** All agents that receive data inputs  
**Purpose:** Validate and quality-score all inputs before processing

---

## The Problem

Current state: Agents accept any input without checking quality.

**What goes wrong:**
- Missing values cause silent failures
- Wrong formats produce garbage output
- Outliers skew analysis
- Users don't know their data has issues

**What should happen:**
- Validate input before processing
- Score data quality
- Alert user to issues
- Suggest fixes or proceed with caveats

---

## Input Validation Flow

```
USER PROVIDES INPUT
        │
        ▼
┌───────────────────────────────────┐
│  STEP 1: FORMAT VALIDATION        │
│  ├── Is file readable?            │
│  ├── Is format correct?           │
│  ├── Are headers present?         │
│  └── Is encoding correct?         │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  STEP 2: COMPLETENESS CHECK       │
│  ├── Missing values (%)           │
│  ├── Empty columns                │
│  ├── Required fields present      │
│  └── Row count vs. expected       │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  STEP 3: QUALITY ASSESSMENT       │
│  ├── Duplicates detected          │
│  ├── Outliers identified          │
│  ├── Data type consistency        │
│  └── Value range validation       │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  STEP 4: QUALITY SCORE            │
│  └── Generate 1-10 score          │
└───────────────────────────────────┘
        │
        ├── Score ≥ 7 ──→ PROCEED (good data)
        │
        ├── Score 4-6 ──→ WARN + PROCEED (acceptable with caveats)
        │
        └── Score < 4 ──→ STOP + REQUIRE FIX (bad data)
```

---

## Validation Checks by Data Type

### Tabular Data (CSV, Excel, Sheets)

```markdown
## Data Validation Report

**File:** [filename]
**Format:** CSV | Excel | Google Sheets
**Rows:** [count] | **Columns:** [count]

### Format Checks
| Check | Status | Notes |
|-------|--------|-------|
| File readable | ✅/❌ | |
| Headers present | ✅/❌ | |
| Consistent columns | ✅/❌ | Row X has different count |
| Encoding | ✅/❌ | UTF-8 expected |

### Completeness Checks
| Column | Missing % | Status |
|--------|-----------|--------|
| [col1] | 0% | ✅ |
| [col2] | 5% | ⚠️ Acceptable |
| [col3] | 25% | 🔴 High |

### Quality Checks
| Issue | Count | Severity |
|-------|-------|----------|
| Duplicates | X rows | ⚠️ |
| Outliers | X values | ⚠️ |
| Type errors | X cells | 🔴 |

### Overall Score: [X/10]
```

### JSON/API Data

```markdown
## JSON Validation Report

**Source:** [URL or file]
**Size:** [KB/MB]

### Structure Checks
| Check | Status |
|-------|--------|
| Valid JSON | ✅/❌ |
| Expected schema | ✅/❌ |
| Required fields | ✅/❌ |

### Completeness
| Field | Present | Type Correct |
|-------|---------|--------------|
| [field1] | ✅/❌ | ✅/❌ |

### Overall Score: [X/10]
```

### Text/Document Input

```markdown
## Document Validation Report

**Type:** Markdown | PDF | Doc
**Length:** [words/pages]

### Quality Checks
| Check | Status |
|-------|--------|
| Readable content | ✅/❌ |
| Language detected | [language] |
| Formatting intact | ✅/❌ |
| Images accessible | ✅/❌ |

### Content Assessment
- Word count: [X]
- Estimated reading time: [X min]
- Key topics detected: [list]

### Overall Score: [X/10]
```

---

## Quality Score Calculation

### Scoring Formula

```
Base Score: 10

Deductions:
- Missing values >5%: -1 per 5% over threshold
- Duplicates >1%: -1
- Type errors: -2
- Format issues: -2
- Outliers >2%: -1
- Missing required fields: -3 each
- Encoding issues: -1

Final Score = max(0, Base Score - Deductions)
```

### Score Interpretation

| Score | Rating | Action |
|-------|--------|--------|
| 9-10 | Excellent | Proceed without caveats |
| 7-8 | Good | Proceed, minor notes |
| 5-6 | Acceptable | Proceed with documented caveats |
| 3-4 | Poor | Warn user, ask to confirm |
| 0-2 | Critical | Stop, require data fix |

---

## User Communication

### Good Data (Score ≥ 7)

```markdown
"✅ Data looks good! 

Quick summary:
- [X] rows, [Y] columns
- No critical issues
- Ready to analyze

Proceeding with analysis..."
```

### Acceptable Data (Score 4-6)

```markdown
"⚠️ Data has some issues I should mention:

**Issues Found:**
- 12% missing values in 'Revenue' column
- 3 outliers detected in 'Growth' column

**Impact on Analysis:**
- Results may be less reliable for Revenue-related insights
- Outliers could skew averages

**Options:**
[A] Proceed anyway (I'll note limitations)
[B] Let me suggest data fixes first
[C] Stop and fix data manually"
```

### Bad Data (Score < 4)

```markdown
"🔴 Data quality is too low for reliable analysis.

**Critical Issues:**
- 45% missing values overall
- Multiple columns with wrong data types
- Duplicate rows detected (15%)

**Required Actions:**
1. Fill or remove missing values
2. Fix data types in columns [X, Y, Z]
3. Remove duplicate rows

I can't proceed until these are fixed. Would you like:
[A] Guidance on how to fix these issues
[B] Proceed anyway (results will be unreliable)
[C] Upload different data"
```

---

## Agent-Specific Validation

### @data-analyst

```markdown
Additional checks:
- Numeric columns have numeric data
- Date columns parse correctly
- Metric columns have reasonable ranges
- Categorical columns have expected values
```

### @financial-modeler

```markdown
Additional checks:
- Financial columns are numeric
- Currency consistency
- Time period alignment
- No negative values where inappropriate
```

### @web-scraper-ninja

```markdown
Output validation:
- URLs are valid and accessible
- Extracted fields match schema
- No empty required fields
- Data freshness timestamp
```

### @competitive-analyst

```markdown
Input validation:
- Competitor names are valid
- Data sources are recent
- Market segments are defined
- Metrics are comparable
```

---

## Auto-Fix Suggestions

### For Missing Values

```markdown
"Missing values in '[column]' (12%):

Suggested fixes:
A) Fill with mean/median (numeric columns)
B) Fill with mode (categorical columns)
C) Remove rows with missing values
D) Flag as 'Unknown' and proceed

What would you prefer?"
```

### For Outliers

```markdown
"Outliers detected in '[column]':
- Value 1,000,000 (3x standard deviation)
- Value -500 (possible data entry error)

Suggested fixes:
A) Cap at 99th percentile
B) Remove outlier rows
C) Keep and note in analysis
D) Investigate manually

What would you prefer?"
```

### For Duplicates

```markdown
"Duplicate rows detected: 15 rows (3%)

Suggested fixes:
A) Remove duplicates (keep first)
B) Remove duplicates (keep last)
C) Aggregate duplicates (sum/average)
D) Keep all and note in analysis

What would you prefer?"
```

---

## Implementation Checklist

### For Each Agent:

- [ ] Add validation step before main processing
- [ ] Calculate quality score
- [ ] Display validation report
- [ ] Handle low-quality gracefully
- [ ] Offer auto-fix suggestions
- [ ] Log data quality in MEMORY.md

---

*"Garbage in, garbage out. Let's catch garbage at the door."*




