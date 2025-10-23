#!/usr/bin/env python3
"""
Flyberry Brand Package - Build System

Converts Markdown content files → HTML using templates + styling
"""

from pathlib import Path
import markdown
from jinja2 import Template
from datetime import datetime
from typing import List, Tuple


def build_act(act_number: int, act_title: str, output_dir: str = "output") -> Path:
    """
    Convert Act Markdown files to single HTML document

    Args:
        act_number: Act number (1-6)
        act_title: Human-readable title (e.g., "Who We Are")
        output_dir: Where to write output HTML

    Returns:
        Path to generated HTML file
    """
    print(f"\n🔨 Building Act {act_number}: {act_title}")

    # 1. Read all Markdown sections from content/act-{N}/
    content_dir = Path(f"content/act-{act_number}")

    if not content_dir.exists():
        raise FileNotFoundError(f"Content directory not found: {content_dir}")

    md_files = sorted(content_dir.glob("*.md"))

    if not md_files:
        raise FileNotFoundError(f"No Markdown files found in {content_dir}")

    print(f"   Found {len(md_files)} Markdown files")

    # 2. Convert each Markdown file to HTML
    sections_html = []

    for md_file in md_files:
        print(f"   • Converting {md_file.name}")
        md_content = md_file.read_text(encoding='utf-8')

        # Convert Markdown to HTML with extensions
        html_content = markdown.markdown(
            md_content,
            extensions=[
                'tables',           # GitHub-style tables
                'fenced_code',      # ```code blocks```
                'nl2br',            # Newlines → <br>
                'sane_lists',       # Better list handling
                'smarty'            # Smart quotes/dashes
            ]
        )

        sections_html.append(html_content)

    # 3. Load template
    template_path = Path("templates/act-template.html")

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    template = Template(template_path.read_text(encoding='utf-8'))

    # 4. Render template with all sections combined
    full_html = template.render(
        act_number=act_number,
        act_title=act_title,
        content="\n".join(sections_html),
        generation_date=datetime.now().strftime("%Y-%m-%d")
    )

    # 5. Write output
    output_filename = f"act-{act_number}-{act_title.lower().replace(' ', '-')}.html"
    output_path = Path(output_dir) / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_html, encoding='utf-8')

    print(f"   ✅ Built: {output_path}")
    print(f"   📄 Total sections: {len(sections_html)}")

    return output_path


def build_all_acts(acts: List[Tuple[int, str]]) -> List[Path]:
    """
    Build multiple Acts at once

    Args:
        acts: List of (act_number, act_title) tuples

    Returns:
        List of generated HTML file paths
    """
    generated_files = []

    print("=" * 60)
    print("🏗️  FLYBERRY BRAND PACKAGE - BUILD SYSTEM")
    print("=" * 60)

    for act_number, act_title in acts:
        try:
            output_file = build_act(act_number, act_title)
            generated_files.append(output_file)
        except Exception as e:
            print(f"   ❌ Error building Act {act_number}: {e}")

    print("\n" + "=" * 60)
    print(f"✅ BUILD COMPLETE - {len(generated_files)} Acts generated")
    print("=" * 60)

    return generated_files


if __name__ == "__main__":
    # Build Act 1 only (for now)
    acts_to_build = [
        (1, "Who We Are"),
        # (2, "Where We Are Today"),
        # (3, "What We Discovered"),
        # (4, "Market Proof"),
        # (5, "Where We Should Go"),
        # (6, "Operating Plan"),
    ]

    try:
        generated = build_all_acts(acts_to_build)

        print("\n📂 Generated Files:")
        for file_path in generated:
            print(f"   • {file_path}")

        print("\n💡 To view:")
        print(f"   open {generated[0]}")

    except Exception as e:
        print(f"\n❌ BUILD FAILED: {e}")
        exit(1)
