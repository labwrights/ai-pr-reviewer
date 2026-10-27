"""Pre-built: reads a unified diff (what `git diff` prints) into files and changed lines.

You don't need to change this file. The reviewer uses it to know exactly which
lines a pull request added, so it can refuse findings anywhere else.
"""

import re
from dataclasses import dataclass, field

HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


@dataclass
class FileDiff:
    path: str  # the file's path after the change, such as fieldnotes/store.py
    text: str = ""  # this file's part of the diff, as git printed it
    added_lines: set[int] = field(default_factory=set)  # new-side line numbers the change added

    @property
    def reviewable(self) -> bool:
        return bool(self.added_lines)


def parse(diff_text: str) -> list[FileDiff]:
    """One FileDiff per changed file. Deleted and binary files have no added lines."""
    files: list[FileDiff] = []
    current: FileDiff | None = None
    line_no = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git "):
            current = FileDiff(path=raw.split(" b/", 1)[-1])
            files.append(current)
        if current is None:
            continue
        current.text += raw + "\n"
        if raw.startswith("+++ "):
            if raw[4:] != "/dev/null":
                current.path = raw[6:] if raw.startswith("+++ b/") else raw[4:]
        elif m := HUNK.match(raw):
            line_no = int(m.group(3))
        elif raw.startswith("+") and not raw.startswith("+++"):
            current.added_lines.add(line_no)
            line_no += 1
        elif raw.startswith(" "):
            line_no += 1
    return files


def numbered(file: FileDiff) -> str:
    """The file's diff with each new-side line number written in, so the model
    never has to count lines: `  37 + code` for added lines, `  36   code` for
    unchanged ones, `     - code` for removed ones."""
    out, line_no = [f"file: {file.path}"], 0
    for raw in file.text.splitlines():
        if m := HUNK.match(raw):
            line_no = int(m.group(3))
            out.append(raw)
        elif raw.startswith(("diff --git", "index ", "--- ", "+++ ", "new file", "deleted file")):
            continue
        elif raw.startswith("+"):
            out.append(f"{line_no:5} + {raw[1:]}")
            line_no += 1
        elif raw.startswith("-"):
            out.append(f"      - {raw[1:]}")
        else:
            out.append(f"{line_no:5}   {raw[1:]}")
            line_no += 1
    return "\n".join(out) + "\n"


def hunks(file: FileDiff) -> list[FileDiff]:
    """The file split into one FileDiff per hunk, for a file too big for one call."""
    header, pieces = [], []
    for raw in file.text.splitlines(keepends=True):
        if HUNK.match(raw):
            pieces.append([raw])
        elif pieces:
            pieces[-1].append(raw)
        else:
            header.append(raw)
    return [p for p in (parse("".join(header + piece)) for piece in pieces) for p in p]
