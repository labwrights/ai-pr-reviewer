"""Tests for the Fieldnotes slice. They pass before any PR, and some planted bugs break them."""

import csv
from datetime import UTC, datetime, timedelta

import pytest

from fieldnotes import export, ops, store, tickets


def test_tickets_are_stored_and_found_by_service():
    db = store.connect()
    store.add_ticket(db, "checkout-api", "Slow checkout", "sev2")
    store.add_ticket(db, "auth-service", "Login errors", "sev1")
    found = store.find_tickets(db, "checkout-api")
    assert [t["title"] for t in found] == ["Slow checkout"]


def test_a_service_name_cannot_change_the_query():
    db = store.connect()
    store.add_ticket(db, "checkout-api", "Slow checkout", "sev2")
    assert store.find_tickets(db, "x' OR '1'='1") == []


def test_invalid_tickets_say_why():
    with pytest.raises(tickets.InvalidTicket, match="severity"):
        tickets.validate("Slow checkout", "urgent")
    with pytest.raises(tickets.InvalidTicket, match="empty"):
        tickets.validate("  ", "sev2")


def test_pages_cover_every_item_exactly_once():
    items = list(range(45))
    pages = [tickets.page(items, n, 20) for n in (1, 2, 3)]
    assert [i for p in pages for i in p] == items


def test_adding_a_tag_never_changes_the_original():
    original = ["checkout"]
    assert tickets.with_tag(original, "latency") == ["checkout", "latency"]
    assert original == ["checkout"]
    assert tickets.with_tag(None, "a") == ["a"] and tickets.with_tag(None, "b") == ["b"]


def test_health_follows_the_latency_budget():
    assert ops.health("checkout-api", 640) == "healthy"
    assert ops.health("checkout-api", 2400) == "degraded"
    assert ops.health("checkout-api", 5000) == "down"


def test_a_sev2_is_overdue_after_30_minutes():
    opened = datetime(2026, 10, 26, 14, 0, tzinfo=UTC)
    assert not ops.response_overdue("sev2", opened.isoformat(), opened + timedelta(minutes=29))
    assert ops.response_overdue("sev2", opened.isoformat(), opened + timedelta(minutes=31))


def test_export_writes_every_ticket(tmp_path):
    rows = [{"id": 1, "service": "checkout-api", "title": "Slow", "severity": "sev2",
             "opened_at": "2026-10-26T14:00:00+00:00"}]
    path = tmp_path / "tickets.csv"
    assert export.export_csv(rows, str(path)) == 1
    assert next(csv.DictReader(path.open()))["title"] == "Slow"
