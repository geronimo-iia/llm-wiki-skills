#!/usr/bin/env python3
"""
Validate all active skills and check plugin.json version matches CHANGELOG.
Exits non-zero if any check fails.
"""

import json
import re
import sys
from pathlib import Path

REQUIRED_FRONTMATTER = ["name", "description", "type", "status", "last_updated", "when_to_use"]
SKILLS_DIR = Path("skills")
PLUGIN_JSON = Path(".claude-plugin/plugin.json")
CHANGELOG = Path("CHANGELOG.md")

errors = []


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---"):
        return {}
    end = text.index("---", 3)
    block = text[3:end]
    result = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"')
    return result


# 1. Validate each skill
for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
    fm = parse_frontmatter(skill_file)
    if not fm:
        errors.append(f"{skill_file}: missing or unreadable frontmatter")
        continue
    for field in REQUIRED_FRONTMATTER:
        if field not in fm:
            errors.append(f"{skill_file}: missing required field '{field}'")
    if fm.get("status") not in ("active", "draft"):
        errors.append(f"{skill_file}: 'status' must be 'active' or 'draft', got '{fm.get('status')}'")
    if fm.get("type") != "skill":
        errors.append(f"{skill_file}: 'type' must be 'skill', got '{fm.get('type')}'")


# 2. Check plugin.json version matches latest CHANGELOG entry
plugin_version = json.loads(PLUGIN_JSON.read_text()).get("version", "")
changelog_text = CHANGELOG.read_text()
match = re.search(r"## \[(\d+\.\d+\.\d+)\]", changelog_text)
if match:
    changelog_version = match.group(1)
    if plugin_version != changelog_version:
        errors.append(
            f"plugin.json version '{plugin_version}' does not match "
            f"latest CHANGELOG entry '[{changelog_version}]'"
        )
else:
    errors.append("CHANGELOG.md: no version entry found (expected '## [x.y.z]')")


# Report
if errors:
    print("Validation failed:")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)

skill_count = len(list(SKILLS_DIR.glob("*/SKILL.md")))
print(f"✓ {skill_count} skills valid, plugin.json {plugin_version} matches CHANGELOG")
