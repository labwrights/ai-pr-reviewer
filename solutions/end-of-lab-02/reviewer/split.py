"""Lab 1: split a change too big for one call, without splitting a finding's context."""

from .diff import FileDiff, hunks


def estimate_tokens(text: str) -> int:
    return len(text) // 4 + 1  # about 4 characters per token for code and English


def split(files: list[FileDiff], budget: int) -> list[list[FileDiff]]:
    """Group files into parts that each fit the budget. A file bigger than the budget
    on its own goes hunk by hunk; a single hunk is never cut."""
    parts: list[list[FileDiff]] = []
    current: list[FileDiff] = []
    size = 0
    for file in files:
        pieces = [file] if estimate_tokens(file.text) <= budget else hunks(file)
        for piece in pieces:
            tokens = estimate_tokens(piece.text)
            if current and size + tokens > budget:  # this piece would overflow: start a new part
                parts.append(current)
                current, size = [], 0
            current.append(piece)
            size += tokens
    if current:
        parts.append(current)
    return parts
