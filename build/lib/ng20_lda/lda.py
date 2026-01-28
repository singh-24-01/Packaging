from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Tuple

import joblib
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

logger = logging.getLogger(__name__)


def iter_txt_files(root_dir: Path) -> List[Path]:
    """Recursively list all .txt files under a directory.

    Args:
        root_dir: Root directory to search.

    Returns:
        List of .txt file paths (sorted for reproducibility).
    """
    files = sorted(p for p in root_dir.rglob("*.txt") if p.is_file())
    return files


def load_texts(files: List[Path]) -> List[str]:
    """Load multiple text files as UTF-8.

    Args:
        files: List of file paths.

    Returns:
        List of text contents.
    """
    texts: List[str] = []
    for p in files:
        texts.append(p.read_text(encoding="utf-8", errors="replace"))
    return texts


def train_lda_from_dir(
    texts_dir: Path,
    n_topics: int = 10,
    max_features: int = 2000,
    random_state: int = 0,
) -> Tuple[LatentDirichletAllocation, CountVectorizer]:
    """Train an LDA model from all txt files found recursively in a folder.

    Args:
        texts_dir: Directory containing .txt files (recursively).
        n_topics: Number of topics for LDA.
        max_features: Vocabulary size limit for CountVectorizer.
        random_state: Random seed.

    Returns:
        (lda_model, vectorizer)
    """
    files = iter_txt_files(texts_dir)
    if len(files) == 0:
        raise ValueError(f"No .txt files found under: {texts_dir}")

    logger.info("Found %d .txt files under %s", len(files), texts_dir)
    texts = load_texts(files)

    vectorizer = CountVectorizer(
        stop_words="english",
        max_features=max_features,
    )
    X = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=random_state,
        learning_method="batch",
    )
    lda.fit(X)

    logger.info("LDA trained: n_topics=%d, vocab_size=%d", n_topics, len(vectorizer.get_feature_names_out()))
    return lda, vectorizer


def save_lda_bundle(model_dir: Path, lda: LatentDirichletAllocation, vectorizer: CountVectorizer) -> Path:
    """Save LDA + vectorizer into a pickle file inside model_dir.

    Args:
        model_dir: Output directory for the model.
        lda: Trained LDA model.
        vectorizer: Fitted CountVectorizer.

    Returns:
        Path to the created pickle file.
    """
    model_dir.mkdir(parents=True, exist_ok=True)
    out_path = model_dir / "lda_bundle.pkl"
    joblib.dump({"lda": lda, "vectorizer": vectorizer}, out_path)
    return out_path


def load_lda_bundle(pickle_path: Path):
    """Load a saved LDA bundle (lda + vectorizer) from pickle."""
    obj = joblib.load(pickle_path)
    return obj["lda"], obj["vectorizer"]

from typing import Dict


def describe_document(
    text: str,
    lda: LatentDirichletAllocation,
    vectorizer: CountVectorizer,
    top_k_topics: int = 3,
    top_k_words: int = 5,
) -> Dict[int, list[str]]:
    """Describe a document with its most relevant topics and top words per topic.

    Args:
        text: Document content.
        lda: Trained LDA model.
        vectorizer: Fitted CountVectorizer.
        top_k_topics: Number of topics to show.
        top_k_words: Number of words to show per topic.

    Returns:
        Dict mapping topic_id -> list of top words.
    """
    X = vectorizer.transform([text])
    topic_dist = lda.transform(X)[0]  # shape: (n_topics,)

    # topics indices sorted by relevance (descending)
    top_topics = topic_dist.argsort()[::-1][:top_k_topics]

    feature_names = vectorizer.get_feature_names_out()
    topic_word_lists: Dict[int, list[str]] = {}

    for topic_id in top_topics:
        # lda.components_[topic_id] gives word weights for that topic
        word_weights = lda.components_[topic_id]
        top_words_idx = word_weights.argsort()[::-1][:top_k_words]
        topic_word_lists[int(topic_id)] = [str(feature_names[i]) for i in top_words_idx]

    return topic_word_lists

