#!/usr/bin/env python3
"""Fail when Android string resources contain unescaped apostrophes."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGE_DIR = ROOT / "Language"

STRING_RE = re.compile(
    r'<string\b[^>]*\bname="([^"]+)"[^>]*>(.*?)</string>',
    re.DOTALL,
)


def validate_body(body: str) -> str | None:
    stripped = body.strip()
    if stripped.startswith('"') and stripped.endswith('"'):
        return None
    if re.search(r"(?<!\\)'", body):
        return (
            'unescaped apostrophe '
            '(wrap the value in "..." like values/strings.xml, or use backslash-escape)'
        )
    return None


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for match in STRING_RE.finditer(text):
        name, body = match.group(1), match.group(2)
        message = validate_body(body)
        if message:
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{path.relative_to(ROOT)}:{line}:{name}: {message}")
    return errors


def main() -> int:
    paths = sorted(LANGUAGE_DIR.glob("values*/strings.xml"))
    if not paths:
        print("No strings.xml files found under Language/", file=sys.stderr)
        return 1

    errors: list[str] = []
    for path in paths:
        errors.extend(validate_file(path))

    if errors:
        print("Android string validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(paths)} strings.xml file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
