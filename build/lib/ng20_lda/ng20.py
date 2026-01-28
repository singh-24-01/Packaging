from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from sklearn.datasets import fetch_20newsgroups

logger = logging.getLogger(__name__)


def export_ng20_category(category: str, n_docs: int, output_dir: Path) -> Path:
    """Export the first N documents of a 20 Newsgroups category into txt files.

    It creates the folder: output_dir/category
    and writes files: 0.txt, 1.txt, ..., (n_docs-1).txt

    Args:
        category: A 20 Newsgroups category name (e.g., "sci.space").
        n_docs: Number of documents to export (first N documents).
        output_dir: Output base directory.

    Returns:
        The created category directory path (output_dir/category).

    Raises:
        ValueError: If n_docs <= 0 or category is empty.
    """
    if not category or category.strip() == "":
        raise ValueError("category must be a non-empty string")
    if n_docs <= 0:
        raise ValueError("n_docs must be > 0")

    logger.info("Fetching 20 Newsgroups for category=%s", category)
    data = fetch_20newsgroups(subset="train", categories=[category], remove=())

    texts: List[str] = list(data.data)
    if len(texts) == 0:
        raise ValueError(f"No documents found for category '{category}'")

    cat_dir = output_dir / category
    cat_dir.mkdir(parents=True, exist_ok=True)

    n = min(n_docs, len(texts))
    logger.info("Exporting %s documents to %s", n, cat_dir)

    for i in range(n):
        (cat_dir / f"{i}.txt").write_text(texts[i], encoding="utf-8", errors="replace")

    return cat_dir

