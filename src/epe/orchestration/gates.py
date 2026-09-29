"""Gate registry and runner."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from epe.core.config import EpeConfig
from epe.core.errors import GateFailure
from epe.core.logging import get_logger

logger = get_logger("orchestration.gates")


@dataclass
class GateResult:
    gate_id: str
    verdict: str            # pass | fail | waive
    severity: str
    findings: list[dict[str, Any]]


class GateRegistry:
    """Resolves gate predicate module paths and invokes them."""

    def __init__(self, config: EpeConfig) -> None:
        self.config = config

    def _resolve(self, gate_id: str):
        if gate_id not in self.config.validation.gate_predicates:
            raise GateFailure(f"Gate not registered: {gate_id}")
        mod_path = self.config.validation.gate_predicates[gate_id].module
        module_name, _, attr = mod_path.rpartition(".")
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            raise GateFailure(f"Cannot import gate module {module_name}: {e}") from e
        predicate = getattr(module, "run", None) or getattr(module, attr, None)
        if predicate is None:
            raise GateFailure(f"Gate module missing 'run': {mod_path}")
        return predicate

    def run(self, gate_id: str, *, project_paths, **kwargs) -> GateResult:
        predicate = self._resolve(gate_id)
        verdict = predicate(project_paths=project_paths, **kwargs)
        # Normalize to a string verdict
        v = getattr(verdict, "value", verdict) or "fail"
        v = str(v).lower()
        severity = self.config.validation.gate_predicates[gate_id].severity
        return GateResult(gate_id=gate_id, verdict=v, severity=severity, findings=[])


def run_gate(gate_id: str, *, config: EpeConfig, project_paths, **kwargs) -> GateResult:
    registry = GateRegistry(config)
    return registry.run(gate_id, project_paths=project_paths, **kwargs)
