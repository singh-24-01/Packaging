import argparse
import logging
from pathlib import Path

from ng20_lda.lda import describe_document, load_lda_bundle
from ng20_lda.logging_utils import setup_logging

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for ng20-describe."""
    parser = argparse.ArgumentParser(prog="ng20-describe")
    parser.add_argument("doc_path", type=str, help="Path to a text document (.txt).")
    parser.add_argument(
        "--model",
        type=str,
        default="/tmp/ng20_model/lda_bundle.pkl",
        help="Path to lda_bundle.pkl (default: /tmp/ng20_model/lda_bundle.pkl).",
    )
    parser.add_argument("--log-level", default="INFO", help="Logging level (INFO, DEBUG, ...).")
    return parser


def main() -> None:
    """Entry point for ng20-describe."""
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(args.log_level)

    doc_path = Path(args.doc_path)
    model_path = Path(args.model)

    logger.info("Loading model from %s", model_path)
    lda, vectorizer = load_lda_bundle(model_path)

    text = doc_path.read_text(encoding="utf-8", errors="replace")

    desc = describe_document(text, lda, vectorizer, top_k_topics=3, top_k_words=5)

    # Print to stdout (human readable)
    for topic_id, words in desc.items():
        print(f"Topic {topic_id}: {', '.join(words)}")

