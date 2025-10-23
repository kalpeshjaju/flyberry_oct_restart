# Quick Start Guide - Flyberry Data Access

**For**: Developers who need to access Flyberry data
**Purpose**: Simple Python interface to all product, recipe, and brand data
**No database needed**: Just load JSON files into memory

---

## 🚀 Instant Usage

```python
from flyberry_data_loader import FlyberryData

# Initialize (loads nothing yet - lazy loading)
data = FlyberryData()

# Get all data for LLM context (114KB - fits in any LLM)
context = data.to_llm_context()

# Send to Claude/GPT with your prompt
# Example: "Generate a brand package for a competitor using this data as reference"
```

---

## 📁 What's Inside?

```
flyberry_oct_restart/
├── extracted_data/              # Production JSON (160KB)
│   ├── products/ (13 files)     # Complete product catalog
│   ├── recipes/ (11 files)      # Recipe collection
│   ├── design/ (1 file)         # Brand design system
│   └── schemas/ (3 files)       # Validation schemas
│
├── input_raw_data_recreate/
│   ├── 01-ORIGINAL-PDFs/        # 9 source PDFs
│   └── input_data_marked_down/  # Reference data
│       ├── claims-registry.json  # 30 health claims
│       └── PDF_TO_DATA_MAPPING.md # Extraction tracking
│
├── flyberry_data_loader.py      # ← Use this to access data
├── example_usage.py              # ← See examples here
└── validate-data.js              # Validation script
```

---

## 🔍 Common Queries

### Get Specific Product
```python
medjoul = data.get_product("medjoul-dates")
print(medjoul['tagline'])  # "Majestic Medjoul Dates"
print(medjoul['packaging']['color'])  # "#5c438d"
```

### Filter Products by Attribute
```python
# By origin
saudi_products = data.find_products_by(origin="Imported Product of Saudi Arabia")
# Returns: Ajwa Dates, Mabroom Dates

# By nested attribute (packaging color)
pink_products = data.find_products_by(**{"packaging.color": "#fd478e"})
# Returns: Mabroom Dates
```

### Find Products with Specific Claim
```python
fiber_products = data.get_products_with_claim("CLAIM-001")
# Returns: ['deri-dates', 'kalmi-dates', 'mabroom-dates', 'medjoul-dates']
```

### Get Recipe with Related Product
```python
recipe = data.get_recipe("natural-caramel")
product = data.get_product(recipe['relatedProduct'])

print(f"{recipe['name']} uses {product['name']}")
# "Natural Caramel uses Mabroom Dates"
```

### Validate All Data
```bash
node validate-data.js
# Expected: 25/25 files valid ✅
```

---

## 📊 What You Have

### Products (13)
- **8 Dates**: Ameri, Ajwa, Deglet Nour, Deri, Halawi, Kalmi, Mabroom, Medjoul
- **5 Nuts**: Macadamia, Pecan, Brazil, Hazelnuts, Pine

**Each product includes:**
- Name, tagline, description
- Packaging colors (hex codes)
- Origin country
- Complete nutritional facts with RDA%
- Health benefits
- Manufacturer info
- Related recipes

### Recipes (11)
- Indian sweets (Kalakand, Katli)
- No-bake treats (Date Bars, Date Bark)
- Desserts (Fondue, Sundae, Caramel)
- Condiments (Vegan Parmesan)
- More!

**Each recipe includes:**
- Ingredients with quantities
- Step-by-step instructions
- Prep/cook/total time
- Difficulty level
- Tips & variations
- Tags for categorization

### Design System (1)
- Typography (fonts, usage)
- Logos (6 variants)
- Color palettes (48 colors with hex + RGB)
- Iconography
- Brand guidelines

---

## ✅ Quality Assurance

**All data validated**: 25/25 files passed (100%)

```bash
# Run validation anytime
node validate-data.js

# Expected output:
# Products:  13/13 valid ✅
# Recipes:   11/11 valid ✅
# Design:    1/1 valid ✅
# Total:     25/25 files valid ✅
```

---

