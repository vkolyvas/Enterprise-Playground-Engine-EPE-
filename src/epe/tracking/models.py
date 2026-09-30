"""Core models for the lifecycle document operating system.

These models provide the traceability spine: cross-stage document lineage
that lets any requirement be traced from CustomerRequirement (Presales)
through SolutionComponent (Architecture) to DeliveryTask (Delivery) to
AcceptanceTest (Delivery) to Evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
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
    # Governance entities
    milestones: list[str] = field(default_factory=list)       # MS-NNN
    rfp_requirements: list[str] = field(default_factory=list)  # RFP-REQ-NNN
    deliverables: list[str] = field(default_factory=list)     # DEL-NNN
    approvals: list[str] = field(default_factory=list)        # APRV-NNN
    stakeholders: list[str] = field(default_factory=list)     # STK-NNN

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
            # Governance entities
            "milestones": self.milestones,
            "rfp_requirements": self.rfp_requirements,
            "deliverables": self.deliverables,
            "approvals": self.approvals,
            "stakeholders": self.stakeholders,
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


# ---------------------------------------------------------------------------
# Governance enums (Issue 4/5/6 corrections)
# ---------------------------------------------------------------------------


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"


class Priority(str, Enum):
    MUST = "must"
    SHOULD = "should"
    COULD = "could"


class MilestoneStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    MISSED = "missed"
    AT_RISK = "at_risk"


class RfpStatus(str, Enum):
    UNADDRESSED = "unaddressed"
    IN_PROGRESS = "in_progress"
    SATISFIED = "satisfied"
    WAIVED = "waived"
    DEVIATED = "deviated"


class DeliverableStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ApprovalType(str, Enum):
    GATE = "gate"
    DOCUMENT = "document"
    MILESTONE = "milestone"
    DELIVERABLE = "deliverable"


class ApprovalDecision(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    CONDITIONAL = "conditional"


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class StakeholderStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"


# ---------------------------------------------------------------------------
# Governance entities — full models with scheduling and critical-path
# ---------------------------------------------------------------------------


@dataclass
class Deliverable:
    """A formal deliverable with full traceability links and scheduling."""

    # Required fields first (no defaults)
    id: str                               # e.g. "DEL-001"
    title: str
    stage: str                            # product | presales | architecture | delivery

    # Optional fields (with defaults)
    description: str | None = None
    mandatory: bool = True
    owner: str | None = None
    status: DeliverableStatus = DeliverableStatus.PENDING
    acceptance_criteria: str | None = None
    completion_criteria: str | None = None
    baseline_end: date | None = None
    forecast_end: date | None = None
    actual_end: date | None = None
    milestone_ref: str | None = None     # MS-NNN
    requirement_refs: list[str] = field(default_factory=list)   # REQ-NNN
    rfp_requirement_refs: list[str] = field(default_factory=list)  # RFP-REQ-NNN
    component_refs: list[str] = field(default_factory=list)     # COMP-NNN
    task_refs: list[str] = field(default_factory=list)          # TASK-NNN
    test_refs: list[str] = field(default_factory=list)          # TEST-NNN
    evidence_refs: list[str] = field(default_factory=list)      # EVD-NNN
    approval_refs: list[str] = field(default_factory=list)     # APRV-NNN
    created_date: datetime | None = None
    updated_date: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "stage": self.stage,
            "mandatory": self.mandatory,
            "owner": self.owner,
            "status": self.status.value if isinstance(self.status, DeliverableStatus) else self.status,
            "acceptance_criteria": self.acceptance_criteria,
            "completion_criteria": self.completion_criteria,
            "baseline_end": str(self.baseline_end) if self.baseline_end else None,
            "forecast_end": str(self.forecast_end) if self.forecast_end else None,
            "actual_end": str(self.actual_end) if self.actual_end else None,
            "milestone_ref": self.milestone_ref,
            "requirement_refs": self.requirement_refs,
            "rfp_requirement_refs": self.rfp_requirement_refs,
            "component_refs": self.component_refs,
            "task_refs": self.task_refs,
            "test_refs": self.test_refs,
            "evidence_refs": self.evidence_refs,
            "approval_refs": self.approval_refs,
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "updated_date": self.updated_date.isoformat() if self.updated_date else None,
        }


@dataclass
class Task:
    """Delivery task with full scheduling and critical-path fields."""

    id: str                               # TASK-NNN
    title: str
    description: str | None = None
    owner: str | None = None
    stage: str = "delivery"              # delivery | architecture | presales
    status: TaskStatus = TaskStatus.TODO
    completion_criteria: str | None = None

    # THREE date types (Issue 5: baseline/forecast/actual)
    baseline_start: date | None = None
    baseline_end: date | None = None
    forecast_start: date | None = None
    forecast_end: date | None = None
    actual_start: date | None = None
    actual_end: date | None = None

    priority: Priority = Priority.MUST
    due_date: date | None = None

    # Multi-entity traceability (Issue 6)
    milestone_ref: str | None = None     # MS-NNN
    rfp_requirement_refs: list[str] = field(default_factory=list)  # RFP-REQ-NNN
    requirement_refs: list[str] = field(default_factory=list)    # REQ-NNN
    component_refs: list[str] = field(default_factory=list)       # COMP-NNN
    dependency_refs: list[str] = field(default_factory=list)      # DEP-NNN
    risk_refs: list[str] = field(default_factory=list)           # RSK-NNN
    decision_refs: list[str] = field(default_factory=list)        # DEC-NNN
    deliverable_refs: list[str] = field(default_factory=list)    # DEL-NNN

    # Blocking relationships
    blocked_by: list[str] = field(default_factory=list)   # TASK-NNN blocking this
    blocking: list[str] = field(default_factory=list)    # TASK-NNN this blocks

    # Critical-path model (Issue 4)
    critical: bool = False
    float_days: int | None = None
    blocking_task: bool = False

    created_date: datetime | None = None
    updated_date: datetime | None = None

    @property
    def schedule_variance_days(self) -> int | None:
        """Schedule variance: forecast_end - baseline_end in days."""
        if self.forecast_end and self.baseline_end:
            return (self.forecast_end - self.baseline_end).days
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "owner": self.owner,
            "stage": self.stage,
            "status": self.status.value if isinstance(self.status, TaskStatus) else self.status,
            "completion_criteria": self.completion_criteria,
            "baseline_start": str(self.baseline_start) if self.baseline_start else None,
            "baseline_end": str(self.baseline_end) if self.baseline_end else None,
            "forecast_start": str(self.forecast_start) if self.forecast_start else None,
            "forecast_end": str(self.forecast_end) if self.forecast_end else None,
            "actual_start": str(self.actual_start) if self.actual_start else None,
            "actual_end": str(self.actual_end) if self.actual_end else None,
            "schedule_variance_days": self.schedule_variance_days,
            "priority": self.priority.value if isinstance(self.priority, Priority) else self.priority,
            "due_date": str(self.due_date) if self.due_date else None,
            "milestone_ref": self.milestone_ref,
            "rfp_requirement_refs": self.rfp_requirement_refs,
            "requirement_refs": self.requirement_refs,
            "component_refs": self.component_refs,
            "dependency_refs": self.dependency_refs,
            "risk_refs": self.risk_refs,
            "decision_refs": self.decision_refs,
            "deliverable_refs": self.deliverable_refs,
            "blocked_by": self.blocked_by,
            "blocking": self.blocking,
            "critical": self.critical,
            "float_days": self.float_days,
            "blocking_task": self.blocking_task,
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "updated_date": self.updated_date.isoformat() if self.updated_date else None,
        }


@dataclass
class Milestone:
    """Project milestone with critical-path and baseline/forecast/actual tracking."""

    id: str                               # MS-NNN
    title: str
    description: str | None = None
    phase: str | None = None              # P1, P2, P3, P4, P5, P6
    gate_ref: str | None = None           # gate this milestone satisfies
    owner: str | None = None
    status: MilestoneStatus = MilestoneStatus.PENDING

    # THREE date types (Issue 5)
    baseline_start: date | None = None
    baseline_end: date | None = None
    forecast_start: date | None = None
    forecast_end: date | None = None
    actual_start: date | None = None
    actual_end: date | None = None

    # Critical-path model (Issue 4)
    critical: bool = False
    float_days: int | None = None
    blocking: bool = False

    depends_on: list[str] = field(default_factory=list)  # MS-NNN
    task_refs: list[str] = field(default_factory=list)   # TASK-NNN
    deliverable_refs: list[str] = field(default_factory=list)  # DEL-NNN
    test_refs: list[str] = field(default_factory=list)   # TEST-NNN
    approval_refs: list[str] = field(default_factory=list)  # APRV-NNN

    created_date: datetime | None = None
    updated_date: datetime | None = None

    @property
    def schedule_variance_days(self) -> int | None:
        """Schedule variance: forecast_end - baseline_end in days."""
        if self.forecast_end and self.baseline_end:
            return (self.forecast_end - self.baseline_end).days
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "phase": self.phase,
            "gate_ref": self.gate_ref,
            "owner": self.owner,
            "status": self.status.value if isinstance(self.status, MilestoneStatus) else self.status,
            "baseline_start": str(self.baseline_start) if self.baseline_start else None,
            "baseline_end": str(self.baseline_end) if self.baseline_end else None,
            "forecast_start": str(self.forecast_start) if self.forecast_start else None,
            "forecast_end": str(self.forecast_end) if self.forecast_end else None,
            "actual_start": str(self.actual_start) if self.actual_start else None,
            "actual_end": str(self.actual_end) if self.actual_end else None,
            "schedule_variance_days": self.schedule_variance_days,
            "critical": self.critical,
            "float_days": self.float_days,
            "blocking": self.blocking,
            "depends_on": self.depends_on,
            "task_refs": self.task_refs,
            "deliverable_refs": self.deliverable_refs,
            "test_refs": self.test_refs,
            "approval_refs": self.approval_refs,
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "updated_date": self.updated_date.isoformat() if self.updated_date else None,
        }


@dataclass
class RfpRequirement:
    """An RFP obligation that can link to multiple entity types (Issue 6 fix)."""

    id: str                               # RFP-REQ-NNN
    title: str
    description: str
    rfp_id: str                           # DOC-NNN of RFP source document
    source_quote: str | None = None
    page_reference: str | None = None
    mandatory: bool = True
    priority: Priority = Priority.MUST
    category: str | None = None          # security | functional | performance | etc.
    owner: str | None = None
    responsible: str | None = None
    status: RfpStatus = RfpStatus.UNADDRESSED
    due_date: date | None = None
    contractual_date: date | None = None
    evidence_required: bool = True
    evidence_refs: list[str] = field(default_factory=list)  # EVD-NNN

    # CRITICAL FIX (Issue 6): Links to MULTIPLE entity types
    customer_refs: list[str] = field(default_factory=list)     # CUST-NNN
    requirement_refs: list[str] = field(default_factory=list)  # REQ-NNN
    deliverable_refs: list[str] = field(default_factory=list)  # DEL-NNN
    milestone_refs: list[str] = field(default_factory=list)   # MS-NNN
    task_refs: list[str] = field(default_factory=list)       # TASK-NNN
    test_refs: list[str] = field(default_factory=list)       # TEST-NNN
    approval_refs: list[str] = field(default_factory=list)   # APRV-NNN

    contractual_commitment: str | None = None
    impact: str | None = None
    created_date: datetime | None = None
    updated_date: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "rfp_id": self.rfp_id,
            "source_quote": self.source_quote,
            "page_reference": self.page_reference,
            "mandatory": self.mandatory,
            "priority": self.priority.value if isinstance(self.priority, Priority) else self.priority,
            "category": self.category,
            "owner": self.owner,
            "responsible": self.responsible,
            "status": self.status.value if isinstance(self.status, RfpStatus) else self.status,
            "due_date": str(self.due_date) if self.due_date else None,
            "contractual_date": str(self.contractual_date) if self.contractual_date else None,
            "evidence_required": self.evidence_required,
            "evidence_refs": self.evidence_refs,
            "customer_refs": self.customer_refs,
            "requirement_refs": self.requirement_refs,
            "deliverable_refs": self.deliverable_refs,
            "milestone_refs": self.milestone_refs,
            "task_refs": self.task_refs,
            "test_refs": self.test_refs,
            "approval_refs": self.approval_refs,
            "contractual_commitment": self.contractual_commitment,
            "impact": self.impact,
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "updated_date": self.updated_date.isoformat() if self.updated_date else None,
        }


@dataclass
class Approval:
    """A formal approval record — cross-cutting across all stages."""

    # Required fields first (no defaults)
    id: str                               # APRV-NNN
    title: str
    approval_type: ApprovalType

    # Optional fields (with defaults)
    description: str | None = None
    target_id: str | None = None         # Gate ID, document path, MS-NNN, DEL-NNN
    approver: str | None = None
    requested_by: str | None = None
    decision_by: str | None = None
    request_date: date | None = None
    decision_date: date | None = None
    deadline: date | None = None
    decision: ApprovalDecision | None = None
    decision_notes: str | None = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    milestone_ref: str | None = None
    deliverable_ref: str | None = None
    rfp_requirement_refs: list[str] = field(default_factory=list)  # RFP-REQ-NNN
    created_date: datetime | None = None
    updated_date: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "approval_type": self.approval_type.value if isinstance(self.approval_type, ApprovalType) else self.approval_type,
            "target_id": self.target_id,
            "approver": self.approver,
            "requested_by": self.requested_by,
            "decision_by": self.decision_by,
            "request_date": str(self.request_date) if self.request_date else None,
            "decision_date": str(self.decision_date) if self.decision_date else None,
            "deadline": str(self.deadline) if self.deadline else None,
            "decision": self.decision.value if isinstance(self.decision, ApprovalDecision) else self.decision,
            "decision_notes": self.decision_notes,
            "status": self.status.value if isinstance(self.status, ApprovalStatus) else self.status,
            "milestone_ref": self.milestone_ref,
            "deliverable_ref": self.deliverable_ref,
            "rfp_requirement_refs": self.rfp_requirement_refs,
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "updated_date": self.updated_date.isoformat() if self.updated_date else None,
        }


@dataclass
class Stakeholder:
    """Project stakeholder with approval authority."""

    id: str                               # STK-NNN
    name: str
    role: str                             # sponsor | architect | PM | reviewer | etc.
    contact: str | None = None
    stage_ownership: list[str] = field(default_factory=list)  # product | presales | etc.
    approval_authority: list[str] = field(default_factory=list)  # APRV-NNN they can grant
    delegate: str | None = None           # who can act on their behalf
    status: StakeholderStatus = StakeholderStatus.ACTIVE
    created_date: datetime | None = None
    updated_date: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "contact": self.contact,
            "stage_ownership": self.stage_ownership,
            "approval_authority": self.approval_authority,
            "delegate": self.delegate,
            "status": self.status.value if isinstance(self.status, StakeholderStatus) else self.status,
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "updated_date": self.updated_date.isoformat() if self.updated_date else None,
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
    # Governance entities
    milestone_id: str | None = None           # MS-NNN
    rfp_requirement_id: str | None = None     # RFP-REQ-NNN
    deliverable_id: str | None = None         # DEL-NNN
    approval_id: str | None = None            # APRV-NNN
    stakeholder_id: str | None = None        # STK-NNN

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
            # Governance
            "milestone_id": self.milestone_id,
            "rfp_requirement_id": self.rfp_requirement_id,
            "deliverable_id": self.deliverable_id,
            "approval_id": self.approval_id,
            "stakeholder_id": self.stakeholder_id,
        }
