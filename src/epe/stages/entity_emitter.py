"""Entity extraction utility — emit per-entity .md files from artifact bodies.

This module provides the ``emit_entity_files()`` function used by stage engines
via the ``post_process()`` hook. Each entity ID found in an artifact body is
written to its own file under the project ``entities/`` directory, with
frontmatter declaring the entity type, source artifact, and provenance.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from epe.core.frontmatter import write_doc
from epe.tracking.ids import ID_PATTERNS, scan_ids

# Mapping from ID pattern key (ID_PATTERNS dict key) to directory name.
# Some entity directories use short names for compatibility with other systems.
_ENTITY_DIR_NAME: dict[str, str] = {
    "MILESTONE": "ms",
    "RFP_REQ": "rfp-req",
    "DELIVERABLE": "del",
    "APPROVAL": "aprv",
    "STAKEHOLDER": "stk",
}


def emit_entity_files(
    artifact_body: str,
    entity_types: list[str],
    output_dir: Path,
    source_artifact: str,
    metadata: dict[str, Any],
) -> dict[str, Path]:
    """Extract entity IDs from ``artifact_body`` and write one file per entity.

    Parameters
    ----------
    artifact_body : str
        The markdown body text to scan for entity IDs.
    entity_types : list[str]
        List of entity prefixes to extract (e.g. ``["REQ", "DEC", "COMP"]``).
    output_dir : Path
        The project root or ``entities/`` directory under which to create
        per-type subdirectories.
    source_artifact : str
        The relative path of the source artifact (e.g. ``"architecture/hld.md"``).
        Used in frontmatter ``source`` field.
    metadata : dict[str, Any]
        Base metadata to include in each entity file frontmatter.
        Fields ``project_id``, ``generated_by``, ``generated_at`` are set
        automatically; everything else is passed through.

    Returns
    -------
    dict[str, Path]
        Mapping of entity ID (e.g. ``"REQ-001"``) to the path of the file
        that was written.
    """
    emitted: dict[str, Path] = {}

    for entity_type in entity_types:
        pattern = ID_PATTERNS.get(entity_type)
        if pattern is None:
            continue

        ids_found = scan_ids(artifact_body, entity_type)
        if not ids_found:
            continue

        # Use short directory name if mapped, otherwise use entity_type.lower()
        dir_name = _ENTITY_DIR_NAME.get(entity_type, entity_type.lower())
        entity_dir = output_dir / dir_name
        entity_dir.mkdir(parents=True, exist_ok=True)

        for entity_id in sorted(ids_found):
            # Build frontmatter for this entity
            entity_meta = dict(metadata)
            entity_meta["entity_type"] = entity_type
            entity_meta["source"] = source_artifact
            entity_meta["generated_by"] = "entity_emitter"
            entity_meta["generated_at"] = datetime.now(timezone.utc).isoformat()

            # Body is a stub that references the source
            entity_name = pattern.entity_name
            body = f"# {entity_id}\n\n**Type:** {entity_name}\n**Source:** {source_artifact}\n\n"
            body += f"This {entity_name} was extracted from [{source_artifact}]({source_artifact}).\n"

            out_path = entity_dir / f"{entity_id}.md"
            write_doc(out_path, body, entity_meta)
            emitted[entity_id] = out_path

    return emitted
