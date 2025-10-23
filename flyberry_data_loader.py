#!/usr/bin/env python3
"""
Flyberry Data Loader - Enhanced with Source Verification

Purpose: Load all Flyberry data for brand package generation
Features:
- JSON data loading (fast)
- Markdown source loading (context)
- Data lineage tracking (verification)
- Cross-reference verification (trust)

Approach: Keep it simple - no databases, no complexity
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import re


class FlyberryData:
    """
    Simple data loader for Flyberry Gourmet product data

    No databases needed - just loads JSON files into memory.
    Fast enough for brand package generation (160KB loads in <1 second).
    """

    def __init__(self, data_dir: str = "extracted_data"):
        """
        Initialize the data loader

        Args:
            data_dir: Path to extracted_data directory
        """
        self.data_dir = Path(data_dir)
        self.root_dir = Path(".")  # Project root

        # Data caches (lazy loaded)
        self._products = None
        self._recipes = None
        self._design = None
        self._claims = None
        self._customer_segments = None
        self._customer_insights = None
        self._origin_stories = None
        self._use_cases = None
        self._founder_story = None

        # NEW: Lineage and source tracking
        self._lineage = None
        self._markdown_cache = {}  # Cache markdown content to avoid re-reading

        # Validate directory exists
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

    def load_all(self) -> Dict[str, Any]:
        """
        Load everything into memory

        Returns:
            Dictionary with products, recipes, design, claims, customer intelligence, and brand story

        Example:
            >>> data = FlyberryData()
            >>> all_data = data.load_all()
            >>> print(f"Loaded {len(all_data['products'])} products")
            >>> print(f"Loaded {len(all_data['customer_segments'])} customer segments")
        """
        return {
            "products": self.products,
            "recipes": self.recipes,
            "design": self.design,
            "claims": self.claims,
            "customer_segments": self.customer_segments,
            "customer_insights": self.customer_insights,
            "origin_stories": self.origin_stories,
            "use_cases": self.use_cases,
            "founder_story": self.founder_story
        }

    @property
    def products(self) -> List[Dict]:
        """Get all products (lazy loaded)"""
        if self._products is None:
            self._products = self._load_json_files("products")
        return self._products

    @property
    def recipes(self) -> List[Dict]:
        """Get all recipes (lazy loaded)"""
        if self._recipes is None:
            self._recipes = self._load_json_files("recipes")
        return self._recipes

    @property
    def design(self) -> Dict:
        """Get brand design system (lazy loaded)"""
        if self._design is None:
            file = self.data_dir / "design/brand-design-system.json"
            self._design = json.loads(file.read_text())
        return self._design

    @property
    def claims(self) -> Dict:
        """Get health claims registry (lazy loaded)"""
        if self._claims is None:
            # Look in extracted_data/claims-registry.json
            file = self.data_dir / "claims-registry.json"
            if not file.exists():
                print("Warning: claims-registry.json not found, returning empty dict")
                return {}
            self._claims = json.loads(file.read_text())
        return self._claims

    @property
    def customer_segments(self) -> Dict:
        """Get customer segment analysis (lazy loaded)"""
        if self._customer_segments is None:
            file = self.data_dir / "customer-segments.json"
            if not file.exists():
                print("Warning: customer-segments.json not found, returning empty dict")
                return {}
            self._customer_segments = json.loads(file.read_text())
        return self._customer_segments

    @property
    def customer_insights(self) -> Dict:
        """Get customer insights from 261+ reviews (lazy loaded)"""
        if self._customer_insights is None:
            file = self.data_dir / "customer-insights.json"
            if not file.exists():
                print("Warning: customer-insights.json not found, returning empty dict")
                return {}
            self._customer_insights = json.loads(file.read_text())
        return self._customer_insights

    @property
    def origin_stories(self) -> Dict:
        """Get product origin stories with terroir data (lazy loaded)"""
        if self._origin_stories is None:
            file = self.data_dir / "origin-stories.json"
            if not file.exists():
                print("Warning: origin-stories.json not found, returning empty dict")
                return {}
            self._origin_stories = json.loads(file.read_text())
        return self._origin_stories

    @property
    def use_cases(self) -> Dict:
        """Get customer use cases - Who Chooses + The Moment + Why It Works (lazy loaded)"""
        if self._use_cases is None:
            file = self.data_dir / "use-cases.json"
            if not file.exists():
                print("Warning: use-cases.json not found, returning empty dict")
                return {}
            self._use_cases = json.loads(file.read_text())
        return self._use_cases

    @property
    def founder_story(self) -> Dict:
        """Get founder journey and company evolution (lazy loaded)"""
        if self._founder_story is None:
            file = self.data_dir / "founder-story.json"
            if not file.exists():
                print("Warning: founder-story.json not found, returning empty dict")
                return {}
            self._founder_story = json.loads(file.read_text())
        return self._founder_story

    def _load_json_files(self, subdir: str) -> List[Dict]:
        """
        Load all JSON files from a subdirectory

        Args:
            subdir: Subdirectory name (products, recipes, etc.)

        Returns:
            List of parsed JSON objects
        """
        files = (self.data_dir / subdir).glob("*.json")
        return [
            json.loads(f.read_text())
            for f in files
            if f.name != "index.json"  # Skip index files
        ]

    def get_product(self, product_id: str, include_sources: bool = False) -> Optional[Dict]:
        """
        Get specific product by ID, optionally with source verification

        Args:
            product_id: Product identifier (e.g., "medjoul-dates")
            include_sources: If True, adds source lineage and markdown context

        Returns:
            Product dictionary or None if not found

        Example:
            >>> data = FlyberryData()
            >>> # Fast: Just get the data
            >>> medjoul = data.get_product("medjoul-dates")
            >>> print(medjoul["tagline"])
            >>>
            >>> # With sources: Get data + verification context
            >>> medjoul_full = data.get_product("medjoul-dates", include_sources=True)
            >>> print(medjoul_full["_sources"])  # Source files
            >>> print(medjoul_full["_markdown_context"])  # Full source text
        """
        product = next(
            (p for p in self.products if p["productId"] == product_id),
            None
        )

        if product and include_sources:
            # Add source lineage and markdown context
            lineage_key = f"products/{product_id}.json"
            lineage = self._get_lineage(lineage_key)

            if lineage:
                product = product.copy()  # Don't modify original
                product["_sources"] = {
                    "markdown": lineage.get("sourceMarkdown"),
                    "raw": lineage.get("sourceRaw"),
                    "extractionMethod": lineage.get("extractionMethod"),
                    "confidence": lineage.get("confidence"),
                    "lastVerified": lineage.get("lastVerified")
                }

                # Load markdown context
                md_path = lineage.get("sourceMarkdown")
                if md_path:
                    product["_markdown_context"] = self._load_markdown(md_path)

        return product

    def get_recipe(self, recipe_id: str, include_sources: bool = False) -> Optional[Dict]:
        """
        Get specific recipe by ID, optionally with source verification

        Args:
            recipe_id: Recipe identifier (e.g., "natural-caramel")
            include_sources: If True, adds source lineage and markdown context

        Returns:
            Recipe dictionary or None if not found
        """
        recipe = next(
            (r for r in self.recipes if r["recipeId"] == recipe_id),
            None
        )

        if recipe and include_sources:
            # Add source lineage and markdown context
            lineage_key = f"recipes/{recipe_id}.json"
            lineage = self._get_lineage(lineage_key)

            if lineage:
                recipe = recipe.copy()  # Don't modify original
                recipe["_sources"] = {
                    "markdown": lineage.get("sourceMarkdown"),
                    "raw": lineage.get("sourceRaw"),
                    "extractionMethod": lineage.get("extractionMethod"),
                    "confidence": lineage.get("confidence"),
                    "lastVerified": lineage.get("lastVerified")
                }

                # Load markdown context
                md_path = lineage.get("sourceMarkdown")
                if md_path:
                    recipe["_markdown_context"] = self._load_markdown(md_path)

        return recipe

    def find_products_by(self, **filters) -> List[Dict]:
        """
        Simple filtering (good enough for 13 products)

        Args:
            **filters: Key-value pairs to filter by
                      Supports nested keys with dot notation (e.g., "packaging.color")

        Returns:
            List of matching products

        Examples:
            >>> data = FlyberryData()
            >>> # Find by origin
            >>> saudi_products = data.find_products_by(origin="Imported Product of Saudi Arabia")
            >>> # Find by color
            >>> pink_products = data.find_products_by(**{"packaging.color": "#fd478e"})
        """
        results = self.products
        for key, value in filters.items():
            if "." in key:  # Nested key: "packaging.color"
                results = [p for p in results if self._get_nested(p, key) == value]
            else:
                results = [p for p in results if p.get(key) == value]
        return results

    def find_recipes_by(self, **filters) -> List[Dict]:
        """
        Simple recipe filtering

        Args:
            **filters: Key-value pairs to filter by

        Returns:
            List of matching recipes

        Example:
            >>> data = FlyberryData()
            >>> easy_recipes = data.find_recipes_by(difficulty="Easy")
        """
        results = self.recipes
        for key, value in filters.items():
            results = [r for r in results if r.get(key) == value]
        return results

    def _get_nested(self, obj: Dict, path: str) -> Any:
        """
        Get nested value using dot notation

        Args:
            obj: Dictionary to search
            path: Dot-separated path (e.g., "packaging.color")

        Returns:
            Value at path or empty dict if not found
        """
        for key in path.split("."):
            obj = obj.get(key, {})
        return obj

    def get_products_with_claim(self, claim_id: str) -> List[str]:
        """
        Get all products that make a specific claim

        Args:
            claim_id: Claim identifier (e.g., "CLAIM-001")

        Returns:
            List of product IDs

        Example:
            >>> data = FlyberryData()
            >>> fiber_products = data.get_products_with_claim("CLAIM-001")
        """
        if not self.claims:
            return []

        # Search through productClaimIndex
        product_claim_index = self.claims.get("productClaimIndex", {})
        return [
            product_id
            for product_id, claims in product_claim_index.items()
            if claim_id in claims
        ]

    # ========== NEW: Lineage and Markdown Loading Methods ==========

    def _get_lineage(self, file_key: str) -> Dict:
        """
        Get source lineage for a data file

        Args:
            file_key: Key in lineage map (e.g., "products/medjoul-dates.json")

        Returns:
            Lineage dictionary with sourceMarkdown, sourceRaw, etc.
        """
        if self._lineage is None:
            lineage_file = self.root_dir / "data-lineage.json"
            if not lineage_file.exists():
                print(f"Warning: data-lineage.json not found at {lineage_file}")
                return {}
            self._lineage = json.loads(lineage_file.read_text())

        return self._lineage.get(file_key, {})

    def _load_markdown(self, path: Union[str, List[str]]) -> Union[str, List[str], None]:
        """
        Load markdown file(s) content

        Args:
            path: Path to markdown file, or list of paths

        Returns:
            Markdown content as string, or list of strings, or None if not found
        """
        # Handle list of paths
        if isinstance(path, list):
            return [self._load_markdown(p) for p in path]

        # Handle single path
        if path in self._markdown_cache:
            return self._markdown_cache[path]

        md_path = self.root_dir / path
        if not md_path.exists():
            print(f"Warning: Markdown file not found: {path}")
            return None

        content = md_path.read_text(encoding='utf-8')
        self._markdown_cache[path] = content
        return content

    # ========== NEW: Verification Methods ==========

    def verify_product(self, product_id: str) -> Dict[str, Any]:
        """
        Verify product data against source markdown

        Args:
            product_id: Product identifier

        Returns:
            Verification report with matches, discrepancies, and confidence score

        Example:
            >>> data = FlyberryData()
            >>> report = data.verify_product("medjoul-dates")
            >>> print(f"Confidence: {report['confidence']}")
            >>> print(f"Verified fields: {report['matches']}")
        """
        product = self.get_product(product_id)
        if not product:
            return {"error": f"Product {product_id} not found"}

        lineage_key = f"products/{product_id}.json"
        lineage = self._get_lineage(lineage_key)

        if not lineage or not lineage.get("sourceMarkdown"):
            return {
                "error": "No source markdown found in lineage",
                "confidence": 0.0
            }

        # Load markdown source
        md_content = self._load_markdown(lineage["sourceMarkdown"])
        if not md_content:
            return {
                "error": f"Could not load markdown: {lineage['sourceMarkdown']}",
                "confidence": 0.0
            }

        # Verify key fields
        matches = []
        discrepancies = []

        # Check product name
        if product.get("name") and product["name"] in md_content:
            matches.append("name")
        else:
            discrepancies.append(f"name: '{product.get('name')}' not found in source")

        # Check origin
        if product.get("origin") and product["origin"] in md_content:
            matches.append("origin")
        else:
            discrepancies.append(f"origin: '{product.get('origin')}' not found in source")

        # Check tagline
        if product.get("tagline"):
            # Fuzzy match - check if key words from tagline appear
            tagline_words = set(re.findall(r'\w+', product["tagline"].lower()))
            md_words = set(re.findall(r'\w+', md_content.lower()))
            overlap = len(tagline_words & md_words) / len(tagline_words) if tagline_words else 0
            if overlap > 0.5:  # 50% overlap
                matches.append("tagline")
            else:
                discrepancies.append(f"tagline: Low overlap with source ({overlap:.0%})")

        # Calculate confidence
        total_checks = len(matches) + len(discrepancies)
        confidence = len(matches) / total_checks if total_checks > 0 else 0.0

        return {
            "productId": product_id,
            "matches": matches,
            "discrepancies": discrepancies,
            "confidence": round(confidence, 2),
            "sourcesChecked": 1,
            "sourceFile": lineage["sourceMarkdown"]
        }

    def verify_recipe(self, recipe_id: str) -> Dict[str, Any]:
        """
        Verify recipe data against source markdown

        Args:
            recipe_id: Recipe identifier

        Returns:
            Verification report with matches, discrepancies, and confidence score
        """
        recipe = self.get_recipe(recipe_id)
        if not recipe:
            return {"error": f"Recipe {recipe_id} not found"}

        lineage_key = f"recipes/{recipe_id}.json"
        lineage = self._get_lineage(lineage_key)

        if not lineage or not lineage.get("sourceMarkdown"):
            return {
                "error": "No source markdown found in lineage",
                "confidence": 0.0
            }

        # Load markdown source
        md_content = self._load_markdown(lineage["sourceMarkdown"])
        if not md_content:
            return {
                "error": f"Could not load markdown: {lineage['sourceMarkdown']}",
                "confidence": 0.0
            }

        # Verify key fields
        matches = []
        discrepancies = []

        # Check recipe name
        if recipe.get("name") and recipe["name"] in md_content:
            matches.append("name")
        else:
            discrepancies.append(f"name: '{recipe.get('name')}' not found in source")

        # Check difficulty
        if recipe.get("difficulty") and recipe["difficulty"] in md_content:
            matches.append("difficulty")

        # Calculate confidence
        total_checks = len(matches) + len(discrepancies)
        confidence = len(matches) / total_checks if total_checks > 0 else 0.0

        return {
            "recipeId": recipe_id,
            "matches": matches,
            "discrepancies": discrepancies,
            "confidence": round(confidence, 2),
            "sourcesChecked": 1,
            "sourceFile": lineage["sourceMarkdown"]
        }

    def get_lineage_summary(self) -> Dict[str, Any]:
        """
        Get summary of all data lineage

        Returns:
            Summary with counts of sources, markdown files, and confidence levels
        """
        if self._lineage is None:
            self._get_lineage("dummy")  # Load lineage

        if not self._lineage:
            return {"error": "No lineage data available"}

        total_files = len(self._lineage) - 1  # Exclude metadata
        high_confidence = sum(1 for v in self._lineage.values()
                              if isinstance(v, dict) and v.get("confidence") == "high")

        markdown_sources = set()
        raw_sources = set()

        for key, value in self._lineage.items():
            if key == "metadata" or not isinstance(value, dict):
                continue

            md = value.get("sourceMarkdown")
            if md:
                if isinstance(md, list):
                    markdown_sources.update(md)
                else:
                    markdown_sources.add(md)

            raw = value.get("sourceRaw")
            if raw:
                if isinstance(raw, list):
                    raw_sources.update(raw)
                else:
                    raw_sources.add(raw)

        return {
            "totalDataFiles": total_files,
            "highConfidence": high_confidence,
            "uniqueMarkdownSources": len(markdown_sources),
            "uniqueRawSources": len(raw_sources),
            "confidenceRate": round(high_confidence / total_files, 2) if total_files > 0 else 0.0
        }

    # ========== NEW: Two-Source Prompting for Claude ==========

    def to_two_source_prompt(
        self,
        product_id: Optional[str] = None,
        recipe_id: Optional[str] = None,
        question: str = "[Your question here]",
        model: str = "claude-sonnet-4-20250514"
    ) -> str:
        """
        Create a two-source prompt (JSON + Markdown) for Claude to prevent hallucinations

        Strategy:
        - JSON = Source of truth (facts: names, numbers, claims)
        - Markdown = Context (narrative, descriptions, stories)
        - Explicit rules to prevent hallucination

        Args:
            product_id: Product identifier (e.g., "medjoul-dates")
            recipe_id: Recipe identifier (e.g., "natural-caramel")
            question: The question to ask Claude
            model: Claude model to use (default: Sonnet 4.5)

        Returns:
            Formatted prompt string ready for Claude API

        Example:
            >>> data = FlyberryData()
            >>> prompt = data.to_two_source_prompt(
            ...     product_id="medjoul-dates",
            ...     question="What is the origin and nutritional profile?"
            ... )
            >>> # Send prompt to Claude API
        """
        # Determine what data to load
        if product_id:
            item = self.get_product(product_id, include_sources=True)
            item_type = "Product"
            item_id = product_id
        elif recipe_id:
            item = self.get_recipe(recipe_id, include_sources=True)
            item_type = "Recipe"
            item_id = recipe_id
        else:
            raise ValueError("Must provide either product_id or recipe_id")

        if not item:
            raise ValueError(f"{item_type} '{item_id}' not found")

        # Extract markdown context (if available)
        markdown_context = item.get("_markdown_context", "No markdown context available")

        # Remove internal fields from JSON for cleaner output
        json_data = {k: v for k, v in item.items() if not k.startswith("_")}

        # Build the two-source prompt
        prompt = f"""You are a highly precise AI assistant powered by {model}.

