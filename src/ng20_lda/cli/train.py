import argparse
import logging
from pathlib import Path

from ng20_lda.lda import save_lda_bundle, train_lda_from_dir
from ng20_lda.logging_utils import setup_logging

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for ng20-train-lda."""
    parser = argparse.ArgumentParser(prog="ng20-train-lda")
    parser.add_argument("texts_dir", type=str, help="Path to directory containing txt files (recursive).")
    parser.add_argument("model_dir", type=str, help="Path to directory that will contain the trained model.")
    parser.add_argument("--n-topics", type=int, default=10, help="Number of LDA topics.")
    parser.add_argument("--max-features", type=int, default=2000, help="Max vocabulary size.")
    parser.add_argument("--random-state", type=int, default=0, help="Random seed.")
    parser.add_argument("--log-level", default="INFO", help="Logging level (INFO, DEBUG, ...).")
    return parser


def main() -> None:
    """Entry point for ng20-train-lda."""
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(args.log_level)

    texts_dir = Path(args.texts_dir)
    model_dir = Path(args.model_dir)

    logger.info(
        "Training LDA from %s -> %s (n_topics=%d, max_features=%d)",
        texts_dir,
        model_dir,
        args.n_topics,
        args.max_features,
    )

    lda, vectorizer = train_lda_from_dir(
        texts_dir=texts_dir,
        n_topics=args.n_topics,
        max_features=args.max_features,
        random_state=args.random_state,
    )
    out_path = save_lda_bundle(model_dir, lda, vectorizer)
    print(str(out_path))

