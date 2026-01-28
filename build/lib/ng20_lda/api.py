from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ng20_lda.lines import count_lines_from_text
from ng20_lda.lda import load_lda_bundle, describe_document
from ng20_lda.ng20 import export_ng20_category

app = FastAPI(title="ng20-lda API", version="1.0.0")


class CountLinesRequest(BaseModel):
    text: str


class DescribeRequest(BaseModel):
    text: str
    model_path: str
    top_topics: int = 3
    top_words: int = 5


class ExportRequest(BaseModel):
    category: str
    n_docs: int
    output_dir: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/count-lines")
def api_count_lines(payload: CountLinesRequest):
    return {"lines": count_lines_from_text(payload.text)}


@app.post("/describe")
def api_describe(payload: DescribeRequest):
    model_path = Path(payload.model_path)
    if not model_path.exists():
        raise HTTPException(status_code=400, detail=f"model_path not found: {model_path}")

    lda, vectorizer = load_lda_bundle(model_path)
    desc = describe_document(
        text=payload.text,
        lda=lda,
        vectorizer=vectorizer,
        top_k_topics=payload.top_topics,
        top_k_words=payload.top_words,
    )
    # JSON-friendly
    return {"topics": desc}


@app.post("/export")
def api_export(payload: ExportRequest):
    out_dir = Path(payload.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cat_dir = export_ng20_category(payload.category, payload.n_docs, out_dir)
    return {"output": str(cat_dir)}

@app.get("/")
def root():
    return {"message": "ng20-lda API is running"}

