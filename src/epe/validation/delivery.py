"""Delivery gate predicates."""

from __future__ import annotations


def deployment_complete(*, project_paths) -> str:
    p = project_paths.project_delivery / "plan.md"
    if not p.exists():
        return "fail"
    text = p.read_text(encoding="utf-8")
    return "pass" if all(h in text for h in ["Sequencing", "Milestones", "Owners"]) else "fail"


def acceptance_complete(*, project_paths) -> str:
    p = project_paths.project_delivery / "acceptance.md"
    if not p.exists():
        return "fail"
    text = p.read_text(encoding="utf-8")
    return "pass" if "Sign-off" in text and "Executed tests" in text else "fail"
