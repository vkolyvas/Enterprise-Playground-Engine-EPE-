"""Lifecycle state machine.

States:
  product_active -> product_ready -> presales_active -> presales_ready ->
  architecture_active -> architecture_ready -> delivery_active ->
  service_live -> optimization -> (feedback to) product_active
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from epe.core.errors import EpeError, GateFailure
from epe.core.logging import audit_log


class State(str, Enum):
    PRODUCT_ACTIVE = "product_active"
    PRODUCT_READY = "product_ready"
    PRESALES_ACTIVE = "presales_active"
    PRESALES_READY = "presales_ready"
    ARCHITECTURE_ACTIVE = "architecture_active"
    ARCHITECTURE_READY = "architecture_ready"
    DELIVERY_ACTIVE = "delivery_active"
    SERVICE_LIVE = "service_live"
    OPTIMIZATION = "optimization"


# Allowed forward transitions
_TRANSITIONS: dict[State, set[State]] = {
    State.PRODUCT_ACTIVE: {State.PRODUCT_READY},
    State.PRODUCT_READY: {State.PRESALES_ACTIVE},
    State.PRESALES_ACTIVE: {State.PRESALES_READY},
    State.PRESALES_READY: {State.ARCHITECTURE_ACTIVE},
    State.ARCHITECTURE_ACTIVE: {State.ARCHITECTURE_READY},
    State.ARCHITECTURE_READY: {State.DELIVERY_ACTIVE},
    State.DELIVERY_ACTIVE: {State.SERVICE_LIVE},
    State.SERVICE_LIVE: {State.OPTIMIZATION},
    State.OPTIMIZATION: {State.PRODUCT_ACTIVE},
}


@dataclass
class LifecycleState:
    raw: dict[str, Any]
    state_path: Path

    @property
    def current(self) -> State:
        try:
            return State(self.raw["stage"] + "_" + self.raw["status"])
        except KeyError:
            return State.PRODUCT_ACTIVE
        except ValueError:
            return State.PRODUCT_ACTIVE

    @property
    def gates(self) -> dict[str, dict[str, str]]:
        return self.raw.get("gates", {})


@dataclass
class Lifecycle:
    state: LifecycleState

    @classmethod
    def load(cls, state_path: Path) -> "Lifecycle":
        if not state_path.exists():
            raise FileNotFoundError(f"No lifecycle state at {state_path}")
        data = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}
        return cls(state=LifecycleState(raw=data, state_path=state_path))

    def save(self) -> None:
        self.state.state_path.write_text(
            yaml.safe_dump(self.state.raw, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    def gate(self, stage: str, name: str, status: str, *, reason: str | None = None) -> None:
        gates = self.state.raw.setdefault("gates", {})
        stage_gates = gates.setdefault(stage, {})
        stage_gates[name] = status
        if reason:
            stage_gates.setdefault(f"{name}_reason", reason)
        audit_log(
            self.state.state_path.parent / ".audit.log",
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "actor": "orchestrator",
                "action": "gate_update",
                "stage": stage,
                "gate": name,
                "status": status,
                "reason": reason,
            },
        )

    def can_transition(self, to: State) -> bool:
        return to in _TRANSITIONS.get(self.state.current, set())

    def transition(self, to: State, *, gate_predicates: dict[str, Any] | None = None) -> None:
        if not self.can_transition(to):
            raise EpeError(
                f"Illegal transition {self.state.current.value} -> {to.value}",
                context={"current": self.state.current.value, "target": to.value},
            )

        # Gate enforcement
        if gate_predicates:
            for gate_id, predicate in gate_predicates.items():
                verdict = predicate()
                if verdict not in ("pass", "waive"):
                    raise GateFailure(
                        f"Gate {gate_id} failed",
                        context={"gate": gate_id, "verdict": verdict},
                    )
                    return

        self.state.raw.setdefault("history", []).append(
            {
                "from": self.state.current.value,
                "to": to.value,
                "at": datetime.now(timezone.utc).isoformat(),
                "actor": "orchestrator",
            }
        )
        # Update stage and status from the new state
        new_value = to.value
        if "_" in new_value:
            stage, status = new_value.rsplit("_", 1)
            self.state.raw["stage"] = stage
            self.state.raw["status"] = status
        self.save()


def create_lifecycle(state_path: Path, initial: dict | None = None) -> Lifecycle:
    initial = initial or {
        "project_id": state_path.parent.name,
        "stage": "product",
        "status": "active",
        "gates": {
            "product": {"status": "pending"},
            "presales": {"qualification": "pending", "scope": "pending", "handover": "pending"},
            "architecture": {"requirements": "pending", "hld": "pending", "lld": "pending"},
            "delivery": {"deployment": "pending", "acceptance": "pending"},
        },
        "history": [],
    }
    state_path.write_text(
        yaml.safe_dump(initial, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return Lifecycle.load(state_path)


def transition(state_path: Path, to: State, *, gate_predicates: dict | None = None) -> Lifecycle:
    lc = Lifecycle.load(state_path)
    lc.transition(to, gate_predicates=gate_predicates)
    return lc
