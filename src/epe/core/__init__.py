"""Core utilities: paths, config, errors, logging."""

from epe.core.config import EpeConfig, load_config
from epe.core.errors import (
    ConfigurationError,
    ContractViolation,
    EpeError,
    GateFailure,
    IngestionError,
    ValidationFailure,
)
from epe.core.logging import get_logger, setup_logging
from epe.core.paths import EpePaths

__all__ = [
    "EpeConfig",
    "load_config",
    "EpePaths",
    "EpeError",
    "ConfigurationError",
    "IngestionError",
    "ValidationFailure",
    "GateFailure",
    "ContractViolation",
    "get_logger",
    "setup_logging",
]
