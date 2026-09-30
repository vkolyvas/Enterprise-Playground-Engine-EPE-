"""Traceability validator: build the project graph and check missing edges."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from epe.core.frontmatter import read_doc
from epe.tracking.ids import ID_PATTERNS, scan_ids
from epe.validation.engine import Finding, make_finding


def build_traceability_graph(project_root: Path) -> dict[str, Any]:
    """Walk the project tree and compute a traceability projection.

    Implements the unified traceability spine:
        CUST → REQ → COMP → DEC → TEST → EVD → ACCEPTANCE → AS-BUILT

    And cross-cutting relationships:
        REQ ── affected_by ── ASM
        REQ ── blocked_by ─── DEP
        REQ ── changed_by ─── CHG
    """
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    def add_node(node_id: str, stage: str, path: Path, **extra) -> None:
        if node_id not in nodes:
            nodes[node_id] = {"stage": stage, "path": str(path.relative_to(project_root)), **extra}

    def add_edge(a: str, b: str, kind: str) -> None:
        """Add edge only if both endpoints exist in nodes."""
        if a in nodes and b in nodes:
            edges.append({"from": a, "to": b, "type": kind})

    # === PRODUCT STAGE: CAP (Capabilities) ===
    catalog_path = project_root / "product" / "catalog.md"
    if catalog_path.exists():
        body = read_doc(catalog_path).body
        for cap in scan_ids(body, "CAP"):
            add_node(cap, "product", catalog_path)

    # === PRESALES STAGE: CUST + REQ + CAP relationships ===
    presales_scope = project_root / "presales" / "scope.md"
    presales_handover = project_root / "presales" / "handover.md"

    for path in (presales_scope, presales_handover):
        if not path.exists():
            continue
        body = read_doc(path).body

        # CUST nodes + refines edge to REQ
        for cust in scan_ids(body, "CUST"):
            add_node(cust, "presales", path)
            for req in scan_ids(body, "REQ"):
                add_node(req, "presales", path)
                add_edge(cust, req, "refines")

        # REQ nodes + supports edge from CAP
        for req in scan_ids(body, "REQ"):
            add_node(req, "presales", path)
            for cap in scan_ids(body, "CAP"):
                add_node(cap, "product", catalog_path if catalog_path.exists() else path)
                add_edge(cap, req, "supports")

        # ASM (Assumptions) - affected_by edge to REQ
        for asm in scan_ids(body, "ASM"):
            add_node(asm, "presales", path)
            for req in scan_ids(body, "REQ"):
                add_edge(req, asm, "affected_by")

        # DEP (Dependencies) - blocked_by edge to REQ
        for dep in scan_ids(body, "DEP"):
            add_node(dep, "presales", path)
            for req in scan_ids(body, "REQ"):
                add_edge(req, dep, "blocked_by")

        # CHG (Changes) - changed_by edge to REQ
        for chg in scan_ids(body, "CHG"):
            add_node(chg, "presales", path)
            for req in scan_ids(body, "REQ"):
                add_edge(req, chg, "changed_by")

    # === ARCHITECTURE STAGE: HLD/LLD/solution_baseline ===
    for art in ("architecture/hld.md", "architecture/lld.md", "architecture/solution-baseline.md"):
        p = project_root / art
        if not p.exists():
            continue
        body = read_doc(p).body

        # COMP nodes + satisfied_by edge from REQ
        for comp in scan_ids(body, "COMP"):
            add_node(comp, "architecture", p)
            for req in scan_ids(body, "REQ"):
                add_edge(comp, req, "satisfied_by")

        # DEC nodes + decided_by edge from COMP
        for dec in scan_ids(body, "DEC"):
            add_node(dec, "architecture", p)
            for comp in scan_ids(body, "COMP"):
                add_edge(comp, dec, "decided_by")

        # TASK nodes (delivery planning)
        for task in scan_ids(body, "TASK"):
            add_node(task, "delivery", p)
            # TASK implements COMP
            for comp in scan_ids(body, "COMP"):
                add_edge(task, comp, "implements")

        # TEST nodes + validated_by edge from DEC
        for test in scan_ids(body, "TEST"):
            add_node(test, "architecture", p)
            for dec in scan_ids(body, "DEC"):
                add_edge(dec, test, "validated_by")
            # TEST verifies REQ
            for req in scan_ids(body, "REQ"):
                add_edge(test, req, "verifies")

    # === DELIVERY STAGE: plan/test/acceptance ===
    for art in ("delivery/plan.md", "delivery/test.md", "delivery/acceptance.md"):
        p = project_root / art
        if not p.exists():
            continue
        body = read_doc(p).body

        # TASK nodes + verified_by edge from TEST
        for task in scan_ids(body, "TASK"):
            add_node(task, "delivery", p)
            for test in scan_ids(body, "TEST"):
                add_node(test, "delivery", p)
                add_edge(task, test, "verified_by")

        # TEST nodes + verifies REQ
        for test in scan_ids(body, "TEST"):
            add_node(test, "delivery", p)
            for req in scan_ids(body, "REQ"):
                add_edge(test, req, "verifies")

        # EVD (Evidence) nodes + verified_by edge from TEST
        for evd in scan_ids(body, "EVD"):
            add_node(evd, "delivery", p)
            for test in scan_ids(body, "TEST"):
                add_edge(test, evd, "verified_by")

    # Orphan analysis
    referenced = {e["from"] for e in edges} | {e["to"] for e in edges}
    orphan = sorted(set(nodes.keys()) - referenced)

    return {
        "nodes": nodes,
        "edges": edges,
        "orphan": orphan,
    }


def write_traceability(graph: dict[str, Any], project_root: Path) -> Path:
    path = project_root / "traceability.json"
    path.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def validate_traceability(artifact_path: Path, context: dict[str, Any]) -> Iterable[Finding]:
    project_paths = context.get("project_paths")
    if project_paths is None:
        return
    project_root = project_paths.project_root
    graph = build_traceability_graph(project_root)

    doc = read_doc(artifact_path)
    body = doc.body
    contract = doc.metadata.get("contract", "")

    # If this artifact declares REQ-NNNs, every one must trace forward
    reqs = scan_ids(body, "REQ")
    if reqs and contract.startswith("presales"):
        for req in sorted(reqs):
            implemented = any(
                e["from"] == req or e["to"] == req
                for e in graph["edges"]
                if e["type"] in ("satisfied_by", "verified_by")
            )
            if not implemented:
                yield make_finding(
                    validator="traceability",
                    severity="warning",
                    location=f"{artifact_path}#{req}",
                    message=f"Requirement {req} has no downstream implementation edge.",
                    kind="orphan_requirement",
                )

    # If this artifact declares COMP-NNNs, every one must trace upstream
    comps = scan_ids(body, "COMP")
    if comps and contract.startswith("architecture"):
        for comp in sorted(comps):
            upstream = any(e["to"] == comp for e in graph["edges"])
            if not upstream:
                yield make_finding(
                    validator="traceability",
                    severity="warning",
                    location=f"{artifact_path}#{comp}",
                    message=f"Component {comp} has no upstream requirement reference.",
                    kind="orphan_component",
                )

    # If this artifact declares TASK-NNNs, every one should trace back to a COMP
    tasks = scan_ids(body, "TASK")
    if tasks and contract.startswith("delivery"):
        for task in sorted(tasks):
            if not any(e["from"] == task or e["to"] == task for e in graph["edges"]):
                yield make_finding(
                    validator="traceability",
                    severity="warning",
                    location=f"{artifact_path}#{task}",
                    message=f"Task {task} has no upstream component or test reference.",
                    kind="orphan_task",
                )

    # If this artifact declares TEST-NNNs, they should have EVD evidence
    tests = scan_ids(body, "TEST")
    if tests and contract.startswith("delivery"):
        for test in sorted(tests):
            has_evidence = any(
                e["from"] == test and e["type"] == "verified_by"
                for e in graph["edges"]
            )
            if not has_evidence:
                yield make_finding(
                    validator="traceability",
                    severity="warning",
                    location=f"{artifact_path}#{test}",
                    message=f"Test {test} has no evidence (EVD) record.",
                    kind="missing_evidence",
                )
