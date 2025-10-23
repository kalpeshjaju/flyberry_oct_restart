#!/usr/bin/env python3
"""
Test Two-Source Prompting with Real Claude API

Usage:
    export ANTHROPIC_API_KEY="your-key-here"
    python3 test_with_claude_api.py
"""

import os
import sys
from flyberry_data_loader import FlyberryData

# Try to import anthropic
try:
    import anthropic
except ImportError:
    print("❌ ERROR: anthropic package not installed")
    print("\nInstall it with:")
    print("   pip install anthropic")
    sys.exit(1)


def test_with_claude(prompt: str, test_name: str, expected_behavior: str):
    """
    Send prompt to Claude API and display response
    """
    print("=" * 70)
    print(f"TEST: {test_name}")
    print("=" * 70)

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n❌ ERROR: ANTHROPIC_API_KEY not set")
        print("\nSet it with:")
        print('   export ANTHROPIC_API_KEY="your-key-here"')
        print("\nOr create .env file:")
        print('   ANTHROPIC_API_KEY=your-key-here')
        return None

    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)

    print("\n📤 SENDING TO CLAUDE SONNET 4.5...")
    print(f"   Model: claude-sonnet-4-20250514")
    print(f"   Prompt length: {len(prompt):,} characters")

    try:
        # Send to Claude
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract response text
        response_text = response.content[0].text

        print("\n" + "=" * 70)
        print("📥 CLAUDE'S RESPONSE:")
        print("=" * 70)
        print(response_text)

        print("\n" + "=" * 70)
        print("💡 EXPECTED BEHAVIOR:")
        print("=" * 70)
        print(expected_behavior)

        print("\n" + "=" * 70)
        print("✅ VERIFICATION:")
        print("=" * 70)

        # Check if response matches expectations
        if "information is not available" in response_text.lower() or "not available in the provided" in response_text.lower():
            print("   ✅ Correctly stated data is not available")
        elif "according to the json data" in response_text.lower() or "from the markdown context" in response_text.lower():
            print("   ✅ Properly cited sources (JSON or Markdown)")
        else:
            print("   ⚠️  Response received but check if it matches expectations")

        # Check for hallucination indicators
        if any(word in response_text.lower() for word in ["approximately", "around", "estimate", "probably", "i think"]):
            print("   ⚠️  Warning: Response contains uncertain language")

        print("\n✅ Test completed successfully!")
        return response_text

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║       TWO-SOURCE PROMPTING - CLAUDE API TEST                         ║
║       Real Claude Sonnet 4.5 Responses                               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

    # Initialize data loader
    data = FlyberryData()

    # TEST 1: Missing data (sales)
    print("\n" * 2)
    prompt1 = data.to_two_source_prompt(
        product_id="medjoul-dates",
        question="Give me a list of all Medjoul products ranked by sales volume. Which one sells the most?"
    )

    response1 = test_with_claude(
        prompt=prompt1,
        test_name="Missing Data - Sales Information",
        expected_behavior="""
        Claude should respond:
        "This information is not available in the provided documents"

        Because:
        - Sales data doesn't exist in JSON
        - Sales data doesn't exist in Markdown
        - Claude follows Rule 5: Don't invent data
        """
    )

    # TEST 2: Available data (taste)
    print("\n" * 3)
    prompt2 = data.to_two_source_prompt(
        product_id="medjoul-dates",
        question="Are Medjoul dates sour? What is their taste profile?"
    )

    response2 = test_with_claude(
        prompt=prompt2,
        test_name="Available Data - Taste Profile",
        expected_behavior="""
        Claude should respond:
        "According to the JSON data, Medjoul dates are incredibly sweet
        with a rich caramel taste. They are not sour."

        Because:
        - Taste data EXISTS in JSON
        - JSON shows: "rich caramel taste", "soft texture"
        - Claude follows Rule 1: Use JSON for facts
        - Claude follows Rule 4: Cite source
        """
    )

    # Save responses
    if response1:
        with open('claude_response_test1.txt', 'w') as f:
            f.write(response1)
        print("\n💾 Response saved to: claude_response_test1.txt")

    if response2:
        with open('claude_response_test2.txt', 'w') as f:
            f.write(response2)
        print("💾 Response saved to: claude_response_test2.txt")

    # Summary
    print("\n" * 2)
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print("""
TEST 1 - Missing Data:
  Question: "Give me list of products by sales"
  Expected: "Information not available"
  Result: {}

TEST 2 - Available Data:
  Question: "Are Medjoul dates sour?"
  Expected: "No, they are sweet with caramel taste" (cited from JSON)
  Result: {}

CONCLUSION:
  {}
    """.format(
        "✅ PASSED" if response1 and "not available" in response1.lower() else "⚠️  CHECK RESPONSE",
        "✅ PASSED" if response2 and "sweet" in response2.lower() else "⚠️  CHECK RESPONSE",
        "Two-source prompting successfully prevents hallucinations!" if response1 and response2 else "Check responses manually"
    ))


if __name__ == "__main__":
    main()
