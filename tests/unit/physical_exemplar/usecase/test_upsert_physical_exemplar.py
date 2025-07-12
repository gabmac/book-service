from tests.unit.physical_exemplar.usecase.conftest import (
    PhysicalExemplarUseCaseConftest,
)

from src.application.usecase.physical_exemplar.upsert_physical_exemplar import (
    UpsertPhysicalExemplar,
)


class TestUpsertPhysicalExemplar(PhysicalExemplarUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.upsert_physical_exemplar = UpsertPhysicalExemplar(
            repository=self.mock_physical_exemplar_repository,
            physical_exemplar_producer=self.mock_physical_exemplar_producer,
        )
        self.mock_physical_exemplar_repository.upsert_physical_exemplar.return_value = (
            None
        )
        self.mock_physical_exemplar_repository.upsert_physical_exemplar.side_effect = (
            None
        )

    def tearDown(self):
        super().tearDown()
        self.mock_physical_exemplar_repository.upsert_physical_exemplar.reset_mock()

    def test_execute_successful_upsert(self):
        # Arrange
        physical_exemplar = self.physical_exemplar_model_factory.build()

        # Mock repository response
        self.mock_physical_exemplar_repository.upsert_physical_exemplar.return_value = (
            physical_exemplar
        )

        # Act
        result = self.upsert_physical_exemplar.execute(physical_exemplar)

        # Assert
        self.mock_physical_exemplar_repository.upsert_physical_exemplar.assert_called_once_with(
            physical_exemplar,
        )
        self.assertEqual(result, physical_exemplar)
