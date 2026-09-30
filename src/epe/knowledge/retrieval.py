"""Hybrid retrieval: semantic + keyword + optional rerank."""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable

from epe.knowledge.models import KnowledgeItem, RetrievalResult
from epe.knowledge.vector_store import InMemoryVectorStore


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_]{2,}", text.lower())


def _keyword_score(query: str, item: KnowledgeItem) -> float:
    q_tokens = Counter(_tokens(query))
    if not q_tokens:
        return 0.0
    i_tokens = Counter(_tokens(item.text + " " + item.section_heading))
    inter = sum((q_tokens & i_tokens).values())
    return inter / sum(q_tokens.values())


def _bm25_like(query: str, items: list[KnowledgeItem], k1: float = 1.5, b: float = 0.75) -> list[float]:
    q_tokens = set(_tokens(query))
    if not q_tokens:
        return [0.0] * len(items)
    N = len(items) or 1
    avgdl = sum(len(_tokens(it.text)) for it in items) / N
    scores: list[float] = []
    for it in items:
        toks = _tokens(it.text)
        dl = len(toks) or 1
        score = 0.0
        for q in q_tokens:
            tf = toks.count(q)
            if tf == 0:
                continue
            df = sum(1 for it2 in items if q in _tokens(it2.text))
            idf = max(0.0, (N - df + 0.5) / (df + 0.5))
            num = tf * (k1 + 1)
            den = tf + k1 * (1 - b + b * dl / max(avgdl, 1))
            score += idf * (num / den)
        scores.append(score)
    return scores


def _reciprocal_rank_fusion(
    semantic: list[tuple[KnowledgeItem, float]],
    keyword: list[tuple[KnowledgeItem, float]],
    k: int = 60,
) -> list[tuple[KnowledgeItem, float, float | None, float | None]]:
    scores: dict[str, tuple[KnowledgeItem, float, float | None, float | None]] = {}
    for rank, (item, sc) in enumerate(semantic):
        cur = scores.get(item.chunk_id)
        s = 1.0 / (k + rank + 1)
        if cur is None:
            scores[item.chunk_id] = (item, s, sc, None)
        else:
            item_, total, sem, _kw = cur
            scores[item.chunk_id] = (item_, total + s, sem, _kw)
    for rank, (item, sc) in enumerate(keyword):
        cur = scores.get(item.chunk_id)
        s = 1.0 / (k + rank + 1)
        if cur is None:
            scores[item.chunk_id] = (item, s, None, sc)
        else:
            item_, total, _sem, kw = cur
            scores[item.chunk_id] = (item_, total + s, _sem, sc)
    fused = sorted(scores.values(), key=lambda kv: kv[1], reverse=True)
    return fused


def hybrid_retrieve(
    *,
    query: str,
    query_vector: list[float],
    store: InMemoryVectorStore,
    top_k: int = 12,
    namespace_filter: list[str] | None = None,
    semantic: bool = True,
    keyword: bool = True,
) -> list[RetrievalResult]:
    candidates = [
        item
        for item in store.all()
        if not namespace_filter or item.namespace in namespace_filter
    ]

    sem_results: list[tuple[KnowledgeItem, float]] = []
    if semantic:
        sem_results = store.query(vector=query_vector, top_k=top_k * 3, namespace_filter=namespace_filter)

    kw_results: list[tuple[KnowledgeItem, float]] = []
    if keyword:
        kw_scores = _bm25_like(query, candidates)
        kw_pairs = list(zip(candidates, kw_scores))
        kw_pairs.sort(key=lambda kv: kv[1], reverse=True)
        kw_results = kw_pairs[: top_k * 3]

    fused = _reciprocal_rank_fusion(sem_results, kw_results)
    fused = fused[:top_k]

    return [
        RetrievalResult(
            item=item,
            score=total,
            semantic_score=sem,
            keyword_score=kw,
        )
        for item, total, sem, kw in fused
    ]


def format_results_for_prompt(results: Iterable[RetrievalResult]) -> str:
    """Format retrieval results as compact evidence blocks for the LLM prompt.

    Produces clean, compact blocks that won't overwhelm context limits.
    Each block shows the source ID and a truncated snippet.
    """
    blocks: list[str] = []
    for r in results:
        item = r.item
        # Truncate long chunks to ~800 chars to keep context manageable
        text = item.text
        if len(text) > 800:
            text = text[:800].rsplit(" ", 1)[0] + " [...]"
        blocks.append(
            f"[{item.source_document_id}] {text}"
        )
    return "\n\n".join(blocks) if blocks else "(no evidence retrieved)"
