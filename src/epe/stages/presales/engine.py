"""Presales engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from epe.core.frontmatter import read_doc
from epe.stages.base import StageContext, StageEngine
from epe.stages.presales.parser import parse_presales_response
from epe.stages.presales.prompts import PRESALES_SYSTEM, PRESALES_USER_TEMPLATE


class PresalesEngine(StageEngine):
    stage = "presales"
    contract = "presales"
    outputs = ["discovery", "qualification", "scope", "sow", "handover"]

    def preconditions(self) -> list[str]:
        return ["product/readiness", "product/catalog"]

    def precondition_inputs(self) -> dict[str, Path]:
        return {
            "product/readiness": self.ctx.paths.project_product / "readiness.md",
            "product/catalog": self.ctx.paths.project_product / "catalog.md",
        }

    def _safe_read(self, path: Path) -> str:
        if not path.exists():
            return "(not provided)"
        doc = read_doc(path)
        return doc.body

    def build_prompts(self, inputs: dict[str, Path]) -> tuple[str, str]:
        readiness = self._safe_read(inputs.get("product/readiness", Path("/dev/null")))
        catalog = self._safe_read(inputs.get("product/catalog", Path("/dev/null")))

        results = self.ctx.knowledge.retrieve(
            query=f"customer requirements opportunity {self.ctx.customer or ''}",
            stage="presales",
        )
        ctx_block = self.ctx.knowledge.format_for_prompt(results)

        prompt = PRESALES_USER_TEMPLATE.format(
            project_id=self.ctx.project_id,
            customer=self.ctx.customer or "(unknown)",
            opportunity=self.ctx.opportunity or "(unknown)",
            readiness=readiness,
            catalog=catalog,
            context=ctx_block or "(no evidence retrieved)",
        )
        return PRESALES_SYSTEM, prompt

    def parse_response(self, response: str) -> dict[str, Any]:
        parsed = parse_presales_response(response)
        # Persist opportunity and customer from the context into metadata.
        if self.ctx.opportunity:
            parsed["metadata"]["opportunity"] = self.ctx.opportunity
        if self.ctx.customer:
            parsed["metadata"]["customer"] = self.ctx.customer
        return parsed

    def post_validate(self, parsed: dict[str, Any]) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        handover = parsed.get("body_handover", "")
        if not handover or len(handover.strip()) < 100:
            findings.append(
                {
                    "id": "F-PRESALES-001",
                    "validator": "content",
                    "severity": "blocker",
                    "message": "Handover body is empty or very short — downstream Architecture cannot proceed.",
                }
            )
        # At least one REQ-NNN must appear
        if "REQ-" not in handover:
            findings.append(
                {
                    "id": "F-PRESALES-002",
                    "validator": "content",
                    "severity": "error",
                    "message": "Handover contains no REQ-NNN identifiers — Architecture cannot trace requirements.",
                }
            )
        # Qualification verdict must be present
        if "verdict" not in parsed.get("body_qualification", "").lower():
            findings.append(
                {
                    "id": "F-PRESALES-003",
                    "validator": "content",
                    "severity": "warning",
                    "message": "Qualification does not state a verdict (qualified | deferred | disqualified).",
                }
            )
        return findings
