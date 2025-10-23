#!/usr/bin/env python3
"""
Test Two-Source Prompting - Real-World Cases

Tests:
1. Data Fetch - Question with MISSING data (sales info)
2. Data Check - Question with AVAILABLE data (taste profile)

This shows how Claude handles both scenarios using the two-source strategy.
"""

from flyberry_data_loader import FlyberryData
import json


def test_case_1_data_fetch_missing():
    """
    TEST 1: Data Fetch - Ask for data that DOESN'T EXIST

    Question: "Give me list of medjoul products by sales"
    Expected: Claude says "information not available" (no hallucination)
    """
    print("=" * 70)
    print("TEST 1: DATA FETCH - Missing Data (Sales Information)")
    print("=" * 70)

    data = FlyberryData()

    # Generate prompt
    prompt = data.to_two_source_prompt(
        product_id="medjoul-dates",
        question="Give me a list of all Medjoul products ranked by sales volume. Which one sells the most?"
    )

    print("\n📋 QUESTION:")
    print("   'Give me list of Medjoul products by sales volume'")

    print("\n🔍 WHAT'S IN THE DATA:")
    product = data.get_product("medjoul-dates")
    print(f"   - Product Name: {product.get('name')}")
    print(f"   - Origin: {product.get('origin')}")
    print(f"   - Benefits: {len(product.get('benefits', []))} listed")
    print(f"   - Sales Data: {'YES' if 'sales' in product or 'salesVolume' in product else '❌ NO (not available)'}")

    print("\n💡 EXPECTED BEHAVIOR:")
    print("   Claude should say: 'This information is not available in the provided documents'")
    print("   (Because sales data doesn't exist in JSON or Markdown)")

    print("\n📤 GENERATED PROMPT LENGTH:")
    print(f"   {len(prompt):,} characters")

    print("\n" + "=" * 70)
    print("PROMPT TO SEND TO CLAUDE:")
    print("=" * 70)
    print(prompt[:1000] + "\n...\n[Prompt continues...]")

    print("\n" + "=" * 70)
    print("HOW TO TEST WITH CLAUDE API:")
    print("=" * 70)
    print("""
import anthropic

client = anthropic.Anthropic(api_key="your-key")
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)
# Expected: "This information is not available in the provided documents"
    """)

    return prompt


def test_case_2_data_check_available():
    """
    TEST 2: Data Check - Ask about data that EXISTS

    Question: "Are Medjoul dates sour?"
    Expected: Claude answers based on JSON taste data
    """
    print("\n" * 2)
    print("=" * 70)
    print("TEST 2: DATA CHECK - Available Data (Taste Profile)")
    print("=" * 70)

    data = FlyberryData()

    # Generate prompt
    prompt = data.to_two_source_prompt(
        product_id="medjoul-dates",
        question="Are Medjoul dates sour? What is their taste profile?"
    )

    print("\n📋 QUESTION:")
    print("   'Are Medjoul dates sour? What is their taste profile?'")

    print("\n🔍 WHAT'S IN THE DATA:")
    product = data.get_product("medjoul-dates")
    print(f"   - Product Name: {product.get('name')}")
    print(f"   - Description: {product.get('description', 'N/A')[:80]}...")
    print(f"   - Characteristics: {product.get('characteristics', 'N/A')}")
    print(f"   - Tasting Notes: {product.get('tastingNotes', 'N/A')[:80]}...")

    print("\n💡 EXPECTED BEHAVIOR:")
    print("   Claude should say:")
    print("   - 'According to JSON data, Medjoul dates have...'")
    print("   - Cite taste characteristics from JSON")
    print("   - Confirm they are SWEET, not sour")
    print("   - Mention 'rich caramel taste', 'soft texture'")

    print("\n📤 GENERATED PROMPT LENGTH:")
    print(f"   {len(prompt):,} characters")

    print("\n" + "=" * 70)
    print("PROMPT TO SEND TO CLAUDE:")
    print("=" * 70)
    print(prompt[:1000] + "\n...\n[Prompt continues...]")

    print("\n" + "=" * 70)
    print("HOW TO TEST WITH CLAUDE API:")
    print("=" * 70)
    print("""
import anthropic

client = anthropic.Anthropic(api_key="your-key")
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)
# Expected: "According to the JSON data, Medjoul dates are described as
#            'incredibly sweet' with a 'rich caramel taste'. They are not sour."
    """)

    return prompt


