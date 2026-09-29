"""Knowledge item and retrieval result models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class KnowledgeItem(BaseModel):
    """A chunked, metadata-bearing piece of knowledge."""

    chunk_id: str
    namespace: str
    source_document_id: str
    source_path: str
    section_heading: str = ""
    section_level: int = 0
    position: int = 0
    text: str = ""

    topics: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    authority: str = "internal"
    confidence: str = "medium"
    sensitivity: str = "internal"

    valid_from: datetime | None = None
    valid_until: datetime | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)

    embedding: list[float] | None = None

    def allowed_for(self, stage_namespaces: list[str]) -> bool:
        if self.namespace in stage_namespaces:
            return True
        if self.namespace.startswith("project:") and "project" in stage_namespaces:
            return True
        return False


class RetrievalResult(BaseModel):
    item: KnowledgeItem
    score: float = 0.0
    semantic_score: float | None = None
    keyword_score: float | None = None
    rerank_score: float | None = None
