"""Stage engines: product, presales, architecture, delivery.

Each stage engine follows the same internal pipeline:
  INPUT → CONTEXT → RETRIEVE → ANALYZE → DECIDE → VALIDATE → OUTPUT → HANDOVER
"""

from epe.stages.base import (
    StageContext,
    StageEngine,
    StageResult,
    load_stage_engine,
    run_stage,
)

__all__ = ["StageEngine", "StageContext", "StageResult", "run_stage", "load_stage_engine"]
