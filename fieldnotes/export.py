"""Export tickets to CSV for the weekly ops review."""

import csv

FIELDS = ["id", "service", "title", "severity", "opened_at"]


def export_csv(tickets: list[dict], path: str) -> int:
    """Write tickets to `path`; returns how many were written."""
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for ticket in tickets:
            writer.writerow(ticket)
    return len(tickets)
