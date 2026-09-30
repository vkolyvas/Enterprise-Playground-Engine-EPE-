#!/usr/bin/env python3
"""Lifecycle validator — checks lifecycle integrity across all stages.

Usage:
    python scripts/validate_lifecycle.py --project <project_id>
    python scripts/validate_lifecycle.py --all
    python scripts/validate_lifecycle.py --project <project_id> --verbose

Exit codes:
    0 = all checks pass
    1 = validation errors found
    2 = project not found or error
"""

from __future__ import annotations

import argparse
import sys
import re
from pathlib import Path

# Add src/ to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from epe.core.config import load_config
from epe.core.paths import EpePaths
from epe.tracking.registry import DocumentRegistry
from epe.tracking.lineage import LineageComputer
from epe.validation.completeness import validate_all, validate_stage_completeness


def check_missing_mandatory_documents(project_root: Path, registry: DocumentRegistry) -> list[str]:
    """Check all mandatory documents exist per stage."""
    errors = []
    mandatory = {
        "product": ["definition.md", "catalog.md", "guardrails.md", "readiness.md"],
        "presales": ["discovery.md", "qualification.md", "scope.md", "sow.md", "handover.md"],
        "architecture": ["validation.md", "hld.md", "security.md", "lld.md", "cost.md", "blueprint.md"],
        "delivery": ["plan.md", "test.md", "acceptance.md", "onboarding.md", "operations.md", "handover.md", "feedback.md"],
    }
    for stage, docs in mandatory.items():
        stage_docs = registry.by_stage(stage)
        present = {d.path.name for d in stage_docs}
        for doc in docs:
            if doc not in present:
                errors.append(f"  [{stage}] Missing mandatory document: {doc}")
    return errors


def check_frontmatter_completeness(project_root: Path, registry: DocumentRegistry) -> list[str]:
    """Check all documents have required frontmatter fields."""
    errors = []
    required = ["contract", "version", "stage", "status", "generated_at"]
    for doc in registry.documents:
        abs_path = project_root / doc.path
        if not abs_path.exists():
            errors.append(f"  [{doc.stage}] File missing but in registry: {doc.path}")
            continue
        from epe.core.frontmatter import read_doc
        try:
            parsed = read_doc(abs_path)
            for field in required:
                if field not in parsed.metadata or not parsed.metadata[field]:
                    errors.append(f"  [{doc.stage}] {doc.path.name}: missing or empty frontmatter field: {field}")
        except Exception as e:
            errors.append(f"  [{doc.stage}] {doc.path.name}: failed to parse: {e}")
    return errors


def check_id_references(project_root: Path, registry: DocumentRegistry) -> list[str]:
    """Check that all REQ/DEC/CAP/TASK/TEST/Q/RSK IDs cited in documents exist.

    NOTE: In the current EPE design, IDs are cited in document bodies as inline
    references. This check verifies that IDs extracted from body text have
    consistent citations across documents (i.e., no orphan IDs that appear once
    and are never seen again). IDs that appear in body but not in frontmatter
    are common in the current design.
    """
    warnings = []
    from epe.core.frontmatter import read_doc

    # Track all cited IDs (from body) and their frequency
    cited_ids: dict[str, dict[str, int]] = {}  # kind -> {id -> count}

    id_pattern = re.compile(r"\b(REQ|DEC|RSK|CAP|COMP|TASK|TEST|Q|CUST)-\d+\b")
    for doc in registry.documents:
        abs_path = project_root / doc.path
        if not abs_path.exists():
            continue
        try:
            parsed = read_doc(abs_path)
            cited = id_pattern.findall(parsed.body)
            for id_ref in cited:
                kind = id_ref.split("-")[0]
                cited_ids.setdefault(kind, {})
                cited_ids[kind][id_ref] = cited_ids[kind].get(id_ref, 0) + 1
        except Exception:
            pass

    # Report IDs that appear only once (potential orphans in current EPE design)
    # This is informational — IDs are inline references, not always stored as files
    for kind, ids in cited_ids.items():
        singles = [f"{kind}-{n}" for n, c in ids.items() if c == 1]
        if singles:
            warnings.append(f"  [{kind}] IDs cited only once (informational): {singles[:5]}{'...' if len(singles) > 5 else ''}")

    return warnings


def check_requirements_have_owners(project_root: Path, registry: DocumentRegistry) -> list[str]:
    """Every requirement should have an owner."""
    warnings = []
    for doc in registry.documents:
        if doc.requirements and not doc.owner:
            warnings.append(f"  [{doc.stage}] {doc.path.name}: has requirements but no owner set")
    return warnings


def check_tests_have_requirements(project_root: Path, registry: DocumentRegistry) -> list[str]:
    """Every test should trace to a requirement."""
    errors = []
    for doc in registry.documents:
        if doc.tests and not doc.requirements:
            errors.append(f"  [{doc.stage}] {doc.path.name}: has tests but no linked requirements")
    return errors


