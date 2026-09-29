"""Architecture gate predicates."""

from __future__ import annotations

import re


def validation_complete(*, project_paths) -> str:
    p = project_paths.project_architecture / "validation.md"
    if not p.exists():
        return "fail"
    return "pass"


def hld_complete(*, project_paths) -> str:
    p = project_paths.project_architecture / "hld.md"
    if not p.exists():
        return "fail"
    text = p.read_text(encoding="utf-8")
    needed = ["Drivers", "Constraints", "Options considered",
              "Selected option", "Logical components", "Decision references"]
    if not all(h in text for h in needed):
        return "fail"
    if not re.search(r"\bCOMP-\d+\b", text):
        return "fail"
    return "pass"


def lld_complete(*, project_paths) -> str:
    p = project_paths.project_architecture / "lld.md"
    if not p.exists():
        return "fail"
    text = p.read_text(encoding="utf-8")
    needed = ["Component design", "Interfaces", "Data models",
              "Configurations", "Failure modes"]
    return "pass" if all(h in text for h in needed) else "fail"
