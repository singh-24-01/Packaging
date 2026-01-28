from __future__ import annotations

from pathlib import Path
from ng20_lda.lines import count_lines_from_path

import typer
import uvicorn

from ng20_lda.logging_utils import setup_logging
from ng20_lda.ng20 import export_ng20_category
from ng20_lda.lda import (
    load_lda_bundle,
    save_lda_bundle,
    train_lda_from_dir,
    describe_document,
)

app = typer.Typer(help="ng20-lda: export, train LDA, describe documents, count lines.")


@app.command("export")
def cmd_export(
    category: str = typer.Argument(..., help="20 Newsgroups category (e.g., sci.space)."),
    n_docs: int = typer.Argument(..., help="Number of documents to export."),
    output_dir: Path = typer.Argument(..., help="Output directory."),
    log_level: str = typer.Option("INFO", help="Logging level (INFO, DEBUG, ...)."),
):
    """Export the first N documents of a category into D/C/i.txt."""
    setup_logging(log_level)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    cat_dir = export_ng20_category(category=category, n_docs=n_docs, output_dir=out)
    typer.echo(str(cat_dir))


@app.command("train-lda")
def cmd_train_lda(
    texts_dir: Path = typer.Argument(..., help="Directory containing txt files (recursive)."),
    model_dir: Path = typer.Argument(..., help="Directory to save the trained model."),
    n_topics: int = typer.Option(10, help="Number of topics."),
    max_features: int = typer.Option(2000, help="Max vocabulary size."),
    random_state: int = typer.Option(0, help="Random seed."),
    log_level: str = typer.Option("INFO", help="Logging level (INFO, DEBUG, ...)."),
):
    """Train an LDA model from texts_dir and save it as a pickle bundle."""
    setup_logging(log_level)
    lda, vectorizer = train_lda_from_dir(
        texts_dir=Path(texts_dir),
        n_topics=n_topics,
        max_features=max_features,
        random_state=random_state,
    )
    out_path = save_lda_bundle(Path(model_dir), lda, vectorizer)
    typer.echo(str(out_path))


@app.command("describe")
def cmd_describe(
    doc_path: Path = typer.Argument(..., help="Path to a document (.txt)."),
    model_path: Path = typer.Argument(..., help="Path to lda_bundle.pkl."),
    top_topics: int = typer.Option(3, help="Number of topics to show."),
    top_words: int = typer.Option(5, help="Number of words per topic."),
    log_level: str = typer.Option("INFO", help="Logging level (INFO, DEBUG, ...)."),
):
    """Describe a document with its top topics and top words per topic."""
    setup_logging(log_level)
    lda, vectorizer = load_lda_bundle(Path(model_path))
    text = Path(doc_path).read_text(encoding="utf-8", errors="replace")

    desc = describe_document(
        text=text,
        lda=lda,
        vectorizer=vectorizer,
        top_k_topics=top_topics,
        top_k_words=top_words,
    )

    for topic_id, words in desc.items():
        typer.echo(f"Topic {topic_id}: {', '.join(words)}")


@app.command("count-lines")
def cmd_count_lines(
    path: Path = typer.Argument(..., help="Path to a text file."),
    log_level: str = typer.Option("INFO", help="Logging level (INFO, DEBUG, ...)."),
):
    """Count lines in a text file and print the result."""
    setup_logging(log_level)
    n = count_lines_from_path(Path(path))
    typer.echo(str(n))


@app.command("serve")
def cmd_serve(
    host: str = typer.Option("127.0.0.1", help="Host to bind."),
    port: int = typer.Option(8000, help="Port to bind."),
):
    """Run the FastAPI server."""
    uvicorn.run("ng20_lda.api:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    app()

