"""Read-only projections used by the FastAPI dashboard.

These functions read Markdown artifacts and lifecycle state. They never mutate
project state. Adding/removing the dashboard loses zero decisions, requirements,
or risks.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import yaml

from epe.core.frontmatter import read_doc


def project_list(projects_root: Path) -> list[dict]:
    if not projects_root.exists():
        return []
    out: list[dict] = []
    for child in sorted(projects_root.iterdir()):
        if not child.is_dir() or child.name.startswith("_") or child.name.startswith("."):
            continue
        state_path = child / "state.yaml"
        if not state_path.exists():
            continue
        try:
            data = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        out.append(
            {
                "project_id": data.get("project_id", child.name),
                "stage": data.get("stage"),
                "status": data.get("status"),
                "customer": data.get("customer"),
            }
        )
    return out


def project_state(state_path: Path) -> dict:
    if not state_path.exists():
        return {}
    return yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}


def project_summary(project_root: Path) -> dict:
    """Build the dashboard summary for a single project."""
    state_path = project_root / "state.yaml"
    state = project_state(state_path)

    artifacts = []
    for stage in ("product", "presales", "architecture", "delivery"):
        for path in sorted((project_root / stage).glob("*.md")):
            try:
                doc = read_doc(path)
                artifacts.append(
                    {
                        "stage": stage,
                        "name": path.name,
                        "contract": doc.metadata.get("contract"),
                        "status": doc.metadata.get("status"),
                        "approved_by": doc.metadata.get("approved_by"),
                        "approved_at": doc.metadata.get("approved_at"),
                        "checksum_sha256": doc.metadata.get("checksum_sha256"),
                        "rel_path": str(path.relative_to(project_root)),
                    }
                )
            except Exception:
                continue

    # Traceability graph
    from epe.validation.traceability import build_traceability_graph

    graph = build_traceability_graph(project_root)

    # Counts
    body_texts = []
    for a in artifacts:
        path = project_root / a["rel_path"]
        try:
            body_texts.append(read_doc(path).body)
        except Exception:
            pass
    all_body = "\n".join(body_texts)
    counts = {
        "requirements": len(_find_ids(all_body, "REQ-")),
        "capabilities": len(_find_ids(all_body, "CAP-")),
        "decisions": len(_find_ids(all_body, "DEC-")),
        "components": len(_find_ids(all_body, "COMP-")),
        "tasks": len(_find_ids(all_body, "TASK-")),
        "tests": len(_find_ids(all_body, "TEST-")),
        "questions": len(_find_ids(all_body, "Q-")),
    }

    # Status counts
    status_counter = Counter(a["status"] for a in artifacts)

    # Handover readiness — derived from existing artifacts and their approval
    readiness = _handover_readiness(artifacts)

    return {
        "project_id": state.get("project_id", project_root.name),
        "stage": state.get("stage"),
        "lifecycle_status": state.get("status"),
        "gates": state.get("gates", {}),
        "history": state.get("history", []),
        "artifacts": artifacts,
        "counts": counts,
        "status_counts": dict(status_counter),
        "traceability": {
            "nodes": len(graph.get("nodes", {})),
            "edges": len(graph.get("edges", [])),
            "orphan": graph.get("orphan", []),
        },
        "handover_readiness": readiness,
    }


def _find_ids(text: str, prefix: str) -> list[str]:
    import re
    return re.findall(rf"\b{re.escape(prefix)}\d+\b", text)


def _handover_readiness(artifacts: list[dict]) -> dict:
    by_stage: dict[str, list[dict]] = {stage: [] for stage in ("product", "presales", "architecture", "delivery")}
    for a in artifacts:
        by_stage.setdefault(a["stage"], []).append(a)
    approved = lambda arts: sum(1 for a in arts if a["status"] == "approved")
    total = lambda arts: len(arts)

    pct = lambda arts: (approved(arts) / total(arts) * 100) if total(arts) else 0.0

    return {
        "product_to_presales": pct(by_stage["product"]),
        "presales_to_architecture": pct(by_stage["presales"]),
        "architecture_to_delivery": pct(by_stage["architecture"]),
    }


def lifecycle_documents_summary(project_root: Path) -> dict:
    """Full lifecycle document view across all stages."""
    from epe.tracking.registry import DocumentRegistry
    from epe.tracking.lineage import LineageComputer
    from epe.validation.completeness import validate_gate_completeness

    registry = DocumentRegistry.from_project(project_root, project_root.name)
    lineage = LineageComputer(registry)
    gate_status = validate_gate_completeness(project_root, registry)
    traceability_matrix = lineage.build_traceability_matrix()

    return {
        "project_id": project_root.name,
        "stages": registry.stage_summary(),
        "gate_status": {
            stage: {
                "readiness": info["readiness"],
                "completeness_score": info["completeness_score"],
                "all_approved": info["all_approved"],
                "missing_documents": info["missing_documents"],
            }
            for stage, info in gate_status.items()
        },
        "documents": registry.to_dict(),
        "traceability_matrix": traceability_matrix,
    }


def lifecycle_stage_view(project_root: Path, stage: str) -> dict:
    """Detailed view for a single stage."""
    from epe.tracking.registry import DocumentRegistry
    from epe.tracking.lineage import LineageComputer
    from epe.validation.completeness import validate_stage_completeness

    registry = DocumentRegistry.from_project(project_root, project_root.name)
    lineage = LineageComputer(registry)
    completeness = validate_stage_completeness(project_root, stage, registry)
    stage_docs = registry.by_stage(stage)

    return {
        "stage": stage,
        "completeness": completeness,
        "documents": [d.to_dict() for d in stage_docs],
        "handover_status": lineage.stage_handoff_status(
            stage, {"product": "presales", "presales": "architecture", "architecture": "delivery"}.get(stage, "")
        ) if stage != "delivery" else None,
    }


def lifecycle_lineage_view(project_root: Path, doc_id: str) -> dict:
    """Full lineage chain for a specific document."""
    from epe.tracking.registry import DocumentRegistry
    from epe.tracking.lineage import LineageComputer

    registry = DocumentRegistry.from_project(project_root, project_root.name)
    lineage = LineageComputer(registry)

    forward = lineage.trace_from_document(doc_id)
    backward = lineage.trace_to_document(doc_id)

    return {
        "doc_id": doc_id,
        "forward_chain": forward.to_dict(),
        "backward_chain": backward.to_dict(),
    }


def lifecycle_gates_view(project_root: Path) -> dict:
    """Gate readiness matrix."""
    from epe.tracking.registry import DocumentRegistry
    from epe.tracking.lineage import LineageComputer
    from epe.validation.completeness import validate_gate_completeness

    registry = DocumentRegistry.from_project(project_root, project_root.name)
    gate_status = validate_gate_completeness(project_root, registry)

    # Per-stage handoff status
    transitions = [
        ("product", "presales"),
        ("presales", "architecture"),
        ("architecture", "delivery"),
    ]
    lineage = LineageComputer(registry)
    handoff_status = {
        f"{f}->{t}": lineage.stage_handoff_status(f, t)
        for f, t in transitions
    }

    return {
        "project_id": project_root.name,
        "gate_status": gate_status,
        "handoff_status": handoff_status,
    }


def project_dashboard_markdown(project_root: Path) -> str:
    """Render the human-readable dashboard as Markdown."""
    summary = project_summary(project_root)
    pid = summary["project_id"]
    stage = summary.get("stage") or "—"
    status = summary.get("lifecycle_status") or "—"
    counts = summary["counts"]
    hr = summary["handover_readiness"]

    def bar(pct: float) -> str:
        full = int(round(pct / 10))
        return "█" * full + "░" * (10 - full)

    lines = [
        f"# EPE — Project {pid}",
        "",
        f"- **Stage**: {stage}",
        f"- **Status**: {status}",
        "",
        "## Handover readiness",
        "",
        f"- Product → Presales:        `{bar(hr['product_to_presales'])}` {hr['product_to_presales']:.0f}%",
        f"- Presales → Architecture:   `{bar(hr['presales_to_architecture'])}` {hr['presales_to_architecture']:.0f}%",
        f"- Architecture → Delivery:   `{bar(hr['architecture_to_delivery'])}` {hr['architecture_to_delivery']:.0f}%",
        "",
        "## Counts",
        "",
        f"- Requirements: {counts['requirements']}",
        f"- Capabilities: {counts['capabilities']}",
        f"- Decisions: {counts['decisions']}",
        f"- Components: {counts['components']}",
        f"- Tasks: {counts['tasks']}",
        f"- Tests: {counts['tests']}",
        f"- Open questions: {counts['questions']}",
        "",
        "## Artifacts",
        "",
    ]
    for stage_name in ("product", "presales", "architecture", "delivery"):
        stage_arts = [a for a in summary["artifacts"] if a["stage"] == stage_name]
        if not stage_arts:
            continue
        lines.append(f"### {stage_name}")
        lines.append("")
        for a in stage_arts:
            status = a["status"] or "—"
            lines.append(f"- {a['name']} — `{a['contract']}` — status: {status}")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Governance projections
# ---------------------------------------------------------------------------


def solution_manager_cockpit(project_root: Path) -> dict:
    """Solution Manager operating cockpit — answers 5 critical questions.

    This is the CENTERPIECE governance view for Solution Managers.
    """
    from datetime import date, timedelta
    from epe.stages.governance.critical_path import build_schedule_network
    from epe.stages.governance.registry_derive import load_all_entities

    entities = load_all_entities(project_root)
    milestones = entities.get("milestones", [])
    tasks = entities.get("tasks", [])

    today = date.today()
    two_weeks = today + timedelta(days=14)

    # 1. What must I do? (owned items)
    my_milestones = [m for m in milestones if m.get("owner")]
    my_tasks = [t for t in tasks if t.get("owner")]

    # 2. What is overdue?
    overdue_tasks = []
    for t in tasks:
        fe = t.get("forecast_end")
        if fe and _parse_date(fe) and _parse_date(fe) < today and t.get("status") != "done":
            overdue_tasks.append(t)

    overdue_milestones = []
    for m in milestones:
        fe = m.get("forecast_end")
        if fe and _parse_date(fe) and _parse_date(fe) < today and m.get("status") != "achieved":
            overdue_milestones.append(m)

    # 3. What is blocking me?
    blocking_tasks = [t for t in tasks if t.get("blocking")]
    task_blockers = []
    for t in tasks:
        for blocked_by_id in t.get("blocked_by", []):
            blocker = next((x for x in tasks if x.get("id") == blocked_by_id), None)
            if blocker and blocker.get("status") != "done":
                task_blockers.append({
                    "blocker_id": blocked_by_id,
                    "blocker_title": blocker.get("title", "?"),
                    "blocked_id": t.get("id"),
                    "blocked_title": t.get("title", "?"),
                })

    # 4. What is coming next? (next 14 days)
    coming_milestones = []
    for m in milestones:
        fs = m.get("forecast_start")
        if fs and _parse_date(fs) and _parse_date(fs) <= two_weeks:
            coming_milestones.append(m)

    coming_tasks = []
    for t in tasks:
        fs = t.get("forecast_start")
        if fs and _parse_date(fs) and _parse_date(fs) <= two_weeks and t.get("status") == "todo":
            coming_tasks.append(t)

    # 5. What can cause committed date to be missed? (critical path)
    network = build_schedule_network(tasks, milestones)
    critical_chain = network.get_critical_chain()

    critical_path_risks = []
    for item in critical_chain:
        variance = item.schedule_variance_days
        if variance is not None and variance > 0:
            critical_path_risks.append({
                "id": item.id,
                "type": item.item_type,
                "title": item.title,
                "variance_days": variance,
                "forecast_end": str(item.forecast_end),
                "baseline_end": str(item.baseline_end),
                "impact": "Delays propagate to final committed date",
            })

    # Compute committed final date (last milestone baseline end)
    final_milestone = None
    for m in sorted(milestones, key=lambda x: x.get("baseline_end", ""), reverse=True):
        final_milestone = m
        break

    return {
        "project_id": project_root.name,
        "generated_at": today.isoformat(),
        "committed_final_date": final_milestone.get("baseline_end") if final_milestone else None,
        "my_milestones": [
            {"id": m.get("id"), "title": m.get("title"), "status": m.get("status"),
             "baseline_end": m.get("baseline_end")}
            for m in my_milestones
        ],
        "my_tasks": [
            {"id": t.get("id"), "title": t.get("title"), "status": t.get("status"),
             "baseline_end": t.get("baseline_end")}
            for t in my_tasks
        ],
        "overdue": {
            "milestones": [{"id": m.get("id"), "title": m.get("title"), "forecast_end": m.get("forecast_end")}
                          for m in overdue_milestones],
            "tasks": [{"id": t.get("id"), "title": t.get("title"), "forecast_end": t.get("forecast_end")}
                     for t in overdue_tasks],
            "count": len(overdue_milestones) + len(overdue_tasks),
        },
        "blockers": {
            "task_blockers": task_blockers,
            "blocking_tasks": [{"id": t.get("id"), "title": t.get("title")} for t in blocking_tasks],
            "count": len(task_blockers) + len(blocking_tasks),
        },
        "coming_next": {
            "milestones": [{"id": m.get("id"), "title": m.get("title"), "forecast_start": m.get("forecast_start")}
                          for m in sorted(coming_milestones, key=lambda x: x.get("forecast_start", ""))[:5]],
            "tasks": [{"id": t.get("id"), "title": t.get("title"), "forecast_start": t.get("forecast_start")}
                     for t in sorted(coming_tasks, key=lambda x: x.get("forecast_start", ""))[:10]],
        },
        "critical_path": {
            "chain": [{"id": i.id, "title": i.title, "float_days": i.float_days} for i in critical_chain],
            "at_risk_items": critical_path_risks,
            "committed_date_at_risk": len(critical_path_risks) > 0,
        },
        "metrics": {
            "total_tasks": len(tasks),
            "completed_tasks": sum(1 for t in tasks if t.get("status") == "done"),
            "total_milestones": len(milestones),
            "achieved_milestones": sum(1 for m in milestones if m.get("status") == "achieved"),
            "at_risk_milestones": sum(1 for m in milestones if m.get("status") == "at_risk"),
            "schedule_variance_days": sum(
                (m.get("schedule_variance_days") or 0) for m in milestones if m.get("schedule_variance_days")
            ),
        },
    }


def governance_summary(project_root: Path) -> dict:
    """Full governance summary across all entity types."""
    from epe.stages.governance.registry_derive import load_all_entities
    from epe.stages.governance.critical_path import build_schedule_network

    entities = load_all_entities(project_root)
    milestones = entities.get("milestones", [])
    tasks = entities.get("tasks", [])
    rfp_reqs = entities.get("rfp_requirements", [])
    deliverables = entities.get("deliverables", [])
    approvals = entities.get("approvals", [])
    stakeholders = entities.get("stakeholders", [])

    network = build_schedule_network(tasks, milestones)
    critical_chain = network.get_critical_chain()

    return {
        "project_id": project_root.name,
        "milestones": {
            "total": len(milestones),
            "achieved": sum(1 for m in milestones if m.get("status") == "achieved"),
            "at_risk": sum(1 for m in milestones if m.get("status") == "at_risk"),
            "pending": sum(1 for m in milestones if m.get("status") in ("pending", "in_progress")),
            "critical": len([m for m in milestones if m.get("critical")]),
        },
        "tasks": {
            "total": len(tasks),
            "done": sum(1 for t in tasks if t.get("status") == "done"),
            "blocked": sum(1 for t in tasks if t.get("status") == "blocked"),
            "critical": len([t for t in tasks if t.get("critical")]),
        },
        "rfp_requirements": {
            "total": len(rfp_reqs),
            "satisfied": sum(1 for r in rfp_reqs if r.get("status") == "satisfied"),
            "unaddressed": sum(1 for r in rfp_reqs if r.get("status") == "unaddressed"),
            "in_progress": sum(1 for r in rfp_reqs if r.get("status") == "in_progress"),
            "mandatory": sum(1 for r in rfp_reqs if r.get("mandatory", True)),
        },
        "deliverables": {
            "total": len(deliverables),
            "accepted": sum(1 for d in deliverables if d.get("status") == "accepted"),
            "pending": sum(1 for d in deliverables if d.get("status") in ("pending", "in_progress")),
        },
        "approvals": {
            "total": len(approvals),
            "approved": sum(1 for a in approvals if a.get("status") == "approved"),
            "pending": sum(1 for a in approvals if a.get("status") == "pending"),
        },
        "stakeholders": {
            "total": len(stakeholders),
            "active": sum(1 for s in stakeholders if s.get("status") == "active"),
        },
        "critical_chain": [i.id for i in critical_chain],
    }


def milestone_summary(project_root: Path) -> dict:
    """Milestone status summary with critical-path info."""
    from epe.stages.governance.registry_derive import load_all_entities
    from epe.stages.governance.critical_path import build_schedule_network

    entities = load_all_entities(project_root)
    milestones = entities.get("milestones", [])
    tasks = entities.get("tasks", [])

    network = build_schedule_network(tasks, milestones)
    critical_chain_ids = {i.id for i in network.get_critical_chain()}

    return {
        "project_id": project_root.name,
        "milestones": [
            {
                "id": m.get("id"),
                "title": m.get("title"),
                "phase": m.get("phase"),
                "gate_ref": m.get("gate_ref"),
                "owner": m.get("owner"),
                "status": m.get("status"),
                "baseline_start": m.get("baseline_start"),
                "baseline_end": m.get("baseline_end"),
                "forecast_start": m.get("forecast_start"),
                "forecast_end": m.get("forecast_end"),
                "actual_start": m.get("actual_start"),
                "actual_end": m.get("actual_end"),
                "schedule_variance_days": m.get("schedule_variance_days"),
                "critical": m.get("id") in critical_chain_ids,
                "blocking": m.get("blocking", False),
                "depends_on": m.get("depends_on", []),
                "task_refs": m.get("task_refs", []),
            }
            for m in sorted(milestones, key=lambda x: x.get("baseline_end", ""))
        ],
    }


def task_summary(project_root: Path) -> dict:
    """Task status summary with blocking relationships."""
    from epe.stages.governance.registry_derive import load_all_entities
    from epe.stages.governance.critical_path import build_schedule_network

    entities = load_all_entities(project_root)
    tasks = entities.get("tasks", [])
    milestones = entities.get("milestones", [])

    network = build_schedule_network(tasks, milestones)
    critical_chain_ids = {i.id for i in network.get_critical_chain()}

    return {
        "project_id": project_root.name,
        "tasks": [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "owner": t.get("owner"),
                "status": t.get("status"),
                "priority": t.get("priority"),
                "milestone_ref": t.get("milestone_ref"),
                "baseline_start": t.get("baseline_start"),
                "baseline_end": t.get("baseline_end"),
                "forecast_start": t.get("forecast_start"),
                "forecast_end": t.get("forecast_end"),
                "actual_start": t.get("actual_start"),
                "actual_end": t.get("actual_end"),
                "schedule_variance_days": t.get("schedule_variance_days"),
                "critical": t.get("id") in critical_chain_ids,
                "blocking_task": t.get("blocking_task", False),
                "blocked_by": t.get("blocked_by", []),
                "blocking": t.get("blocking", []),
                "rfp_requirement_refs": t.get("rfp_requirement_refs", []),
                "requirement_refs": t.get("requirement_refs", []),
            }
            for t in sorted(tasks, key=lambda x: x.get("baseline_end", ""))
        ],
    }


def rfp_summary(project_root: Path) -> dict:
    """RFP requirements status summary."""
    from epe.stages.governance.registry_derive import load_all_entities

    entities = load_all_entities(project_root)
    rfp_reqs = entities.get("rfp_requirements", [])

    return {
        "project_id": project_root.name,
        "rfp_requirements": [
            {
                "id": r.get("id"),
                "title": r.get("title"),
                "rfp_id": r.get("rfp_id"),
                "mandatory": r.get("mandatory", True),
                "priority": r.get("priority"),
                "category": r.get("category"),
                "owner": r.get("owner"),
                "responsible": r.get("responsible"),
                "status": r.get("status"),
                "due_date": r.get("due_date"),
                "contractual_date": r.get("contractual_date"),
                "evidence_required": r.get("evidence_required", True),
                "customer_refs": r.get("customer_refs", []),
                "requirement_refs": r.get("requirement_refs", []),
                "deliverable_refs": r.get("deliverable_refs", []),
                "milestone_refs": r.get("milestone_refs", []),
                "task_refs": r.get("task_refs", []),
                "test_refs": r.get("test_refs", []),
                "approval_refs": r.get("approval_refs", []),
            }
            for r in sorted(rfp_reqs, key=lambda x: x.get("due_date", ""))
        ],
    }


def _parse_date(value: Any) -> date | None:
    """Parse a date from string or date object."""
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None
