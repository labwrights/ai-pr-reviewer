"""Pre-built: posts one review on a pull request through GitHub's REST API.

Standard library only, so the workflow installs nothing extra. The token is
the workflow's own GITHUB_TOKEN, limited by the workflow's `permissions:`.
"""

import json
import os
import urllib.error
import urllib.request

API = "https://api.github.com"


def post_review(repo: str, number: int, body: str, comments: list[dict]) -> dict:
    """Create a review with `event: COMMENT`: it comments, and never approves."""
    payload = {"event": "COMMENT", "body": body, "comments": comments}
    request = urllib.request.Request(
        f"{API}/repos/{repo}/pulls/{number}/reviews", method="POST",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as err:
        raise RuntimeError(f"GitHub said {err.code}: {err.read().decode()[:300]}") from None
