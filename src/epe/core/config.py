"""Configuration loader and Pydantic models."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator

from epe.core.errors import ConfigurationError


class SystemPathsConfig(BaseModel):
    projects_root: str
    knowledge_root: str
    sources_root: str
    schemas_root: str
    templates_root: str
    workflows_root: str = "workflows"
    audit_root: str = "projects/_audit"


class SystemConfig(BaseModel):
    paths: SystemPathsConfig
    logging: dict[str, Any]
    environment: str = "dev"


class EmbeddingConfig(BaseModel):
    provider: str
    model: str
    dimensions: int
    batch_size: int = 32
    normalize: bool = True
    cache_dir: str | None = None


class VectorStoreConfig(BaseModel):
    provider: str
    database: str
    collection_prefix: str = "epe_"


class LLMConfig(BaseModel):
    provider: str
    model: str
    max_tokens: int = 8192
    temperature: float = 0.2
    timeout_s: int = 120
    retries: int = 3


class RerankerConfig(BaseModel):
    enabled: bool = False
    provider: str = "local"
    model: str | None = None


class ModelsConfig(BaseModel):
    embedding: EmbeddingConfig
    vector_store: VectorStoreConfig
    llm: LLMConfig
    reranker: RerankerConfig = RerankerConfig()


class RetrievalStageConfig(BaseModel):
    strategy: str = "hybrid"
    semantic: bool = True
    keyword: bool = True
    rerank: bool = True
    top_k: int = 12


class StageConfig(BaseModel):
    llm: str = "llm"
    retrieval: RetrievalStageConfig = Field(default_factory=RetrievalStageConfig)
    knowledge: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    gates: list[str] = Field(default_factory=list)


class StagesConfig(BaseModel):
    stages: dict[str, StageConfig]


class GatePredicate(BaseModel):
    module: str
    severity: str = "blocker"


class ValidationConfig(BaseModel):
    severity_levels: list[str] = Field(default_factory=lambda: ["info", "warning", "error", "blocker"])
    gate_predicates: dict[str, GatePredicate]


class OutputContractPaths(BaseModel):
    model_config = {"extra": "allow"}


class OutputConfig(BaseModel):
    contracts: dict[str, dict[str, Any]]


class IngestionConfig(BaseModel):
    extractors: dict[str, str]
    classifier: dict[str, str]
    chunking: dict[str, Any] = Field(default_factory=dict)
    deduplication: dict[str, Any] = Field(default_factory=dict)


class EpeConfig(BaseModel):
    """Top-level EPE configuration."""

    system: SystemConfig
    models: ModelsConfig
    stages: StagesConfig
    validation: ValidationConfig
    output: OutputConfig
    ingestion: IngestionConfig

    @field_validator("system")
    @classmethod
    def _validate_system(cls, v: SystemConfig) -> SystemConfig:
        return v

    # Convenience accessors ------------------------------------------------

    def stage(self, name: str) -> StageConfig:
        if name not in self.stages.stages:
            raise ConfigurationError(f"Stage not configured: {name}")
        return self.stages.stages[name]

    def gate_predicate(self, gate_id: str) -> GatePredicate:
        if gate_id not in self.validation.gate_predicates:
            raise ConfigurationError(f"Gate predicate not configured: {gate_id}")
        return self.validation.gate_predicates[gate_id]


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigurationError(f"Missing config file: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ConfigurationError(f"Top-level YAML must be a mapping: {path}")
    return data


def load_config(repo_root: Path | None = None) -> EpeConfig:
    """Load and validate all EPE config files in the documented order."""
    from epe.core.paths import REPO_ROOT

    root = repo_root or REPO_ROOT
    config_dir = root / "config"

    system = SystemConfig(**_read_yaml(config_dir / "system.yaml"))
    models = ModelsConfig(**_read_yaml(config_dir / "models.yaml"))
    stages_data = _read_yaml(config_dir / "stages.yaml")
    stages = StagesConfig(**stages_data)
    validation = ValidationConfig(**_read_yaml(config_dir / "validation.yaml"))
    output = OutputConfig(**_read_yaml(config_dir / "output.yaml"))
    ingestion = IngestionConfig(**_read_yaml(config_dir / "ingestion.yaml"))

    return EpeConfig(
        system=system,
        models=models,
        stages=stages,
        validation=validation,
        output=output,
        ingestion=ingestion,
    )
