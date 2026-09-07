# SPDX-License-Identifier: Apache-2.0
"""Check that every Python file starts with the Apache-2.0 SPDX header.

LMCache requires ``# SPDX-License-Identifier: Apache-2.0`` as line 1 of every
Python file, and this repo follows that standard for its pipeline tooling. Run as
a pre-commit hook with the candidate files as arguments.
"""

# Standard
import sys

EXPECTED = "# SPDX-License-Identifier: Apache-2.0"


def has_header(path: str) -> bool:
    """Return whether ``path`` starts with the expected SPDX header.

    Args:
        path: Path to a Python source file.

    Returns:
        True if the file's first line is exactly the expected SPDX header.

    Raises:
        OSError: If the file cannot be read.
    """
    with open(path, encoding="utf-8") as handle:
        first_line = handle.readline().strip()
    return first_line == EXPECTED


def main(paths: list[str]) -> int:
    """Check each path and report the ones missing the header.

    Args:
        paths: Python files to check.

    Returns:
        0 if every file carries the header, 1 otherwise.
    """
    missing = [path for path in paths if not has_header(path)]
    if not missing:
        return 0

    print("")
    print("========================================")
    print("  Missing SPDX header on line 1")
    print(f"  Add: {EXPECTED}")
    print("========================================")
    print("")
    for path in missing:
        print(f"  {path}")
    print("")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
