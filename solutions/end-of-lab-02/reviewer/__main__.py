"""Review one change from the terminal.

    python -m reviewer data/prs/01-sql-string     # a prepared pull request
    python -m reviewer my-change.patch            # any diff: git diff main > my-change.patch
    python -m reviewer data/prs/08-refactor-with-tests --budget 150   # force a split (Step 5)
"""

import sys
from pathlib import Path

from .review import BUDGET_TOKENS, review


def main(argv: list[str]) -> int:
    budget = BUDGET_TOKENS
    if "--budget" in argv:  # a smaller budget, to see a change split into parts
        i = argv.index("--budget")
        budget, argv = int(argv[i + 1]), argv[:i] + argv[i + 2:]
    if len(argv) != 1:
        print(__doc__.strip())
        return 2
    target = Path(argv[0])
    if target.is_dir():  # a prepared PR: its diff and its title and description
        diff_text = (target / "diff.patch").read_text()
        pr_text = (target / "description.md").read_text()
    else:
        diff_text, pr_text = target.read_text(), ""
    r = review(diff_text, pr_text, budget)
    for f in r.findings:
        print(f"{f['severity'].upper():6} {f['file']}:{f['line']}  {f['title']}")
        print(f"       {f['reason']}")
    if not r.findings:
        print("no findings")
    for d in r.dropped:
        print(f"dropped: {d['file']}:{d['line']} {d['title']} ({d['why']})")
    print(f"parts: {r.parts} · tokens {r.input_tokens} in, {r.output_tokens} out · "
          f"cost ${r.cost_usd:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
