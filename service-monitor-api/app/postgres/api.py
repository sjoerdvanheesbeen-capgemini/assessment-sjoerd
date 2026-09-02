from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from postgres.checker import PostgresqlChecker

router = APIRouter()

@router.get("/health/postgres/{name}")
async def health_postgres(name: str):
    try:
        checker = PostgresqlChecker(name)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to initialize the database check",
        ) from error

    result = await checker.check()
    if result["status"] == "unhealthy":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=result,
        )

    return result