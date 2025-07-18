from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get(
    "/health",
    tags=["Health"],
    status_code=status.HTTP_200_OK,
)
async def index() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Ok"},
    )
