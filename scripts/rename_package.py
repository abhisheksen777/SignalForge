#!/usr/bin/env python3


import argparse
import io
import shutil
import sys
from pathlib import Path

#  Windows 
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

OLD_PACKAGE_NAME = "signalforge"
OLD_PROJECT_NAME = "signalforge"


def get_project_root() -> Path:
    """"""
    return Path(__file__).parent.parent


def validate_package_name(name: str) -> bool:
    """
    """
    import keyword

    if not name:
        return False

    #  Python 
    if not name.isidentifier():
        return False

    #  Python 
    return not keyword.iskeyword(name)


def to_project_name(package_name: str) -> str:
    """
     ()
    : my_awesome_project -> my-awesome-project
    """
    return package_name.replace("_", "-")


def rename_directory(root: Path, new_package_name: str) -> bool:
    """"""
    old_dir = root / "src" / OLD_PACKAGE_NAME
    new_dir = root / "src" / new_package_name

    if not old_dir.exists():
        print(f"❌ : : {old_dir}")
        return False

    if new_dir.exists():
        print(f"❌ : : {new_dir}")
        return False

    try:
        shutil.move(str(old_dir), str(new_dir))
        print(f"✅ : {old_dir.name} -> {new_dir.name}")
        return True
    except Exception as e:
        print(f"❌ : {e}")
        return False


def update_file_content(
    file_path: Path,
    old_package: str,
    new_package: str,
    old_project: str,
    new_project: str,
) -> bool:
    """"""
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        #  ()
        content = content.replace(old_package, new_package)

        #  ()
        content = content.replace(old_project, new_project)

        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            return True
        return False
    except UnicodeDecodeError:
        return False
    except Exception as e:
        print(f"⚠️  {file_path}: {e}")
        return False


def get_files_to_update(root: Path) -> list[Path]:
    """"""
    files = []

    extensions = {
        ".py",
        ".md",
        ".toml",
        ".yaml",
        ".yml",
        ".txt",
        ".rst",
        ".cfg",
        ".ini",
    }

    exclude_dirs = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".ruff_cache",
        ".pytest_cache",
        "node_modules",
        ".history",
        "logs",
    }

    for item in root.rglob("*"):
        if any(excluded in item.parts for excluded in exclude_dirs):
            continue

        if item.is_file() and (
            item.suffix in extensions
            or item.name in {"Makefile", "Dockerfile", ".gitignore", ".env.example"}
        ):
            files.append(item)

    return files


def main():
    parser = argparse.ArgumentParser(
        description=" Python ",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
:
    python scripts/rename_package.py my_new_package
    python scripts/rename_package.py --dry-run my_new_package
        """,
    )
    parser.add_argument(
        "new_package_name",
        help=" (, : my_awesome_project)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="",
    )

    args = parser.parse_args()
    new_package_name = args.new_package_name
    dry_run = args.dry_run

    if not validate_package_name(new_package_name):
        print(f"❌ : '{new_package_name}'")
        print(":")
        print("  - ")
        print("  - ")
        print("  -  Python ")
        sys.exit(1)

    new_project_name = to_project_name(new_package_name)
    root = get_project_root()

    print(f"\n{'=' * 60}")
    print("")
    print(f"{'=' * 60}")
    print(f": {root}")
    print(f": {OLD_PACKAGE_NAME} -> : {new_package_name}")
    print(f": {OLD_PROJECT_NAME} -> : {new_project_name}")
    if dry_run:
        print("⚠️  - ")
    print(f"{'=' * 60}\n")

    old_dir = root / "src" / OLD_PACKAGE_NAME
    if not old_dir.exists():
        print(f"❌ : : {old_dir}")
        print("")
        sys.exit(1)

    files = get_files_to_update(root)

    files_to_modify = []
    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8")
            if OLD_PACKAGE_NAME in content or OLD_PROJECT_NAME in content:
                files_to_modify.append(file_path)
        except (UnicodeDecodeError, Exception):
            continue

    print("📁 :")
    print(f"   src/{OLD_PACKAGE_NAME} -> src/{new_package_name}")
    print()

    print(f"📝  ({len(files_to_modify)} ):")
    for f in sorted(files_to_modify):
        print(f"   {f.relative_to(root)}")
    print()

    if dry_run:
        print("✅  --dry-run ")
        sys.exit(0)

    confirm = input("? (y/N): ").strip().lower()
    if confirm != "y":
        print("")
        sys.exit(0)

    print("\n...\n")

    # 1. 
    updated_count = 0
    for file_path in files_to_modify:
        if update_file_content(
            file_path,
            OLD_PACKAGE_NAME,
            new_package_name,
            OLD_PROJECT_NAME,
            new_project_name,
        ):
            updated_count += 1
            print(f"  ✅ : {file_path.relative_to(root)}")

    # 2. 
    print()
    if not rename_directory(root, new_package_name):
        print("\n❌ ")
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print("✅ !")
    print(f"{'=' * 60}")
    print(f"  •  {updated_count} ")
    print("  • ")
    print()
    print("📌 :")
    print("  1. : git diff")
    print("  2. : uv pip install -e .")
    print("  3. : pytest")
    print("  4. : git add -A && git commit -m 'chore: rename package'")
    print()


if __name__ == "__main__":
    main()
