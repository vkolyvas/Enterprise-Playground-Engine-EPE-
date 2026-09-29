"""Parse the LLM response from the product engine."""

from __future__ import annotations

import json
import re
from typing import Any


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        # remove leading and trailing fences
        text = re.sub(r"^```[a-zA-Z0-9]*\n", "", text)
        text = re.sub(r"\n```\s*$", "", text)
    return text.strip()


def parse_product_response(response: str) -> dict[str, Any]:
    if not response:
        # Return a deterministic scaffold so dry-runs still produce artifacts.
        return _scaffold()

    text = _strip_code_fences(response)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract a JSON object from the text
        m = re.search(r"\{[\s\S]*\}", text)
        if not m:
            return _scaffold()
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError:
            return _scaffold()

    # Normalize keys
    return {
        "body_definition": data.get("body_definition") or _default_definition(),
        "body_catalog": data.get("body_catalog") or _default_catalog(),
        "body_guardrails": data.get("body_guardrails") or _default_guardrails(),
        "body_readiness": data.get("body_readiness") or _default_readiness(),
        "metadata": {
            "provenance": {
                "source_documents": data.get("metadata", {}).get("provenance", {}).get(
                    "source_documents", []
                )
            }
        },
    }


def _scaffold() -> dict[str, Any]:
    return {
        "body_definition": _default_definition(),
        "body_catalog": _default_catalog(),
        "body_guardrails": _default_guardrails(),
        "body_readiness": _default_readiness(),
        "metadata": {"provenance": {"source_documents": []}},
    }


def _default_definition() -> str:
    return """# Product Definition

## Product name and one-line description
_Unavailable — engine produced no output. Provide a definition manually._

## Problem statement
## Target users and personas
## Use cases (must / should / could)
## Out-of-scope (explicit non-goals)
## Differentiators
## Evidence references (with document IDs)
"""


def _default_catalog() -> str:
    return """# Product Catalog

| ID | Capability | Classification | Depends on | Notes |
|----|------------|----------------|------------|-------|
"""


def _default_guardrails() -> str:
    return """# Product Guardrails

## Technical limits
## Compliance posture
## Data residency
## Commercial constraints
## Things we will NOT do
"""


def _default_readiness() -> str:
    return """# Product Readiness

## What is the product?
## Who is it for?
## What problems does it solve?
## What does it contain?
## What does it NOT contain?
## What can Presales sell?
## What requires Architecture?
## What are the technical limits?
## What are the commercial constraints?
## What evidence exists?
## What is configurable?
## What is custom?
"""
