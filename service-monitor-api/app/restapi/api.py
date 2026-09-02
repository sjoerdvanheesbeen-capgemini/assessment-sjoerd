from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from restapi.checker import RestChecker

router = APIRouter()

@router.get("/health/restapi/{name}")
async def health_restapi(name: str):
    try:
        checker = RestChecker(name)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to initialize REST API health check for '{name}'",
        ) from error

    result = await checker.check()
    if result["status"] == "unhealthy":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=result,
        )

    return result