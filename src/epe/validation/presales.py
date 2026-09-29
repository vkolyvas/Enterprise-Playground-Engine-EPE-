"""Presales gate predicates."""

from __future__ import annotations

import re


def _has_id(text: str, prefix: str) -> bool:
    return re.search(rf"\b{prefix}-\d+\b", text) is not None


def qualification_complete(*, project_paths) -> str:
    p = project_paths.project_presales / "qualification.md"
    if not p.exists():
        return "fail"
    text = p.read_text(encoding="utf-8")
    needed = ["Budget", "Authority", "Need", "Timeline", "Fit", "Verdict"]
    return "pass" if all(h in text for h in needed) else "fail"


def scope_complete(*, project_paths) -> str:
    p = project_paths.project_presales / "scope.md"
    if not p.exists():
        return "fail"
    text = p.read_text(encoding="utf-8")
    needed = ["In-scope", "Out-of-scope", "Assumptions", "Dependencies",
              "Product capabilities", "Security", "SLA"]
    return "pass" if all(h in text for h in needed) else "fail"


def handover_complete(*, project_paths) -> str:
    p = project_paths.project_presales / "handover.md"
    if not p.exists():
        return "fail"
    text = p.read_text(encoding="utf-8")
    needed = [
        "Opportunity", "Customer", "Business Objective",
        "Confirmed Requirements", "Technical Requirements",
        "Non-Functional Requirements", "Assumptions", "Constraints",
        "Product Capabilities Used", "Security Requirements",
        "SLA Requirements", "Open Questions",
        "Architecture Decisions Required", "Acceptance Criteria",
    ]
    if not all(h in text for h in needed):
        return "fail"
    if not _has_id(text, "REQ"):
        return "fail"
    return "pass"
