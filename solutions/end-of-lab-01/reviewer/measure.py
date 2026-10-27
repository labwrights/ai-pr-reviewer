"""Lab 1: how good is the reviewer? Run it on the prepared pull requests and count.

    python -m reviewer.measure            # 3 runs of each prepared PR
    python -m reviewer.measure --runs 5

A planted bug counts as caught when a kept finding is in the planted file, on
one of the lines the bug added. A false alarm is a high or medium finding on a
clean pull request. A model's choices vary, so one run proves little: count
over several, and report the range.
"""

import json
import sys
import time
from pathlib import Path

from .review import review

PRS = Path(__file__).resolve().parents[1] / "data" / "prs"


def prepared() -> list[Path]:
    """The eight measured PRs; 09 (the injection demo) is lab 2's."""
    return [p for p in sorted(PRS.iterdir()) if not p.name.startswith("09")]


def score(expected: dict, findings: list[dict]) -> dict:
    planted = expected["planted"]
    if planted is None:  # a clean PR: anything serious is a false alarm
        return {"caught": None,
                "false_alarms": sum(f["severity"] in ("high", "medium") for f in findings)}
    start, end = planted["lines"]
    caught = any(f["file"] == planted["file"] and start <= f["line"] <= end for f in findings)
    return {"caught": caught, "false_alarms": 0}


def main(argv: list[str]) -> int:
    runs = int(argv[argv.index("--runs") + 1]) if "--runs" in argv else 3
    rows, cost = [], 0.0
    for pr in prepared():
        expected = json.loads((pr / "expected.json").read_text())
        results = []
        for run in range(1, runs + 1):
            r = review((pr / "diff.patch").read_text(), (pr / "description.md").read_text())
            results.append({"run": run, **score(expected, r.findings),
                            "findings": len(r.findings), "dropped": len(r.dropped),
                            "cost_usd": r.cost_usd})
            cost += r.cost_usd
        rows.append({"pr": pr.name, "planted": expected["planted"], "results": results})
        if expected["planted"]:
            hits = sum(x["caught"] for x in results)
            print(f"  {pr.name:26} bug   caught {hits}/{runs}")
        else:
            alarms = [x["false_alarms"] for x in results]
            print(f"  {pr.name:26} clean false alarms {alarms}")
    per_run = [sum(row["results"][i]["caught"] is True for row in rows) for i in range(runs)]
    alarms = [sum(row["results"][i]["false_alarms"] for row in rows) for i in range(runs)]
    bugs = sum(1 for row in rows if row["planted"])
    print(f"caught per run: {per_run} of {bugs} · false alarms per run: {alarms} · "
          f"total cost ${cost:.4f} for {len(rows) * runs} reviews")
    out = Path(f"measure-{time.strftime('%Y%m%d-%H%M%S')}.json")
    out.write_text(json.dumps(rows, indent=2))
    print(f"details: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
