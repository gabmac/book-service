from enum import StrEnum


class BookType(StrEnum):
    """Book type enum."""

    PHYSICAL = "physical"
    EBOOK = "ebook"
    BOTH = "both"
