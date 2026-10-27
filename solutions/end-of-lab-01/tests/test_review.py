"""Lab 1's reviewer with a scripted model: no Azure, no cost."""

import json
from pathlib import Path

import pytest

from reviewer import diff, measure, model, review
from reviewer.split import split
from reviewer.validate import validate

PRS = Path(__file__).resolve().parents[1] / "data" / "prs"


def finding(file, line, severity="high", title="A problem"):
    return {"file": file, "line": line, "severity": severity, "title": title, "reason": "because"}


@pytest.fixture()
def scripted(monkeypatch):
    """Replaces the model: plays back prepared replies, and keeps every prompt it was sent."""
    calls = []

    def ask(instructions, prompt, schema, name="review"):
        calls.append(prompt)
        findings = calls_replies.pop(0) if calls_replies else []
        return model.Reply({"findings": findings, "summary": "ok"}, 100, 20)

    calls_replies: list = []
    monkeypatch.setattr(model, "ask", ask)
    return calls, calls_replies


def test_a_finding_on_an_unchanged_line_is_dropped_with_why():
    files = diff.parse((PRS / "01-sql-string" / "diff.patch").read_text())
    kept, dropped = validate([finding("fieldnotes/store.py", 37), finding("fieldnotes/store.py", 12),
                              finding("app.py", 1)], files)
    assert [f["line"] for f in kept] == [37]
    assert [d["why"] for d in dropped] == ["line 12 wasn't changed", "file not in this change"]


def test_the_model_sees_numbered_lines_and_the_pr_text_as_data(scripted):
    calls, replies = scripted
    replies.append([finding("fieldnotes/store.py", 37)])
    r = review.review((PRS / "01-sql-string" / "diff.patch").read_text(), "Simplify the query")
    assert "   37 + " in calls[0]
    assert calls[0].startswith("<untrusted_pr_text>\nSimplify the query\n</untrusted_pr_text>")
    assert len(r.findings) == 1 and r.parts == 1 and r.cost_usd > 0


def test_a_change_over_the_budget_is_reviewed_file_by_file(scripted):
    calls, _ = scripted
    r = review.review((PRS / "08-refactor-with-tests" / "diff.patch").read_text(), budget=150)
    assert r.parts == 2 and len(calls) == 2
    assert all(c.count("file: ") == 1 for c in calls)


def test_a_file_over_the_budget_goes_hunk_by_hunk():
    big = diff.parse((PRS / "08-refactor-with-tests" / "diff.patch").read_text())
    parts = split(big, budget=20)
    assert sum(len(diff.hunks(f)) for f in big) == len(parts) == 2  # one hunk per part
    assert all(len(p) == 1 for p in parts)


def test_the_score_counts_only_the_planted_lines():
    expected = json.loads((PRS / "01-sql-string" / "expected.json").read_text())
    assert measure.score(expected, [finding("fieldnotes/store.py", 37)])["caught"] is True
    assert measure.score(expected, [finding("fieldnotes/store.py", 25)])["caught"] is False
    clean = {"planted": None}
    assert measure.score(clean, [finding("x", 1, "low"), finding("x", 2, "high")])["false_alarms"] == 1
