"""Architecture engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from epe.core.frontmatter import read_doc
from epe.stages.base import StageContext, StageEngine
from epe.stages.architecture.parser import parse_architecture_response
from epe.stages.architecture.prompts import (
    ARCHITECTURE_SYSTEM,
    ARCHITECTURE_USER_TEMPLATE,
)


class ArchitectureEngine(StageEngine):
    stage = "architecture"
    contract = "architecture"
    outputs = ["validation", "hld", "security", "lld", "cost", "blueprint"]

    def preconditions(self) -> list[str]:
        return ["presales/handover"]

    def precondition_inputs(self) -> dict[str, Path]:
        return {
            "presales/handover": self.ctx.paths.project_presales / "handover.md",
            "product/readiness": self.ctx.paths.project_product / "readiness.md",
        }

    def _safe_read(self, path: Path) -> str:
        if not path.exists():
            return "(not provided)"
        return read_doc(path).body

    def build_prompts(self, inputs: dict[str, Path]) -> tuple[str, str]:
        handover = self._safe_read(inputs.get("presales/handover", Path("/dev/null")))
        readiness = self._safe_read(inputs.get("product/readiness", Path("/dev/null")))
        results = self.ctx.knowledge.retrieve(
            query="architecture reference patterns NFR security compliance",
            stage="architecture",
        )
        ctx_block = self.ctx.knowledge.format_for_prompt(results)
        prompt = ARCHITECTURE_USER_TEMPLATE.format(
            project_id=self.ctx.project_id,
            customer=self.ctx.customer or "(unknown)",
            opportunity=self.ctx.opportunity or "(unknown)",
            handover=handover,
            readiness=readiness,
            context=ctx_block or "(no evidence retrieved)",
        )
        return ARCHITECTURE_SYSTEM, prompt

    def parse_response(self, response: str) -> dict[str, Any]:
        return parse_architecture_response(response)

    def post_validate(self, parsed: dict[str, Any]) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        hld = parsed.get("body_hld", "")
        lld = parsed.get("body_lld", "")
        blueprint = parsed.get("body_blueprint", "")
        if "COMP-" not in hld:
            findings.append(
                {
                    "id": "F-ARCH-001",
                    "validator": "content",
                    "severity": "warning",
                    "message": "HLD has no COMP-NNN component identifiers.",
                }
            )
        if "DEC-" not in hld:
            findings.append(
                {
                    "id": "F-ARCH-002",
                    "validator": "content",
                    "severity": "warning",
                    "message": "HLD does not reference DEC-NNN decisions.",
                }
            )
        if "TASK-" not in blueprint:
            findings.append(
                {
                    "id": "F-ARCH-003",
                    "validator": "content",
                    "severity": "error",
                    "message": "Blueprint has no TASK-NNN implementation tasks — Delivery cannot proceed.",
                }
            )
        if "TEST-" not in blueprint:
            findings.append(
                {
                    "id": "F-ARCH-004",
                    "validator": "content",
                    "severity": "error",
                    "message": "Blueprint has no TEST-NNN acceptance tests.",
                }
            )
        if len(lld.strip()) < 200:
            findings.append(
                {
                    "id": "F-ARCH-005",
                    "validator": "content",
                    "severity": "warning",
                    "message": "LLD body is very short — Delivery will need more detail.",
                }
            )
        return findings
