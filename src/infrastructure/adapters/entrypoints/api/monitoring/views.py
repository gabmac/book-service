from fastapi import APIRouter
from fastapi import status as http_status

router = APIRouter()


@router.get("/health", status_code=http_status.HTTP_200_OK)
def health_check() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
