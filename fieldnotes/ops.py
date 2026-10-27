"""Service health and incident deadlines."""

from datetime import UTC, datetime, timedelta

# p95 latency budgets: above the budget a service is degraded, above 5x it's down.
LATENCY_BUDGET_MS = {"checkout-api": 800, "payments-api": 600, "auth-service": 300}
DEFAULT_BUDGET_MS = 1000

# How soon someone must respond to a ticket, by severity.
RESPONSE_TIME = {"sev1": timedelta(minutes=15), "sev2": timedelta(minutes=30),
                 "sev3": timedelta(hours=4)}


def health(service: str, p95_latency_ms: int) -> str:
    budget = LATENCY_BUDGET_MS.get(service, DEFAULT_BUDGET_MS)
    if p95_latency_ms > 5 * budget:
        return "down"
    if p95_latency_ms > budget:
        return "degraded"
    return "healthy"


def response_overdue(severity: str, opened_at: str, now: datetime | None = None) -> bool:
    """True once a ticket has waited longer than its severity allows.

    `opened_at` is an ISO 8601 time with a time zone, as the store saves it.
    """
    now = now or datetime.now(UTC)
    waited = now - datetime.fromisoformat(opened_at)
    return waited > RESPONSE_TIME[severity]
