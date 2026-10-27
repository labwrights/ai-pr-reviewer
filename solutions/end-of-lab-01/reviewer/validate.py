"""Lab 1: refuse findings on lines the change didn't touch."""

from .diff import FileDiff


def validate(findings: list[dict], files: list[FileDiff]) -> tuple[list[dict], list[dict]]:
    """Split the model's findings into the ones to keep and the ones to drop, with why.

    A finding is kept only when its file is in this change and its line is one the
    change added. Models sometimes invent line numbers; a comment on the wrong line
    is worse than no comment, and GitHub refuses lines outside the diff anyway.
    """
    added = {f.path: f.added_lines for f in files}
    kept, dropped = [], []
    for finding in findings:
        if finding["file"] not in added:
            dropped.append({**finding, "why": "file not in this change"})
        elif finding["line"] not in added[finding["file"]]:
            dropped.append({**finding, "why": f"line {finding['line']} wasn't changed"})
        else:
            kept.append(finding)
    return kept, dropped
