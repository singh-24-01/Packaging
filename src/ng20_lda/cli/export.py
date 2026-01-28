import argparse
import logging
from pathlib import Path

from ng20_lda.logging_utils import setup_logging
from ng20_lda.ng20 import export_ng20_category

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for ng20-export."""
    parser = argparse.ArgumentParser(prog="ng20-export")
    parser.add_argument("category", type=str, help="20 Newsgroups category (e.g., sci.space).")
    parser.add_argument("n_docs", type=int, help="Number of documents to export.")
    parser.add_argument("output_dir", type=str, help="Output directory.")
    parser.add_argument("--log-level", default="INFO", help="Logging level (INFO, DEBUG, ...).")
    return parser


def main() -> None:
    """Entry point for ng20-export."""
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(args.log_level)

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    logger.info("Running export: category=%s n_docs=%s output_dir=%s", args.category, args.n_docs, out)
    cat_dir = export_ng20_category(args.category, args.n_docs, out)
    print(str(cat_dir))

