"""Validation engine core types and orchestrator."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

from epe.core.frontmatter import read_doc
from epe.core.logging import get_logger

logger = get_logger("validation.engine")


@dataclass
class Finding:
    id: str
    validator: str
    severity: str             # info | warning | error | blocker
    location: str
    message: str
    remediation: str | None = None
    kind: str | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ValidationReport:
    contract: str
    project_id: str
    artifact_path: str
    validated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    validators: list[str] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    @property
    def verdict(self) -> str:
        if any(f.severity == "blocker" for f in self.findings):
            return "fail"
        if any(f.severity == "error" for f in self.findings):
            return "fail"
        return "pass"

    def to_dict(self) -> dict:
        return {
            "contract": self.contract,
            "project_id": self.project_id,
            "artifact_path": self.artifact_path,
            "validated_at": self.validated_at,
            "validators": self.validators,
            "verdict": self.verdict,
            "summary": self._summary(),
            "findings": [f.to_dict() for f in self.findings],
        }

    def _summary(self) -> dict[str, int]:
        out = {"info": 0, "warning": 0, "error": 0, "blocker": 0}
        for f in self.findings:
            out[f.severity] = out.get(f.severity, 0) + 1
        return out


def make_finding(
    *,
    validator: str,
    severity: str,
    location: str,
    message: str,
    remediation: str | None = None,
    kind: str | None = None,
) -> Finding:
    return Finding(
        id=f"F-{uuid.uuid4().hex[:8].upper()}",
        validator=validator,
        severity=severity,
        location=location,
        message=message,
        remediation=remediation,
        kind=kind,
    )


# Per-stage required sections (mirrors docs/OUTPUT_CONTRACTS.md)
REQUIRED_SECTIONS: dict[str, list[str]] = {
    "product.definition": [
        "Product name and one-line description",
        "Problem statement",
        "Target users and personas",
        "Use cases",
        "Out-of-scope",
        "Differentiators",
        "Evidence references",
    ],
    "product.catalog": [],   # catalog is a table; validated by content rules
    "product.guardrails": [
        "Technical limits",
        "Compliance posture",
        "Data residency",
        "Commercial constraints",
    ],
    "product.readiness": [
        "What is the product?",
        "Who is it for?",
        "What problems does it solve?",
        "What does it contain?",
        "What does it NOT contain?",
        "What can Presales sell?",
        "What requires Architecture?",
        "What are the technical limits?",
        "What are the commercial constraints?",
        "What evidence exists?",
        "What is configurable?",
        "What is custom?",
    ],
    "presales.discovery": [
        "Stakeholders",
        "Business objectives",
        "Current state",
        "Drivers",
        "Timeline",
        "Success criteria",
    ],
    "presales.qualification": ["Budget", "Authority", "Need", "Timeline", "Fit", "Verdict"],
    "presales.scope": [
        "In-scope",
        "Out-of-scope",
        "Assumptions",
        "Dependencies",
        "Product capabilities",
        "Product gaps",
        "Custom requirements",
        "Integrations",
        "Security",
        "SLA",
        "Commercial constraints",
    ],
    "presales.sow": [
        "Parties",
        "Scope reference",
        "Deliverables",
        "Timeline",
        "Acceptance",
        "Pricing summary",
        "Assumptions",
        "Signatures",
    ],
    "presales.handover": [
        "Opportunity",
        "Customer",
        "Business Objective",
        "Confirmed Requirements",
        "Technical Requirements",
        "Non-Functional Requirements",
        "Assumptions",
        "Constraints",
        "Product Capabilities Used",
        "Product Gaps",
        "Custom Requirements",
        "Integrations",
        "Security Requirements",
        "SLA Requirements",
        "Commercial Constraints",
        "Open Questions",
        "Architecture Decisions Required",
        "Acceptance Criteria",
    ],
    "architecture.validation": ["Per-requirement validation", "Findings"],
    "architecture.hld": [
        "Drivers", "Constraints", "Options considered",
        "Selected option", "Logical components", "Data flows",
        "NFR mapping", "Decision references",
    ],
    "architecture.security": [
        "Threat model", "Controls", "Identity", "Data protection",
        "Network", "Logging", "Audit", "Compliance",
    ],
    "architecture.lld": [
        "Component design", "Interfaces", "Data models",
        "Configurations", "Failure modes", "Runbook stubs",
    ],
    "architecture.cost": [
        "Line items", "Assumptions", "Ranges", "Optimization opportunities",
    ],
    "architecture.blueprint": [
        "Components", "Implementation tasks", "Test plan",
        "Rollout strategy", "Acceptance criteria",
        "Risks and mitigations", "Dependencies",
    ],
    "delivery.plan": [
        "Sequencing", "Milestones", "Owners", "Dependencies", "Prerequisites",
    ],
    "delivery.test": ["Per-test mapping"],
    "delivery.acceptance": ["Executed tests", "Evidence", "Sign-off"],
    "delivery.onboarding": ["Onboarding steps", "Training plan", "Support contacts"],
    "delivery.operations": ["Monitoring", "Alerting", "SLO/SLA", "Runbooks", "Escalation"],
    "delivery.handover": ["Customer handover"],
    "delivery.feedback": [
        "Incidents", "Cost variance", "Usage telemetry",
        "Deployment problems", "Customer feedback", "Operational lessons",
    ],
}


ValidatorFn = Callable[[Path, dict[str, Any]], Iterable[Finding]]


def run_validators(
    artifact_path: Path,
    *,
    validators: list[str] | None = None,
    project_paths=None,
) -> ValidationReport:
    """Run the named validators (or all by default) against an artifact."""
    from epe.validation.structural import validate_structural
    from epe.validation.content import validate_content
    from epe.validation.security import validate_security
    from epe.validation.traceability import validate_traceability
    from epe.validation.consistency import validate_consistency

    doc = read_doc(artifact_path)
    contract = doc.metadata.get("contract", "(unknown)")
    project_id = doc.metadata.get("project_id", "(unknown)")

    validators = validators or [
        "structural", "content", "traceability", "consistency", "security"
    ]
    report = ValidationReport(
        contract=contract,
        project_id=project_id,
        artifact_path=str(artifact_path),
        validators=list(validators),
    )

    context: dict[str, Any] = {"doc": doc, "project_paths": project_paths}
    mapping: dict[str, ValidatorFn] = {
        "structural": validate_structural,
        "content": validate_content,
        "traceability": validate_traceability,
        "consistency": validate_consistency,
        "security": validate_security,
    }
    for v in validators:
        fn = mapping.get(v)
        if not fn:
            continue
        for f in fn(artifact_path, context):
            report.add(f)
    return report


def run_all(artifact_path: Path, *, project_paths=None) -> ValidationReport:
    return run_validators(artifact_path, project_paths=project_paths)


def write_report(report: ValidationReport, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = Path(report.artifact_path).with_suffix(".yaml").name
    path = output_dir / f"{name}.validation.yaml"
    payload = report.to_dict()
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
