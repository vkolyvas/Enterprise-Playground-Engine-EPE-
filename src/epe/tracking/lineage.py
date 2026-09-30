"""Lineage computation — trace requirements and documents through the lifecycle.

Given a requirement ID (e.g. REQ-001) or a document ID, the LineageComputer
builds the full forward chain:

    Customer Requirement (Presales)
        → Requirement (Architecture)
        → Solution Component (Architecture)
        → Architecture Decision (Architecture)
        → Delivery Task (Delivery)
        → Acceptance Test (Delivery)
        → Evidence

And the backward chain:

    Evidence
        → Acceptance Test
        → Delivery Task
        → Solution Component
        → Requirement
        → Customer Requirement
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from epe.tracking.models import DocumentRecord, LineageEntry, LinkType
from epe.tracking.registry import DocumentRegistry


@dataclass
class LineageChain:
    """A complete lineage path through the lifecycle."""

    entries: list[LineageEntry] = field(default_factory=list)
    stages_covered: list[str] = field(default_factory=list)

    def add(self, entry: LineageEntry) -> None:
        self.entries.append(entry)
        if entry.link_type and entry.link_type not in self.stages_covered:
            self.stages_covered.append(entry.link_type)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entries": [e.to_dict() for e in self.entries],
            "stages_covered": self.stages_covered,
        }


class LineageComputer:
    """Computes traceability lineage for documents and requirements."""

    # Stage order for forward tracing
    _STAGE_ORDER = ["presales", "architecture", "delivery"]

    def __init__(self, registry: DocumentRegistry) -> None:
        self.registry = registry

    # -------------------------------------------------------------------------
    # Forward trace: from a requirement or document to its downstream chain
    # -------------------------------------------------------------------------

    def trace_from_requirement(self, req_id: str) -> LineageChain:
        """Trace a requirement forward to delivery evidence.

        REQ-NNN (Presales scope or Architecture validation)
            → COMP-NNN (Architecture HLD/LLD)
            → TASK-NNN (Delivery plan)
            → TEST-NNN (Delivery test)
        """
        chain = LineageChain()
        visited: set[str] = set()

        # Find the document that defines this requirement
        source_docs = [
            d for d in self.registry.documents
            if req_id in d.requirements
        ]

        for doc in source_docs:
            self._trace_from_doc(doc.doc_id, chain, visited, req_id=req_id)

        return chain

    def trace_from_customer_requirement(self, cust_id: str) -> LineageChain:
        """Trace a customer requirement forward to solution requirements.

        CUST-NNN (Presales)
            → REQ-NNN (Presales scope or Architecture validation)
            → COMP-NNN (Architecture HLD/LLD)
            → TASK-NNN (Delivery plan)
            → TEST-NNN (Delivery test)
        """
        chain = LineageChain()
        visited: set[str] = set()

        # Find documents that define this customer requirement
        source_docs = [
            d for d in self.registry.documents
            if cust_id in d.customer_requirements
        ]

        for doc in source_docs:
            self._trace_from_doc(doc.doc_id, chain, visited, cust_id=cust_id)

        return chain

    def trace_from_document(self, doc_id: str) -> LineageChain:
        """Trace a document forward to all downstream documents."""
        chain = LineageChain()
        visited: set[str] = set()
        self._trace_from_doc(doc_id, chain, visited)
        return chain

    def _trace_from_doc(
        self,
        doc_id: str,
        chain: LineageChain,
        visited: set[str],
        *,
        req_id: str | None = None,
        cust_id: str | None = None,
    ) -> None:
        """Recursively trace from a document to its outputs."""
        if doc_id in visited:
            return
        visited.add(doc_id)

        doc = self.registry.get(doc_id)
        if not doc:
            return

        # Find output documents
        output_docs = self.registry.get_outputs(doc_id)
        for out_doc in output_docs:
            entry = LineageEntry(
                from_doc=doc_id,
                to_doc=out_doc.doc_id,
                link_type="traces_to",
                customer_requirement_id=cust_id,
                requirement_id=req_id,
                component_id=next((c for c in out_doc.components), None),
                task_id=next((t for t in out_doc.tasks), None),
                test_id=next((t for t in out_doc.tests), None),
            )
            chain.add(entry)
            self._trace_from_doc(out_doc.doc_id, chain, visited, req_id=req_id, cust_id=cust_id)

        # Also trace through COMP embedded in this doc's body
        for comp_id in doc.components:
            comp_docs = [d for d in self.registry.documents if comp_id in d.components]
            for comp_doc in comp_docs:
                if comp_doc.doc_id not in visited:
                    entry = LineageEntry(
                        from_doc=doc_id,
                        to_doc=comp_doc.doc_id,
                        link_type="implements",
                        component_id=comp_id,
                    )
                    chain.add(entry)
                    self._trace_from_doc(comp_doc.doc_id, chain, visited, req_id=req_id, cust_id=cust_id)

        for task_id in doc.tasks:
            task_docs = [d for d in self.registry.documents if task_id in d.tasks]
            for task_doc in task_docs:
                if task_doc.doc_id not in visited:
                    entry = LineageEntry(
                        from_doc=doc_id,
                        to_doc=task_doc.doc_id,
                        link_type="implements",
                        task_id=task_id,
                    )
                    chain.add(entry)
                    self._trace_from_doc(task_doc.doc_id, chain, visited, req_id=req_id, cust_id=cust_id)

    # -------------------------------------------------------------------------
    # Backward trace: from a document to its upstream sources
    # -------------------------------------------------------------------------

    def trace_to_document(self, doc_id: str) -> LineageChain:
        """Trace a document backward to all upstream documents and requirements."""
        chain = LineageChain()
        visited: set[str] = set()
        self._trace_to_doc(doc_id, chain, visited)
        return chain

    def _trace_to_doc(
        self,
        doc_id: str,
        chain: LineageChain,
        visited: set[str],
    ) -> None:
        """Recursively trace from a document to its inputs."""
        if doc_id in visited:
            return
        visited.add(doc_id)

        doc = self.registry.get(doc_id)
        if not doc:
            return

        # Find input documents
        input_docs = self.registry.get_inputs(doc_id)
        for inp_doc in input_docs:
            entry = LineageEntry(
                from_doc=inp_doc.doc_id,
                to_doc=doc_id,
                link_type="supported_by",
                requirement_id=next((r for r in inp_doc.requirements), None),
            )
            chain.add(entry)
            self._trace_to_doc(inp_doc.doc_id, chain, visited)

        # Also trace through embedded REQ/CAP/DEC in this doc
        for req_id in doc.requirements:
            req_docs = [d for d in self.registry.documents if req_id in d.requirements]
            for req_doc in req_docs:
                if req_doc.doc_id not in visited:
                    entry = LineageEntry(
                        from_doc=req_doc.doc_id,
                        to_doc=doc_id,
                        link_type="traces_to",
                        requirement_id=req_id,
                    )
                    chain.add(entry)
                    self._trace_to_doc(req_doc.doc_id, chain, visited)

    # -------------------------------------------------------------------------
    # Full lifecycle traceability matrix
    # -------------------------------------------------------------------------

    def build_traceability_matrix(self) -> dict[str, Any]:
        """Build the complete traceability matrix for a project.

        Returns a dict keyed by requirement ID, with all downstream
        components, decisions, tasks, tests, and evidence.
        """
        matrix: dict[str, dict[str, Any]] = {}

        # Find all requirements across all documents
        all_reqs: set[str] = set()
        all_custs: set[str] = set()
        for doc in self.registry.documents:
            all_reqs.update(doc.requirements)
            all_custs.update(doc.customer_requirements)

        for cust_id in sorted(all_custs):
            chain = self.trace_from_customer_requirement(cust_id)
            matrix[f"cust:{cust_id}"] = {
                "customer_requirement": cust_id,
                "chain": chain.to_dict(),
                "requirements": list({
                    e.requirement_id for e in chain.entries if e.requirement_id
                }),
                "components": list({
                    e.component_id for e in chain.entries if e.component_id
                }),
                "decisions": list({
                    e.decision_id for e in chain.entries if e.decision_id
                }),
                "tasks": list({e.task_id for e in chain.entries if e.task_id}),
                "tests": list({e.test_id for e in chain.entries if e.test_id}),
                "evidence": list({e.evidence_id for e in chain.entries if e.evidence_id}),
            }

        for req_id in sorted(all_reqs):
            chain = self.trace_from_requirement(req_id)
            matrix[req_id] = {
                "requirement": req_id,
                "chain": chain.to_dict(),
                "components": list({
                    e.component_id for e in chain.entries if e.component_id
                }),
                "decisions": list({
                    e.decision_id for e in chain.entries if e.decision_id
                }),
                "tasks": list({e.task_id for e in chain.entries if e.task_id}),
                "tests": list({e.test_id for e in chain.entries if e.test_id}),
                "evidence": list({e.evidence_id for e in chain.entries if e.evidence_id}),
            }

        return matrix

    # -------------------------------------------------------------------------
    # Stage handoff completeness
    # -------------------------------------------------------------------------

    def stage_handoff_status(
        self,
        from_stage: str,
        to_stage: str,
    ) -> dict[str, Any]:
        """Check the completeness of the handoff from one stage to the next.

        Returns dict with:
        - handover_doc: the handoff document (e.g. handover.md or blueprint.md)
        - required_inputs: documents from the source stage consumed by to_stage
        - missing_inputs: input documents that don't exist
        - downstream_docs: all documents in the target stage
        """
        # Identify the handover artifact
        handover_name = self._handover_name(to_stage)
        handover_doc = self.registry.get(handover_name)

        # Find all documents in the target stage that have inputs
        target_docs = self.registry.by_stage(to_stage)
        all_inputs: set[str] = set()
        for doc in target_docs:
            all_inputs.update(doc.inputs)

        # Find all source-stage documents
        source_docs = self.registry.by_stage(from_stage)
        source_ids = {d.doc_id for d in source_docs}

        missing = [inp for inp in all_inputs if inp not in source_ids and not self.registry.get(inp)]

        return {
            "from_stage": from_stage,
            "to_stage": to_stage,
            "handover_doc": handover_doc.doc_id if handover_doc else None,
            "handover_approved": handover_doc.is_approved if handover_doc else False,
            "target_doc_count": len(target_docs),
            "all_inputs": sorted(all_inputs),
            "missing_inputs": missing,
            "has_missing": len(missing) > 0,
        }

    def _handover_name(self, stage: str) -> str:
        """Return the canonical handoff document name for each stage."""
        mapping = {
            "presales": "presales/handover.md",
            "architecture": "architecture/solution-baseline.md",
            "delivery": "delivery/handover.md",
        }
        return mapping.get(stage, f"{stage}/handover.md")
