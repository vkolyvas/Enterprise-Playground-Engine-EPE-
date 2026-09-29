"""Parse the LLM response from the architecture engine."""

from __future__ import annotations

import json
import re
from typing import Any


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z0-9]*\n", "", text)
        text = re.sub(r"\n```\s*$", "", text)
    return text.strip()


def parse_architecture_response(response: str) -> dict[str, Any]:
    if not response:
        return _scaffold()
    text = _strip_code_fences(response)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", text)
        if not m:
            return _scaffold()
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError:
            return _scaffold()

    return {
        "body_validation": data.get("body_validation", ""),
        "body_hld": data.get("body_hld", ""),
        "body_security": data.get("body_security", ""),
        "body_lld": data.get("body_lld", ""),
        "body_cost": data.get("body_cost", ""),
        "body_blueprint": data.get("body_blueprint", ""),
        "metadata": {
            "provenance": {
                "source_documents": data.get("metadata", {}).get("provenance", {}).get(
                    "source_documents", []
                )
            },
        },
    }


def _scaffold() -> dict[str, Any]:
    return {
        "body_validation": "# Architecture Validation\n\n## Per-requirement validation\n## Findings\n",
        "body_hld": "# HLD\n\n## Drivers\n## Constraints\n## Options considered\n## Selected option\n## Logical components\n## Data flows\n## NFR mapping\n## Decision references\n",
        "body_security": "# Security\n\n## Threat model\n## Controls\n## Identity\n## Data protection\n## Network\n## Logging\n## Audit\n## Compliance\n",
        "body_lld": "# LLD\n\n## Component design\n## Interfaces\n## Data models\n## Configurations\n## Failure modes\n## Runbook stubs\n",
        "body_cost": "# Cost\n\n## Line items\n## Assumptions\n## Ranges\n## Optimization opportunities\n",
        "body_blueprint": "# Implementation Blueprint\n\n## Components\n## Implementation tasks\n## Test plan\n## Rollout strategy\n## Acceptance criteria\n## Risks and mitigations\n## Dependencies\n",
        "metadata": {"provenance": {"source_documents": []}},
    }