**MANDATORY RULES - YOU MUST FOLLOW THESE:**
1. The <json_data> section is the ABSOLUTE SOURCE OF TRUTH for all factual information
   - Names, numbers, claims, specifications, origins, dates = Use JSON ONLY
2. The <markdown_context> section provides narrative, descriptions, and storytelling context
   - Use for understanding tone, style, positioning, and background
3. If there is ANY conflict between JSON and Markdown: JSON wins, always
4. ALWAYS cite your source when answering:
   - "According to the JSON data, ..."
   - "From the markdown context, ..."
   - "The JSON shows X, while the markdown describes Y..."
5. If you cannot find the answer in the provided data, you MUST respond:
   - "This information is not available in the provided documents"
   - DO NOT invent, infer, or guess answers

<json_data>
{json.dumps(json_data, indent=2, ensure_ascii=False)}
</json_data>

<markdown_context>
{markdown_context[:5000]}{"..." if len(markdown_context) > 5000 else ""}
</markdown_context>

Now, answer the following question using ONLY the information provided above:

**Question:** {question}

**Answer:**"""

        return prompt

    # ========== END: Two-Source Prompting ==========

    def to_llm_context(self) -> str:
        """
        Format all data for LLM context

        Returns:
            JSON string formatted for LLM consumption

        Example:
            >>> data = FlyberryData()
            >>> context = data.to_llm_context()
            >>> # Send to Claude/GPT
        """
        all_data = self.load_all()
        return json.dumps(all_data, indent=2)


# Example usage
if __name__ == "__main__":
    # Load data
    print("Loading Flyberry data...")
    data = FlyberryData()

    # Load everything
    all_data = data.load_all()
    print(f"✅ Loaded {len(all_data['products'])} products")
    print(f"✅ Loaded {len(all_data['recipes'])} recipes")
    print(f"✅ Loaded design system with {len(all_data['design']['colorPalettes'])} color palettes")
    print(f"✅ Loaded {all_data['claims']['claimsRegistry']['totalClaims']} health claims")

    # Example queries
    print("\n--- Example Queries ---")

    # Get specific product
    medjoul = data.get_product("medjoul-dates")
    print(f"Medjoul tagline: {medjoul['tagline']}")

    # Find products by origin
    saudi_products = data.find_products_by(origin="Imported Product of Saudi Arabia")
    print(f"Products from Saudi Arabia: {[p['name'] for p in saudi_products]}")

    # Find easy recipes
    easy_recipes = data.find_recipes_by(difficulty="Easy")
    print(f"Easy recipes: {[r['name'] for r in easy_recipes]}")

    # Get products with high fiber claim
    fiber_products = data.get_products_with_claim("CLAIM-001")
    print(f"Products with excellent fiber: {fiber_products}")

    print("\n✅ Data loader working perfectly!")
    print(f"💡 Use data.to_llm_context() to send to LLM")
