"""Secret scanning for ingestion."""

from __future__ import annotations

import re
from dataclasses import dataclass

_PATTERNS = [
    ("anthropic_api_key", re.compile(r"sk-ant-[A-Za-z0-9_-]{16,}")),
    ("github_pat", re.compile(r"ghp_[A-Za-z0-9]{16,}")),
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private_key_block", re.compile(
        r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"
    )),
    ("slack_token", re.compile(r"xox[abpr]-[A-Za-z0-9-]{10,}")),
]


@dataclass
class SecretFinding:
    kind: str
    location: str
    excerpt: str


def scan_for_secrets(text: str, *, location: str = "<text>") -> list[SecretFinding]:
    """Return any secret-pattern matches in the given text."""
    findings: list[SecretFinding] = []
    for kind, pat in _PATTERNS:
        for m in pat.finditer(text):
            excerpt = text[max(0, m.start() - 8): m.end() + 8]
            findings.append(SecretFinding(kind=kind, location=location, excerpt=excerpt))
    return findings
