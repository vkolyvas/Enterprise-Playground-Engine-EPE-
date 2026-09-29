"""End-to-end ingestion pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from epe.core.logging import get_logger
from epe.core.paths import EpePaths
from epe.ingestion.chunker import chunk_by_section, chunks_to_index_file
from epe.ingestion.classifier import DocumentClassifier
from epe.ingestion.extractors import ExtractedDocument, extract as extract_doc
from epe.ingestion.metadata import (
    SourceDocument,
    file_sha256,
    generate_document_id,
    write_metadata,
)
from epe.ingestion.security import SecretFinding, scan_for_secrets


@dataclass
class IngestionResult:
    document_id: str
    path: Path
    success: bool
    metadata_path: Path | None = None
    chunks_path: Path | None = None
    error: str | None = None
    warnings: list[str] = field(default_factory=list)
    secret_findings: list[SecretFinding] = field(default_factory=list)


@dataclass
class IngestionReport:
    started_at: str
    finished_at: str | None
    results: list[IngestionResult] = field(default_factory=list)

    @property
    def success_count(self) -> int:
        return sum(1 for r in self.results if r.success)

    @property
    def failure_count(self) -> int:
        return sum(1 for r in self.results if not r.success)

    @property
    def secret_findings_count(self) -> int:
        return sum(len(r.secret_findings) for r in self.results)

    def to_dict(self) -> dict:
        return {
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "summary": {
                "total": len(self.results),
                "success": self.success_count,
                "failure": self.failure_count,
                "secret_findings": self.secret_findings_count,
            },
            "results": [
                {
                    "document_id": r.document_id,
                    "path": str(r.path),
                    "success": r.success,
                    "metadata_path": str(r.metadata_path) if r.metadata_path else None,
                    "chunks_path": str(r.chunks_path) if r.chunks_path else None,
                    "error": r.error,
                    "warnings": r.warnings,
                    "secret_findings": [
                        {"kind": s.kind, "location": s.location, "excerpt": s.excerpt}
                        for s in r.secret_findings
                    ],
                }
                for r in self.results
            ],
        }


class IngestionPipeline:
    def __init__(self, paths: EpePaths, *, project_id: str | None = None) -> None:
        self.paths = paths
        self.project_id = project_id
        self.classifier = DocumentClassifier()
        self.logger = get_logger("ingestion")

    def ingest_one(
        self,
        source_path: Path,
        *,
        hints: dict | None = None,
        project_id: str | None = None,
        sensitivity_hint: str | None = None,
    ) -> IngestionResult:
        try:
            document_id = generate_document_id(source_path)
            sha = file_sha256(source_path)
            extracted: ExtractedDocument = extract_doc(source_path)
        except Exception as e:
            self.logger.exception("Failed to extract %s", source_path)
            return IngestionResult(
                document_id="(unknown)",
                path=source_path,
                success=False,
                error=str(e),
            )

        secret_findings = scan_for_secrets(extracted.text, location=str(source_path))

        result = self.classifier.classify(filename=source_path.name, text=extracted.text, hints=hints)
        effective_project = project_id or self.project_id

        metadata = SourceDocument(
            document_id=document_id,
            filename=source_path.name,
            source_path=str(source_path),
            sha256=sha,
            document_type=result.document_type,
            domain=result.domain,
            stage_relevance=result.stage_relevance,
            authority=result.authority,
            confidence=result.confidence,
            topics=result.topics,
            contains=result.contains,
            sensitivity=result.sensitivity,
            project_id=effective_project,
        )

        # Choose namespace: project-scoped source if project_id present, else global
        if effective_project:
            namespace = f"project:{effective_project}"
            classified_dir = self.paths.sources_classified / effective_project
            processed_dir = self.paths.sources_processed / effective_project
        else:
            namespace = "global"
            classified_dir = self.paths.sources_classified
            processed_dir = self.paths.sources_processed

        classified_dir.mkdir(parents=True, exist_ok=True)
        processed_dir.mkdir(parents=True, exist_ok=True)

        metadata_path = classified_dir / f"{document_id}.yaml"
        write_metadata(metadata, metadata_path)

        # Write the normalized text and chunk it
        normalized_dir = processed_dir / "documents" / document_id
        normalized_dir.mkdir(parents=True, exist_ok=True)
        normalized_path = normalized_dir / "normalized.md"
        normalized_path.write_text(extracted.text, encoding="utf-8")

        chunks = chunk_by_section(
            extracted,
            namespace=namespace,
            source_document_id=document_id,
        )
        chunks_path = processed_dir / "chunks" / f"{document_id}.json"
        chunks_to_index_file(chunks, chunks_path)

        return IngestionResult(
            document_id=document_id,
            path=source_path,
            success=True,
            metadata_path=metadata_path,
            chunks_path=chunks_path,
            warnings=extracted.warnings,
            secret_findings=secret_findings,
        )

    def ingest_directory(
        self,
        source_dir: Path,
        *,
        project_id: str | None = None,
    ) -> IngestionReport:
        started = datetime.now(timezone.utc).isoformat()
        report = IngestionReport(started_at=started, finished_at=None)
        if not source_dir.exists():
            report.finished_at = datetime.now(timezone.utc).isoformat()
            return report

        for path in sorted(source_dir.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {
                ".pdf", ".docx", ".xlsx", ".pptx", ".md", ".markdown",
                ".txt", ".csv", ".json", ".yaml", ".yml",
            }:
                continue
            result = self.ingest_one(path, project_id=project_id)
            report.results.append(result)

        report.finished_at = datetime.now(timezone.utc).isoformat()
        # write report
        report_dir = self.paths.sources_processed / (project_id or "_global")
        report_dir.mkdir(parents=True, exist_ok=True)
        (report_dir / "ingestion-report.json").write_text(
            json.dumps(report.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return report
