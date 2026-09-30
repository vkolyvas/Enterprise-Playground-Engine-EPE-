"""Document completeness validator — checks that required sections and metadata are present.

Unlike ``content.py`` which validates one document at a time, this validator
operates on the entire project and produces per-stage and per-gate completeness
assessments.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

from epe.core.frontmatter import read_doc
from epe.tracking.registry import DocumentRegistry
from epe.validation.engine import Finding, make_finding


# Per-document metadata requirements
_REQUIRED_FRONTMATTER = [
    "contract",
    "version",
    "stage",
    "status",
    "generated_at",
]

# Per-stage mandatory documents (filename → description)
_MANDATORY_DOCUMENTS: dict[str, dict[str, str]] = {
    "product": {
        "definition.md": "Product definition and problem statement",
        "catalog.md": "Capability catalog",
        "guardrails.md": "Technical and commercial guardrails",
        "readiness.md": "Product → Presales handover contract",
    },
    "presales": {
        "discovery.md": "Stakeholder and requirement discovery",
        "qualification.md": "Opportunity qualification",
        "scope.md": "Scoped requirements and fit/gap",
        "sow.md": "Statement of work",
        "handover.md": "Presales → Architecture handover",
    },
    "architecture": {
        "validation.md": "Requirement validation",
        "hld.md": "High-level design",
        "security.md": "Security architecture",
        "lld.md": "Low-level design",
        "cost.md": "Cost and sizing",
        "solution-baseline.md": "Architecture → Delivery solution baseline",
    },
    "delivery": {
        "plan.md": "Implementation plan",
        "test.md": "Test plan",
        "acceptance.md": "Acceptance test results",
        "onboarding.md": "Customer onboarding",
        "operations.md": "Operational runbook",
        "handover.md": "Customer handover",
        "feedback.md": "Delivery → Product feedback",
    },
}

# Map filename stem to contract for section lookup
_FILENAME_TO_CONTRACT: dict[str, str] = {
    "definition": "product.definition",
    "catalog": "product.catalog",
    "guardrails": "product.guardrails",
    "readiness": "product.readiness",
    "discovery": "presales.discovery",
    "qualification": "presales.qualification",
    "scope": "presales.scope",
    "sow": "presales.sow",
    "handover": "presales.handover",
    "validation": "architecture.validation",
    "hld": "architecture.hld",
    "security": "architecture.security",
    "lld": "architecture.lld",
    "cost": "architecture.cost",
    "solution_baseline": "architecture.solution_baseline",
    "plan": "delivery.plan",
    "test": "delivery.test",
    "acceptance": "delivery.acceptance",
    "onboarding": "delivery.onboarding",
    "operations": "delivery.operations",
    "handover_d": "delivery.handover",  # delivery/handover.md uses key handover_d
    "feedback": "delivery.feedback",
    # Governance entity files
    "MS-001": "governance.milestone",
    "TASK-001": "governance.task",
    "RFP-REQ-001": "governance.rfp_requirement",
    "DEL-001": "governance.deliverable",
    "APRV-001": "governance.approval",
    "STK-001": "governance.stakeholder",
}


# ---------------------------------------------------------------------------
# Document category separation (Issue 7 fix)
# ---------------------------------------------------------------------------

# Document category enum
class GovernanceDocumentCategory:
    """Document category for validation severity determination."""
    AUTHORITATIVE_ENTITY = "authoritative_entity"  # Entity files — WARNING if incomplete
    DERIVED_VIEW = "derived_view"                   # Auto-generated — never "missing"
    MANDATORY_PROJECT = "mandatory_project"          # Governance required — WARNING if missing
    OPTIONAL = "optional"                            # INFO if missing


# Governance entity files that should exist (authoritative data)
_GOVERNANCE_ENTITY_FILES: set[str] = {
    "entities/ms/MS-001.md",
    "entities/task/TASK-001.md",
    "entities/rfp-req/RFP-REQ-001.md",
    "entities/del/DEL-001.md",
    "entities/aprv/APRV-001.md",
    "entities/stk/STK-001.md",
}

# Derived governance views (auto-generated — never "missing")
_DERIVED_DOCUMENTS: set[str] = {
    "governance/milestone-register.md",
    "governance/task-register.md",
    "governance/rfp-obligations.md",
    "governance/traceability-matrix.md",
    "governance/governance.md",
    "architecture/solution-manager-cockpit.md",
    "product/product-control.md",
    "presales/presales-control.md",
    "delivery/delivery-control.md",
}

# Optional governance documents
_OPTIONAL_DOCUMENTS: set[str] = {
    "governance/decision-log.md",
    "governance/project-plan.md",
}


def _get_document_category(path: str) -> str:
    """Determine the validation category for a document path."""
    if path in _DERIVED_DOCUMENTS:
        return GovernanceDocumentCategory.DERIVED_VIEW
    if path in _GOVERNANCE_ENTITY_FILES:
        return GovernanceDocumentCategory.AUTHORITATIVE_ENTITY
    if path in _OPTIONAL_DOCUMENTS:
        return GovernanceDocumentCategory.OPTIONAL
    # Check if it's a stage mandatory doc
    for stage_docs in _MANDATORY_DOCUMENTS.values():
        if path in stage_docs:
            return GovernanceDocumentCategory.MANDATORY_PROJECT
    return GovernanceDocumentCategory.MANDATORY_PROJECT  # Default to mandatory project


def validate_document_completeness(
    artifact_path: Path,
    context: dict[str, Any],
) -> Iterable[Finding]:
    """Validate a single document's frontmatter completeness.

    Checks:
    - All required frontmatter fields present
    - Body has substantive content (> 100 chars)
    - Sections required by contract are present (delegates to content validator)
    - Document has a title
    """
    doc = read_doc(artifact_path)
    doc_id = artifact_path.name

    # Check required frontmatter
    for field in _REQUIRED_FRONTMATTER:
        if field not in doc.metadata or not doc.metadata[field]:
            yield make_finding(
                validator="completeness",
                severity="error",
                location=str(artifact_path),
                message=f"Required frontmatter field '{field}' is missing or empty.",
                remediation=f"Add '{field}' to the document YAML frontmatter.",
            )

    # Check document has a title
    title = doc.metadata.get("title")
    if not title and len(doc.body) < 20:
        yield make_finding(
            validator="completeness",
            severity="warning",
            location=str(artifact_path),
            message="Document has no title and body is empty or near-empty.",
            remediation="Add a 'title' field to frontmatter and add substantive content.",
        )

    # Check body is substantive (more than a scaffold)
    if len(doc.body.strip()) < 100:
        yield make_finding(
            validator="completeness",
            severity="warning",
            location=str(artifact_path),
            message="Document body is less than 100 characters — may be an empty scaffold.",
            remediation="Ensure the document has substantive content beyond headings.",
            kind="scaffold",
        )

    # Check contract-specific required sections using the content validator
    contract = doc.metadata.get("contract")
    if contract:
        from epe.validation.content import validate_content
        yield from validate_content(artifact_path, context)


def validate_stage_completeness(
    project_root: Path,
    stage: str,
    registry: DocumentRegistry,
) -> dict[str, Any]:
    """Assess the completeness of an entire stage.

    Returns a dict with:
    - mandatory_documents: list of mandatory filenames
    - present_documents: list of filenames that exist
    - missing_documents: list of missing mandatory filenames
    - optional_documents: list of optional documents present
    - completeness_score: 0.0–1.0 fraction of mandatory docs present
    - all_approved: bool — whether all mandatory docs are approved
    - findings: list of Finding dicts for missing/empty docs
    """
    mandatory = _MANDATORY_DOCUMENTS.get(stage, {})
    mandatory_names = set(mandatory.keys())
    stage_docs = registry.by_stage(stage)
    present_names = {d.path.name for d in stage_docs}

    missing = mandatory_names - present_names
    present_mandatory = mandatory_names & present_names

    # Check each present mandatory document for completeness
    findings = []
    for doc in stage_docs:
        if doc.path.name in mandatory_names:
            abs_path = project_root / doc.path
            fnd = list(validate_document_completeness(abs_path, {}))
            findings.extend(fnd)

    # For missing mandatory documents, report them
    for fname in missing:
        findings.append(
            make_finding(
                validator="completeness",
                severity="blocker",
                location=f"{stage}/",
                message=f"Mandatory document '{fname}' is missing for stage '{stage}'.",
                remediation=f"Generate or create {stage}/{fname}.",
                kind="missing_mandatory",
            )
        )

    completeness_score = len(present_mandatory) / len(mandatory_names) if mandatory_names else 1.0
    all_approved = all(d.is_approved for d in stage_docs if d.path.name in mandatory_names)

    return {
        "stage": stage,
        "mandatory_documents": sorted(mandatory_names),
        "present_documents": sorted(present_names & mandatory_names),
        "missing_documents": sorted(missing),
        "optional_documents": sorted(present_names - mandatory_names),
        "completeness_score": completeness_score,
        "all_approved": all_approved,
        "approved_count": sum(1 for d in stage_docs if d.is_approved and d.path.name in mandatory_names),
        "total_mandatory": len(mandatory_names),
        "findings": [f.to_dict() for f in findings],
    }


def validate_gate_completeness(
    project_root: Path,
    registry: DocumentRegistry,
) -> dict[str, Any]:
    """Assess gate readiness across all stages.

    Gate readiness states:
    - READY: all mandatory documents present and approved
    - BLOCKED: mandatory documents missing or not approved
    - WARNING: all mandatory docs present but not all approved
    - IN_PROGRESS: some mandatory docs present but incomplete
    """
    stages = ["product", "presales", "architecture", "delivery"]
    results = {}

    for stage in stages:
        completeness = validate_stage_completeness(project_root, stage, registry)
        score = completeness["completeness_score"]
        all_app = completeness["all_approved"]
        missing = completeness["missing_documents"]
        findings_blockers = [f for f in completeness["findings"] if f.get("severity") == "blocker"]

        if score >= 1.0 and all_app:
            readiness = "READY"
        elif score >= 1.0 and not all_app:
            readiness = "WARNING"  # docs present but not approved
        elif len(missing) > 0 or findings_blockers:
            readiness = "BLOCKED"
        else:
            readiness = "IN_PROGRESS"

        results[stage] = {
            "readiness": readiness,
            "completeness_score": score,
            "all_approved": all_app,
            "missing_documents": missing,
            "findings_count": len(completeness["findings"]),
            "blockers": len(findings_blockers),
            **completeness,
        }

    return results


def validate_all(
    project_root: Path,
    registry: DocumentRegistry | None = None,
) -> dict[str, Any]:
    """Run full completeness validation on a project.

    Returns dict with per-stage results and overall gate status.
    """
    if registry is None:
        registry = DocumentRegistry.from_project(project_root, project_root.name)

    gate_status = validate_gate_completeness(project_root, registry)

    overall_blockers = sum(r.get("blockers", 0) for r in gate_status.values())
    all_ready = all(r["readiness"] == "READY" for r in gate_status.values())

    return {
        "project_id": project_root.name,
        "overall_status": "READY" if all_ready and overall_blockers == 0 else "BLOCKED",
        "overall_blockers": overall_blockers,
        "gate_status": gate_status,
    }


def validate_governance_completeness(
    project_root: Path,
) -> dict[str, Any]:
    """Validate governance entity file completeness.

    Governance entities are authoritative data — they should exist and have
    complete frontmatter. However, governance completeness is WARNING severity,
    never BLOCKER (governance does NOT block stage transitions).

    Derived views (milestone-register.md, etc.) are NEVER checked as missing.
    """
    findings = []

    # Check entity directories exist
    entities_base = project_root / "entities"
    entity_dirs = ["ms", "task", "rfp-req", "del", "aprv", "stk"]

    for dir_name in entity_dirs:
        entity_dir = entities_base / dir_name
        if not entity_dir.is_dir():
            findings.append(
                make_finding(
                    validator="governance_completeness",
                    severity="warning",
                    location=str(entity_dir),
                    message=f"Governance entity directory '{dir_name}' does not exist.",
                    remediation=f"Create {entity_dir} to store entity files.",
                    kind="missing_entity_dir",
                )
            )
            continue

        # Check for at least one entity file
        entity_files = list(entity_dir.glob("*.md"))
        if not entity_files:
            findings.append(
                make_finding(
                    validator="governance_completeness",
                    severity="warning",
                    location=str(entity_dir),
                    message=f"No entity files found in '{dir_name}/' directory.",
                    remediation=f"Create entity files in {entity_dir}/ to define governance data.",
                    kind="empty_entity_dir",
                )
            )

        # Check each entity file for required frontmatter
        for entity_file in entity_files:
            doc = None
            try:
                doc = read_doc(entity_file)
            except Exception as exc:
                findings.append(
                    make_finding(
                        validator="governance_completeness",
                        severity="warning",
                        location=str(entity_file),
                        message=f"Failed to read entity file: {exc}",
                        remediation=f"Fix or remove corrupted file {entity_file}",
                        kind="corrupt_entity_file",
                    )
                )
                continue

            # Check required fields based on entity type
            required_fields = ["title", "status"]
            if dir_name == "ms":
                required_fields.extend(["phase", "baseline_end"])
            elif dir_name == "task":
                required_fields.extend(["status", "baseline_end"])

            for field in required_fields:
                if not doc.get(field):
                    findings.append(
                        make_finding(
                            validator="governance_completeness",
                            severity="warning",
                            location=str(entity_file),
                            message=f"Entity file missing required field '{field}'.",
                            remediation=f"Add '{field}' to the frontmatter of {entity_file}",
                            kind="incomplete_entity",
                        )
                    )

    # Check derived documents exist (WARNING if missing, never BLOCKER)
    for doc_path in _DERIVED_DOCUMENTS:
        full_path = project_root / doc_path
        if not full_path.exists():
            findings.append(
                make_finding(
                    validator="governance_completeness",
                    severity="warning",
                    location=str(full_path),
                    message=f"Derived governance view '{doc_path}' is missing.",
                    remediation=f"Run governance engine to generate {doc_path}",
                    kind="missing_derived",
                )
            )

    # Summary
    warning_count = sum(1 for f in findings if f.severity == "warning")
    error_count = sum(1 for f in findings if f.severity == "error")

    return {
        "project_id": project_root.name,
        "governance_complete": warning_count == 0 and error_count == 0,
        "warning_count": warning_count,
        "error_count": error_count,
        "severity": "error" if error_count > 0 else "warning" if warning_count > 0 else "ok",
        "findings": [f.to_dict() for f in findings],
    }
