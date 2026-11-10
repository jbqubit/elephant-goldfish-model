# Copyright 2026 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Check that language profiles follow contributing/language_extension.md."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = ROOT / "resources/preflight.md"
ROW = re.compile(r"^\| (.+?) \| `([^`]+)` \| \[[^\]]+\]\((languages/[^)]+\.md)\) \|$")


def registered() -> dict[str, tuple[str, str]]:
  rows = {}
  for line in PREFLIGHT.read_text(encoding="utf-8").splitlines():
    match = ROW.match(line)
    if match:
      language, pattern, path = match.groups()
      rows[path] = (language, pattern)
  return rows


def test_every_profile_is_registered_in_the_preflight() -> None:
  profiles = {f"languages/{p.name}" for p in (ROOT / "resources/languages").glob("*.md")}
  assert profiles, "no language profiles found"
  assert set(registered()) == profiles


def test_profiles_have_the_required_sections() -> None:
  for path, (language, pattern) in registered().items():
    assert pattern.startswith("*."), f"{path}: pattern must be a file glob"
    text = (ROOT / "resources" / path).read_text(encoding="utf-8")
    headings = re.findall(r"^(#{1,3}) (.+)$", text, re.M)
    assert headings[0] == ("#", f"{language} Language Profile"), path
    second = {title for level, title in headings if level == "##"}
    assert {"Recognize", "Skill Notes"} <= second, f"{path}: missing sections"
    assert "../preflight.md" in text, f"{path}: must link back to the preflight"
