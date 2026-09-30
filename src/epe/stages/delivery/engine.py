"""Delivery engine."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from epe.core.frontmatter import read_doc, write_doc
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
        return ["architecture/solution_baseline"]

    def precondition_inputs(self) -> dict[str, Path]:
        return {
            "architecture/solution_baseline": self.ctx.paths.project_architecture / "solution-baseline.md",
            "architecture/lld": self.ctx.paths.project_architecture / "lld.md",
        }

    def _safe_read(self, path: Path) -> str:
        if not path.exists():
            return "(not provided)"
        return read_doc(path).body

    def build_prompts(self, inputs: dict[str, Path]) -> tuple[str, str]:
        solution_baseline = self._safe_read(inputs.get("architecture/solution_baseline", Path("/dev/null")))
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
            solution_baseline=solution_baseline,
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
        # Emit EVD records for each TEST-NNN found in acceptance with a result
        acceptance = parsed.get("body_acceptance", "")
        if acceptance:
            evd_findings = self._emit_evidence_records(acceptance)
            findings.extend(evd_findings)
        return findings

    def _emit_evidence_records(self, acceptance_body: str) -> list[dict[str, Any]]:
        """Parse TEST-NNN results from acceptance and emit EVD records.

        For each TEST-NNN found with a PASS/FAIL result in the acceptance
        document, writes an EVD record to the evidence/ directory.
        """
        findings: list[dict[str, Any]] = []
        evidence_dir = self.ctx.paths.project_root / "evidence"
        evidence_dir.mkdir(parents=True, exist_ok=True)

        # Find all TEST-NNN references with result patterns
        test_pattern = re.compile(r"\b(TEST-\d+)\b", re.IGNORECASE)
        result_pattern = re.compile(
            r"\b(TEST-\d+)\b[\s\S]{0,200}?(PASS|PASSED|FAIL|FAILED)",
            re.IGNORECASE,
        )

        # Scan for test results
        for match in result_pattern.finditer(acceptance_body):
            test_id = match.group(1).upper()
            result = match.group(2).upper()

            # Generate EVD ID
            evd_count = len(list(evidence_dir.glob("EVD-*.md"))) + 1
            evd_id = f"EVD-{evd_count:03d}"

            meta = {
                "project_id": self.ctx.project_id,
                "stage": self.stage,
                "entity_type": "EVD",
                "test_id": test_id,
                "result": result,
                "status": "draft",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "generated_by": "delivery-engine",
                "source": "delivery/acceptance.md",
            }
            if self.ctx.opportunity:
                meta["opportunity"] = self.ctx.opportunity
            if self.ctx.customer:
                meta["customer"] = self.ctx.customer

            body = (
                f"# {evd_id}\n\n"
                f"**Test:** {test_id}\n"
                f"**Result:** {result}\n"
                f"**Source:** delivery/acceptance.md\n\n"
                f"Evidence record for {test_id} with result {result}.\n"
            )

            evd_path = evidence_dir / f"{evd_id}.md"
            write_doc(evd_path, body, meta)
            self.logger.info("Emitted evidence record %s for %s", evd_id, test_id)

        # Warn about TEST-NNNs without results
        all_tests = test_pattern.findall(acceptance_body.upper())
        tested = {m.group(1).upper() for m in result_pattern.finditer(acceptance_body)}
        for test_id in sorted(set(all_tests)):
            if test_id not in tested:
                findings.append(
                    {
                        "id": "F-DELIVERY-004",
                        "validator": "content",
                        "severity": "warning",
                        "message": f"Test {test_id} has no result recorded in acceptance.md.",
                    }
                )
        return findings