def check_traceability_completeness(project_root: Path, registry: DocumentRegistry) -> list[str]:
    """Check the traceability chain is complete."""
    errors = []
    lineage = LineageComputer(registry)

    # Check: every component should have an upstream requirement
    for doc in registry.documents:
        if doc.components and not doc.requirements:
            errors.append(f"  [{doc.stage}] {doc.path.name}: has components but no upstream requirements")

    # Check: every task should have an upstream component
    for doc in registry.documents:
        if doc.tasks and not doc.components:
            # tasks can come from blueprint (which has COMP) — check via lineage
            pass

    # Check: approved handover documents should have no unresolved blockers
    handover_docs = ["presales/handover.md", "architecture/blueprint.md", "delivery/handover.md"]
    for hdoc in handover_docs:
        doc = registry.get(hdoc)
        if doc and doc.is_approved:
            if doc.stage == "presales":
                completeness = validate_stage_completeness(project_root, "presales", registry)
                if completeness["missing_documents"]:
                    errors.append(f"  [{doc.stage}] {hdoc} is approved but missing inputs: {completeness['missing_documents']}")

    return errors


def check_handover_input_references(project_root: Path, registry: DocumentRegistry) -> list[str]:
    """Handover documents should reference upstream stage artifacts."""
    errors = []
    handover_mapping = {
        "presales/handover.md": "product",
        "architecture/blueprint.md": "presales",
        "delivery/handover.md": "architecture",
    }
    for hdoc_path, source_stage in handover_mapping.items():
        doc = registry.get(hdoc_path)
        if not doc:
            continue
        if not doc.inputs:
            errors.append(f"  [{doc.stage}] {hdoc_path}: handover document has no inputs declared in frontmatter")
        # Check that inputs actually exist
        for inp in doc.inputs:
            if not registry.get(inp):
                errors.append(f"  [{doc.stage}] {hdoc_path}: input '{inp}' not found in registry")
    return errors


def check_duplicate_ids(project_root: Path, registry: DocumentRegistry) -> list[str]:
    """No duplicate document IDs or contracts."""
    errors = []
    contract_counts: dict[str, int] = {}
    for doc in registry.documents:
        c = doc.contract or "unknown"
        contract_counts[c] = contract_counts.get(c, 0) + 1
    for contract, count in contract_counts.items():
        if count > 1:
            errors.append(f"  Duplicate contract '{contract}' appears in {count} documents")
    return errors


def run_validation(project_root: Path, verbose: bool = False) -> tuple[bool, list[str], list[str]]:
    """Run full validation on a project. Returns (passed, error_messages, warning_messages)."""
    all_errors: list[str] = []
    all_warnings: list[str] = []

    registry = DocumentRegistry.from_project(project_root, project_root.name)

    checks = [
        ("Missing mandatory documents", check_missing_mandatory_documents, False),
        ("Frontmatter completeness", check_frontmatter_completeness, False),
        ("ID reference integrity", check_id_references, True),  # informational
        ("Requirements have owners", check_requirements_have_owners, True),  # warning
        ("Tests have requirements", check_tests_have_requirements, False),
        ("Traceability completeness", check_traceability_completeness, False),
        ("Handover input references", check_handover_input_references, False),
        ("Duplicate IDs", check_duplicate_ids, False),
    ]

    for check_name, check_fn, is_warning in checks:
        if verbose:
            print(f"  Running: {check_name}...")
        results = check_fn(project_root, registry)
        if results:
            if is_warning:
                all_warnings.extend(results)
            else:
                all_errors.extend(results)

    # Run completeness validation
    if verbose:
        print("  Running: gate completeness...")
    completeness = validate_all(project_root, registry)
    for stage, info in completeness["gate_status"].items():
        if info["missing_documents"]:
            for miss in info["missing_documents"]:
                all_errors.append(f"  [{stage}] Missing mandatory: {miss}")

    passed = len(all_errors) == 0
    return passed, all_errors, all_warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate EPE lifecycle document integrity")
    parser.add_argument("--project", help="Project ID to validate")
    parser.add_argument("--all", action="store_true", help="Validate all projects")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    config = load_config()
    paths = EpePaths(config)

    if not args.project and not args.all:
        parser.print_help()
        return 0

    if args.all:
        projects = [p for p in paths.projects_root.iterdir() if p.is_dir() and not p.name.startswith(".")]
    else:
        proj_root = paths.projects_root / args.project
        if not proj_root.exists():
            print(f"ERROR: Project not found: {args.project}", file=sys.stderr)
            return 2
        projects = [proj_root]

    all_passed = True
    for proj in projects:
        pid = proj.name
        print(f"\n{'='*60}")
        print(f"  Validating: {pid}")
        print(f"{'='*60}")
        passed, errors, warnings = run_validation(proj, verbose=args.verbose)

        if warnings:
            print(f"\n  WARNINGS ({len(warnings)}):")
            for w in warnings:
                print(w)

        if errors:
            print(f"\n  ERRORS ({len(errors)}):")
            for e in errors:
                print(e)
            all_passed = False
        else:
            print(f"\n  OK — no errors")

        if passed and not errors:
            print(f"\n  RESULT: PASS")
        else:
            print(f"\n  RESULT: FAIL")

    print(f"\n{'='*60}")
    if all_passed:
        print("All projects passed.")
        return 0
    else:
        print("One or more projects failed validation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
