"""Product engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from epe.core.frontmatter import read_doc
from epe.stages.base import StageContext, StageEngine
from epe.stages.product.parser import parse_product_response
from epe.stages.product.prompts import PRODUCT_SYSTEM, PRODUCT_USER_TEMPLATE


class ProductEngine(StageEngine):
    stage = "product"
    contract = "product"
    outputs = ["definition", "catalog", "guardrails", "readiness"]

    def preconditions(self) -> list[str]:
        return []  # Product is the entry point.

    def precondition_inputs(self) -> dict[str, Path]:
        return {}

    def build_prompts(self, inputs: dict[str, Path]) -> tuple[str, str]:
        # Retrieve from product + global knowledge, plus project sources.
        results = self.ctx.knowledge.retrieve(
            query="product definition capabilities evidence market",
            stage="product",
        )
        ctx_block = self.ctx.knowledge.format_for_prompt(results)
        # Also include any documents the project has ingested, so that the
        # prompt reflects actual evidence.
        user_prompt = PRODUCT_USER_TEMPLATE.format(
            project_id=self.ctx.project_id,
            context=ctx_block or "(no evidence retrieved)",
        )
        return PRODUCT_SYSTEM, user_prompt

    def parse_response(self, response: str) -> dict[str, Any]:
        return parse_product_response(response)

    def post_validate(self, parsed: dict[str, Any]) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        body = parsed.get("body_readiness", "")
        if not body or len(body.strip()) < 50:
            findings.append(
                {
                    "id": "F-PRODUCT-001",
                    "validator": "content",
                    "severity": "warning",
                    "message": "Product readiness body is empty or very short.",
                }
            )
        # Catalog must have at least one capability row
        catalog = parsed.get("body_catalog", "")
        if "| standard" not in catalog and "| configurable" not in catalog \
                and "| custom" not in catalog and "| unsupported" not in catalog:
            findings.append(
                {
                    "id": "F-PRODUCT-002",
                    "validator": "content",
                    "severity": "warning",
                    "message": "Product catalog has no capability rows.",
                }
            )
        return findings

    # Override to read the just-written readiness artifact if we want to
    # pull content forward into a chained stage.
    def read_output(self, name: str) -> dict[str, Any]:
        path = self._output_path(name)
        if not path.exists():
            return {}
        doc = read_doc(path)
        return {"metadata": doc.metadata, "body": doc.body}
