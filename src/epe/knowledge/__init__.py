"""Knowledge layer: namespaces, embeddings, vector store, retrieval."""

from epe.knowledge.engine import KnowledgeEngine
from epe.knowledge.models import KnowledgeItem, RetrievalResult

__all__ = ["KnowledgeEngine", "KnowledgeItem", "RetrievalResult"]
