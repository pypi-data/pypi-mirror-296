from __future__ import annotations

import contextlib
import time
import types
from typing import TYPE_CHECKING, Any, Mapping, Union, cast

if TYPE_CHECKING:
    import ddtrace.context

try:
    import ddtrace
    from datadog.dogstatsd.base import statsd

    def safe_set_gauge(gauge: str, value: int | float):
        statsd.gauge(gauge, value)

    def safe_incr(counter: str, value: int | float, tags: list[str] | None = None):
        statsd.increment(counter, value, tags)

    def safe_distribution(counter: str, value: int | float, tags: list[str] | None = None):
        statsd.distribution(counter, value, tags)

    @contextlib.contextmanager
    def safe_trace(span_id: str, attributes: Mapping[str, str] | None = None):
        with ddtrace.tracer.trace(name=span_id) as span:
            if attributes:
                span.set_tags(cast(Any, attributes))
            yield

    def safe_add_metrics(metrics: Mapping[str, Union[int, float]]):
        span = ddtrace.tracer.current_span()
        if span:
            span.set_metrics(cast(Any, metrics))

    def safe_add_tags(tags: Mapping[str, str]):
        span = ddtrace.tracer.current_span()
        if span:
            span.set_tags(cast(Any, tags))

    def safe_current_trace_context():  # pyright: ignore[reportRedeclaration]
        return ddtrace.tracer.current_trace_context()

    def safe_activate_trace_context(
        ctx: ddtrace.context.Context | ddtrace.Span | None,  # pyright: ignore[reportPrivateImportUsage]
    ) -> None:
        ddtrace.tracer.context_provider.activate(ctx)

except ImportError:

    def safe_set_gauge(gauge: str, value: int | float):
        pass

    def safe_incr(counter: str, value: int | float, tags: list[str] | None = None):
        pass

    @contextlib.contextmanager
    def safe_trace(span_id: str, attributes: Mapping[str, str] | None = None):
        yield

    def safe_add_metrics(metrics: Mapping[str, Union[int, float]]):
        pass

    def safe_add_tags(tags: Mapping[str, str]):
        pass

    def safe_current_trace_context():
        return

    def safe_activate_trace_context(
        ctx: ddtrace.context.Context | ddtrace.Span | None,  # pyright: ignore[reportPrivateImportUsage]
    ) -> None:
        pass

    def safe_distribution(counter: str, value: int | float, tags: list[str] | None = None):
        pass


class PerfTimer:
    def __init__(self):
        super().__init__()
        self._start = None
        self._end = None

    def __enter__(self):
        """Start a new timer as a context manager"""
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_typ: type[BaseException] | None, exc: BaseException | None, tb: types.TracebackType | None):
        """Stop the context manager timer"""
        self._end = time.perf_counter()

    @property
    def duration_seconds(self):
        assert self._start is not None
        end = time.perf_counter() if self._end is None else self._end
        return end - self._start

    @property
    def duration_ms(self):
        return self.duration_seconds * 1_000
