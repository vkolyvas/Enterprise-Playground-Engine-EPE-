"""Document ingestion: classify, extract, normalize, metadata."""

from epe.ingestion.classifier import DocumentClassifier
from epe.ingestion.metadata import SourceDocument, generate_document_id, write_metadata
from epe.ingestion.pipeline import IngestionPipeline, IngestionReport
from epe.ingestion.security import scan_for_secrets

__all__ = [
    "DocumentClassifier",
    "SourceDocument",
    "generate_document_id",
    "write_metadata",
    "IngestionPipeline",
    "IngestionReport",
    "scan_for_secrets",
]
