"""Document classifier: heuristic + rule-based stage_relevance detection."""

from __future__ import annotations

import re
from dataclasses import dataclass

from epe.ingestion.metadata import (
    Authority,
    Confidence,
    Contains,
    DocumentType,
    Domain,
    Sensitivity,
    Stage,
)


@dataclass
class ClassifierResult:
    document_type: DocumentType
    domain: Domain
    authority: Authority
    confidence: Confidence
    stage_relevance: list[Stage]
    contains: Contains
    topics: list[str]
    sensitivity: Sensitivity


_TYPE_KEYWORDS: dict[DocumentType, list[str]] = {
    DocumentType.REQUIREMENTS: ["requirement", "rfp", "rfi", "specification", "scope of work", "needs"],
    DocumentType.ARCHITECTURE: ["architecture", "design", "topology", "diagram", "schematic"],
    DocumentType.PRICING: ["pricing", "price list", "quote", "commercial", "cost"],
    DocumentType.COMPLIANCE: ["compliance", "iso", "soc2", "gdpr", "hipaa", "pci"],
    DocumentType.VENDOR: ["vendor", "datasheet", "manual", "release notes"],
    DocumentType.MARKET: ["market", "analyst", "gartner", "forrester", "trends"],
    DocumentType.INTERNAL: ["internal", "playbook", "runbook", "sop"],
}


_TOPIC_KEYWORDS = [
    "networking", "security", "cloud", "identity", "kubernetes", "database",
    "postgresql", "mysql", "redis", "kafka", "object storage", "observability",
    "monitoring", "logging", "ci/cd", "automation", "compliance",
    "ai", "ml", "analytics", "billing", "saas", "api", "sso", "saml", "oauth",
]


class DocumentClassifier:
    """Deterministic, rule-based document classifier."""

    def classify(
        self,
        *,
        filename: str,
        text: str,
        hints: dict | None = None,
    ) -> ClassifierResult:
        hints = hints or {}
        text_lower = text.lower()
        name_lower = filename.lower()
        haystack = f"{name_lower}\n{text_lower}"

        # Document type
        best_type = DocumentType.OTHER
        best_score = 0
        for t, kws in _TYPE_KEYWORDS.items():
            score = sum(1 for k in kws if k in haystack)
            if score > best_score:
                best_score = score
                best_type = t
        if hints.get("document_type"):
            best_type = DocumentType(hints["document_type"])

        # Stage relevance
        stages: list[Stage] = []
        stage_signals = {
            Stage.PRODUCT: ["product", "roadmap", "feature", "vision"],
            Stage.PRESALES: ["customer", "rfp", "rfq", "proposal", "presales", "sow"],
            Stage.ARCHITECTURE: ["architecture", "design", "hld", "lld", "topology", "diagram"],
            Stage.DELIVERY: ["deployment", "runbook", "operations", "onboarding", "sla"],
        }
        for stage, sigs in stage_signals.items():
            if any(s in haystack for s in sigs):
                stages.append(stage)
        if not stages:
            stages = [Stage.PRESALES, Stage.ARCHITECTURE]
        if hints.get("stage_relevance"):
            stages = [Stage(s) for s in hints["stage_relevance"]]

        # Domain
        domain = Domain.INTERNAL
        if any(w in haystack for w in ["customer", "client", "rfp", "rfq"]):
            domain = Domain.CUSTOMER
        elif any(w in haystack for w in ["vendor", "supplier", "datasheet"]):
            domain = Domain.VENDOR
        elif any(w in haystack for w in ["market", "analyst", "trends"]):
            domain = Domain.MARKET
        if hints.get("domain"):
            domain = Domain(hints["domain"])

        # Authority mirrors domain by default
        authority = Authority(domain.value)

        # Confidence: high if many keyword matches, medium if few, low if none
        confidence = Confidence.HIGH if best_score >= 2 else Confidence.MEDIUM if best_score >= 1 else Confidence.LOW

        # Contains
        contains = Contains(
            requirements=bool(re.search(r"\b(must|shall|should|requirement|REQ-\d+)\b", text, re.IGNORECASE)),
            architecture=best_type is DocumentType.ARCHITECTURE,
            pricing=best_type is DocumentType.PRICING,
            compliance=best_type is DocumentType.COMPLIANCE or "iso 27001" in text_lower or "soc2" in text_lower,
            decisions=bool(re.search(r"\bdecision|ADR-\d+|DEC-\d+\b", text, re.IGNORECASE)),
            risks=bool(re.search(r"\brisks?|RSK-\d+\b", text, re.IGNORECASE)),
        )

        # Topics
        topics = sorted({t for t in _TOPIC_KEYWORDS if t in haystack})
        if hints.get("topics"):
            topics = sorted(set(topics + list(hints["topics"])))

        # Sensitivity
        sensitivity = Sensitivity.INTERNAL
        if any(w in haystack for w in ["confidential", "restricted", "nda"]):
            sensitivity = Sensitivity.CONFIDENTIAL
        elif "public" in haystack and "marketing" in haystack:
            sensitivity = Sensitivity.PUBLIC
        if hints.get("sensitivity"):
            sensitivity = Sensitivity(hints["sensitivity"])

        return ClassifierResult(
            document_type=best_type,
            domain=domain,
            authority=authority,
            confidence=confidence,
            stage_relevance=stages,
            contains=contains,
            topics=topics,
            sensitivity=sensitivity,
        )
