"""Parse the LLM response from the delivery engine."""

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


def parse_delivery_response(response: str) -> dict[str, Any]:
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
        "body_plan": data.get("body_plan", ""),
        "body_test": data.get("body_test", ""),
        "body_acceptance": data.get("body_acceptance", ""),
        "body_onboarding": data.get("body_onboarding", ""),
        "body_operations": data.get("body_operations", ""),
        "body_handover_d": data.get("body_handover_d", ""),
        "body_feedback": data.get("body_feedback", ""),
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
        "body_plan": "# Delivery Plan\n\n## Sequencing\n## Milestones\n## Owners\n## Dependencies\n## Prerequisites\n",
        "body_test": "# Test Plan\n\n## Per-test mapping\n",
        "body_acceptance": "# Acceptance\n\n## Executed tests\n## Evidence\n## Sign-off\n",
        "body_onboarding": "# Onboarding\n\n## Onboarding steps\n## Training plan\n## Support contacts\n",
        "body_operations": "# Operations\n\n## Monitoring\n## Alerting\n## SLO/SLA\n## Runbooks\n## Escalation\n",
        "body_handover_d": "# Customer Handover\n\n## Customer handover\n",
        "body_feedback": "# Feedback to Product\n\n## Incidents\n## Cost variance\n## Usage telemetry\n## Deployment problems\n## Customer feedback\n## Operational lessons\n",
        "metadata": {"provenance": {"source_documents": []}},
    }
