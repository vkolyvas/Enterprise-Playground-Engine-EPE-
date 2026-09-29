"""EPE exception hierarchy."""


class EpeError(Exception):
    """Base exception for all EPE errors."""

    def __init__(self, message: str, *, context: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.context = context or {}


class ConfigurationError(EpeError):
    """Raised when configuration is missing or invalid."""


class IngestionError(EpeError):
    """Raised when document ingestion fails for a source."""


class ValidationFailure(EpeError):
    """Raised when a validation step fails."""

    def __init__(self, message: str, *, findings: list | None = None, **kw) -> None:
        super().__init__(message, **kw)
        self.findings = findings or []


class GateFailure(EpeError):
    """Raised when a lifecycle gate fails."""


class ContractViolation(EpeError):
    """Raised when a stage engine produces output violating its contract."""
