# ACT 1 DOCUMENT SPECIFICATIONS

**Purpose**: Modular templates for each Act 1 document - defines section structure, content requirements, quality standards.

---

## ARCHITECTURE OVERVIEW

```
INPUT (Source of Truth)
├── act-1-master-blueprint.md           ← Overall structure, standards, quality rubric
├── act-1-document-specs/               ← Document-specific templates (YOU ARE HERE)
│   ├── README.md                       ← This file
│   ├── doc-00-brand-foundation.md      ← ✅ COMPLETE
│   ├── doc-01-product-portfolio.md     ← TODO: Create
│   ├── doc-02-sourcing-philosophy.md   ← TODO: Create
│   ├── doc-03-hero-products.md         ← TODO: Create
│   ├── doc-04-nutritional-excellence.md ← TODO: Create
│   ├── doc-05-fortune-500-validation.md ← TODO: Create
│   └── doc-06-brand-promise.md         ← TODO: Create
└── brand-foundation.md                 ← Brand positioning data

GENERATOR (Logic)
└── generators/act1_generator.py        ← Reads blueprint + specs + data → Markdown

OUTPUT (HTML)
└── docs/act-1-who-we-are.html          ← Final rendered HTML
```

---

## HOW IT WORKS

### **1. Master Blueprint** (act-1-master-blueprint.md)
**Defines WHAT to build**:
- Document structure (7 documents, MECE framework)
- Content frameworks (Pyramid, MECE, SO WHAT, Confidence)
- Writing standards (tone, voice, formatting, rhythm)
- Specificity standard (no generic claims)
- Quality rubric (5 dimensions, 100 points)
- Depth requirements (every product needs 7 components)

**When to update**: When overall standards change (new content framework, quality standard, writing style)

---

### **2. Document Specifications** (this folder)
**Defines HOW to build each document**:
- Section structure (10 sections for Doc 00, 8 for Doc 01, etc.)
- Content templates (what goes in each section)
- Data sources (which JSON files to pull from)
- Quality requirements (must have / must avoid)
- Output format (markdown structure)

**When to update**: When document-specific content changes (new section added, section reordered, template modified)

---

### **3. Generator** (generators/act1_generator.py)
**Executes the build**:
- Reads master blueprint (understands standards)
- Reads document specs (understands structure)
- Pulls data from JSON sources (products, design, brand-foundation)
- Applies templates to data
- Generates markdown following quality standards
- Writes to source/ folder

**When to update**: When logic changes (new data source, new processing rule, new validation)

---

## MODULAR UPDATE WORKFLOW

### **Scenario 1: Change Writing Style** (e.g., make more concise)
**Update**: `act-1-master-blueprint.md` → Writing Standards section
**Result**: Next build applies new style to ALL documents automatically

### **Scenario 2: Add New Section to Document 00** (e.g., "Our History")
**Update**: `doc-00-brand-foundation.md` → Add new section template
**Result**: Generator adds new section to Doc 00 only, other docs unchanged

### **Scenario 3: Change Brand Positioning** (e.g., new tagline)
**Update**: `brand-foundation.md` → Update tagline
**Result**: Next build pulls new tagline automatically, no code changes needed

### **Scenario 4: Add New Product** (e.g., Pistachio Nuts)
**Update**: `products/pistachio-nuts.json` → Add new product file
**Result**: Generator automatically includes in Product Portfolio (Doc 01), updates counts in Doc 00

---

## CONSISTENCY GUARANTEES

✅ **All documents follow same blueprint** (master-blueprint.md)
✅ **All documents use same standards** (tone, specificity, quality)
✅ **All documents pull from same data** (JSON sources)
✅ **Changes propagate automatically** (rebuild → all updates applied)

---

## TEMPLATE STRUCTURE

Each document spec has:

### **Header** (Metadata)
```markdown
# DOCUMENT [XX]: [TITLE] - SPECIFICATION

**Version**: X.X
**Last Updated**: YYYY-MM-DD
**Read Time**: X minutes
```

### **Purpose** (Why this document exists)
One paragraph explaining document's role in Act 1.

### **Data Sources** (Where content comes from)
List of JSON files to pull from (e.g., `brand-foundation.md`, `products/*.json`)

### **Section Structure** (How document is organized)
For each section:
- **Purpose**: Why this section exists
- **Content Template**: Markdown structure to follow
- **Requirements**: Must have / must avoid checklist

