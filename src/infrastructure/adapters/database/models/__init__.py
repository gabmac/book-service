# Import all models to ensure they are registered with SQLModel.metadata
from .author import Author
from .author_book_link import AuthorBookLink
from .base_model import Base
from .book import Book
from .book_book_category_link import BookBookCategoryLink
from .book_category import BookCategory
from .book_data import BookData
from .book_lending import BookLending
from .branch import Branch
from .physical_exemplar import PhysicalExemplar
from .user import User, UserType
from .user_configuration import UserConfiguration

__all__ = [
    "Base",
    "Author",
    "AuthorBookLink",
    "BookBookCategoryLink",
    "BookCategory",
    "BookData",
    "BookLending",
    "Book",
    "Branch",
    "PhysicalExemplar",
    "User",
    "UserType",
    "UserConfiguration",
]
