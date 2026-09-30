"""Provider abstractions for embeddings and LLMs."""

from __future__ import annotations

import os
from typing import Protocol

import numpy as np

from epe.core.errors import ConfigurationError


class EmbeddingProvider(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]:
        ...

    @property
    def dimensions(self) -> int:
        ...


class LLMProvider(Protocol):
    def generate(
        self,
        *,
        system: str,
        prompt: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        ...


class HashEmbeddingProvider:
    """Deterministic, dependency-free embedding provider.

    Useful for development and tests. Not a real semantic embedding.
    """

    def __init__(self, dimensions: int = 256) -> None:
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, texts: list[str]) -> list[list[float]]:
        import hashlib

        out: list[list[float]] = []
        for t in texts:
            # bucket character n-grams into a fixed-dim vector
            v = np.zeros(self._dimensions, dtype=np.float32)
            tokens = t.lower().split()
            for tok in tokens:
                h = hashlib.sha256(tok.encode("utf-8")).digest()
                for i in range(0, len(h), 4):
                    bucket = int.from_bytes(h[i:i + 4], "big") % self._dimensions
                    v[bucket] += 1.0
            norm = float(np.linalg.norm(v))
            if norm > 0:
                v = v / norm
            out.append(v.tolist())
        return out


class AnthropicLLMProvider:
    """Anthropic Claude LLM provider."""

    def __init__(self, model: str, api_key: str | None = None, timeout_s: int = 120) -> None:
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ConfigurationError(
                "ANTHROPIC_API_KEY is not set. Configure it via environment or .env."
            )
        try:
            import anthropic  # type: ignore[import-not-found]
        except ImportError as e:
            raise ConfigurationError(
                "anthropic SDK not installed. `pip install -e '.[all]'`"
            ) from e
        self._client = anthropic.Anthropic(api_key=api_key, timeout=timeout_s)
        self._model = model

    def generate(
        self,
        *,
        system: str,
        prompt: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        # Try streaming first to avoid long-lived connection timeouts.
        # MiniMax endpoint may not support temperature in stream() mode,
        # so fall back without it if needed.
        parts: list[str] = []
        try:
            with self._client.messages.stream(
                model=self._model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                msg = stream.get_final_message()
        except TypeError:
            # Endpoint doesn't support temperature in stream() — retry without it.
            try:
                with self._client.messages.stream(
                    model=self._model,
                    max_tokens=max_tokens,
                    system=system,
                    messages=[{"role": "user", "content": prompt}],
                ) as stream:
                    msg = stream.get_final_message()
            except TypeError:
                # Streaming not supported — fall back to non-streaming create().
                try:
                    msg = self._client.messages.create(
                        model=self._model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        system=system,
                        messages=[{"role": "user", "content": prompt}],
                    )
                except TypeError:
                    # Temperature not supported — final fallback without it.
                    msg = self._client.messages.create(
                        model=self._model,
                        max_tokens=max_tokens,
                        system=system,
                        messages=[{"role": "user", "content": prompt}],
                    )
                # Non-streaming: content is directly on msg.content
                for block in msg.content:
                    if hasattr(block, "text"):
                        parts.append(block.text)
                return "\n".join(parts)

        # Streaming path: extract text from message
        for block in msg.content:
            if hasattr(block, "text"):
                parts.append(block.text)
        return "\n".join(parts)


class StubLLMProvider:
    """Deterministic stand-in for tests."""

    def generate(self, *, system: str, prompt: str, max_tokens: int, temperature: float) -> str:
        return (
            "<<<STUB>>>\n"
            f"system: {system[:80]}\n"
            f"prompt: {prompt[:240]}\n"
            "<<<END>>>"
        )


def make_embedding_provider(config) -> EmbeddingProvider:
    provider = config.provider
    if provider == "local" or provider == "hash":
        return HashEmbeddingProvider(dimensions=config.dimensions)
    raise ConfigurationError(f"Embedding provider not implemented: {provider}")


def make_llm_provider(config) -> LLMProvider:
    provider = config.provider
    if provider == "anthropic":
        return AnthropicLLMProvider(model=config.model)
    if provider == "stub":
        return StubLLMProvider()
    raise ConfigurationError(f"LLM provider not implemented: {provider}")
