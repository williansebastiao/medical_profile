from sqlalchemy.orm import Session

from app.core import logger
from app.repositories import PatientRepository
from app.schemas import CreatePatientSchema


class PatientService:

    def __init__(
        self, patient_repository: PatientRepository = PatientRepository()
    ):
        self.patient_repository = patient_repository

    async def create(
        self,
        payload: CreatePatientSchema,
        session: Session,
    ):
        logger.info(f"Patient Service payload: {payload.model_dump()}")
        return await self.patient_repository.create(
            payload=payload,
            session=session,
        )

    async def find_all(
        self,
        filter: str,
        session: Session,
    ):
        logger.info(f"Find all patient service")
        return await self.patient_repository.find_all(
            filter=filter,
            session=session,
        )

    async def find_by_uuid(
        self,
        uuid: str,
        session: Session,
    ):
        logger.info(f"Find all patient service")
        return await self.patient_repository.find_by_uuid(
            uuid=uuid,
            session=session,
        )

    async def update(
        self,
        uuid: str,
        payload: CreatePatientSchema,
        session: Session,
    ):
        logger.info(f"Find all patient service")
        return await self.patient_repository.update(
            uuid=uuid,
            payload=payload,
            session=session,
        )

    async def delete(
        self,
        uuid: str,
        session: Session,
    ):
        logger.info(f"Find all patient service")
        return await self.patient_repository.delete(
            uuid=uuid,
            session=session,
        )
