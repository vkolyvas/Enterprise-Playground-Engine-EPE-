"""Parse the LLM response from the presales engine."""

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


def parse_presales_response(response: str) -> dict[str, Any]:
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
        "body_discovery": data.get("body_discovery", ""),
        "body_qualification": data.get("body_qualification", ""),
        "body_scope": data.get("body_scope", ""),
        "body_sow": data.get("body_sow", ""),
        "body_handover": data.get("body_handover", ""),
        "metadata": {
            "provenance": {
                "source_documents": data.get("metadata", {}).get("provenance", {}).get(
                    "source_documents", []
                )
            },
            "opportunity": data.get("metadata", {}).get("opportunity"),
            "customer": data.get("metadata", {}).get("customer"),
        },
    }


def _scaffold() -> dict[str, Any]:
    return {
        "body_discovery": "# Discovery\n\n## Stakeholders\n## Business objectives\n## Current state\n## Drivers\n## Timeline\n## Success criteria\n",
        "body_qualification": "# Qualification\n\n## Budget\n## Authority\n## Need\n## Timeline\n## Fit\n## Verdict\n## Rationale\n",
        "body_scope": "# Scope\n\n## In-scope\n## Out-of-scope\n## Assumptions\n## Dependencies\n## Product capabilities\n## Product gaps\n## Custom requirements\n## Integrations\n## Security\n## SLA\n## Commercial constraints\n",
        "body_sow": "# Statement of Work\n\n## Parties\n## Scope reference\n## Deliverables\n## Timeline\n## Acceptance\n## Pricing summary\n## Assumptions\n## Signatures\n",
        "body_handover": _default_handover(),
        "metadata": {"provenance": {"source_documents": []}},
    }


def _default_handover() -> str:
    return """# Presales → Architecture Handover

## Opportunity
## Customer
## Business Objective
## Confirmed Requirements
## Technical Requirements
## Non-Functional Requirements
## Assumptions
## Constraints
## Product Capabilities Used
## Product Gaps
## Custom Requirements
## Integrations
## Security Requirements
## SLA Requirements
## Commercial Constraints
## Open Questions
## Architecture Decisions Required
## Acceptance Criteria
"""
