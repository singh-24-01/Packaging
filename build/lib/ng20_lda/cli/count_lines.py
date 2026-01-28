import argparse
import logging
from pathlib import Path

from ng20_lda.logging_utils import setup_logging
from ng20_lda.lines import count_lines_from_path

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for ng20-count-lines."""
    parser = argparse.ArgumentParser(prog="ng20-count-lines")
    parser.add_argument("path", type=str, help="Path to a text file.")
    parser.add_argument("--log-level", default="INFO", help="Logging level (INFO, DEBUG, ...).")
    return parser


def main() -> None:
    """Entry point for ng20-count-lines."""
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(args.log_level)
    path = Path(args.path)

    logger.info("Counting lines in file: %s", path)
    n = count_lines_from_path(path)
    print(n)

