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

    print("\n" + "=" * 60)
    print("✅ All examples completed successfully!")
    print("💡 This simple approach works perfectly for 13-100 products")
    print("🚀 No database, no complexity, just works!")
    print("=" * 60)


if __name__ == "__main__":
    main()
