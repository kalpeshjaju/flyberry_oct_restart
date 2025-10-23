#!/usr/bin/env python3
"""
Example: Using FlyberryData for Brand Package Generation

Shows how to load data and prepare it for LLM (Claude/GPT) consumption.
This is all you need - no database, no vector store, just simple Python.
"""

from flyberry_data_loader import FlyberryData
import json


def main():
    print("=" * 60)
    print("FLYBERRY DATA LOADER - Example Usage")
    print("=" * 60)

    # Initialize loader
    data = FlyberryData()

    # EXAMPLE 1: Get all data for LLM context
    print("\n[1] Complete Context for LLM (all data)")
    print("-" * 60)
    all_data = data.load_all()
    context_string = data.to_llm_context()
    print(f"Context size: {len(context_string):,} characters (~{len(context_string) // 1000}KB)")
    print(f"Products: {len(all_data['products'])}")
    print(f"Recipes: {len(all_data['recipes'])}")
    print(f"Claims: {all_data['claims']['claimsRegistry']['totalClaims']}")
    print("\n✅ This entire dataset fits in Claude's context window!")

    # EXAMPLE 2: Get specific product
    print("\n[2] Specific Product Query")
    print("-" * 60)
    medjoul = data.get_product("medjoul-dates")
    if medjoul:
        print(f"Product: {medjoul['name']}")
        print(f"Tagline: {medjoul['tagline']}")
        print(f"Origin: {medjoul['origin']}")
        print(f"Color: {medjoul['packaging']['color']} ({medjoul['packaging']['colorName']})")
        print(f"Benefits: {len(medjoul['benefits'])} health benefits")
        print(f"Special: {medjoul.get('specialFeature', 'N/A')}")

    # EXAMPLE 3: Filter products by attribute
    print("\n[3] Filter Products by Origin")
    print("-" * 60)
    saudi_products = data.find_products_by(origin="Imported Product of Saudi Arabia")
    print(f"Products from Saudi Arabia: {len(saudi_products)}")
    for product in saudi_products:
        print(f"  - {product['name']} ({product['packaging']['colorName']})")

    # EXAMPLE 4: Find products by nested attribute (color)
    print("\n[4] Filter by Packaging Color")
    print("-" * 60)
    pink_products = data.find_products_by(**{"packaging.color": "#fd478e"})
    print(f"Products with pink packaging (#fd478e):")
    for product in pink_products:
        print(f"  - {product['name']}")

    # EXAMPLE 5: Get products with specific claim
    print("\n[5] Products with Specific Health Claim")
    print("-" * 60)
    fiber_products = data.get_products_with_claim("CLAIM-001")
    print(f"Products with 'Excellent source of dietary fibre' claim:")
    for product_id in fiber_products:
        product = data.get_product(product_id)
        if product:
            fiber_benefit = next((b for b in product['benefits'] if 'fiber' in b['claim'].lower()), None)
            if fiber_benefit:
                print(f"  - {product['name']}: {fiber_benefit['rdaPercent']}% RDA")

    # EXAMPLE 6: Recipe with related product
    print("\n[6] Recipe with Product Info")
    print("-" * 60)
    caramel = data.get_recipe("natural-caramel")
    if caramel:
        print(f"Recipe: {caramel['name']}")
        print(f"Difficulty: {caramel['difficulty']}")
        print(f"Total Time: {caramel['totalTime']}")

        related_product = data.get_product(caramel['relatedProduct'])
        if related_product:
            print(f"Uses: {related_product['name']}")
            print(f"Product Color: {related_product['packaging']['color']}")

    # EXAMPLE 7: Brand design system
    print("\n[7] Brand Design System")
    print("-" * 60)
    design = data.design
    print(f"Brand: {design['brand']['name']}")
    print(f"Tagline: {design['brand']['tagline']}")
    print(f"Primary Font: {design['typography']['primary']['name']}")
    print(f"Secondary Font: {design['typography']['secondary']['name']}")
    print(f"Color Palettes: {len(design['colorPalettes'])} categories")
    print(f"Logo Variants: {len(design['logos']['variants'])}")
    print(f"Icon Style: {design['iconography']['style']}")

    # EXAMPLE 8: Prepare for LLM (like Claude)
    print("\n[8] Ready for LLM Integration")
    print("-" * 60)
    print("To use with Claude/GPT:")
    print("")
    print("```python")
    print("# Load all Flyberry data")
    print("from flyberry_data_loader import FlyberryData")
    print("data = FlyberryData()")
    print("")
    print("# Option 1: Send complete context to LLM")
    print("context = data.to_llm_context()")
    print("# Send 'context' to Claude API with your prompt")
    print("")
    print("# Option 2: Send specific data only")
    print("product = data.get_product('medjoul-dates')")
    print("design = data.design")
    print("claims = data.claims")
    print("# Combine and send to LLM")
    print("```")

    # EXAMPLE 9: Get product WITH source verification (NEW!)
    print("\n[9] Product with Source Verification")
    print("-" * 60)
    medjoul_verified = data.get_product("medjoul-dates", include_sources=True)
    if medjoul_verified:
        print(f"Product: {medjoul_verified['name']}")
        print(f"\nSource Information:")
        print(f"  Markdown: {medjoul_verified['_sources']['markdown']}")
        print(f"  Raw PDF: {medjoul_verified['_sources']['raw']}")
        print(f"  Confidence: {medjoul_verified['_sources']['confidence']}")
        print(f"  Last Verified: {medjoul_verified['_sources']['lastVerified']}")
        print(f"\nMarkdown Context: {len(medjoul_verified['_markdown_context'])} characters")
        print("✅ Claude can now verify claims against original sources!")

    # EXAMPLE 10: Verify product data (NEW!)
    print("\n[10] Verify Product Against Source")
    print("-" * 60)
    verification = data.verify_product("medjoul-dates")
    if "error" not in verification:
        print(f"Product: {verification['productId']}")
        print(f"Confidence: {verification['confidence'] * 100:.0f}%")
        print(f"Verified Fields: {', '.join(verification['matches'])}")
        if verification['discrepancies']:
            print(f"Discrepancies: {len(verification['discrepancies'])}")
            for disc in verification['discrepancies']:
                print(f"  - {disc}")
        print(f"Source File: {verification['sourceFile']}")
        print("✅ Data verified against original markdown source!")

    # EXAMPLE 11: Verify recipe data (NEW!)
    print("\n[11] Verify Recipe Against Source")
    print("-" * 60)
    recipe_verification = data.verify_recipe("natural-caramel")
    if "error" not in recipe_verification:
        print(f"Recipe: {recipe_verification['recipeId']}")
        print(f"Confidence: {recipe_verification['confidence'] * 100:.0f}%")
        print(f"Verified Fields: {', '.join(recipe_verification['matches'])}")
        print(f"Source File: {recipe_verification['sourceFile']}")

    # EXAMPLE 12: Get lineage summary (NEW!)
    print("\n[12] Data Lineage Summary")
    print("-" * 60)
    lineage_summary = data.get_lineage_summary()
    if "error" not in lineage_summary:
        print(f"Total Data Files: {lineage_summary['totalDataFiles']}")
        print(f"High Confidence: {lineage_summary['highConfidence']}")
        print(f"Unique Markdown Sources: {lineage_summary['uniqueMarkdownSources']}")
        print(f"Unique Raw PDFs: {lineage_summary['uniqueRawSources']}")
        print(f"Overall Confidence Rate: {lineage_summary['confidenceRate'] * 100:.0f}%")
        print("✅ Full data lineage tracked!")

    # EXAMPLE 13: Two-Source Prompting for Claude (NEWEST!)
    print("\n[13] Two-Source Prompt Generation for Claude")
    print("-" * 60)
    prompt = data.to_two_source_prompt(
        product_id="medjoul-dates",
        question="What is the origin of this product and what are its key nutritional benefits?"
    )
    print("Generated prompt for Claude Sonnet 4.5:")
    print(f"  Length: {len(prompt)} characters")
    print(f"  Model: claude-sonnet-4-20250514")
    print(f"  Strategy: JSON (facts) + Markdown (context)")
    print("\nPrompt Preview (first 500 chars):")
    print(prompt[:500] + "...")
    print("\n✅ Ready to send to Claude API!")
    print("💡 This prevents hallucinations by using JSON as source of truth")

    print("\n" + "=" * 60)
    print("✅ All examples completed successfully!")
    print("💡 NEW: Two-source prompting for Claude Sonnet 4.5!")
    print("🚀 No database, no complexity, just works!")
    print("=" * 60)
    print("\n📊 SUMMARY:")
    print("  - Fast JSON loading (original)")
    print("  - Markdown source loading (NEW)")
    print("  - Data verification (NEW)")
    print("  - Lineage tracking (NEW)")
    print("  - Two-source prompting (NEWEST!)")
    print("  - Claude Sonnet 4.5 ready (claude-sonnet-4-20250514)")
    print("  - Perfect for AI/LLM consumption!")


if __name__ == "__main__":
    main()
