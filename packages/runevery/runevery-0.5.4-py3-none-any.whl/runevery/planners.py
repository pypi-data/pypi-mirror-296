from __future__ import annotations

from typing import Any, Callable, Protocol, Sequence

from .utils import format_duration, format_time


class SchedulingPlanner:
    interval_strategy: IntervalStrategy

    def __init__(self, *, interval_strategy: IntervalStrategy = "start"):
        self.interval_strategy = interval_strategy

    def check(self, task: SchedulingTask, /) -> bool:
        return False

    def on_run(self, task: SchedulingTask, /) -> Any:
        return None

    def __str__(self) -> str:
        return "never"


class NeverPlanner(SchedulingPlanner):
    pass


class IntervalPlanner(SchedulingPlanner):
    def __init__(
        self,
        interval: float,
        *,
        interval_strategy: IntervalStrategy = "start",
    ):
        self.interval = interval
        self.interval_strategy = interval_strategy

    def check(self, task: SchedulingTask, /):
        if not self.interval:
            return not task.get_last_run(self.interval_strategy)

        return (task.get_last_run(self.interval_strategy) + self.interval) <= task.time

    def __str__(self):
        if not self.interval:
            return "once"

        return f"every {format_duration(self.interval)}"


class CooldownSource(Protocol):
    def get_cooldown(self, interval: float) -> float:
        ...


class CooldownPlanner(SchedulingPlanner):
    def __init__(
        self,
        cooldown_source: CooldownSource,
        interval: float,
        *,
        interval_strategy: IntervalStrategy = "start",
    ) -> None:
        self.cooldown_source = cooldown_source
        self.interval = interval
        self.interval_strategy = interval_strategy

    def check(self, task: SchedulingTask, /) -> bool:
        remaining = self.cooldown_source.get_cooldown(self.interval)
        return remaining <= 0

    def __str__(self):
        return f"every {format_duration(self.interval)} (cooling down using {self.cooldown_source})"


class FixedOffsetPlanner(SchedulingPlanner):
    """
    Planner that you can use to plan something at a fixed timestamp, optionally at intervals after.
    Keep in mind that `offset` is from unixtime 0, not from the program start although
    """

    def __init__(
        self,
        offset: float,
        interval: float,
        *,
        interval_strategy: IntervalStrategy = "start",
    ):
        self.offset = offset
        self.interval = interval
        self.interval_strategy = interval_strategy

    def get_period(self, ts: float) -> int:
        if not self.interval:
            return int(ts > self.offset)

        return int((ts - self.offset) // self.interval)

    def check(self, task: SchedulingTask, /) -> bool:
        return self.get_period(task.time) != self.get_period(
            task.get_last_run(self.interval_strategy)
        )

    def __str__(self):
        start_fmt = format_time(self.offset)

        if not self.interval:
            return f"at {start_fmt}"

        return f"every {format_duration(self.interval)} since {start_fmt}"


class SwitchPlanner(SchedulingPlanner):
    """
    An advanced scheduler that switches between schedulers using a callback.
    """

    def __init__(
        self,
        *,
        planners: Sequence[SchedulingPlanner],
        switch_callback: Callable[[SchedulingTask], int],
        interval_strategy: IntervalStrategy = "start",
    ):
        self.planners = list(planners)
        self.planner_index = 0
        self.switch_callback = switch_callback

    @property
    def current_planner(self) -> SchedulingPlanner:
        return self.planners[self.planner_index % len(self.planners)]

    def check(self, task: SchedulingTask, /) -> bool:
        return self.current_planner.check(task)

    def on_run(self, task: SchedulingTask):
        self.current_planner.on_run(task)
        self.planner_index = self.switch_callback(task)


from .scheduler import IntervalStrategy
from .task import SchedulingTask