### **Quality Requirements** (Quality checklist)
- Must Have: [ ] checklist
- Must Avoid: ❌ list

### **Output Format** (Final markdown structure)
Complete document structure with placeholders.

### **Changelog** (Version history)
Track changes to this spec over time.

---

## CREATING NEW DOCUMENT SPECS

**Template** (copy this for new documents):

```markdown
# DOCUMENT [XX]: [TITLE] - SPECIFICATION

**Version**: 1.0
**Last Updated**: YYYY-MM-DD
**Read Time**: X minutes

---

## PURPOSE

[One paragraph: What this document covers, why it matters]

---

## DATA SOURCES

**Primary**: `[filename.json]` (contains X, Y, Z data)
**Supporting**: `[other-file.json]` (if needed)

---

## SECTION STRUCTURE

### **Section 1: [NAME]**
**Purpose**: [Why this section exists]

**Content Template**:
```markdown
## [SECTION HEADLINE]

[Template with placeholders for dynamic content]

**[Subsection]**:
- [Bullet structure]
```

**Requirements**:
- [ ] Specific requirement 1
- [ ] Specific requirement 2

---

[Repeat for all sections]

---

## QUALITY REQUIREMENTS

### **Must Have**:
- [ ] Requirement 1
- [ ] Requirement 2

### **Must Avoid**:
- ❌ Anti-pattern 1
- ❌ Anti-pattern 2

---

## OUTPUT FORMAT

[Complete markdown structure with placeholders]

---

## CHANGELOG

**v1.0** (YYYY-MM-DD):
- Initial specification
```

---

## NEXT STEPS

1. ✅ **Master Blueprint created** (act-1-master-blueprint.md)
2. ✅ **Document 00 spec created** (doc-00-brand-foundation.md)
3. ⏳ **Create remaining 6 document specs** (doc-01 through doc-06)
4. ⏳ **Update generator** to read from blueprint + specs
5. ⏳ **Test modular build** (change blueprint → rebuild → verify propagation)

---

## BENEFITS OF THIS ARCHITECTURE

### **Easy to Update**:
- Change one file → rebuild → all documents updated consistently
- No copy-paste across documents
- No risk of inconsistency

### **Easy to Maintain**:
- Clear separation: blueprint (standards) vs specs (structure) vs data (content)
- Version control friendly (see what changed in each file)
- Rollback friendly (revert to previous version if needed)

### **Easy to Understand**:
- Blueprint explains WHY (standards, principles)
- Specs explain WHAT (structure, sections)
- Generator explains HOW (logic, processing)
- Data explains CONTENT (actual information)

### **Scalable**:
- Add new document → create new spec → generator includes it
- Change standard → update blueprint → all documents comply
- Add new data → update JSON → all relevant documents updated

---

## USAGE

**For Developers**:
```bash
# 1. Update blueprint (if standards change)
vim act-1-master-blueprint.md

# 2. Update document spec (if structure changes)
vim act-1-document-specs/doc-XX-name.md

# 3. Update data (if content changes)
vim products/some-product.json

# 4. Rebuild
python3 build.py

# 5. Verify output
open docs/act-1-who-we-are.html
```

**For Content Writers**:
- Don't edit HTML directly (will be overwritten)
- Edit markdown specs (structure) or JSON data (content)
- Rebuild to see changes in HTML

**For Reviewers**:
- Use master blueprint quality rubric to assess output
- Check that generator follows document specs
- Verify data sources are being used correctly

---

## QUESTIONS?

**Q: Where do I change the actual product information?**
A: In `products/*.json` files (e.g., `products/medjoul-dates.json`)

**Q: Where do I change the structure of Document 01?**
A: In `act-1-document-specs/doc-01-product-portfolio.md`

**Q: Where do I change the writing style for all documents?**
A: In `act-1-master-blueprint.md` → Writing Standards section

**Q: Where do I change the quality standards?**
A: In `act-1-master-blueprint.md` → Quality Checklist or Depth Rubric sections

**Q: How do I add a new document to Act 1?**
A:
1. Create new spec: `act-1-document-specs/doc-07-new-doc.md`
2. Update master blueprint: Add to document structure list
3. Update generator: Add logic to build new document
4. Rebuild: `python3 build.py`

---

**Last Updated**: 2025-10-23
**Version**: 1.0
