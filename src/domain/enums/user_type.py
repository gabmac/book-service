from enum import StrEnum


class UserType(StrEnum):
    """User type enum."""

    ADMIN = "admin"
    NORMAL = "normal"
    LIBRARIAN = "librarian"
    STUDENT = "student"
    TEACHER = "teacher"
