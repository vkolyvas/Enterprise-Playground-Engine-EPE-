"""Governance Engine — NON-LLM deterministic derivation from entity files.

The GovernanceEngine is a cross-cutting overlay that:
1. Scans entity directories (ms/, task/, rfp-req/, del/, aprv/, stk/)
2. Computes critical path using forward/backward pass
3. Derives registers and control views from entity data

It runs WITHOUT an LLM — all outputs are deterministic derivations.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from epe.core.frontmatter import write_doc
from epe.core.logging import get_logger
from epe.stages.base import StageContext, StageEngine, StageResult
from epe.stages.governance.critical_path import (
    build_schedule_network,
    compute_critical_chain,
    ScheduleNetwork,
)
from epe.stages.governance.registry_derive import (
    derive_milestone_register,
    derive_rfp_obligations,
    derive_task_register,
    derive_traceability_matrix,
    load_all_entities,
)

logger = get_logger("stages.governance")


class GovernanceEngine(StageEngine):
    """Non-LLM governance engine that derives control views from entity files.

    This engine does NOT generate content via LLM. It:
    - Reads entity files from entities/ms/, entities/task/, etc.
    - Computes critical path using forward/backward pass
    - Writes derived views to governance/ directory
    """

    def __init__(self, ctx: StageContext) -> None:
        super().__init__(ctx)
        self.project_root = ctx.project_root

    @property
    def stage(self) -> str:
        return "governance"

    def run(self, dry_run: bool = False) -> StageResult:
        """Run the governance derivation.

        This is a non-LLM operation: scan entities → compute critical path →
        derive registers → write control views.
        """
        logger.info("Running governance engine for %s", self.project_root)

        # Load all entities
        entities = load_all_entities(self.project_root)
        logger.info(
            "Loaded: %d tasks, %d milestones, %d RFP-REQs, %d deliverables, %d approvals, %d stakeholders",
            len(entities["tasks"]),
            len(entities["milestones"]),
            len(entities["rfp_requirements"]),
            len(entities["deliverables"]),
            len(entities["approvals"]),
            len(entities["stakeholders"]),
        )

        # Compute critical path
        network = build_schedule_network(entities["tasks"], entities["milestones"])
        critical_chain = network.get_critical_chain()

        # Derive registers and control views
        outputs: dict[str, Path] = {}

        if not dry_run:
            # Write milestone register
            ms_path = self.project_root / "governance" / "milestone-register.md"
            ms_path.parent.mkdir(parents=True, exist_ok=True)
            _write_governance_doc(
                ms_path,
                derive_milestone_register(entities),
                {"stage": "governance", "type": "derived", "critical_chain": [i.id for i in critical_chain]},
            )
            outputs["milestone-register"] = ms_path

            # Write task register
            task_path = self.project_root / "governance" / "task-register.md"
            _write_governance_doc(
                task_path,
                derive_task_register(entities),
                {"stage": "governance", "type": "derived"},
            )
            outputs["task-register"] = task_path

            # Write RFP obligations
            rfp_path = self.project_root / "governance" / "rfp-obligations.md"
            _write_governance_doc(
                rfp_path,
                derive_rfp_obligations(entities),
                {"stage": "governance", "type": "derived"},
            )
            outputs["rfp-obligations"] = rfp_path

            # Write traceability matrix
            matrix_path = self.project_root / "governance" / "traceability-matrix.md"
            _write_governance_doc(
                matrix_path,
                derive_traceability_matrix(entities),
                {"stage": "governance", "type": "derived"},
            )
            outputs["traceability-matrix"] = matrix_path

            # Write master governance control
            gov_path = self.project_root / "governance" / "governance.md"
            _write_governance_doc(
                gov_path,
                derive_governance_control(entities, network, critical_chain),
                {"stage": "governance", "type": "derived", "critical_chain": [i.id for i in critical_chain]},
            )
            outputs["governance-control"] = gov_path

            # Write stage control documents
            _write_stage_control_docs(self.project_root, entities, network, critical_chain)

        logger.info("Governance engine completed. Outputs: %s", list(outputs.keys()))
        return StageResult(success=True, artifacts=list(outputs.values()))

    def preconditions(self) -> list[str]:
        """Governance has no preconditions — runs as overlay."""
        return []

    def post_process(self) -> None:
        """No post-processing needed — all work done in run()."""
        pass


def _write_governance_doc(path: Path, body: str, metadata: dict[str, Any]) -> None:
    """Write a governance document with standard frontmatter."""
    meta = dict(metadata)
    meta["generated_by"] = "governance_engine"
    meta["generated_at"] = datetime.now(timezone.utc).isoformat()
    write_doc(path, body, meta)


def derive_governance_control(
    entities: dict[str, list[dict[str, Any]]],
    network: ScheduleNetwork,
    critical_chain: list,
) -> str:
    """Derive the master governance.md control document."""
    milestones = entities.get("milestones", [])
    tasks = entities.get("tasks", [])
    rfp_reqs = entities.get("rfp_requirements", [])

    # Compute summary stats
    total_ms = len(milestones)
    achieved_ms = sum(1 for m in milestones if m.get("status") == "achieved")
    at_risk_ms = sum(1 for m in milestones if m.get("status") == "at_risk")
    pending_ms = sum(1 for m in milestones if m.get("status") in ("pending", "in_progress"))

    total_tasks = len(tasks)
    done_tasks = sum(1 for t in tasks if t.get("status") == "done")
    blocked_tasks = sum(1 for t in tasks if t.get("status") == "blocked")

    total_rfp = len(rfp_reqs)
    satisfied_rfp = sum(1 for r in rfp_reqs if r.get("status") == "satisfied")
    unaddressed_rfp = sum(1 for r in rfp_reqs if r.get("status") == "unaddressed")

    lines = [
        "# Governance Control",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Type:** Derived View (Non-LLM)",
        "",
        "## Executive Summary",
        "",
        f"| Metric | Value |",
        "|--------|-------|",
        f"| Total Milestones | {total_ms} |",
        f"| Achieved | {achieved_ms} |",
        f"| At Risk | {at_risk_ms} |",
        f"| Pending | {pending_ms} |",
        f"| Total Tasks | {total_tasks} |",
        f"| Completed | {done_tasks} |",
        f"| Blocked | {blocked_tasks} |",
        f"| Total RFP Requirements | {total_rfp} |",
        f"| Satisfied | {satisfied_rfp} |",
        f"| Unaddressed | {unaddressed_rfp} |",
        "",
        "## Critical Path",
        "",
        f"**Chain:** {' → '.join([i.id for i in critical_chain]) if critical_chain else 'No critical chain computed'}",
        "",
    ]

    if critical_chain:
        lines.append("| ID | Title | Type | Float | Variance |")
        lines.append("|----|-------|------|-------|----------|")
        for item in critical_chain:
            variance = item.schedule_variance_days
            variance_str = f"{variance}d" if variance is not None else "—"
            lines.append(
                f"| {item.id} | {item.title} | {item.item_type} | {item.float_days}d | {variance_str} |"
            )
    else:
        lines.append("*No critical chain items found.*")

    lines.extend([
        "",
        "## Governance Registers",
        "",
        "- [Milestone Register](milestone-register.md)",
        "- [Task Register](task-register.md)",
        "- [RFP Obligations](rfp-obligations.md)",
        "- [Traceability Matrix](traceability-matrix.md)",
        "",
        "## Stage Controls",
        "",
        "- [Product Control](../product/product-control.md)",
        "- [Presales Control](../presales/presales-control.md)",
        "- [Solution Manager Cockpit](../architecture/solution-manager-cockpit.md)",
        "- [Delivery Control](../delivery/delivery-control.md)",
    ])

    return "\n".join(lines)


def _write_stage_control_docs(
    project_root: Path,
    entities: dict[str, list[dict[str, Any]]],
    network: ScheduleNetwork,
    critical_chain: list,
) -> None:
    """Write stage control documents (product-control, presales-control, etc.)."""
    today = date.today()
    milestones = entities.get("milestones", [])

    # Product control — is product ready?
    product_path = project_root / "product" / "product-control.md"
    product_path.parent.mkdir(parents=True, exist_ok=True)
    product_body = _derive_product_control(milestones, today)
    _write_governance_doc(
        product_path,
        product_body,
        {"stage": "product", "type": "derived"},
    )

    # Presales control
    presales_path = project_root / "presales" / "presales-control.md"
    presales_body = _derive_presales_control(milestones, entities.get("rfp_requirements", []), today)
    _write_governance_doc(
        presales_path,
        presales_body,
        {"stage": "presales", "type": "derived"},
    )

    # Solution Manager cockpit (architecture stage)
    arch_path = project_root / "architecture" / "solution-manager-cockpit.md"
    arch_body = _derive_solution_manager_cockpit(entities, network, critical_chain, today)
    _write_governance_doc(
        arch_path,
        arch_body,
        {"stage": "architecture", "type": "derived", "critical_chain": [i.id for i in critical_chain]},
    )

    # Delivery control
    delivery_path = project_root / "delivery" / "delivery-control.md"
    delivery_body = _derive_delivery_control(entities, today)
    _write_governance_doc(
        delivery_path,
        delivery_body,
        {"stage": "delivery", "type": "derived"},
    )


def _derive_product_control(milestones: list[dict], today: date) -> str:
    """Derive product/product-control.md."""
    # Product stage gates: MS-001 (Requirements Baseline)
    ms001 = next((m for m in milestones if m.get("id") == "MS-001"), None)

    lines = [
        "# Product Stage Control",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Type:** Derived View",
        "",
        "## Product Readiness Status",
        "",
    ]

    if ms001:
        status = ms001.get("status", "pending")
        forecast_end = ms001.get("forecast_end", "—")
        baseline_end = ms001.get("baseline_end", "—")
        lines.extend([
            f"- **MS-001 (Requirements Baseline):** {status.upper()}",
            f"  - Baseline End: {baseline_end}",
            f"  - Forecast End: {forecast_end}",
        ])

        # Check if product is ready for presales
        if status == "achieved":
            lines.append("")
            lines.append("**Product is ready for Presales transition.**")
        else:
            lines.append("")
            lines.append("**Product is NOT yet ready for Presales transition.**")
    else:
        lines.append("*No milestone data found.*")

    return "\n".join(lines)


def _derive_presales_control(
    milestones: list[dict],
    rfp_reqs: list[dict],
    today: date,
) -> str:
    """Derive presales/presales-control.md."""
    # Presales gates: MS-002 (Architecture Ready)
    ms002 = next((m for m in milestones if m.get("id") == "MS-002"), None)

    lines = [
        "# Presales Stage Control",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Type:** Derived View",
        "",
        "## Presales Status",
        "",
    ]

    if ms002:
        status = ms002.get("status", "pending")
        lines.extend([
            f"- **MS-002 (Architecture Ready):** {status.upper()}",
            f"  - Forecast End: {ms002.get('forecast_end', '—')}",
        ])
    else:
        lines.append("*No MS-002 milestone data found.*")

    # RFP unaddressed count
    unaddressed = sum(1 for r in rfp_reqs if r.get("status") == "unaddressed")
    lines.extend([
        "",
        f"## RFP Requirements: {len(rfp_reqs)} total, {unaddressed} unaddressed",
    ])

    return "\n".join(lines)


def _derive_solution_manager_cockpit(
    entities: dict[str, list[dict[str, Any]]],
    network: ScheduleNetwork,
    critical_chain: list,
    today: date,
) -> str:
    """Derive architecture/solution-manager-cockpit.md — the CENTERPIECE."""
    milestones = entities.get("milestones", [])
    tasks = entities.get("tasks", [])

    # My actions (owned tasks/milestones)
    my_tasks = [t for t in tasks if t.get("owner")]
    my_milestones = [m for m in milestones if m.get("owner")]

    # Overdue
    overdue_tasks = [
        t for t in tasks
        if t.get("forecast_end") and _parse_date(t.get("forecast_end")) < today
        and t.get("status") != "done"
    ]
    overdue_milestones = [
        m for m in milestones
        if m.get("forecast_end") and _parse_date(m.get("forecast_end")) < today
        and m.get("status") != "achieved"
    ]

    # Coming next (next 14 days)
    coming_milestones = [
        m for m in milestones
        if m.get("forecast_start") and _parse_date(m.get("forecast_start")) <= today + __import__("datetime").timedelta(days=14)
    ]

    lines = [
        "# Solution Manager Cockpit",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Type:** Derived View (Non-LLM)",
        "",
        "---",
        "",
        "## 1. What Must I Do?",
        "",
        f"**My Milestones:** {len(my_milestones)}",
    ]

    for m in sorted(my_milestones, key=lambda x: x.get("baseline_end", "")):
        lines.append(f"- **{m.get('id')}** {m.get('title')} — {m.get('status')} (end: {m.get('baseline_end', '?')})")

    lines.extend([
        "",
        f"**My Tasks:** {len(my_tasks)}",
    ])

    for t in sorted(my_tasks, key=lambda x: x.get("baseline_end", "")):
        lines.append(f"- **{t.get('id')}** {t.get('title')} — {t.get('status')} (end: {t.get('baseline_end', '?')})")

    lines.extend([
        "",
        "---",
        "",
        "## 2. What Is Overdue?",
        "",
        f"**Overdue Milestones:** {len(overdue_milestones)}",
    ])

    for m in overdue_milestones:
        lines.append(f"- ⚠️ **{m.get('id')}** {m.get('title')} — was due {m.get('forecast_end')}")

    lines.extend([
        "",
        f"**Overdue Tasks:** {len(overdue_tasks)}",
    ])

    for t in overdue_tasks:
        lines.append(f"- ⚠️ **{t.get('id')}** {t.get('title')} — was due {t.get('forecast_end')}")

    lines.extend([
        "",
        "---",
        "",
        "## 3. What Is Blocking Me?",
        "",
    ])

    # Find blocking relationships
    blocking_tasks = [t for t in tasks if t.get("blocking")]
    if blocking_tasks:
        for t in blocking_tasks:
            blocked = ", ".join(t.get("blocked_by", [])) or "?"
            lines.append(f"- 🚧 **{t.get('id')}** {t.get('title')} blocks task(s): {blocked}")
    else:
        lines.append("*No active blockers identified.*")

    lines.extend([
        "",
        "---",
        "",
        "## 4. What Is Coming Next? (Next 14 Days)",
        "",
    ])

    for m in sorted(coming_milestones, key=lambda x: x.get("forecast_start", ""))[:5]:
        lines.append(f"- 📅 **{m.get('id')}** {m.get('title')} starts {m.get('forecast_start', '?')}")

    lines.extend([
        "",
        "---",
        "",
        "## 5. What Can Cause the Committed Date to Be Missed?",
        "",
        f"**Critical Path Items:** {len(critical_chain)}",
        "",
    ])

    if critical_chain:
        lines.append("Items on the critical path (zero float) that directly affect final delivery:")
        lines.append("")
        for item in critical_chain:
            variance = item.schedule_variance_days
            if variance and variance > 0:
                lines.append(f"- 🔴 **{item.id}** {item.title}: +{variance}d variance (forecast: {item.forecast_end})")
            elif variance and variance < 0:
                lines.append(f"- 🟢 **{item.id}** {item.title}: {variance}d ahead ({item.forecast_end})")
            else:
                lines.append(f"- ⚪ **{item.id}** {item.title}: on schedule")
    else:
        lines.append("*No critical path computed.*")

    lines.extend([
        "",
        "---",
        "",
        "## Metrics Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total Milestones | {len(milestones)} |",
        f"| Achieved | {sum(1 for m in milestones if m.get('status') == 'achieved')} |",
        f"| At Risk | {sum(1 for m in milestones if m.get('status') == 'at_risk')} |",
        f"| Total Tasks | {len(tasks)} |",
        f"| Completed | {sum(1 for t in tasks if t.get('status') == 'done')} |",
        f"| Blocked | {sum(1 for t in tasks if t.get('status') == 'blocked')} |",
    ])

    return "\n".join(lines)


def _derive_delivery_control(entities: dict[str, list[dict[str, Any]]], today: date) -> str:
    """Derive delivery/delivery-control.md."""
    tasks = entities.get("tasks", [])
    milestones = entities.get("milestones", [])

    # Delivery gates: MS-005 (UAT Ready), MS-006 (Final Acceptance), MS-007 (Project Complete)
    delivery_ms = [m for m in milestones if m.get("id", "").startswith("MS-0") and int(m.get("id", "MS-0").split("-")[1]) >= 5]

    lines = [
        "# Delivery Stage Control",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
        f"**Type:** Derived View",
        "",
        "## Delivery Status",
        "",
        f"**Total Tasks:** {len(tasks)}",
        f"**Completed:** {sum(1 for t in tasks if t.get('status') == 'done')}",
        f"**Blocked:** {sum(1 for t in tasks if t.get('status') == 'blocked')}",
        "",
        "## Delivery Milestones",
        "",
    ]

    for m in delivery_ms:
        status = m.get("status", "pending")
        lines.append(f"- **{m.get('id')}** {m.get('title')}: {status.upper()} (end: {m.get('forecast_end', '?')})")

    return "\n".join(lines)


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
