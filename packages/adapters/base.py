"""Fail-closed adapter contract. No live ERP adapter is implemented here."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Protocol

from packages.review.workflow import ReviewRecord


@dataclass
class AdapterResult:
    success: bool
    mode: str
    external_id: str | None
    message: str
    verified: bool = False
    details: dict[str, Any] | None = None


class ApplicationAdapter(Protocol):
    def preview(self, record: ReviewRecord) -> AdapterResult: ...
    def submit(self, record: ReviewRecord) -> AdapterResult: ...


class LiveWritesDisabled(RuntimeError):
    """Raised whenever a live adapter is requested without an explicit safe implementation."""


class MockAdapter:
    """Deterministic test adapter; simulates responses and never touches external systems."""

    name = "mock"

    def preview(self, record: ReviewRecord) -> AdapterResult:
        return AdapterResult(
            success=True, mode="dry_run", external_id=None,
            message="Preview generated; no external application was changed.",
            verified=False,
            details={"workflow": record.workflow, "fields": dict(record.fields)},
        )

    def submit(self, record: ReviewRecord) -> AdapterResult:
        if record.status != "approved":
            return AdapterResult(
                success=False, mode="mock", external_id=None,
                message="Submission blocked: record requires explicit human approval.",
            )
        return AdapterResult(
            success=True, mode="mock", external_id=f"MOCK-{record.id[:8]}",
            message="Mock submission only; no external application was changed.",
            verified=False, details={"workflow": record.workflow},
        )


def get_adapter(name: str, *, allow_live: bool = False) -> ApplicationAdapter:
    normalized = name.strip().lower()
    if normalized == "mock":
        return MockAdapter()
    if normalized in {"marg", "marg_erp", "third_party"}:
        raise LiveWritesDisabled(
            "Live adapters are disabled until the target application's supported integration "
            "method is verified and a tested adapter is explicitly installed."
        )
    raise ValueError(f"Unknown adapter: {name}")