def test_case_3_verify_json_markdown_consistency():
    """
    TEST 3: Verify JSON and Markdown say the same thing
    """
    print("\n" * 2)
    print("=" * 70)
    print("TEST 3: CONSISTENCY CHECK - JSON vs Markdown")
    print("=" * 70)

    data = FlyberryData()

    # Get product with sources
    product = data.get_product("medjoul-dates", include_sources=True)

    print("\n🔍 JSON DATA SAYS:")
    print(f"   Name: {product.get('name')}")
    print(f"   Tagline: {product.get('tagline')}")
    print(f"   Description: {product.get('description', 'N/A')[:100]}...")
    print(f"   Characteristics: {product.get('characteristics')}")

    print("\n🔍 MARKDOWN CONTEXT:")
    md_context = product.get('_markdown_context', '')
    print(f"   Length: {len(md_context)} characters")
    print(f"   Contains 'Medjoul': {'✅ YES' if 'Medjoul' in md_context else '❌ NO'}")
    print(f"   Contains 'sweet': {'✅ YES' if 'sweet' in md_context.lower() else '❌ NO'}")
    print(f"   Contains 'caramel': {'✅ YES' if 'caramel' in md_context.lower() else '❌ NO'}")

    print("\n✅ VERIFICATION:")
    verification = data.verify_product("medjoul-dates")
    print(f"   Confidence: {verification['confidence'] * 100:.0f}%")
    print(f"   Matches: {', '.join(verification['matches'])}")
    if verification['discrepancies']:
        print(f"   Discrepancies: {len(verification['discrepancies'])}")
        for disc in verification['discrepancies'][:3]:
            print(f"      - {disc}")


def save_prompts_to_file(prompt1, prompt2):
    """
    Save generated prompts to files for easy testing
    """
    with open('test_prompt_1_missing_data.txt', 'w') as f:
        f.write(prompt1)

    with open('test_prompt_2_available_data.txt', 'w') as f:
        f.write(prompt2)

    print("\n" * 2)
    print("=" * 70)
    print("PROMPTS SAVED TO FILES:")
    print("=" * 70)
    print("   1. test_prompt_1_missing_data.txt")
    print("   2. test_prompt_2_available_data.txt")
    print("\n   You can copy-paste these into Claude's web interface to test!")


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║       TWO-SOURCE PROMPTING TEST SUITE                                ║
║       Testing Claude Sonnet 4.5 with Flyberry Data                   ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

    # Run tests
    prompt1 = test_case_1_data_fetch_missing()
    prompt2 = test_case_2_data_check_available()
    test_case_3_verify_json_markdown_consistency()

    # Save prompts for manual testing
    save_prompts_to_file(prompt1, prompt2)

    print("\n" * 2)
    print("=" * 70)
    print("SUMMARY - HOW TO TEST")
    print("=" * 70)
    print("""
OPTION 1: Test with Claude API (Automated)
-------------------------------------------
pip install anthropic
export ANTHROPIC_API_KEY="your-key-here"

Then run:
    python3 test_with_claude_api.py

OPTION 2: Test with Claude Web Interface (Manual)
--------------------------------------------------
1. Open: https://claude.ai
2. Copy content from: test_prompt_1_missing_data.txt
3. Paste into Claude chat
4. Check if Claude says "information not available" ✅
5. Repeat with: test_prompt_2_available_data.txt
6. Check if Claude cites JSON data about sweet taste ✅

OPTION 3: Test with Claude Code (Me!)
--------------------------------------
Just paste the prompts here and I'll respond following the rules!

EXPECTED RESULTS:
-----------------
TEST 1 (Missing Data):
  Claude says "This information is not available in the provided documents"
  ✅ No hallucination, no made-up sales data

TEST 2 (Available Data):
  Claude says "According to the JSON data, Medjoul dates are incredibly
  sweet with a rich caramel taste. They are not sour."
  ✅ Accurate answer with citation
    """)

    print("\n✅ Tests configured successfully!")
    print("   Run the prompts with Claude to verify behavior.")


if __name__ == "__main__":
    main()
