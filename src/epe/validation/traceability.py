"""Traceability validator: build the project graph and check missing edges."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from epe.core.frontmatter import read_doc
from epe.validation.engine import Finding, make_finding


_REQ_RE = re.compile(r"\bREQ-\d+\b")
_CAP_RE = re.compile(r"\bCAP-\d+\b")
_DEC_RE = re.compile(r"\bDEC-\d+\b")
_TASK_RE = re.compile(r"\bTASK-\d+\b")
_TEST_RE = re.compile(r"\bTEST-\d+\b")
_COMP_RE = re.compile(r"\bCOMP-\d+\b")


def _scan_ids(text: str, pat: re.Pattern) -> set[str]:
    return set(pat.findall(text))


def build_traceability_graph(project_root: Path) -> dict[str, Any]:
    """Walk the project tree and compute a traceability projection."""
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    def add_node(node_id: str, stage: str, path: Path, **extra) -> None:
        if node_id not in nodes:
            nodes[node_id] = {"stage": stage, "path": str(path.relative_to(project_root)), **extra}

    def add_edge(a: str, b: str, kind: str) -> None:
        if a in nodes and b in nodes:
            edges.append({"from": a, "to": b, "type": kind})

    # Scan presales/scope.md and presales/handover.md for REQ-NNN declarations
    presales_scope = project_root / "presales" / "scope.md"
    presales_handover = project_root / "presales" / "handover.md"
    catalog_path = project_root / "product" / "catalog.md"

    if catalog_path.exists():
        for m in _CAP_RE.finditer(read_doc(catalog_path).body):
            add_node(f"CAP-{_idnum(m.group(0))}", "product", catalog_path)

    for path in (presales_scope, presales_handover):
        if not path.exists():
            continue
        body = read_doc(path).body
        for req in _scan_ids(body, _REQ_RE):
            add_node(req, "presales", path)
            for cap in _scan_ids(body, _CAP_RE):
                add_node(cap, "product", catalog_path if catalog_path.exists() else path)
                add_edge(cap, req, "supports")

    # Architecture stage: HLD/LLD/blueprint reference REQ, COMP, DEC, TASK, TEST
    for art in ("architecture/hld.md", "architecture/lld.md", "architecture/blueprint.md"):
        p = project_root / art
        if not p.exists():
            continue
        body = read_doc(p).body
        for comp in _scan_ids(body, _COMP_RE):
            add_node(comp, "architecture", p)
            for req in _scan_ids(body, _REQ_RE):
                add_edge(comp, req, "implements")
        for dec in _scan_ids(body, _DEC_RE):
            add_node(dec, "architecture", p)
            for req in _scan_ids(body, _REQ_RE):
                add_edge(dec, req, "decides_on")
        for task in _scan_ids(body, _TASK_RE):
            add_node(task, "delivery", p)
        for test in _scan_ids(body, _TEST_RE):
            add_node(test, "delivery", p)
            for req in _scan_ids(body, _REQ_RE):
                add_edge(test, req, "verifies")

    # Delivery: plan and test reference TASK/TEST
    for art in ("delivery/plan.md", "delivery/test.md", "delivery/acceptance.md"):
        p = project_root / art
        if not p.exists():
            continue
        body = read_doc(p).body
        for task in _scan_ids(body, _TASK_RE):
            add_node(task, "delivery", p)
            for test in _scan_ids(body, _TEST_RE):
                add_node(test, "delivery", p)
                add_edge(task, test, "verified_by")
        for test in _scan_ids(body, _TEST_RE):
            add_node(test, "delivery", p)
            for req in _scan_ids(body, _REQ_RE):
                add_edge(test, req, "verifies")

    # Orphan analysis
    referenced = {e["from"] for e in edges} | {e["to"] for e in edges}
    orphan = sorted(set(nodes.keys()) - referenced)

    return {
        "nodes": nodes,
        "edges": edges,
        "orphan": orphan,
    }


def _idnum(s: str) -> str:
    m = re.search(r"\d+", s)
    return m.group(0) if m else s


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
    reqs = _scan_ids(body, _REQ_RE)
    if reqs and contract.startswith("presales"):
        for req in sorted(reqs):
            implemented = any(
                e["from"] == req or e["to"] == req
                for e in graph["edges"]
                if e["type"] in ("implements", "verifies")
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
    comps = _scan_ids(body, _COMP_RE)
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
    tasks = _scan_ids(body, _TASK_RE)
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
