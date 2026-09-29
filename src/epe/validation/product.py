"""Product gate predicates."""

from __future__ import annotations

from pathlib import Path


def definition_complete(*, project_paths) -> str:
    p = project_paths.project_product / "definition.md"
    if not p.exists():
        return "fail"
    text = p.read_text(encoding="utf-8")
    required = [
        "Product name and one-line description",
        "Problem statement",
        "Target users and personas",
        "Use cases",
        "Out-of-scope",
        "Differentiators",
    ]
    return "pass" if all(h in text for h in required) else "fail"


def readiness_complete(*, project_paths) -> str:
    p = project_paths.project_product / "readiness.md"
    if not p.exists():
        return "fail"
    text = p.read_text(encoding="utf-8")
    required = [
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
    ]
    return "pass" if all(h in text for h in required) else "fail"
