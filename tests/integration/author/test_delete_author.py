from tests.integration.author.conftest import AuthorViewConfTest


class TestDeleteAuthor(AuthorViewConfTest):
    def test_delete_author(self):

        # Scenario: Delete an author

        # Given an author is stored in the database
        author = self.author_model_factory.build(
            name="Author to Delete",
            created_by="test_user",
            updated_by="test_user",
        )
        stored_author = self.author_repository.upsert_author(author)

        # When a request is made to delete the author
        response = self.client.delete(
            "api/author",
            params={"id": str(stored_author.id)},
        )

        # Then the response is a 202 status code
        self.assertEqual(response.status_code, 202)

        # And the message is consumed from the queue
        self.consumer.consume("author.deletion")

        # And the author is deleted from the database
        authors_after = self.author_repository.get_author_by_filter(None)
        self.assertEqual(authors_after, [])
