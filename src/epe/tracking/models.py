"""Core models for the lifecycle document operating system.

These models provide the traceability spine: cross-stage document lineage
that lets any requirement be traced from CustomerRequirement (Presales)
through SolutionComponent (Architecture) to DeliveryTask (Delivery) to
AcceptanceTest (Delivery) to Evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class DocumentStatus(str, Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


class DocumentType(str, Enum):
    """What kind of document this is in the lifecycle."""

    TEMPLATE = "template"
    INSTANCE = "instance"
    EVIDENCE = "evidence"
    DECISION = "decision"
    DELIVERABLE = "deliverable"
    REFERENCE = "reference"


class LinkType(str, Enum):
    """Type of relationship between documents."""

    INPUTS = "inputs"               # this document consumes the other
    OUTPUTS = "outputs"             # this document produces the other
    SUPPORTED_BY = "supported_by"   # evidence supports this document
    APPROVES = "approves"           # a review document approves this one
    TRACES_TO = "traces_to"         # requirement traces forward
    VERIFIES = "verifies"           # test verifies requirement/component
    IMPLEMENTS = "implements"       # task implements component


# ---------------------------------------------------------------------------
# Core document record
# ---------------------------------------------------------------------------


@dataclass
class DocumentRecord:
    """A lifecycle document with enhanced traceability metadata.

    The document identity is its relative path within the project
    (e.g. ``presales/scope.md``).  This avoids a proliferation of ID
    schemes — the filename is already unique within a project.
    """

    # Identity
    path: Path                            # relative path within project
    project_id: str

    # Core frontmatter
    contract: str | None = None           # e.g. "presales.scope"
    version: int | str = 1
    stage: str | None = None              # product | presales | architecture | delivery
    status: DocumentStatus = DocumentStatus.DRAFT
    doc_type: DocumentType = DocumentType.INSTANCE

    # Enhanced metadata
    title: str | None = None
    owner: str | None = None              # role or person responsible
    created_at: str | None = None
    updated_at: str | None = None
    approved_by: str | None = None
    approved_at: str | None = None

    # Provenance
    generated_by: str | None = None
    opportunity: str | None = None
    customer: str | None = None

    # Traceability links
    inputs: list[str] = field(default_factory=list)   # upstream doc IDs / filenames
    outputs: list[str] = field(default_factory=list)   # downstream doc IDs / filenames
    # Core lifecycle spine entities
    requirements: list[str] = field(default_factory=list)   # REQ-NNN
    customer_requirements: list[str] = field(default_factory=list)  # CUST-NNN
    components: list[str] = field(default_factory=list)      # COMP-NNN
    decisions: list[str] = field(default_factory=list)       # DEC-NNN
    tasks: list[str] = field(default_factory=list)           # TASK-NNN
    tests: list[str] = field(default_factory=list)           # TEST-NNN
    evidence: list[str] = field(default_factory=list)         # EVD-NNN
    # Supporting/cross-cutting entities
    risks: list[str] = field(default_factory=list)          # RSK-NNN
    assumptions: list[str] = field(default_factory=list)    # ASM-NNN
    dependencies: list[str] = field(default_factory=list)   # DEP-NNN
    changes: list[str] = field(default_factory=list)        # CHG-NNN

    # Versioning
    supersedes: str | None = None            # filename of older version
    superseded_by: str | None = None         # filename of newer version

    @property
    def doc_id(self) -> str:
        """Stable document identifier = relative path."""
        return str(self.path)

    @property
    def is_approved(self) -> bool:
        return self.status == DocumentStatus.APPROVED

    @property
    def is_complete(self) -> bool:
        """Heuristic: has meaningful content and required metadata."""
        return bool(
            self.title
            and self.stage
            and self.status != DocumentStatus.DRAFT
            or self.approved_by  # draft is OK if approved
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "contract": self.contract,
            "version": self.version,
            "stage": self.stage,
            "status": self.status.value if isinstance(self.status, DocumentStatus) else self.status,
            "doc_type": self.doc_type.value if isinstance(self.doc_type, DocumentType) else self.doc_type,
            "title": self.title,
            "owner": self.owner,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "generated_by": self.generated_by,
            "opportunity": self.opportunity,
            "customer": self.customer,
            "inputs": self.inputs,
            "outputs": self.outputs,
            # Core lifecycle spine
            "requirements": self.requirements,
            "customer_requirements": self.customer_requirements,
            "components": self.components,
            "decisions": self.decisions,
            "tasks": self.tasks,
            "tests": self.tests,
            "evidence": self.evidence,
            # Supporting/cross-cutting
            "risks": self.risks,
            "assumptions": self.assumptions,
            "dependencies": self.dependencies,
            "changes": self.changes,
            "supersedes": self.supersedes,
            "superseded_by": self.superseded_by,
        }


# ---------------------------------------------------------------------------
# Cross-stage entities
# ---------------------------------------------------------------------------


@dataclass
class CustomerRequirement:
    """A requirement captured during Presales that is specific to a customer."""

    id: str                               # e.g. "CUST-001"
    title: str
    source: str                            # DOC-NNN of source document
    source_quote: str | None = None        # verbatim from customer
    priority: str = "must"                # must | should | could | wont
    status: str = "draft"                 # draft | confirmed | rejected | deferred
    type: str = "functional"               # functional | non-functional | security | operational
    customer: str | None = None
    opportunity: str | None = None
    created_at: str | None = None
    created_by: str | None = None
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "source_quote": self.source_quote,
            "priority": self.priority,
            "status": self.status,
            "type": self.type,
            "customer": self.customer,
            "opportunity": self.opportunity,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "notes": self.notes,
        }


@dataclass
class Evidence:
    """An evidence record showing a test or requirement has been verified."""

    id: str                               # e.g. "EVD-001"
    title: str
    doc_id: str                            # filename of the document that produced this
    test_id: str | None = None             # TEST-NNN this evidence verifies
    requirement_id: str | None = None      # REQ-NNN this evidence verifies
    type: str = "test_result"             # test_result | screenshot | log | certificate
    status: str = "pending"               # pending | passed | failed | blocked
    result: str | None = None
    captured_at: str | None = None
    captured_by: str | None = None
    artifact_path: str | None = None       # path to evidence file

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "doc_id": self.doc_id,
            "test_id": self.test_id,
            "requirement_id": self.requirement_id,
            "type": self.type,
            "status": self.status,
            "result": self.result,
            "captured_at": self.captured_at,
            "captured_by": self.captured_by,
            "artifact_path": self.artifact_path,
        }


@dataclass
class Deliverable:
    """A formal deliverable with stage/gate/owner metadata."""

    id: str                               # filename
    stage: str
    gate: str | None = None               # which gate this satisfies
    owner: str | None = None
    mandatory: bool = True
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    status: DocumentStatus = DocumentStatus.DRAFT
    version: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "stage": self.stage,
            "gate": self.gate,
            "owner": self.owner,
            "mandatory": self.mandatory,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "status": self.status.value if isinstance(self.status, DocumentStatus) else self.status,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class DocumentLink:
    """A typed relationship between two documents."""

    from_doc: str     # source doc_id (filename)
    to_doc: str       # target doc_id (filename)
    link_type: LinkType
    label: str | None = None   # human-readable label

    def to_dict(self) -> dict[str, Any]:
        return {
            "from": self.from_doc,
            "to": self.to_doc,
            "type": self.link_type.value if isinstance(self.link_type, LinkType) else self.link_type,
            "label": self.label,
        }


@dataclass
class LineageEntry:
    """A single step in a document lineage chain."""

    from_doc: str
    to_doc: str
    link_type: str
    # Spine entities
    customer_requirement_id: str | None = None  # CUST-NNN
    requirement_id: str | None = None           # REQ-NNN
    component_id: str | None = None            # COMP-NNN
    decision_id: str | None = None             # DEC-NNN
    task_id: str | None = None                 # TASK-NNN
    test_id: str | None = None                # TEST-NNN
    evidence_id: str | None = None             # EVD-NNN
    # Cross-cutting entities
    assumption_id: str | None = None          # ASM-NNN
    dependency_id: str | None = None           # DEP-NNN
    change_id: str | None = None              # CHG-NNN

    def to_dict(self) -> dict[str, Any]:
        return {
            "from": self.from_doc,
            "to": self.to_doc,
            "link_type": self.link_type,
            # Spine
            "customer_requirement_id": self.customer_requirement_id,
            "requirement_id": self.requirement_id,
            "component_id": self.component_id,
            "decision_id": self.decision_id,
            "task_id": self.task_id,
            "test_id": self.test_id,
            "evidence_id": self.evidence_id,
            # Cross-cutting
            "assumption_id": self.assumption_id,
            "dependency_id": self.dependency_id,
            "change_id": self.change_id,
        }
