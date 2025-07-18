from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import db_session
from app.exceptions import UniqueViolation
from app.schemas import PatienResponseSchema, PatientRequestSchema
from app.services import PatientService

router = APIRouter(
    prefix="/patient",
    tags=["Patient"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[PatienResponseSchema],
)
async def find_all(
    search: str = None,
    session: Session = Depends(db_session),
) -> List[PatienResponseSchema]:
    try:
        service = PatientService()
        response = await service.find_all(
            search=search,
            session=session,
        )
        return response
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.get(
    "/{uuid}",
    response_model=PatienResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def find_by_uuid(
    uuid: str,
    session: Session = Depends(db_session),
) -> PatienResponseSchema:
    try:
        service = PatientService()
        response = await service.find_by_uuid(
            uuid=uuid,
            session=session,
        )
        return response
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PatienResponseSchema,
)
async def create(
    payload: PatientRequestSchema,
    session: Session = Depends(db_session),
) -> PatienResponseSchema:
    try:
        service = PatientService()
        response = await service.create(
            payload=payload,
            session=session,
        )
        return response
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.put(
    "/{uuid}",
    response_model=PatienResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update(
    uuid: str,
    payload: PatientRequestSchema,
    session: Session = Depends(db_session),
) -> PatienResponseSchema:
    try:
        service = PatientService()
        response = await service.update(
            uuid=uuid,
            payload=payload,
            session=session,
        )
        return response
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.delete(
    "/{uuid}",
    status_code=status.HTTP_200_OK,
)
async def delete(
    uuid: str,
    session: Session = Depends(db_session),
) -> bool:
    try:
        service = PatientService()
        response = await service.delete(
            uuid=uuid,
            session=session,
        )
        return response
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.post(
    "/import",
    status_code=status.HTTP_201_CREATED,
)
async def import_patient(
    file: UploadFile = File(...),
    session: Session = Depends(db_session),
) -> bool:
    try:
        service = PatientService()
        response = await service.import_patient(
            file=file,
            session=session,
        )
        return response
    except IntegrityError as e:
        raise UniqueViolation() from e
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e
