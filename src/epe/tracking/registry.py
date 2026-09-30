"""Document registry — scans a project and builds the document catalog.

The registry is derived on demand from the existing artifact files.
It does not create new files — it reads what's there and produces
DocumentRecord objects with enhanced traceability metadata.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from epe.core.frontmatter import read_doc
from epe.core.logging import get_logger
from epe.tracking.ids import ID_PATTERNS, scan_all_ids
from epe.tracking.models import (
    DocumentRecord,
    DocumentStatus,
    DocumentType,
    DocumentLink,
    LinkType,
    Task,
    Milestone,
    RfpRequirement,
    Deliverable,
    Approval,
    Stakeholder,
)

logger = get_logger("tracking.registry")


def _parse_status(value: str | None) -> DocumentStatus:
    if not value:
        return DocumentStatus.DRAFT
    try:
        return DocumentStatus(value)
    except ValueError:
        return DocumentStatus.DRAFT


def _parse_doc_type(value: str | None) -> DocumentType:
    if not value:
        return DocumentType.INSTANCE
    try:
        return DocumentType(value)
    except ValueError:
        return DocumentType.INSTANCE


def _extract_ids(body: str) -> dict[str, list[str]]:
    """Extract all typed IDs from document body text using canonical patterns."""
    return scan_all_ids(body)


def _stage_from_path(path: Path) -> str | None:
    """Infer stage from path segments."""
    parts = path.parts
    if "product" in parts:
        return "product"
    if "presales" in parts:
        return "presales"
    if "architecture" in parts:
        return "architecture"
    if "delivery" in parts:
        return "delivery"
    if "entities" in parts:
        return "governance"
    return None


def _contract_from_filename(filename: str, stage: str | None) -> str | None:
    """Derive a contract name from filename when not in frontmatter."""
    name = Path(filename).stem  # e.g. "hld", "scope", "definition"
    if stage:
        return f"{stage}.{name}"
    return name


def _normalize_inputs_outputs(value: Any) -> list[str]:
    """Normalize inputs/outputs field to a list of strings."""
    if not value:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return []


class DocumentRegistry:
    """Scans a project directory and builds a catalog of DocumentRecords.

    Usage::

        registry = DocumentRegistry.from_project(project_path, project_id)
        docs = registry.documents                    # all documents
        product_docs = registry.by_stage("product")  # filtered by stage
        doc = registry.get("presales/scope.md")     # by path
    """

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id
        self._documents: dict[str, DocumentRecord] = {}
        self._links: list[DocumentLink] = []

    @classmethod
    def from_project(cls, project_root: Path, project_id: str) -> "DocumentRegistry":
        """Scan a project root and build the registry."""
        registry = cls(project_id)
        registry.scan(project_root)
        return registry

    def scan(self, project_root: Path) -> None:
        """Walk the project and register every .md artifact."""
        stage_dirs = ["product", "presales", "architecture", "delivery"]
        for stage in stage_dirs:
            stage_path = project_root / stage
            if not stage_path.is_dir():
                continue
            for md_file in stage_path.glob("*.md"):
                self._register(md_file, project_root)

        # Also scan entity subdirectories for standalone entity docs
        # Legacy flat entity directories
        for subdir in ["requirements", "decisions", "risks", "questions",
                       "assumptions", "dependencies", "changes", "evidence"]:
            subdir_path = project_root / subdir
            if not subdir_path.is_dir():
                continue
            for md_file in subdir_path.glob("*.md"):
                self._register(md_file, project_root)

        # Governance entity subdirectories (nested under entities/)
        # Structure: entities/ms/, entities/rfp-req/, entities/del/, entities/aprv/, entities/stk/
        entities_base = project_root / "entities"
        if entities_base.is_dir():
            for entity_type_dir in entities_base.iterdir():
                if entity_type_dir.is_dir():
                    for md_file in entity_type_dir.glob("*.md"):
                        self._register(md_file, project_root)

    def _register(self, path: Path, project_root: Path) -> None:
        """Register a single document file."""
        try:
            doc = read_doc(path)
        except Exception as exc:
            logger.warning("Failed to read %s: %s", path, exc)
            return

        rel = path.relative_to(project_root)
        stage = _stage_from_path(rel) or doc.stage
        contract = doc.contract or _contract_from_filename(path.name, stage)

        # Extract IDs from body
        body_ids = _extract_ids(doc.body)

        # Build record
        record = DocumentRecord(
            path=rel,
            project_id=self.project_id,
            contract=contract,
            version=doc.get("version", 1),
            stage=stage,
            status=_parse_status(doc.status),
            doc_type=_parse_doc_type(doc.get("type")),
            title=doc.get("title", path.stem),
            owner=doc.get("owner"),
            created_at=doc.get("created_at"),
            updated_at=doc.get("generated_at"),  # generated_at serves as updated
            approved_by=doc.get("approved_by"),
            approved_at=doc.get("approved_at"),
            generated_by=doc.get("generated_by"),
            opportunity=doc.get("opportunity"),
            customer=doc.get("customer"),
            inputs=_normalize_inputs_outputs(doc.get("inputs")),
            outputs=_normalize_inputs_outputs(doc.get("outputs")),
            # Core lifecycle spine
            requirements=body_ids.get("REQ", []),
            customer_requirements=body_ids.get("CUST", []),
            components=body_ids.get("COMP", []),
            decisions=body_ids.get("DEC", []),
            tasks=body_ids.get("TASK", []),
            tests=body_ids.get("TEST", []),
            evidence=body_ids.get("EVD", []),
            # Supporting/cross-cutting
            risks=body_ids.get("RSK", []),
            assumptions=body_ids.get("ASM", []),
            dependencies=body_ids.get("DEP", []),
            changes=body_ids.get("CHG", []),
            # Governance entities
            milestones=body_ids.get("MILESTONE", []),
            rfp_requirements=body_ids.get("RFP_REQ", []),
            deliverables=body_ids.get("DELIVERABLE", []),
            approvals=body_ids.get("APPROVAL", []),
            stakeholders=body_ids.get("STAKEHOLDER", []),
            supersedes=doc.get("supersedes"),
            superseded_by=doc.get("superseded_by"),
        )
        self._documents[str(rel)] = record

        # Build links from inputs/outputs
        for inp in record.inputs:
            self._links.append(DocumentLink(
                from_doc=inp,
                to_doc=str(rel),
                link_type=LinkType.INPUTS,
            ))
        for out in record.outputs:
            self._links.append(DocumentLink(
                from_doc=str(rel),
                to_doc=out,
                link_type=LinkType.OUTPUTS,
            ))

    @property
    def documents(self) -> list[DocumentRecord]:
        """All registered documents."""
        return list(self._documents.values())

    @property
    def links(self) -> list[DocumentLink]:
        """All document links."""
        return self._links

    def by_stage(self, stage: str) -> list[DocumentRecord]:
        """All documents for a given stage."""
        return [d for d in self._documents.values() if d.stage == stage]

    def by_status(self, status: DocumentStatus) -> list[DocumentRecord]:
        return [d for d in self._documents.values() if d.status == status]

    def by_contract(self, contract: str) -> list[DocumentRecord]:
        return [d for d in self._documents.values() if d.contract == contract]

    def get(self, doc_id: str) -> DocumentRecord | None:
        """Get a document by its doc_id (relative path)."""
        return self._documents.get(doc_id)

    def get_inputs(self, doc_id: str) -> list[DocumentRecord]:
        """Get all documents that are inputs to the given document."""
        input_doc_ids = set()
        for link in self._links:
            if link.to_doc == doc_id and link.link_type == LinkType.INPUTS:
                input_doc_ids.add(link.from_doc)
        return [self._documents[d] for d in input_doc_ids if d in self._documents]

    def get_outputs(self, doc_id: str) -> list[DocumentRecord]:
        """Get all documents that are outputs of the given document."""
        output_doc_ids = set()
        for link in self._links:
            if link.from_doc == doc_id and link.link_type == LinkType.OUTPUTS:
                output_doc_ids.add(link.to_doc)
        return [self._documents[d] for d in output_doc_ids if d in self._documents]

    def by_milestone(self, milestone_id: str) -> list[DocumentRecord]:
        """All documents that reference a given milestone (MS-NNN)."""
        return [d for d in self._documents.values() if milestone_id in d.milestones]

    def by_rfp_requirement(self, rfp_req_id: str) -> list[DocumentRecord]:
        """All documents that reference a given RFP requirement (RFP-REQ-NNN)."""
        return [d for d in self._documents.values() if rfp_req_id in d.rfp_requirements]

    def by_deliverable(self, del_id: str) -> list[DocumentRecord]:
        """All documents that reference a given deliverable (DEL-NNN)."""
        return [d for d in self._documents.values() if del_id in d.deliverables]

    def by_approval(self, aprv_id: str) -> list[DocumentRecord]:
        """All documents that reference a given approval (APRV-NNN)."""
        return [d for d in self._documents.values() if aprv_id in d.approvals]

    def by_stakeholder(self, stk_id: str) -> list[DocumentRecord]:
        """All documents that reference a given stakeholder (STK-NNN)."""
        return [d for d in self._documents.values() if stk_id in d.stakeholders]

    def by_entity(self, entity_id: str) -> list[DocumentRecord]:
        """All documents that reference a given entity (any type)."""
        return [
            d for d in self._documents.values()
            if entity_id in (d.milestones + d.rfp_requirements + d.deliverables +
                            d.approvals + d.stakeholders + d.requirements +
                            d.customer_requirements + d.components + d.decisions +
                            d.tasks + d.tests + d.evidence + d.risks +
                            d.assumptions + d.dependencies + d.changes)
        ]

    def stage_summary(self) -> dict[str, dict[str, Any]]:
        """Summarize document counts and statuses per stage."""
        stages = ["product", "presales", "architecture", "delivery", "governance"]
        summary: dict[str, dict[str, Any]] = {}
        for stage in stages:
            docs = self.by_stage(stage)
            approved = sum(1 for d in docs if d.is_approved)
            summary[stage] = {
                "total": len(docs),
                "approved": approved,
                "draft": sum(1 for d in docs if d.status == DocumentStatus.DRAFT),
                "in_review": sum(1 for d in docs if d.status == DocumentStatus.IN_REVIEW),
                "documents": [d.doc_id for d in docs],
            }
        return summary

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "stage_summary": self.stage_summary(),
            "documents": {d.doc_id: d.to_dict() for d in self._documents.values()},
            "links": [link.to_dict() for link in self._links],
        }
