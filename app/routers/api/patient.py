from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import db_session
from app.exceptions import UniqueViolation
from app.schemas import CreatePatienResponseSchema, CreatePatientSchema
from app.services import PatientService

router = APIRouter(
    prefix="/patient",
    tags=["Patient"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[CreatePatienResponseSchema],
)
async def find_all(
    filter: str = None,
    session: Session = Depends(db_session),
) -> List[CreatePatienResponseSchema]:
    try:
        service = PatientService()
        response = await service.find_all(
            filter=filter,
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
    response_model=CreatePatienResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def find_by_uuid(
    uuid: str,
    session: Session = Depends(db_session),
) -> CreatePatienResponseSchema:
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
    response_model=CreatePatienResponseSchema,
)
async def create(
    payload: CreatePatientSchema,
    session: Session = Depends(db_session),
) -> CreatePatienResponseSchema:
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
    response_model=CreatePatienResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update(
    uuid: str,
    payload: CreatePatientSchema,
    session: Session = Depends(db_session),
) -> CreatePatienResponseSchema:
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
