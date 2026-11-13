#!/usr/bin/env python3
"""Turn a copy of this template into a project.

Renames the placeholder package in every file and path, writes the project's README, and removes the files
only the template needs, including this script.

    python3 scripts/rename.py my_project --repo owner/my-project
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = "packageName"
TEMPLATE_DESCRIPTION = "Modern C++20 + CMake template"
REPOSITORY_PLACEHOLDER = "OWNER/REPOSITORY"
PROJECT_README = ".github/template/README.md"
TEMPLATE_ONLY = (
    "Readme.md",
    ".github/template",
    ".github/workflows/template-check.yaml",
    ".github/workflows/template-first-use.yaml",
    "scripts/rename.py",
)
SKIPPED_DIRECTORIES = {".git", "build"}


def identifier(raw):
    """Return raw as a C++ and CMake identifier, turning '-', '.' and spaces into '_'."""
    name = re.sub(r"[-. ]+", "_", raw.strip())
    if len(name) < 2 or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name):
        raise ValueError(f"'{raw}' cannot be a package name: use letters, digits and '_', starting with a letter")
    return name


def spellings(name):
    """Map each spelling of the placeholder to the same spelling of name."""
    pascal = "".join(part[:1].upper() + part[1:] for part in name.split("_") if part)
    return {
        PLACEHOLDER: name,
        "PackageName": pascal,
        PLACEHOLDER.upper(): name.upper(),
        PLACEHOLDER.lower(): name.lower(),
    }


def project_paths():
    """Yield every path in the project, deepest first, skipping git and build directories."""
    paths = [p for p in ROOT.rglob("*") if not SKIPPED_DIRECTORIES & set(p.relative_to(ROOT).parts)]
    return sorted(paths, key=lambda p: len(p.parts), reverse=True)


def rename(name, description, repository):
    """Rename the placeholder package to name and remove the template-only files."""
    names = spellings(name)
    pattern = re.compile("|".join(re.escape(spelling) for spelling in names))

    def substitute(text):
        return pattern.sub(lambda match: names[match.group(0)], text)

    this_script = Path(__file__).resolve()
    for path in project_paths():
        if path.is_file() and path.resolve() != this_script:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            updated = substitute(text.replace(TEMPLATE_DESCRIPTION, description))
            if updated != text:
                path.write_text(updated, encoding="utf-8")
        if pattern.search(path.name):
            path.rename(path.with_name(substitute(path.name)))

    readme = (ROOT / PROJECT_README).read_text(encoding="utf-8")
    if repository:
        readme = readme.replace(REPOSITORY_PLACEHOLDER, repository)
    else:
        readme = "".join(line for line in readme.splitlines(keepends=True) if REPOSITORY_PLACEHOLDER not in line)

    for relative in TEMPLATE_ONLY:
        path = ROOT / relative
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
    scripts = ROOT / "scripts"
    if scripts.is_dir() and not any(scripts.iterdir()):
        scripts.rmdir()
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


def main():
    """Parse arguments and rename the project."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name", help="the project's name; '-', '.' and spaces become '_'")
    parser.add_argument("--repo", help="GitHub repository as owner/name, for the README's build badge")
    parser.add_argument("--description", help="one-line description of the project")
    args = parser.parse_args()

    if not (ROOT / PLACEHOLDER).is_dir():
        print(f"no {PLACEHOLDER}/ directory: this project has already been renamed", file=sys.stderr)
        return 1
    try:
        name = identifier(args.name)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    rename(name, args.description or f"The {name} library", args.repo)
    print(f"renamed the package to {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
