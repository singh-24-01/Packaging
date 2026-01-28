from __future__ import annotations

from pathlib import Path


def count_lines_from_text(text: str) -> int:
    """Count the number of lines in a text.

    A line is separated by '\\n'.

    Args:
        text: Input text.

    Returns:
        Number of lines.

    Examples:
        >>> count_lines_from_text("a\\nb\\n")
        2
        >>> count_lines_from_text("")
        0
        >>> count_lines_from_text("one line")
        1
    """
    if text == "":
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def count_lines_from_path(path: Path) -> int:
    """Count the number of lines in a UTF-8 text file.

    Args:
        path: Path to the file.

    Returns:
        Number of lines in the file.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    return count_lines_from_text(text)

