"""Common stage engine scaffolding.

Every stage engine implements:

  class <Name>Engine(StageEngine):
      contract = "<dot.path>"
      outputs = [<output_filename>, ...]
      def build_prompts(...) -> (system, prompt)
      def parse_response(...) -> dict[str, Any]   # parsed frontmatter + body fields

The base class handles:
- project context loading
- knowledge retrieval
- LLM invocation
- structural validation of the response
- writing the artifact to disk with checksum + provenance
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from epe.core.config import EpeConfig
from epe.core.errors import ContractViolation, EpeError
from epe.core.frontmatter import write_doc
from epe.core.logging import audit_log, get_logger
from epe.core.paths import EpePaths
from epe.knowledge.engine import KnowledgeEngine
from epe.knowledge.providers import LLMProvider, make_llm_provider


@dataclass
class StageContext:
    config: EpeConfig
    paths: EpePaths
    knowledge: KnowledgeEngine
    llm: LLMProvider
    project_id: str
    opportunity: str | None = None
    customer: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class StageResult:
    stage: str
    outputs: dict[str, Path]
    metadata: dict[str, Any]
    validation_passed: bool
    findings: list[dict[str, Any]] = field(default_factory=list)


class StageEngine(ABC):
    """Abstract base for all stage engines."""

    stage: str = "abstract"
    contract: str = "abstract"
    outputs: list[str] = []

    def __init__(self, ctx: StageContext) -> None:
        self.ctx = ctx
        self.logger = get_logger(f"stage.{self.stage}")

    # The following hooks can be overridden -----------------------------------

    def preconditions(self) -> list[str]:
        """List of required input artifact paths; return ['product/readiness.md', ...]."""
        return []

    def precondition_inputs(self) -> dict[str, Path]:
        """Resolve precondition paths to actual files (if they exist)."""
        return {}

    @abstractmethod
    def build_prompts(self, inputs: dict[str, Any]) -> tuple[str, str]:
        """Return (system_prompt, user_prompt) for this stage run."""

    @abstractmethod
    def parse_response(self, response: str) -> dict[str, Any]:
        """Parse the LLM response into structured fields {key: value}."""

    def post_validate(self, parsed: dict[str, Any]) -> list[dict[str, Any]]:
        """Optional post-validation. Return a list of finding dicts."""
        return []

    # Standard pipeline ------------------------------------------------------

    def run(self, *, dry_run: bool = False) -> StageResult:
        self.logger.info("Running stage %s for project %s", self.stage, self.ctx.project_id)
        inputs = self.precondition_inputs()
        for required in self.preconditions():
            if required not in inputs or not inputs[required].exists():
                self.logger.warning(
                    "Missing precondition %s for stage %s (will proceed with available context)",
                    required,
                    self.stage,
                )

        system, prompt = self.build_prompts(inputs)
        if dry_run:
            self.logger.info("Dry run — skipping LLM call")
            response = ""
        else:
            response = self.ctx.llm.generate(
                system=system,
                prompt=prompt,
                max_tokens=self.ctx.config.models.llm.max_tokens,
                temperature=self.ctx.config.models.llm.temperature,
            )

        parsed = self.parse_response(response)
        findings = self.post_validate(parsed)
        if any(f.get("severity") == "blocker" for f in findings):
            raise ContractViolation(
                f"Stage {self.stage} produced contract-violating output",
                context={"findings": findings, "parsed": parsed},
            )

        outputs: dict[str, Path] = {}
        for name in self.outputs:
            body = parsed.get(f"body_{name}", parsed.get("body", ""))
            meta = dict(parsed.get("metadata", {}))
            meta.setdefault("contract", f"{self.stage}.{name}")
            meta.setdefault("version", 1)
            meta["stage"] = self.stage
            meta.setdefault("status", "draft")
            meta.setdefault("generated_at", datetime.now(timezone.utc).isoformat())
            meta.setdefault("generated_by", f"{self.stage}-engine")
            meta.setdefault("project_id", self.ctx.project_id)
            if self.ctx.opportunity:
                meta.setdefault("opportunity", self.ctx.opportunity)
            if self.ctx.customer:
                meta.setdefault("customer", self.ctx.customer)

            out_path = self._output_path(name)
            write_doc(out_path, body, meta)

            audit_log(
                self.ctx.paths.project_audit_log,
                {
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "actor": f"engine:{self.stage}",
                    "action": "write_artifact",
                    "target": str(out_path),
                    "contract": meta.get("contract"),
                },
            )
            outputs[name] = out_path

        return StageResult(
            stage=self.stage,
            outputs=outputs,
            metadata=parsed.get("metadata", {}),
            validation_passed=not any(f.get("severity") == "blocker" for f in findings),
            findings=findings,
        )

    # Helpers ----------------------------------------------------------------

    def _output_path(self, name: str) -> Path:
        mapping = {
            "definition": self.ctx.paths.project_product / "definition.md",
            "catalog": self.ctx.paths.project_product / "catalog.md",
            "guardrails": self.ctx.paths.project_product / "guardrails.md",
            "readiness": self.ctx.paths.project_product / "readiness.md",
            "discovery": self.ctx.paths.project_presales / "discovery.md",
            "qualification": self.ctx.paths.project_presales / "qualification.md",
            "scope": self.ctx.paths.project_presales / "scope.md",
            "sow": self.ctx.paths.project_presales / "sow.md",
            "handover": self.ctx.paths.project_presales / "handover.md",
            "validation": self.ctx.paths.project_architecture / "validation.md",
            "hld": self.ctx.paths.project_architecture / "hld.md",
            "security": self.ctx.paths.project_architecture / "security.md",
            "lld": self.ctx.paths.project_architecture / "lld.md",
            "cost": self.ctx.paths.project_architecture / "cost.md",
            "blueprint": self.ctx.paths.project_architecture / "blueprint.md",
            "plan": self.ctx.paths.project_delivery / "plan.md",
            "test": self.ctx.paths.project_delivery / "test.md",
            "acceptance": self.ctx.paths.project_delivery / "acceptance.md",
            "onboarding": self.ctx.paths.project_delivery / "onboarding.md",
            "operations": self.ctx.paths.project_delivery / "operations.md",
            "handover_d": self.ctx.paths.project_delivery / "handover.md",
            "feedback": self.ctx.paths.project_delivery / "feedback.md",
        }
        if name not in mapping:
            raise ValueError(f"Unknown output for stage {self.stage}: {name}")
        return mapping[name]


# Registry -----------------------------------------------------------------


def load_stage_engine(stage: str, ctx: StageContext) -> StageEngine:
    if stage == "product":
        from epe.stages.product.engine import ProductEngine
        return ProductEngine(ctx)
    if stage == "presales":
        from epe.stages.presales.engine import PresalesEngine
        return PresalesEngine(ctx)
    if stage == "architecture":
        from epe.stages.architecture.engine import ArchitectureEngine
        return ArchitectureEngine(ctx)
    if stage == "delivery":
        from epe.stages.delivery.engine import DeliveryEngine
        return DeliveryEngine(ctx)
    raise EpeError(f"Unknown stage: {stage}")


def run_stage(
    stage: str,
    ctx: StageContext,
    *,
    dry_run: bool = False,
) -> StageResult:
    engine = load_stage_engine(stage, ctx)
    return engine.run(dry_run=dry_run)
