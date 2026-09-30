"""Critical-path computation using forward/backward pass algorithm.

This module provides the scheduling network model and critical-path computation
for the governance layer. It operates on Task and Milestone entities loaded
from entity files, NOT on document content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any


@dataclass
class ScheduleItem:
    """A node in the project schedule network.

    Can represent a Task or Milestone with scheduling data.
    """
    id: str
    title: str
    item_type: str  # "task" | "milestone"

    # Dependencies
    depends_on: list[str] = field(default_factory=list)  # IDs of predecessor items

    # Scheduling (human-controlled)
    baseline_start: date | None = None
    baseline_end: date | None = None
    forecast_start: date | None = None
    forecast_end: date | None = None
    actual_start: date | None = None
    actual_end: date | None = None

    # Computed by forward/backward pass
    earliest_start: date | None = None
    earliest_finish: date | None = None
    latest_start: date | None = None
    latest_finish: date | None = None
    float_days: int | None = None
    critical: bool = False

    # Critical-path annotations
    blocking: bool = False
    blocking_task: bool = False

    @property
    def duration_days(self) -> int | None:
        """Duration in days based on forecast_end - forecast_start."""
        if self.forecast_start and self.forecast_end:
            return (self.forecast_end - self.forecast_start).days
        if self.baseline_start and self.baseline_end:
            return (self.baseline_end - self.baseline_start).days
        return None

    @property
    def schedule_variance_days(self) -> int | None:
        """Schedule variance: forecast_end - baseline_end in days."""
        if self.forecast_end and self.baseline_end:
            return (self.forecast_end - self.baseline_end).days
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "item_type": self.item_type,
            "depends_on": self.depends_on,
            "baseline_start": str(self.baseline_start) if self.baseline_start else None,
            "baseline_end": str(self.baseline_end) if self.baseline_end else None,
            "forecast_start": str(self.forecast_start) if self.forecast_start else None,
            "forecast_end": str(self.forecast_end) if self.forecast_end else None,
            "actual_start": str(self.actual_start) if self.actual_start else None,
            "actual_end": str(self.actual_end) if self.actual_end else None,
            "duration_days": self.duration_days,
            "earliest_start": str(self.earliest_start) if self.earliest_start else None,
            "earliest_finish": str(self.earliest_finish) if self.earliest_finish else None,
            "latest_start": str(self.latest_start) if self.latest_start else None,
            "latest_finish": str(self.latest_finish) if self.latest_finish else None,
            "float_days": self.float_days,
            "critical": self.critical,
            "blocking": self.blocking,
            "blocking_task": self.blocking_task,
            "schedule_variance_days": self.schedule_variance_days,
        }


@dataclass
class ScheduleNetwork:
    """A project schedule network with forward/backward pass computed."""
    items: dict[str, ScheduleItem] = field(default_factory=dict)

    def topological_sort(self) -> list[ScheduleItem]:
        """Return items in topological order (predecessors before successors)."""
        visited: set[str] = set()
        result: list[ScheduleItem] = []

        def visit(item_id: str) -> None:
            if item_id in visited:
                return
            visited.add(item_id)
            item = self.items.get(item_id)
            if item:
                for dep_id in item.depends_on:
                    visit(dep_id)
                result.append(item)

        for item_id in self.items:
            visit(item_id)

        return result

    def get_critical_chain(self) -> list[ScheduleItem]:
        """Return items on the critical path (float == 0), sorted by earliest start."""
        return sorted(
            [i for i in self.items.values() if i.critical],
            key=lambda i: i.earliest_start or i.baseline_start or date.max
        )


def build_schedule_network(tasks: list[dict], milestones: list[dict]) -> ScheduleNetwork:
    """Build a schedule network from task and milestone entities.

    Parameters
    ----------
    tasks : list[dict]
        List of Task entity dicts with fields: id, title, depends_on (task IDs),
        baseline_start, baseline_end, forecast_start, forecast_end,
        actual_start, actual_end, blocking_task
    milestones : list[dict]
        List of Milestone entity dicts with fields: id, title, depends_on (MS IDs),
        baseline_start, baseline_end, forecast_start, forecast_end,
        actual_start, actual_end, blocking

    Returns
    -------
    ScheduleNetwork
        Network with forward/backward pass already computed.
    """
    network = ScheduleNetwork()

    # Add tasks to network
    for task in tasks:
        item = ScheduleItem(
            id=task["id"],
            title=task["title"],
            item_type="task",
            depends_on=task.get("depends_on", []),
            baseline_start=_parse_date(task.get("baseline_start")),
            baseline_end=_parse_date(task.get("baseline_end")),
            forecast_start=_parse_date(task.get("forecast_start")),
            forecast_end=_parse_date(task.get("forecast_end")),
            actual_start=_parse_date(task.get("actual_start")),
            actual_end=_parse_date(task.get("actual_end")),
            blocking_task=task.get("blocking_task", False),
        )
        network.items[item.id] = item

    # Add milestones to network
    for ms in milestones:
        item = ScheduleItem(
            id=ms["id"],
            title=ms["title"],
            item_type="milestone",
            depends_on=ms.get("depends_on", []),
            baseline_start=_parse_date(ms.get("baseline_start")),
            baseline_end=_parse_date(ms.get("baseline_end")),
            forecast_start=_parse_date(ms.get("forecast_start")),
            forecast_end=_parse_date(ms.get("forecast_end")),
            actual_start=_parse_date(ms.get("actual_start")),
            actual_end=_parse_date(ms.get("actual_end")),
            blocking=ms.get("blocking", False),
        )
        network.items[item.id] = item

    # Compute forward/backward pass
    compute_forward_pass(network)
    compute_backward_pass(network)
    compute_float_and_critical(network)

    return network


def _parse_date(value: Any) -> date | None:
    """Parse a date from string or date object."""
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def compute_forward_pass(network: ScheduleNetwork) -> None:
    """Forward pass: compute earliest start and earliest finish for each item.

    Earliest Start = max(Earliest Finish of all predecessors)
    Earliest Finish = Earliest Start + Duration
    """
    for item in network.topological_sort():
        if not item.depends_on:
            # No predecessors — use baseline_start or forecast_start
            item.earliest_start = item.forecast_start or item.baseline_start
        else:
            # Max of all predecessor earliest finishes
            max_finish: date | None = None
            for dep_id in item.depends_on:
                dep = network.items.get(dep_id)
                if dep and dep.earliest_finish:
                    if max_finish is None or dep.earliest_finish > max_finish:
                        max_finish = dep.earliest_finish
            item.earliest_start = max_finish

        if item.earliest_start and item.duration_days is not None:
            item.earliest_finish = item.earliest_start + timedelta(days=item.duration_days)


def compute_backward_pass(network: ScheduleNetwork) -> None:
    """Backward pass: compute latest finish and latest start for each item.

    Latest Finish = min(Latest Start of all successors)
    Latest Start = Latest Finish - Duration
    """
    # Build successor map
    successors: dict[str, list[str]] = {}
    for item_id, item in network.items.items():
        for dep_id in item.depends_on:
            if dep_id not in successors:
                successors[dep_id] = []
            successors[dep_id].append(item_id)

    # Find final items (no successors or explicitly marked as final)
    final_items = [
        item_id for item_id, item in network.items.items()
        if item_id not in successors
    ]

    # Initialize latest_finish for final items
    for item_id in final_items:
        item = network.items[item_id]
        item.latest_finish = item.earliest_finish or item.forecast_end or item.baseline_end

    # Backward pass in reverse topological order
    for item in reversed(network.topological_sort()):
        if item.id in successors:
            # Has successors — latest finish is min of successor latest starts
            min_latest_start: date | None = None
            for succ_id in successors[item.id]:
                succ = network.items.get(succ_id)
                if succ and succ.latest_start:
                    if min_latest_start is None or succ.latest_start < min_latest_start:
                        min_latest_start = succ.latest_start
            item.latest_finish = min_latest_start
        else:
            # Final item — already initialized
            pass

        if item.latest_finish and item.duration_days is not None:
            item.latest_start = item.latest_finish - timedelta(days=item.duration_days)
        else:
            item.latest_start = item.earliest_start


def compute_float_and_critical(network: ScheduleNetwork) -> None:
    """Compute float (slack) and critical path flag for each item.

    Float = Latest Start - Earliest Start
    Critical = Float == 0
    """
    for item in network.items.values():
        if item.latest_start and item.earliest_start:
            float_delta = item.latest_start - item.earliest_start
            item.float_days = float_delta.days
        else:
            item.float_days = None
        item.critical = item.float_days == 0


def compute_critical_chain(tasks: list[dict], milestones: list[dict]) -> list[ScheduleItem]:
    """Compute the critical chain from tasks and milestones.

    This is a convenience function that builds the schedule network and returns
    the critical chain items.

    Parameters
    ----------
    tasks : list[dict]
        List of Task entity dicts.
    milestones : list[dict]
        List of Milestone entity dicts.

    Returns
    -------
    list[ScheduleItem]
        Items on the critical path (float == 0), sorted by earliest start.
    """
    network = build_schedule_network(tasks, milestones)
    return network.get_critical_chain()
