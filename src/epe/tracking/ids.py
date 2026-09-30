"""Canonical ID patterns for EPE lifecycle entities.

This module is the single source of truth for all typed ID patterns used across
the tracking, traceability, and lineage systems. All 13 entity types are defined
here with their regex patterns and valid edge types.

Entity hierarchy (traceability spine):
    CUST → REQ → COMP → DEC → TEST → EVD → ACCEPTANCE → AS-BUILT

Cross-cutting relationships:
    REQ ── affected_by ── ASM
    REQ ── blocked_by ─── DEP
    REQ ── changed_by ─── CHG
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class IDPattern:
    """A typed ID pattern with metadata for the EPE lifecycle."""

    prefix: str
    regex: re.Pattern
    entity_name: str
    edge_types: list[str]


ID_PATTERNS: dict[str, IDPattern] = {
    # Core lifecycle spine
    "CUST": IDPattern(
        "CUST",
        re.compile(r"\bCUST-\d+\b"),
        "Customer Requirement",
        ["refines"],  # CUST → REQ
    ),
    "REQ": IDPattern(
        "REQ",
        re.compile(r"\bREQ-\d+\b"),
        "Requirement",
        ["satisfied_by", "affected_by", "blocked_by", "changed_by"],  # REQ → COMP, ASM, DEP, CHG
    ),
    "CAP": IDPattern(
        "CAP",
        re.compile(r"\bCAP-\d+\b"),
        "Capability",
        ["supports"],  # CAP → REQ
    ),
    "COMP": IDPattern(
        "COMP",
        re.compile(r"\bCOMP-\d+\b"),
        "Solution Component",
        ["decided_by", "satisfied_by"],  # COMP ← DEC, REQ
    ),
    "DEC": IDPattern(
        "DEC",
        re.compile(r"\bDEC-\d+\b"),
        "Decision",
        ["validated_by"],  # DEC → TEST
    ),
    "TASK": IDPattern(
        "TASK",
        re.compile(r"\bTASK-\d+\b"),
        "Delivery Task",
        ["implements"],  # TASK → COMP
    ),
    "TEST": IDPattern(
        "TEST",
        re.compile(r"\bTEST-\d+\b"),
        "Acceptance Test",
        ["verified_by"],  # TEST → EVD
    ),
    "EVD": IDPattern(
        "EVD",
        re.compile(r"\bEVD-\d+\b"),
        "Evidence",
        ["accepted_by"],  # EVD → ACCEPTANCE
    ),
    # Supporting entities (no spine edges)
    "RSK": IDPattern(
        "RSK",
        re.compile(r"\bRSK-\d+\b"),
        "Risk",
        [],  # standalone
    ),
    "Q": IDPattern(
        "Q",
        re.compile(r"\bQ-\d+\b"),
        "Open Question",
        [],  # standalone
    ),
    # Cross-cutting entities
    "ASM": IDPattern(
        "ASM",
        re.compile(r"\bASM-\d+\b"),
        "Assumption",
        ["affects"],  # ASM → REQ
    ),
    "DEP": IDPattern(
        "DEP",
        re.compile(r"\bDEP-\d+\b"),
        "Dependency",
        ["blocks"],  # DEP → REQ
    ),
    "CHG": IDPattern(
        "CHG",
        re.compile(r"\bCHG-\d+\b"),
        "Change Request",
        ["modifies"],  # CHG → REQ
    ),
}


def scan_ids(text: str, prefix: str) -> set[str]:
    """Extract all IDs of the given type from text.

    Args:
        text: The text to scan.
        prefix: The ID prefix (e.g., "REQ", "CUST", "ASM").

    Returns:
        Set of matching IDs (e.g., {"REQ-001", "REQ-002"}).
    """
    pattern = ID_PATTERNS.get(prefix)
    if pattern is None:
        return set()
    return set(pattern.regex.findall(text))


def scan_all_ids(text: str) -> dict[str, list[str]]:
    """Extract all typed IDs from text.

    Returns:
        Dict mapping prefix → sorted list of unique IDs.
    """
    result: dict[str, list[str]] = {}
    for prefix, pattern in ID_PATTERNS.items():
        ids = pattern.regex.findall(text)
        if ids:
            result[prefix] = sorted(set(ids))
    return result
