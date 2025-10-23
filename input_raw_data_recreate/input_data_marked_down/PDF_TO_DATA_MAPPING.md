# PDF to Extracted Data Mapping

**Project**: Flyberry Oct Restart - Data Extraction
**Purpose**: Track which PDFs have been processed and where their data lives
**Last Updated**: 2025-10-22

---

## 📊 Processing Status

| PDF File | Pages | Status | Output Location | Notes |
|----------|-------|--------|-----------------|-------|
| **DESIGN GUIDELINES (1)_compressed.pdf** | ~40 | ✅ Complete | `extracted_data/design/brand-design-system.json` | Full brand design system extracted |
| **E-COMM PRIMARY CARDS_11zon.pdf** | 84 | ✅ Complete | `extracted_data/products/` + `extracted_data/recipes/` | 13 products + 11 recipes extracted |
| **Brand Guidelines (The Art of Snacking - Past Work) (1)_compressed.pdf** | ~50 | ⏳ Pending | `input_data_marked_down/PAST-BRAND-GUIDELINES-EXTRACTED.md` | Preliminary markdown only |
| **RETAIL CATALOGUE_11zon.pdf** | ~30 | ⏳ Pending | `input_data_marked_down/RETAIL-CATALOG-EXTRACTED.md` | Preliminary markdown only |
| **GIFTING CATALOUGE_11zon.pdf** | ~20 | ⏳ Pending | `input_data_marked_down/GIFTING-CATALOG-EXTRACTED.md` | Preliminary markdown only |
| **TRAINING CATALOUGE_11zon.pdf** | ~15 | ⏳ Pending | `input_data_marked_down/TRAINING-CATALOG-EXTRACTED.md` | Preliminary markdown only |
| **HOPE GIFT BOX.pdf** | ~5 | ⏳ Pending | `input_data_marked_down/HOPE-GIFT-BOX-EXTRACTED.md` | Preliminary markdown only |
| **INVESTOR UPDATE Q1 _ FY 26_compressed.pdf** | ~12 | ⏳ Pending | `input_data_marked_down/INVESTOR-UPDATE-Q1-FY26-EXTRACTED.md` | Preliminary markdown only |
| **INVESTOR UPDATE - Q4 FY25_compressed.pdf** | ~10 | ⏳ Pending | `input_data_marked_down/INVESTOR-UPDATE-Q4-FY25-EXTRACTED.md` | Preliminary markdown only |

**Summary**: 2/9 PDFs fully processed (22%), 7 with preliminary markdown extractions

---

## ✅ Completed Extractions (JSON Format)

### 1. DESIGN GUIDELINES PDF → JSON
**Source**: `01-ORIGINAL-PDFs/DESIGN GUIDELINES (1)_compressed.pdf`
**Output**: `extracted_data/design/brand-design-system.json`

**Extracted**:
- Typography (Baloo primary, Nunito secondary)
- Logo variants (6 versions)
- Color palettes (4 categories, 48 colors total)
  - Date packaging (13 products)
  - Exotic nuts (5 products)
  - Ambient packaging (6 products)
  - Branding pastels (4 colors)
- Iconography (21 line icons)
- Illustration style guidelines
- Product photography standards
- Merchandise designs
- Print banner specifications
- Brand messaging

**Validation**: ✅ Passed (design-schema.json)

---

### 2. E-COMM PRIMARY CARDS PDF → JSON
**Source**: `01-ORIGINAL-PDFs/E-COMM PRIMARY CARDS_11zon.pdf` (84 pages)
**Output**:
- `extracted_data/products/` (13 products)
- `extracted_data/recipes/` (11 recipes)

#### Products Extracted (13)

**Dates (8):**
1. **Ameri Dates** (Pages 1-6) → `ameri-dates.json`
2. **Ajwa Dates** (Pages 7-12) → `ajwa-dates.json` + `ajwa-kalakand.json`
3. **Deglet Nour Dates** (Pages 13-18) → `deglet-nour-dates.json` + `date-bars.json`
4. **Deri Dates** (Pages 19-24) → `deri-dates.json` + `dark-chocolate-fondue.json`
5. **Halawi Dates** (Pages 25-30) → `halawi-dates.json` + `date-bark.json`
6. **Kalmi Dates** (Pages 31-36) → `kalmi-dates.json` + `caramely-date-sundae.json`
7. **Mabroom Dates** (Pages 37-42) → `mabroom-dates.json` + `natural-caramel.json`
8. **Medjoul Dates** (Pages 43-54) → `medjoul-dates.json` (with workout benefits)

**Nuts (5):**
9. **Macadamia Nuts** (Pages 55-60) → `macadamia-nuts.json` + `nut-pulao.json`
10. **Pecan Nuts** (Pages 61-66) → `pecan-nuts.json` + `roasted-spiced-pecan-nuts.json`
11. **Brazil Nuts** (Pages 67-72) → `brazil-nuts.json` + `vegan-parmesan.json`
12. **Hazelnuts** (Pages 73-78) → `hazelnuts.json` + `hazelnut-katli.json`
13. **Pine Nuts** (Pages 79-84) → `pine-nuts.json` + `pine-nut-candy.json`

