"""Transparent text loading and tokenization."""

import re
from pathlib import Path

from .models import Document


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+|[\u4e00-\u9fff]")


def tokenize(text: str) -> list[str]:
    """Return lowercase Latin tokens and individual CJK characters."""
    return TOKEN_PATTERN.findall(text.lower())


def load_documents(directory: Path) -> list[Document]:
    """Load UTF-8 Markdown and text files in deterministic path order."""
    paths = sorted(
        path
        for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}
    )
    return [
        Document(
            document_id=path.stem,
            source=str(path.relative_to(directory)).replace("\\", "/"),
            text=path.read_text(encoding="utf-8"),
        )
        for path in paths
    ]
