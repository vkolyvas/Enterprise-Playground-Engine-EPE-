"""Derived registry views — build registers from entity files.

This module provides functions to derive milestone-register.md, task-register.md,
rfp-obligations.md, and traceability-matrix.md from the authoritative entity files.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from epe.core.frontmatter import read_doc
from epe.tracking.ids import ID_PATTERNS, scan_ids


def load_entity_file(path: Path) -> dict[str, Any]:
    """Load an entity .md file and return its frontmatter + body.

    Returns a dict with frontmatter fields and 'body' key.
    """
    try:
        doc = read_doc(path)
        return {
            "path": path,
            **doc.metadata,
            "body": doc.body,
        }
    except Exception:
        return {"path": path, "body": ""}


def load_entity_dir(entity_dir: Path, id_prefix: str) -> list[dict[str, Any]]:
    """Load all entity files from a directory for a given ID prefix.

    For example, entities/ms/ with prefix "MILESTONE" loads MS-001.md, etc.
    """
    entities = []
    if not entity_dir.is_dir():
        return entities

    for md_file in sorted(entity_dir.glob("*.md")):
        entity_data = load_entity_file(md_file)
        # Extract the entity ID from filename
        entity_id = md_file.stem  # e.g. "MS-001"
        entity_data["entity_id"] = entity_id
        entity_data["id"] = entity_id
        entities.append(entity_data)

    return entities


def load_all_entities(project_root: Path) -> dict[str, list[dict[str, Any]]]:
    """Load all governance entity files from a project.

    Returns dict with keys: tasks, milestones, rfp_requirements, deliverables,
    approvals, stakeholders.
    """
    entities_base = project_root / "entities"

    return {
        "tasks": load_entity_dir(entities_base / "task", "TASK"),
        "milestones": load_entity_dir(entities_base / "ms", "MILESTONE"),
        "rfp_requirements": load_entity_dir(entities_base / "rfp-req", "RFP_REQ"),
        "deliverables": load_entity_dir(entities_base / "del", "DELIVERABLE"),
        "approvals": load_entity_dir(entities_base / "aprv", "APPROVAL"),
        "stakeholders": load_entity_dir(entities_base / "stk", "STAKEHOLDER"),
    }


def derive_milestone_register(entities: dict[str, list[dict[str, Any]]]) -> str:
    """Derive milestone-register.md content from milestone entities."""
    milestones = entities.get("milestones", [])
    lines = [
        "# Milestone Register",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Total Milestones:** {len(milestones)}",
        "",
        "| ID | Title | Phase | Gate | Owner | Status | Baseline End | Forecast End | Actual End | Variance | Critical |",
        "|----|-------|-------|------|-------|--------|---------------|--------------|-----------|----------|----------|",
    ]

    for ms in sorted(milestones, key=lambda x: x.get("baseline_end", "")):
        lines.append(_format_milestone_row(ms))

    return "\n".join(lines)


def _format_milestone_row(ms: dict[str, Any]) -> str:
    """Format a milestone row for the register table."""
    baseline_end = ms.get("baseline_end", "—")
    forecast_end = ms.get("forecast_end", "—")
    actual_end = ms.get("actual_end", "—")

    # Compute variance if both dates available
    variance = "—"
    if forecast_end and baseline_end and isinstance(forecast_end, str) and isinstance(baseline_end, str):
        try:
            fe = date.fromisoformat(forecast_end)
            be = date.fromisoformat(baseline_end)
            variance = str((fe - be).days)
        except ValueError:
            pass

    critical = "Yes" if ms.get("critical") else "No"
    blocking = "Yes" if ms.get("blocking") else "No"

    return (
        f"| {ms.get('id', '—')} "
        f"| {ms.get('title', '—')} "
        f"| {ms.get('phase', '—')} "
        f"| {ms.get('gate_ref', '—')} "
        f"| {ms.get('owner', '—')} "
        f"| {ms.get('status', 'pending')} "
        f"| {baseline_end} "
        f"| {forecast_end} "
        f"| {actual_end} "
        f"| {variance} "
        f"| {critical} ({blocking}) |"
    )


def derive_task_register(entities: dict[str, list[dict[str, Any]]]) -> str:
    """Derive task-register.md content from task entities."""
    tasks = entities.get("tasks", [])
    lines = [
        "# Task Register",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Total Tasks:** {len(tasks)}",
        "",
        "| ID | Title | Owner | Status | Priority | Baseline End | Forecast End | Actual End | Variance | Critical | Blocking | Blocked By |",
        "|----|-------|-------|--------|----------|---------------|--------------|-----------|----------|----------|----------|------------|",
    ]

    for task in sorted(tasks, key=lambda x: x.get("baseline_end", "")):
        lines.append(_format_task_row(task))

    return "\n".join(lines)


def _format_task_row(task: dict[str, Any]) -> str:
    """Format a task row for the register table."""
    baseline_end = task.get("baseline_end", "—")
    forecast_end = task.get("forecast_end", "—")
    actual_end = task.get("actual_end", "—")

    # Compute variance if both dates available
    variance = "—"
    if forecast_end and baseline_end and isinstance(forecast_end, str) and isinstance(baseline_end, str):
        try:
            fe = date.fromisoformat(forecast_end)
            be = date.fromisoformat(baseline_end)
            variance = str((fe - be).days)
        except ValueError:
            pass

    critical = "Yes" if task.get("critical") else "No"
    blocking = "Yes" if task.get("blocking_task") else "No"
    blocked_by = ", ".join(task.get("blocked_by", [])) or "—"

    return (
        f"| {task.get('id', '—')} "
        f"| {task.get('title', '—')} "
        f"| {task.get('owner', '—')} "
        f"| {task.get('status', 'todo')} "
        f"| {task.get('priority', 'must')} "
        f"| {baseline_end} "
        f"| {forecast_end} "
        f"| {actual_end} "
        f"| {variance} "
        f"| {critical} "
        f"| {blocking} "
        f"| {blocked_by} |"
    )


def derive_rfp_obligations(entities: dict[str, list[dict[str, Any]]]) -> str:
    """Derive rfp-obligations.md content from RFP requirement entities."""
    rfp_reqs = entities.get("rfp_requirements", [])
    lines = [
        "# RFP Obligations Register",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Total RFP Requirements:** {len(rfp_reqs)}",
        "",
        "| ID | Title | Mandatory | Priority | Status | Due Date | Contractual Date | Evidence Required | Links |",
        "|----|-------|-----------|----------|--------|----------|------------------|-------------------|-------|",
    ]

    for rfp in sorted(rfp_reqs, key=lambda x: x.get("due_date", "")):
        lines.append(_format_rfp_row(rfp))

    return "\n".join(lines)


def _format_rfp_row(rfp: dict[str, Any]) -> str:
    """Format an RFP requirement row for the register table."""
    mandatory = "Yes" if rfp.get("mandatory", True) else "No"
    evidence = "Yes" if rfp.get("evidence_required", True) else "No"

    # Build links string
    links = []
    for ref_field in ["requirement_refs", "deliverable_refs", "milestone_refs",
                      "task_refs", "test_refs", "approval_refs"]:
        refs = rfp.get(ref_field, [])
        if refs:
            links.extend(refs)
    links_str = ", ".join(sorted(set(links))) or "—"

    return (
        f"| {rfp.get('id', '—')} "
        f"| {rfp.get('title', '—')} "
        f"| {mandatory} "
        f"| {rfp.get('priority', 'must')} "
        f"| {rfp.get('status', 'unaddressed')} "
        f"| {rfp.get('due_date', '—')} "
        f"| {rfp.get('contractual_date', '—')} "
        f"| {evidence} "
        f"| {links_str} |"
    )


def derive_traceability_matrix(entities: dict[str, list[dict[str, Any]]]) -> str:
    """Derive traceability-matrix.md showing all entity relationships."""
    lines = [
        "# Traceability Matrix",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        "",
    ]

    # RFP-REQ → REQ → COMP → DEL → TASK → TEST → EVD
    lines.append("## Core Traceability Spine (RFP-REQ → REQ → COMP → DEL → TASK → TEST → EVD)")
    lines.append("")

    rfp_reqs = entities.get("rfp_requirements", [])
    for rfp in sorted(rfp_reqs, key=lambda x: x.get("id", "")):
        lines.append(f"### {rfp.get('id')}: {rfp.get('title', '—')}")
        lines.append(f"- **Status:** {rfp.get('status', 'unaddressed')}")
        lines.append(f"- **Priority:** {rfp.get('priority', 'must')}")
        lines.append(f"- **Links:**")
        for ref_field in ["requirement_refs", "deliverable_refs", "milestone_refs",
                          "task_refs", "test_refs", "approval_refs"]:
            refs = rfp.get(ref_field, [])
            if refs:
                lines.append(f"  - {ref_field[:-1]}: {', '.join(sorted(set(refs)))}")
        lines.append("")

    # Milestone dependencies
    lines.append("## Milestone Dependencies")
    lines.append("")
    milestones = entities.get("milestones", [])
    for ms in sorted(milestones, key=lambda x: x.get("id", "")):
        lines.append(f"### {ms.get('id')}: {ms.get('title', '—')}")
        lines.append(f"- **Phase:** {ms.get('phase', '—')}")
        lines.append(f"- **Status:** {ms.get('status', 'pending')}")
        lines.append(f"- **Depends On:** {', '.join(ms.get('depends_on', [])) or '—'}")
        lines.append(f"- **Task Refs:** {', '.join(ms.get('task_refs', [])) or '—'}")
        lines.append("")

    # Task dependencies
    lines.append("## Task Dependencies")
    lines.append("")
    tasks = entities.get("tasks", [])
    for task in sorted(tasks, key=lambda x: x.get("id", "")):
        lines.append(f"### {task.get('id')}: {task.get('title', '—')}")
        lines.append(f"- **Status:** {task.get('status', 'todo')}")
        lines.append(f"- **Priority:** {task.get('priority', 'must')}")
        lines.append(f"- **Blocked By:** {', '.join(task.get('blocked_by', [])) or '—'}")
        lines.append(f"- **Blocking:** {', '.join(task.get('blocking', [])) or '—'}")
        lines.append(f"- **Milestone:** {task.get('milestone_ref', '—')}")
        lines.append("")

    return "\n".join(lines)
