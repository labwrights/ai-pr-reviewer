"""Ticket rules: what a valid ticket is, paging through lists, and tags."""

SEVERITIES = ("sev1", "sev2", "sev3")
MAX_TITLE = 200


class InvalidTicket(ValueError):
    pass


def validate(title: str, severity: str) -> None:
    """Raise InvalidTicket with a reason a person can act on."""
    if not title.strip():
        raise InvalidTicket("the title is empty")
    if len(title) > MAX_TITLE:
        raise InvalidTicket(f"the title is longer than {MAX_TITLE} characters")
    if severity not in SEVERITIES:
        raise InvalidTicket(f"severity must be one of {', '.join(SEVERITIES)}")


def page(items: list, page_number: int, page_size: int = 20) -> list:
    """One page of a list; page_number starts at 1."""
    if page_number < 1 or page_size < 1:
        raise ValueError("page_number and page_size start at 1")
    start = (page_number - 1) * page_size
    return items[start:start + page_size]


def with_tag(tags: list[str] | None, tag: str) -> list[str]:
    """A new list of tags with `tag` added once; the input list is never changed."""
    result = list(tags or [])
    if tag not in result:
        result.append(tag)
    return result
