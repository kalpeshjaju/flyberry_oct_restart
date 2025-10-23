#!/usr/bin/env python3
"""
Flyberry Data Loader - Simple and Solid

Purpose: Load all Flyberry data for brand package generation
Approach: Keep it simple - no databases, no complexity
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any


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
        self._products = None
        self._recipes = None
        self._design = None
        self._claims = None

        # Validate directory exists
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

    def load_all(self) -> Dict[str, Any]:
        """
        Load everything into memory

        Returns:
            Dictionary with products, recipes, design, claims

        Example:
            >>> data = FlyberryData()
            >>> all_data = data.load_all()
            >>> print(f"Loaded {len(all_data['products'])} products")
        """
        return {
            "products": self.products,
            "recipes": self.recipes,
            "design": self.design,
            "claims": self.claims
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
            file = Path("input_raw_data_recreate/input_data_marked_down/claims-registry.json")
            if not file.exists():
                # Fallback if structure changes
                print("Warning: claims-registry.json not found, returning empty dict")
                return {}
            self._claims = json.loads(file.read_text())
        return self._claims

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

    def get_product(self, product_id: str) -> Optional[Dict]:
        """
        Get specific product by ID

        Args:
            product_id: Product identifier (e.g., "medjoul-dates")

        Returns:
            Product dictionary or None if not found

        Example:
            >>> data = FlyberryData()
            >>> medjoul = data.get_product("medjoul-dates")
            >>> print(medjoul["tagline"])
        """
        return next(
            (p for p in self.products if p["productId"] == product_id),
            None
        )

    def get_recipe(self, recipe_id: str) -> Optional[Dict]:
        """
        Get specific recipe by ID

        Args:
            recipe_id: Recipe identifier (e.g., "natural-caramel")

        Returns:
            Recipe dictionary or None if not found
        """
        return next(
            (r for r in self.recipes if r["recipeId"] == recipe_id),
            None
        )

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
