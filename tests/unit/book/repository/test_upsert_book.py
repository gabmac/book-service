from tests.unit.book.repository.conftest import BookRepositoryConftest


class TestUpsertBook(BookRepositoryConftest):

    def test_upsert_book(self):
        book = self.book_model_factory.build()
        self.assertEqual(
            self.book_repository.upsert_book(book=book),
            book,
        )
