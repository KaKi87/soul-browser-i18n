from pathlib import Path
import sys
import xml.etree.ElementTree as ET


# Uses only Python's standard library.
# Created by AR Rahman

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
LANGUAGES_DIR = ROOT_DIR / "Language"

ORIGINAL_LANGUAGE = "values"


def find_strings_file(folder: Path) -> Path | None:
    """Return strings.xml inside the given language folder."""
    file_path = folder / "strings.xml"
    return file_path if file_path.is_file() else None


def load_strings(file_path: Path) -> dict[str, str]:
    """Load strings.xml and return a dictionary of key -> value."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    strings: dict[str, str] = {}

    for string in root.findall("string"):
        key = string.get("name")

        if not key:
            continue

        # itertext() supports strings containing nested XML markup.
        value = "".join(string.itertext()).strip()
        strings[key] = value

    return strings


def compare_strings(
    original_language: str,
    translated_language: str,
) -> bool:
    """
    Compare a translated strings.xml against the original.

    Returns True when translation is 100% complete.
    """
    original_folder = LANGUAGES_DIR / original_language
    translated_folder = LANGUAGES_DIR / translated_language

    original_file = find_strings_file(original_folder)
    translated_file = find_strings_file(translated_folder)

    if not original_file:
        print(f"❌ No strings.xml found in: {original_folder}")
        return False

    if not translated_file:
        print(f"❌ No strings.xml found in: {translated_folder}")
        return False

    try:
        original = load_strings(original_file)
    except ET.ParseError as error:
        print(f"❌ Invalid XML: {original_file}")
        print(f"   {error}")
        return False

    try:
        translated = load_strings(translated_file)
    except ET.ParseError as error:
        print(f"❌ Invalid XML: {translated_file}")
        print(f"   {error}")
        return False

    missing_keys = [
        key
        for key in original
        if key not in translated
    ]

    empty_keys = [
        key
        for key in original
        if key in translated and not translated[key].strip()
    ]

    # Optional but useful:
    # detect keys in translation that don't exist in original.
    extra_keys = [
        key
        for key in translated
        if key not in original
    ]

    total = len(original)
    translated_count = total - len(missing_keys) - len(empty_keys)

    percent = (
        (translated_count / total) * 100
        if total > 0
        else 100.0
    )

    language_code = translated_language.removeprefix("values-")

    print()
    print("=" * 60)
    print(f"🌐 Language: {language_code}")
    print("=" * 60)
    print(f"Original:   {original_file}")
    print(f"Translated: {translated_file}")
    print()

    print(f"Total strings:          {total}")
    print(f"Translated strings:     {translated_count}")
    print(f"Missing translations:   {len(missing_keys)}")
    print(f"Empty translations:     {len(empty_keys)}")
    print(f"Extra translations:     {len(extra_keys)}")
    print(f"Translation completion: {percent:.2f}%")
    print()

    if missing_keys:
        print("❌ Missing keys:")
        for key in missing_keys:
            print(f"  - {key}")

    if empty_keys:
        print()
        print("⚠️ Empty translations:")
        for key in empty_keys:
            print(f"  - {key}")

    if extra_keys:
        print()
        print("⚠️ Extra keys not found in original:")
        for key in extra_keys:
            print(f"  - {key}")

    complete = not missing_keys and not empty_keys

    if complete:
        print("✅ All keys are translated. 100% complete.")

    return complete


def get_available_languages() -> list[str]:
    """Return available translated language folders."""
    if not LANGUAGES_DIR.is_dir():
        return []

    languages: list[str] = []

    for folder in LANGUAGES_DIR.iterdir():
        if not folder.is_dir():
            continue

        if folder.name == ORIGINAL_LANGUAGE:
            continue

        if not folder.name.startswith("values-"):
            continue

        if find_strings_file(folder):
            languages.append(folder.name)

    return sorted(languages)


def print_available_languages() -> None:
    """Print all available translation languages."""
    languages = get_available_languages()

    print("Available languages:")
    print()

    if not languages:
        print("  No translation folders found.")
        return

    for folder_name in languages:
        language_code = folder_name.removeprefix("values-")
        print(
            f"  --{language_code:<12} "
            f"→ Language/{folder_name}/strings.xml"
        )


def test_all_languages() -> bool:
    """Test all translation folders."""
    languages = get_available_languages()

    if not languages:
        print("❌ No translated languages found.")
        return False

    results: list[tuple[str, bool]] = []

    for language in languages:
        result = compare_strings(
            original_language=ORIGINAL_LANGUAGE,
            translated_language=language,
        )

        results.append((language, result))

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = 0

    for language, success in results:
        language_code = language.removeprefix("values-")

        if success:
            status = "✅ 100%"
            passed += 1
        else:
            status = "❌ Incomplete"

        print(f"{language_code:<15} {status}")

    print()
    print(f"Completed: {passed}/{len(results)}")

    return passed == len(results)


def normalize_language_argument(argument: str) -> str:
    """
    Convert command line option into Android values folder.

    Examples:
        --bn       -> values-bn
        --fr       -> values-fr
        --pt-rBR   -> values-pt-rBR
        --zh-rCN   -> values-zh-rCN
    """
    language = argument.removeprefix("--").strip()

    if language.startswith("values-"):
        return language

    return f"values-{language}"


def print_usage() -> None:
    """Print command usage."""
    print("Translation Coverage Checker")
    print()
    print("Usage:")
    print("  python test_covarage.py --bn")
    print("  python test_covarage.py --fr")
    print("  python test_covarage.py --de")
    print("  python test_covarage.py --all")
    print("  python test_covarage.py --list")
    print()
    print_available_languages()


def main() -> int:
    if not LANGUAGES_DIR.is_dir():
        print(f"❌ Language directory not found:")
        print(f"   {LANGUAGES_DIR}")
        return 1

    if len(sys.argv) < 2:
        print_usage()
        return 1

    argument = sys.argv[1].strip()

    if argument in {"--help", "-h"}:
        print_usage()
        return 0

    if argument == "--list":
        print_available_languages()
        return 0

    if argument == "--all":
        success = test_all_languages()
        return 0 if success else 1

    if not argument.startswith("--"):
        print(f"❌ Invalid argument: {argument}")
        print()
        print("Use a language option such as:")
        print("  python test_covarage.py --bn")
        return 1

    translated_language = normalize_language_argument(argument)

    translated_folder = LANGUAGES_DIR / translated_language

    if not translated_folder.is_dir():
        print(
            f"❌ Language '{argument}' was not found."
        )
        print(
            f"Expected folder: {translated_folder}"
        )
        print()

        print_available_languages()
        return 1

    success = compare_strings(
        original_language=ORIGINAL_LANGUAGE,
        translated_language=translated_language,
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
