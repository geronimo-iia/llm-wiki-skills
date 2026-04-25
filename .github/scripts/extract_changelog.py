#!/usr/bin/env python3
"""
Extract the release notes for a given version tag from CHANGELOG.md.
Usage: extract_changelog.py v0.3.0
Prints the matching section body to stdout.
"""

import re
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: extract_changelog.py <tag>", file=sys.stderr)
    sys.exit(1)

tag = sys.argv[1].lstrip("v")
changelog = Path("CHANGELOG.md").read_text()

# Find the section for this version
pattern = rf"## \[{re.escape(tag)}\][^\n]*\n(.*?)(?=\n## \[|\Z)"
match = re.search(pattern, changelog, re.DOTALL)

if not match:
    print(f"No CHANGELOG entry found for version {tag}", file=sys.stderr)
    sys.exit(1)

print(match.group(1).strip())
