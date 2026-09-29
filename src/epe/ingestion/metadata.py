"""Source document metadata model."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    PRICING = "pricing"
    COMPLIANCE = "compliance"
    VENDOR = "vendor"
    MARKET = "market"
    INTERNAL = "internal"
    OTHER = "other"


class Domain(str, Enum):
    CUSTOMER = "customer"
    VENDOR = "vendor"
    INTERNAL = "internal"
    MARKET = "market"


class Authority(str, Enum):
    CUSTOMER = "customer"
    VENDOR = "vendor"
    INTERNAL = "internal"
    MARKET = "market"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Sensitivity(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class Stage(str, Enum):
    PRODUCT = "product"
    PRESALES = "presales"
    ARCHITECTURE = "architecture"
    DELIVERY = "delivery"


class Contains(BaseModel):
    requirements: bool = False
    architecture: bool = False
    pricing: bool = False
    compliance: bool = False
    decisions: bool = False
    risks: bool = False


class SourceDocument(BaseModel):
    document_id: str
    filename: str
    source_path: str
    sha256: str

    document_type: DocumentType = DocumentType.OTHER
    domain: Domain = Domain.INTERNAL
    stage_relevance: list[Stage] = Field(default_factory=list)

    authority: Authority = Authority.INTERNAL
    confidence: Confidence = Confidence.MEDIUM

    version: str = "1.0"
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    topics: list[str] = Field(default_factory=list)
    contains: Contains = Field(default_factory=Contains)

    sensitivity: Sensitivity = Sensitivity.INTERNAL
    retention: str = "P7Y"

    project_id: str | None = None
    title: str | None = None
    description: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)

    def to_yaml(self) -> str:
        data = self.model_dump(mode="json")
        return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def generate_document_id(path: Path) -> str:
    h = hashlib.sha256(path.read_bytes()).hexdigest()[:12].upper()
    return f"DOC-{h}"


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_metadata(doc: SourceDocument, metadata_path: Path) -> Path:
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(doc.to_yaml(), encoding="utf-8")
    return metadata_path


def load_metadata(metadata_path: Path) -> SourceDocument:
    data = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    return SourceDocument.model_validate(data)


def to_jsonable(doc: SourceDocument) -> dict[str, Any]:
    return json.loads(doc.model_dump_json())
