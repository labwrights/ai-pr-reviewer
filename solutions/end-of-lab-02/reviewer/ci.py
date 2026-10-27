"""Lab 2: review a pull request in GitHub Actions, and post the review on it.

The workflow (.github/workflows/ai-review.yml) gives this script everything
through environment variables: the diff, the PR's title and description, its
number, and the workflow's own GITHUB_TOKEN. PR text never goes into a shell
command, where a crafted title could run code.
"""

import os
import sys
from pathlib import Path

from . import github
from .review import Review, review

FORK_NOTICE = ("This pull request comes from a fork. GitHub gives workflows on fork PRs no "
               "sign-in token, so the AI review is skipped. Open it from a branch to review it.")


def comment(finding: dict) -> str:
    return f"**{finding['severity'].upper()}: {finding['title']}**\n\n{finding['reason']}"


def build(r: Review) -> tuple[str, list[dict]]:
    """The review's body and its inline comments. The body is written by this code from
    validated findings, never copied from the model's free text: free text is where an
    instruction hidden in the PR could try to speak."""
    comments = [{"path": f["file"], "line": f["line"], "side": "RIGHT", "body": comment(f)}
                for f in r.findings]
    count = f"{len(r.findings)} finding{'s' if len(r.findings) != 1 else ''}"
    body = (f"**AI review**: {count} on lines this pull request changed."
            f"{f' {len(r.dropped)} more pointed at unchanged lines and were left out.' if r.dropped else ''}"
            f"\n\nThis review: {r.input_tokens} tokens in, {r.output_tokens} out, "
            f"about ${r.cost_usd:.4f}.")
    return body, comments


def main() -> int:
    if os.environ.get("HEAD_IS_FORK") == "true":
        print(f"::notice::{FORK_NOTICE}")
        return 0
    repo, number = os.environ["GITHUB_REPOSITORY"], int(os.environ["PR_NUMBER"])
    pr_text = f"{os.environ.get('PR_TITLE', '')}\n\n{os.environ.get('PR_BODY', '')}"
    r = review(Path(os.environ["PR_DIFF"]).read_text(), pr_text)
    body, comments = build(r)
    try:
        posted = github.post_review(repo, number, body, comments)
    except RuntimeError as err:
        if "422" not in str(err):
            raise
        # GitHub refused a line it doesn't show in this PR: post every finding in the body.
        listed = "\n".join(f"- `{c['path']}:{c['line']}` {c['body'].splitlines()[0]}" for c in comments)
        posted = github.post_review(repo, number, f"{body}\n\n{listed}", [])
    print(f"posted: {posted.get('html_url', '(no url)')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
