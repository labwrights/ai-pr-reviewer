"""The pre-built diff parser, on the prepared pull requests."""

from pathlib import Path

from reviewer import diff

PRS = Path(__file__).resolve().parents[1] / "data" / "prs"


def test_added_lines_are_the_new_side_numbers():
    files = diff.parse((PRS / "01-sql-string" / "diff.patch").read_text())
    assert [f.path for f in files] == ["fieldnotes/store.py"]
    assert files[0].added_lines == {37}


def test_a_change_to_two_files_gives_two_entries():
    files = diff.parse((PRS / "08-refactor-with-tests" / "diff.patch").read_text())
    assert {f.path for f in files} == {"fieldnotes/ops.py", "fieldnotes/tests/test_fieldnotes.py"}


def test_every_prepared_pr_parses_and_its_planted_lines_were_added():
    import json
    for pr in sorted(PRS.iterdir()):
        files = {f.path: f for f in diff.parse((pr / "diff.patch").read_text())}
        planted = json.loads((pr / "expected.json").read_text())["planted"]
        if planted:
            start, end = planted["lines"]
            assert set(range(start, end + 1)) & files[planted["file"]].added_lines, pr.name
