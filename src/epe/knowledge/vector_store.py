"""In-memory vector store with cosine similarity.

The abstraction allows swapping in pgvector, chroma, qdrant, etc.
"""

from __future__ import annotations

import math
from typing import Iterable

from epe.knowledge.models import KnowledgeItem


def _cosine(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


class InMemoryVectorStore:
    """A simple in-memory vector store keyed by chunk_id."""

    def __init__(self) -> None:
        self._items: dict[str, KnowledgeItem] = {}

    def upsert(self, item: KnowledgeItem) -> None:
        self._items[item.chunk_id] = item

    def upsert_many(self, items: Iterable[KnowledgeItem]) -> None:
        for it in items:
            self.upsert(it)

    def delete(self, chunk_id: str) -> None:
        self._items.pop(chunk_id, None)

    def get(self, chunk_id: str) -> KnowledgeItem | None:
        return self._items.get(chunk_id)

    def all(self) -> list[KnowledgeItem]:
        return list(self._items.values())

    def query(
        self,
        *,
        vector: list[float],
        top_k: int = 12,
        namespace_filter: list[str] | None = None,
    ) -> list[tuple[KnowledgeItem, float]]:
        scored: list[tuple[KnowledgeItem, float]] = []
        for item in self._items.values():
            if item.embedding is None:
                continue
            if namespace_filter and item.namespace not in namespace_filter:
                continue
            scored.append((item, _cosine(vector, item.embedding)))
        scored.sort(key=lambda kv: kv[1], reverse=True)
        return scored[:top_k]

    def __len__(self) -> int:
        return len(self._items)
