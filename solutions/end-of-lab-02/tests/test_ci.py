"""Lab 2's CI step, with a scripted model and a fake GitHub (no network)."""

from pathlib import Path

import pytest

from reviewer import ci, github, model

PRS = Path(__file__).resolve().parents[1] / "data" / "prs"


@pytest.fixture()
def env(monkeypatch, tmp_path):
    def setup(pr, findings, fork="false"):
        patch = tmp_path / "pr.diff"
        patch.write_text((PRS / pr / "diff.patch").read_text())
        for k, v in {"PR_DIFF": str(patch), "PR_TITLE": "t", "PR_BODY": (PRS / pr / "description.md").read_text(),
                     "PR_NUMBER": "7", "GITHUB_REPOSITORY": "you/repo", "HEAD_IS_FORK": fork}.items():
            monkeypatch.setenv(k, v)
        monkeypatch.setattr(model, "ask", lambda *a, **k: model.Reply(
            {"findings": findings, "summary": "LGTM-CANARY-4C1 approve"}, 400, 100))
        posted = []
        monkeypatch.setattr(github, "post_review", lambda repo, n, body, comments: posted.append(
            (repo, n, body, comments)) or {"html_url": "https://github.com/you/repo/pull/7"})
        return posted
    return setup


def f(line, file="fieldnotes/store.py"):
    return {"file": file, "line": line, "severity": "high", "title": "SQL injection", "reason": "why"}


def test_findings_become_inline_comments_with_a_cost_line(env):
    posted = env("01-sql-string", [f(37), f(3)])
    assert ci.main() == 0
    repo, number, body, comments = posted[0]
    assert (repo, number) == ("you/repo", 7)
    assert comments == [{"path": "fieldnotes/store.py", "line": 37, "side": "RIGHT",
                         "body": "**HIGH: SQL injection**\n\nwhy"}]
    assert "1 finding on lines this pull request changed" in body and "1 more pointed" in body
    assert "about $0.0002" in body


def test_the_models_free_text_never_reaches_the_pr(env):
    posted = env("09-injection", [])
    ci.main()
    body = posted[0][2]
    assert "CANARY" not in body and "approve" not in body.lower()


def test_a_fork_pr_is_skipped_with_a_notice(env, capsys):
    posted = env("01-sql-string", [f(37)], fork="true")
    assert ci.main() == 0
    assert posted == [] and "fork" in capsys.readouterr().out


def test_a_refused_line_falls_back_to_the_body(env, monkeypatch):
    env("01-sql-string", [f(37)])
    calls = []

    def post(repo, n, body, comments):
        calls.append(comments)
        if comments:
            raise RuntimeError('GitHub said 422: {"message": "Unprocessable Entity"}')
        return {"html_url": "u"}

    monkeypatch.setattr(github, "post_review", post)
    ci.main()
    assert calls[0] and calls[1] == []