#### Recipes Extracted (11)
1. `ajwa-kalakand.json` - Indian sweet (30 min)
2. `date-bars.json` - No-bake energy bars (2h 15m)
3. `dark-chocolate-fondue.json` - Party dessert (15 min)
4. `date-bark.json` - No-bake chocolate treat (2h 15m)
5. `caramely-date-sundae.json` - Quick dessert (20 min)
6. `natural-caramel.json` - Vegan condiment (15 min)
7. `nut-pulao.json` - Indian rice dish (40 min)
8. `roasted-spiced-pecan-nuts.json` - Snack (20 min)
9. `vegan-parmesan.json` - Cheese alternative (5 min)
10. `hazelnut-katli.json` - Indian sweet (2h 35m)
11. `pine-nut-candy.json` - Middle Eastern candy (1h 25m)

**Validation**: ✅ All 24 files passed (product-schema.json, recipe-schema.json)

---

## ⏳ Preliminary Extractions (Markdown Format)

These PDFs have been extracted to markdown but not yet converted to structured JSON:

### 3. RETAIL CATALOGUE
**Source**: `01-ORIGINAL-PDFs/RETAIL CATALOGUE_11zon.pdf`
**Output**: `input_data_marked_down/RETAIL-CATALOG-EXTRACTED.md`
**Status**: Markdown only (needs JSON conversion)

### 4. GIFTING CATALOGUE
**Source**: `01-ORIGINAL-PDFs/GIFTING CATALOUGE_11zon.pdf`
**Output**: `input_data_marked_down/GIFTING-CATALOG-EXTRACTED.md`
**Status**: Markdown only (needs JSON conversion)

### 5. TRAINING CATALOGUE
**Source**: `01-ORIGINAL-PDFs/TRAINING CATALOUGE_11zon.pdf`
**Output**: `input_data_marked_down/TRAINING-CATALOG-EXTRACTED.md`
**Status**: Markdown only (needs JSON conversion)

### 6. HOPE GIFT BOX
**Source**: `01-ORIGINAL-PDFs/HOPE GIFT BOX.pdf`
**Output**: `input_data_marked_down/HOPE-GIFT-BOX-EXTRACTED.md`
**Status**: Markdown only (needs JSON conversion)

### 7. PAST BRAND GUIDELINES
**Source**: `01-ORIGINAL-PDFs/Brand Guidelines (The Art of Snacking - Past Work) (1)_compressed.pdf`
**Output**: `input_data_marked_down/PAST-BRAND-GUIDELINES-EXTRACTED.md`
**Status**: Markdown only (reference document)

### 8. INVESTOR UPDATE Q1 FY26
**Source**: `01-ORIGINAL-PDFs/INVESTOR UPDATE Q1 _ FY 26_compressed.pdf`
**Output**: `input_data_marked_down/INVESTOR-UPDATE-Q1-FY26-EXTRACTED.md`
**Status**: Markdown only (business intelligence)

### 9. INVESTOR UPDATE Q4 FY25
**Source**: `01-ORIGINAL-PDFs/INVESTOR UPDATE - Q4 FY25_compressed.pdf`
**Output**: `input_data_marked_down/INVESTOR-UPDATE-Q4-FY25-EXTRACTED.md`
**Status**: Markdown only (business intelligence)

---

## 🌐 Web Research

### COMPETITIVE LANDSCAPE
**Source**: Web research (manual)
**Output**: `input_data_marked_down/COMPETITIVE-LANDSCAPE-WEB-RESEARCH-2025-10.md`
**Status**: Markdown only (market intelligence)

---

## 📋 Next Steps for Phase 2

### High Priority
1. **Extract Claims Registry** from products data
2. **Convert Catalogs to JSON**:
   - Retail Catalogue → Product listings JSON
   - Gifting Catalogue → Gift box configurations JSON
   - Training Catalogue → Training materials JSON

### Medium Priority
3. **Extract Business Intelligence**:
   - Investor updates → Financial metrics JSON
   - Market trends from competitive landscape

### Low Priority
4. **Reference Documents**:
   - Past brand guidelines (historical reference)
   - Hope Gift Box (specific campaign)

---

## 🔄 Extraction Methodology

### Phase 1 (Completed)
**Method**: Hybrid approach
1. Vision API reads PDF (multimodal)
2. Extract data to structured JSON
3. Validate against JSON Schema
4. Create index files

**Applied to**: Design Guidelines + E-Comm Cards

### Phase 2 (Pending)
**Method**: Same hybrid approach
**Apply to**: Remaining 7 PDFs

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| PDFs processed | 2/9 (22%) |
| JSON files created | 31 |
| Total pages processed | ~124 pages |
| Validation pass rate | 100% (25/25 files) |
| Data size | 160KB |

---

**Mapping maintained by**: Automated extraction process
**Last updated**: 2025-10-22
