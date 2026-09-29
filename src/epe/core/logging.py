"""Structured logging for EPE."""

from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

from epe.core.config import EpeConfig

_SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_-]{16,}"),
    re.compile(r"ghp_[A-Za-z0-9]{16,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----[\s\S]*?-----END"),
]


def _scrub(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    scrubbed = value
    for pat in _SECRET_PATTERNS:
        scrubbed = pat.sub("[REDACTED]", scrubbed)
    return scrubbed


class ScrubbingFilter(logging.Filter):
    """Scrub secrets from log records."""

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        record.msg = _scrub(record.msg)
        if record.args:
            record.args = tuple(_scrub(a) for a in record.args)
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # noqa: A003
        payload: dict[str, Any] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for k, v in record.__dict__.items():
            if k in ("name", "msg", "args", "levelname", "levelno", "pathname",
                     "filename", "module", "exc_info", "exc_text", "stack_info",
                     "lineno", "funcName", "created", "msecs", "relativeCreated",
                     "thread", "threadName", "processName", "process", "message",
                     "taskName"):
                continue
            if k.startswith("_"):
                continue
            try:
                json.dumps(v)
                payload[k] = v
            except TypeError:
                payload[k] = repr(v)
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(config: EpeConfig | None = None) -> None:
    root = logging.getLogger("epe")
    if root.handlers:
        return
    level_name = (config.system.logging.get("level") if config else None) or "INFO"
    json_mode = (config.system.logging.get("json") if config else None) or False

    handler = logging.StreamHandler(sys.stdout)
    if json_mode:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
    handler.addFilter(ScrubbingFilter())
    root.addHandler(handler)
    root.setLevel(level_name)
    root.propagate = False


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"epe.{name}")


def audit_log(path: Path, event: dict[str, Any]) -> None:
    """Append an audit event to a per-project audit log."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_scrub(event), ensure_ascii=False) + "\n")
