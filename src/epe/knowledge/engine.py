"""KnowledgeEngine — public entry point for the knowledge layer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from epe.core.config import EpeConfig
from epe.core.paths import EpePaths
from epe.knowledge.models import KnowledgeItem, RetrievalResult
from epe.knowledge.providers import EmbeddingProvider, make_embedding_provider
from epe.knowledge.retrieval import format_results_for_prompt, hybrid_retrieve
from epe.knowledge.vector_store import InMemoryVectorStore


class KnowledgeEngine:
    """Coordinates namespaces, embeddings, and retrieval for a project."""

    def __init__(
        self,
        config: EpeConfig,
        paths: EpePaths,
        *,
        embedding_provider: EmbeddingProvider | None = None,
        vector_store: InMemoryVectorStore | None = None,
        project_id: str | None = None,
    ) -> None:
        self.config = config
        self.paths = paths
        self.project_id = project_id or paths.project_id
        self.embeddings = embedding_provider or make_embedding_provider(config.models.embedding)
        self.store = vector_store or InMemoryVectorStore()
        self._loaded = False

    # Ingestion --------------------------------------------------------------

    def index_chunks(self, chunks: list[dict]) -> int:
        """Index chunk dicts (as produced by the ingestion pipeline)."""
        items: list[KnowledgeItem] = []
        for c in chunks:
            item = KnowledgeItem(
                chunk_id=c["chunk_id"],
                namespace=c["namespace"],
                source_document_id=c["source_document_id"],
                source_path=c["source_path"],
                section_heading=c.get("section_heading", ""),
                section_level=c.get("section_level", 0),
                position=c.get("position", 0),
                text=c.get("text", ""),
                topics=c.get("metadata", {}).get("topics", []),
                metadata=c.get("metadata", {}),
            )
            items.append(item)
        if items:
            vectors = self.embeddings.embed([it.text for it in items])
            for it, v in zip(items, vectors):
                it.embedding = v
            self.store.upsert_many(items)
        return len(items)

    def load_from_processed(self, processed_dir: Path) -> int:
        """Load all chunk JSON files under processed_dir."""
        if not processed_dir.exists():
            self._loaded = True
            return 0
        total = 0
        for path in processed_dir.rglob("chunks/*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if isinstance(data, list):
                total += self.index_chunks(data)
        self._loaded = True
        return total

    def load_namespace(self, namespace: str) -> int:
        """Load static knowledge from a namespace directory."""
        ns_path = self.paths.knowledge_namespace(namespace)
        if not ns_path.exists():
            return 0
        total = 0
        for path in ns_path.rglob("*.md"):
            chunks = self._md_to_chunks(path, namespace)
            total += self.index_chunks(chunks)
        self._loaded = True
        return total

    def _md_to_chunks(self, path: Path, namespace: str) -> list[dict]:
        from epe.ingestion.extractors.markdown import extract as md_extract

        doc = md_extract(path)
        chunks: list[dict] = []
        for i, section in enumerate(doc.sections):
            text = "\n".join(section.get("lines", [])).strip()
            if not text:
                continue
            chunks.append(
                {
                    "chunk_id": f"KNW-{namespace}-{path.stem}-{i:04d}",
                    "namespace": namespace,
                    "source_document_id": f"KNW-{namespace}-{path.stem}",
                    "source_path": str(path),
                    "section_heading": section.get("heading", ""),
                    "section_level": section.get("level", 0),
                    "position": i,
                    "text": text,
                    "metadata": {},
                }
            )
        if not chunks and doc.text.strip():
            chunks.append(
                {
                    "chunk_id": f"KNW-{namespace}-{path.stem}-0000",
                    "namespace": namespace,
                    "source_document_id": f"KNW-{namespace}-{path.stem}",
                    "source_path": str(path),
                    "section_heading": "",
                    "section_level": 0,
                    "position": 0,
                    "text": doc.text,
                    "metadata": {},
                }
            )
        return chunks

    # Retrieval --------------------------------------------------------------

    def allowed_namespaces(self, stage: str) -> list[str]:
        ns = list(self.config.stage(stage).knowledge)
        if self.project_id:
            ns.append(f"project:{self.project_id}")
        return ns

    def retrieve(
        self,
        *,
        query: str,
        stage: str,
        top_k: int | None = None,
        semantic: bool = True,
        keyword: bool = True,
        rerank: bool = False,
    ) -> list[RetrievalResult]:
        ns = self.allowed_namespaces(stage)
        stage_cfg = self.config.stage(stage)
        top_k = top_k or stage_cfg.retrieval.top_k
        semantic = semantic and stage_cfg.retrieval.semantic
        keyword = keyword and stage_cfg.retrieval.keyword

        if not self._loaded:
            self.load_namespace("global")

        # Filter by sensitivity/namespace ACL
        candidates = [it for it in self.store.all() if it.allowed_for(ns)]

        # Embed query and run hybrid retrieval
        if candidates:
            [qvec] = self.embeddings.embed([query])
        else:
            qvec = [0.0] * self.embeddings.dimensions
            return []

        # Build a filtered store view by namespace for the inner store query
        results = hybrid_retrieve(
            query=query,
            query_vector=qvec,
            store=self.store,
            top_k=top_k,
            namespace_filter=ns,
            semantic=semantic,
            keyword=keyword,
        )

        if rerank and self.config.models.reranker.enabled:
            results = self._rerank(query, results)

        return results

    def _rerank(self, query: str, results: list[RetrievalResult]) -> list[RetrievalResult]:
        # Simple lexical overlap as a stand-in for a neural reranker; preserves
        # the abstraction so a real cross-encoder can drop in here.
        q = set(query.lower().split())
        for r in results:
            toks = set(r.item.text.lower().split())
            overlap = len(q & toks) / max(len(q), 1)
            r.rerank_score = overlap
        results.sort(key=lambda r: r.rerank_score or 0.0, reverse=True)
        return results

    def format_for_prompt(self, results: Iterable[RetrievalResult]) -> str:
        return format_results_for_prompt(results)
