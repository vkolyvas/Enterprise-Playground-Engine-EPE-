"""PDF extractor using pymupdf, with graceful fallback."""

from __future__ import annotations

from pathlib import Path

from epe.ingestion.extractors import ExtractedDocument


def extract(path: Path) -> ExtractedDocument:
    warnings: list[str] = []
    try:
        import fitz  # type: ignore[import-not-found]
    except ImportError as e:  # pragma: no cover
        warnings.append(f"pymupdf not installed: {e}. Falling back to raw-text read.")
        return ExtractedDocument(
            path=path,
            text=path.read_text(encoding="utf-8", errors="replace"),
            extractor="pdf-fallback",
            warnings=warnings,
        )

    doc = fitz.open(path)
    pages: list[str] = []
    for page in doc:
        pages.append(page.get_text("text"))
    text = "\n\n".join(pages)
    return ExtractedDocument(
        path=path,
        text=text,
        pages=pages,
        structure={"page_count": len(pages)},
        extractor="pdf",
        warnings=warnings,
    )
