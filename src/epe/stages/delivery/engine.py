"""Delivery engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from epe.core.frontmatter import read_doc
from epe.stages.base import StageContext, StageEngine
from epe.stages.delivery.parser import parse_delivery_response
from epe.stages.delivery.prompts import (
    DELIVERY_SYSTEM,
    DELIVERY_USER_TEMPLATE,
)


class DeliveryEngine(StageEngine):
    stage = "delivery"
    contract = "delivery"
    outputs = ["plan", "test", "acceptance", "onboarding", "operations", "handover_d", "feedback"]

    def preconditions(self) -> list[str]:
        return ["architecture/blueprint"]

    def precondition_inputs(self) -> dict[str, Path]:
        return {
            "architecture/blueprint": self.ctx.paths.project_architecture / "blueprint.md",
            "architecture/lld": self.ctx.paths.project_architecture / "lld.md",
        }

    def _safe_read(self, path: Path) -> str:
        if not path.exists():
            return "(not provided)"
        return read_doc(path).body

    def build_prompts(self, inputs: dict[str, Path]) -> tuple[str, str]:
        blueprint = self._safe_read(inputs.get("architecture/blueprint", Path("/dev/null")))
        lld = self._safe_read(inputs.get("architecture/lld", Path("/dev/null")))
        results = self.ctx.knowledge.retrieve(
            query="deployment runbook operations SLA monitoring",
            stage="delivery",
        )
        ctx_block = self.ctx.knowledge.format_for_prompt(results)
        prompt = DELIVERY_USER_TEMPLATE.format(
            project_id=self.ctx.project_id,
            customer=self.ctx.customer or "(unknown)",
            opportunity=self.ctx.opportunity or "(unknown)",
            blueprint=blueprint,
            lld=lld,
            context=ctx_block or "(no evidence retrieved)",
        )
        return DELIVERY_SYSTEM, prompt

    def parse_response(self, response: str) -> dict[str, Any]:
        return parse_delivery_response(response)

    def post_validate(self, parsed: dict[str, Any]) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        test = parsed.get("body_test", "")
        plan = parsed.get("body_plan", "")
        ops = parsed.get("body_operations", "")
        if "TEST-" not in test:
            findings.append(
                {
                    "id": "F-DELIVERY-001",
                    "validator": "content",
                    "severity": "warning",
                    "message": "Test plan does not reference any TEST-NNN.",
                }
            )
        if "TASK-" not in plan:
            findings.append(
                {
                    "id": "F-DELIVERY-002",
                    "validator": "content",
                    "severity": "warning",
                    "message": "Delivery plan does not reference any TASK-NNN.",
                }
            )
        if "sla" not in ops.lower() and "slo" not in ops.lower():
            findings.append(
                {
                    "id": "F-DELIVERY-003",
                    "validator": "content",
                    "severity": "warning",
                    "message": "Operations doc does not mention SLO/SLA targets.",
                }
            )
        return findings
