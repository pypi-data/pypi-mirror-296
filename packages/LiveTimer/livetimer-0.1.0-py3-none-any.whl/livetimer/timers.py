import sys
import time
from collections import defaultdict
from collections.abc import Callable
from contextlib import contextmanager
from typing import IO

from rich.console import Console
from rich.live import Live
from rich.table import Table

__all__ = ["Cycle", "RichTimer"]


class Cycle:
    """A single cycle of a timer. Used to set logpoints for the timer.

    Each iteration of the operation should use a new cycle."""

    def __init__(self, counter_fn: Callable) -> None:
        self.start_time = time.perf_counter()
        self.timers = defaultdict(lambda: 0)
        self.last_logged_time = self.start_time
        self.counter_fn = counter_fn

    def log(self, name: str):
        """Log a new timestamp in the timer and measure the difference between now and the previous (or start) time.

        Log points should have the same name across each cycle so that they can be averaged.
        """
        if name in self.timers:
            raise ValueError("Please give each log point a unique name ('Timestamp 1', 'Timestamp 2', 'Post Op', etc)")

        name = "- " + name

        current_time = self.counter_fn()
        self.timers[name] = self.counter_fn() - self.last_logged_time

        self.last_logged_time = current_time


class RichTimer:
    """The main timer class, used to log a full operation."""

    def __init__(
        self,
        counter_fn: Callable | None = None,
        refresh_per_second=4,
        output: IO[str] | None = sys.stderr,
    ) -> None:
        """Initialize a performance timer.

        Args:
        ----
            counter_fn (Callable): The timing function to use. This defaults to `time.perf_counter` and outputs in
            milliseconds. Use a different counter for different precisions. All operations will use the output of
            this function, so if the counter function outputs at second precision, that will be the precision
            used in the ouput too.

            refresh_per_second (int): Refresh rate of the table.

            output (IO): The output to print to. By default, this is `sys.stderr`. If `None`, it will print to the
            console as per default for Rich.

        """
        self.console = Console(file=output)
        self.counter_fn = counter_fn or time.perf_counter
        self.refresh_per_second = refresh_per_second

        self.started = False
        self.count: int = None
        self.start_time: float = None
        self.timers: dict = None
        self.current_cycle: Cycle = None
        self.live: Live = None

        self.total_timer_str = "Time per Iteration"

    def _generate_table(self) -> Table:
        """Make a new table or refresh the existing one to display updated values."""
        table = Table()
        table.add_column("Metric")
        table.add_column("Total")
        table.add_column("Avg")
        table.add_column("Min")
        table.add_column("Max")
        table.add_row("Count", str(self.count))

        self._add_table_row(table, self.timers[self.total_timer_str], self.total_timer_str)
        for timer_name, timer_values in ((k, v) for k, v in self.timers.items() if k != self.total_timer_str):
            self._add_table_row(table, timer_values, timer_name)

        return table

    def _add_table_row(self, table: Table, timer_values: dict, timer_name: str) -> None:
        """Add one row to the output table."""
        if timer_values["count"] == 0:
            return
        avg_duration = timer_values["total_duration"] / timer_values["count"]
        table.add_row(
            timer_name,
            None,
            f"{avg_duration:.6f}",
            f"{timer_values['min']:.6f}",
            f"{timer_values['max']:.6f}",
        )

    @property
    @contextmanager
    def cycle(self) -> Cycle:
        """Start a new cycle.

        This should be used as a context manager within the main context of a RichTimer instance at the beginning of
        each operation iteration. This creates a new cycle of log points. Note that log points should have the same
        name across each cycle in order to collect timing data.

        Usage:

        >> with RichTimer().start as timer:
        >>     for _ in range(10):
        >>         with timer.cycle as cycle:  # <--
        >>             cycle.log("Time 1")

        """
        if self.start_time is None:  # Start the timer with the first cycle
            self.start_time = self.counter_fn()

        self.current_cycle = Cycle(counter_fn=self.counter_fn)
        try:
            yield self.current_cycle
            self.current_cycle.timers[self.total_timer_str] = self.counter_fn() - self.current_cycle.start_time

            self.count += 1
            for timer_name, duration in self.current_cycle.timers.items():
                self.timers[timer_name]["total_duration"] += duration
                self.timers[timer_name]["count"] += 1
                self.timers[timer_name]["max"] = max((self.timers[timer_name]["max"], duration))

                if self.timers[timer_name]["min"] is None:
                    self.timers[timer_name]["min"] = duration
                self.timers[timer_name]["min"] = min((self.timers[timer_name]["min"], duration))

        except Exception as err:
            self.live.console.print(f"[bold red]Error within timer: {err}")
            raise

        self.live.update(self._generate_table())

    @property
    @contextmanager
    def start(self) -> "RichTimer":
        """Start the timer.

        Use this as a context manager. This resets any stored times and prepares it for a new session. Within this
        context, use the other context manager `RichTimer.cycle()` to start a new cycle.

        Usage:

        >> with RichTimer().start as timer:
        >>     for _ in range(10):
        >>         with timer.cycle as cycle:
        >>             time.sleep(1)
        >>             cycle.log("Time 1")
        >>             time.sleep(1)
        >>             cycle.log("Time 2")

        """
        if self.started:
            raise RuntimeError(
                "A RichTimer should only be entered once. Use `with mytimer.cycle() as cycle` to start a new cycle."
            )

        self.timers = defaultdict(lambda: {"total_duration": 0, "count": 0, "min": None, "max": 0})
        self.count = 0
        self.start_time = None

        with Live(
            self._generate_table(),
            refresh_per_second=self.refresh_per_second,
            console=self.console,
        ) as self.live:
            yield self

        self.started = False
