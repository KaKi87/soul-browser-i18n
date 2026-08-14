#!/usr/bin/env python3
"""Insert a translation-completion table into README.md between I18N markers."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

BEGIN_MARK = "<!-- BEGIN I18N -->"
END_MARK = "<!-- END I18N -->"
BAR_WIDTH = 20
LANGUAGE_NAME_KEY = "language_name"
BADGE_FILE = "i18n-badge.json"

RESOURCE_TAGS = {"string", "plurals", "string-array"}


def parse_resources(strings_xml: Path) -> tuple[set[str], str | None]:
    """Return translatable resource names and the locale's display label."""
    root = ET.parse(strings_xml).getroot()
    keys: set[str] = set()
    label: str | None = None
    for child in root:
        tag = child.tag.split("}")[-1]
        if tag not in RESOURCE_TAGS:
            continue
        name = child.get("name")
        if not name:
            continue
        if name == LANGUAGE_NAME_KEY:
            text = "".join(child.itertext()).strip()
            label = text or None
        if child.get("translatable") == "false":
            continue
        keys.add(name)
    return keys, label


def progress_bar(ratio: float, width: int = BAR_WIDTH) -> str:
    if ratio >= 1:
        return "█" * width
    filled = int(ratio * width)
    return "█" * filled + "░" * (width - filled)


def collect_stats(language_dir: Path) -> tuple[int, list[dict]]:
    base_dir = language_dir / "values"
    base_xml = base_dir / "strings.xml"
    if not base_xml.is_file():
        raise SystemExit(f"English base not found: {base_xml}")

    base_keys, _ = parse_resources(base_xml)
    base_total = len(base_keys)

    rows: list[dict] = []
    for folder in sorted(p for p in language_dir.iterdir() if p.is_dir() and p.name.startswith("values")):
        xml_path = folder / "strings.xml"
        if not xml_path.is_file():
            continue
        keys, label = parse_resources(xml_path)
        translated = len(base_keys & keys)
        missing = base_total - translated
        ratio = translated / base_total if base_total else 1.0
        rows.append(
            {
                "folder": folder.name,
                "name": label or folder.name,
                "translated": translated,
                "missing": missing,
                "ratio": ratio,
                "is_base": folder.name == "values",
            }
        )

    rows.sort(key=lambda row: (not row["is_base"], row["folder"]))
    return base_total, rows


def render_table(base_total: int, rows: list[dict]) -> str:
    lines = [
        "## Translation status",
        "",
        f"Completion of each language relative to the English base (`Language/values`, {base_total} keys).",
        "",
        "| Language | Directory | Translated | Missing | Completion |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        pct = 100.0 * row["ratio"]
        label = f"{row['name']} (base)" if row["is_base"] else row["name"]
        label = label.replace("|", "\\|")
        bar = progress_bar(row["ratio"])
        lines.append(
            f"| {label} | `{row['folder']}` | {row['translated']} | {row['missing']} "
            f"| `{bar}` {pct:.1f}% |"
        )
    lines.extend(
        [
            "",
            "_This table is generated automatically. Run `python3 scripts/update_i18n_table.py` to refresh it locally._",
        ]
    )
    return "\n".join(lines)


def badge_color(ratio: float) -> str:
    if ratio >= 0.99:
        return "brightgreen"
    if ratio >= 0.95:
        return "green"
    if ratio >= 0.80:
        return "yellow"
    return "red"


def render_badge(rows: list[dict]) -> str:
    locales = [row for row in rows if not row["is_base"]]
    average = sum(row["ratio"] for row in locales) / len(locales) if locales else 1.0
    payload = {
        "schemaVersion": 1,
        "label": "i18n",
        "message": f"{len(locales)} locales · {average * 100:.1f}%",
        "color": badge_color(average),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def replace_marked_section(readme: str, inner: str) -> str:
    block = f"{BEGIN_MARK}\n\n{inner}\n\n{END_MARK}"
    pattern = re.compile(
        re.escape(BEGIN_MARK) + r".*?" + re.escape(END_MARK),
        flags=re.DOTALL,
    )
    if pattern.search(readme):
        return pattern.sub(block, readme, count=1)

    if BEGIN_MARK in readme or END_MARK in readme:
        raise SystemExit(
            f"README.md must contain both {BEGIN_MARK} and {END_MARK} (or neither)."
        )

    stripped = readme.rstrip()
    separator = "\n\n" if stripped else ""
    return f"{stripped}{separator}{block}\n"


def write_if_changed(path: Path, content: str, check: bool) -> int:
    original = path.read_text(encoding="utf-8") if path.is_file() else None
    if original == content:
        print(f"{path} is already up to date.")
        return 0
    if check:
        print(f"{path} is out of date. Run python3 scripts/update_i18n_table.py")
        return 1
    path.write_text(content, encoding="utf-8")
    print(f"Updated {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root (default: parent of this script)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with status 1 if generated files would change",
    )
    args = parser.parse_args(argv)

    root: Path = args.root
    base_total, rows = collect_stats(root / "Language")
    readme_path = root / "README.md"
    original_readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
    status = write_if_changed(
        readme_path,
        replace_marked_section(original_readme, render_table(base_total, rows)),
        check=args.check,
    )
    status |= write_if_changed(root / BADGE_FILE, render_badge(rows), check=args.check)
    return 1 if status else 0


if __name__ == "__main__":
    sys.exit(main())