## 🎯 Common Use Cases

### 1. Find a product by color
```bash
grep -r "#fd478e" extracted_data/products/
# Returns: Mabroom Dates (Pink)
```

### 2. Find vegan recipes
```bash
grep -l "Vegan" extracted_data/recipes/*.json
# Returns: vegan-parmesan.json, date-bars.json, natural-caramel.json
```

### 3. List all dates from Jordan
```bash
jq -r '.dates[] | select(.origin | contains("Jordan")) | .name' extracted_data/products/index.json
# Returns: Ameri Dates, Medjoul Dates
```

### 4. Find highest fiber product
```bash
jq -r '.dates[] | "\(.name): \(.nutritionalFacts.dietaryFiberPercent)"' extracted_data/products/index.json
# Shows fiber % for all dates
```

---

## 📖 Read These First

1. **`EXTRACTION_COMPLETE.md`** - What was accomplished
2. **`PROJECT_INDEX.md`** - Full project structure
3. **`extracted_data/README.json`** - Data documentation

---

## 📊 Performance

| Operation | Time | Data Size |
|-----------|------|-----------|
| Load all data | <1 second | 160KB JSON |
| Find product | <1ms | In-memory search |
| Filter products | <5ms | Linear scan (13 items) |
| Get LLM context | <10ms | JSON stringify |

**Why it's fast**: Only 13 products, all in memory, no database overhead

---

## 🎯 Use Cases

### 1. LLM Brand Package Generation
```python
from flyberry_data_loader import FlyberryData

data = FlyberryData()
context = data.to_llm_context()

# Send to Claude API
prompt = f"""
Using this brand data as reference:
{context}

Generate a brand package for [COMPETITOR NAME]
"""
# Send prompt to Claude API
```

### 2. Product Comparison
```python
data = FlyberryData()

# Compare nutritional profiles
for product in data.products:
    fiber_benefit = next((b for b in product['benefits'] if 'fiber' in b['claim'].lower()), None)
    if fiber_benefit:
        print(f"{product['name']}: {fiber_benefit['rdaPercent']}% fiber")
```

### 3. Recipe Content Creation
```python
data = FlyberryData()

recipe = data.get_recipe("natural-caramel")
product = data.get_product(recipe['relatedProduct'])

print(f"Recipe: {recipe['name']}")
print(f"Uses: {product['name']} ({product['packaging']['colorName']})")
```

---

## 🎨 Cool Data Points

- **Highest Fiber**: Medjoul Dates (13.5% RDA)
- **Highest Selenium**: Brazil Nuts (254% RDA - limit 2-4/day)
- **Quickest Recipe**: Vegan Parmesan (5 minutes)
- **Most Complex Recipe**: Hazelnut Katli (2h 35m)
- **Total Colors**: 48 (hex codes + RGB values)
- **Total Recipes**: 11 (from 5 cuisines)

---

## 🚀 Next Steps

Ready to use this data?

1. **For Brand Builder**: Integrate with LLM as knowledge base
2. **For Vector DB**: Ingest JSON for semantic search
3. **For API**: Serve data via REST endpoints
4. **For Website**: Display products dynamically
5. **For Analysis**: Compare nutritional profiles

---

## ⚠️ Important Notes

- **Data validated**: All 25 files passed schema validation
- **No hallucination**: All data from official PDFs
- **Production-ready**: Clean, consistent, structured
- **LLM-friendly**: Semantic field names, nested structures
- **Extensible**: Easy to add more products/recipes

---

## 📞 Need Help?

Check these resources:

- **Full project guide**: `PROJECT_INDEX.md`
- **Completion report**: `EXTRACTION_COMPLETE.md`
- **Data documentation**: `extracted_data/README.json`
- **Product schema**: `extracted_data/schemas/product-schema.json`
- **Recipe schema**: `extracted_data/schemas/recipe-schema.json`

---

**That's it! You're ready to use Flyberry structured data.** 🎉

Start exploring with:
```bash
cat extracted_data/products/index.json
```

---

*Last updated: 2025-10-22*
