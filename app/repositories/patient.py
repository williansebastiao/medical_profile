from typing import List

from sqlalchemy import asc, delete, or_, select, update
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm import Session

from app.core import logger
from app.enums import (
    DATA_PERSISTENCE_FINISHED,
    DELETE_PATIENT_BY_UUID,
    FIND_ALL_PATIENTS_SERVICE,
    FIND_PATIENT_BY_UUID,
    IMPORT_PATIENTS,
    INITIALIZING_DATA_PERSISTENCE,
    PATIENT_NOT_FOUND,
    UNABLE_TO_DELETE_RECORD,
    UPDATE_PATIENT,
)
from app.exceptions import NotFound, UniqueViolation
from app.models import PatientModel
from app.schemas import PatientRequestSchema


class PatientRepository:

    def __init__(
        self,
        patient: PatientModel = PatientModel,
    ):
        self.patient = patient

    async def create(
        self,
        payload: PatientRequestSchema,
        session: Session,
    ) -> PatientModel:

        try:
            logger.info(
                f"{INITIALIZING_DATA_PERSISTENCE}: {payload.model_dump()}"
            )

            stmt = self.patient(**payload.model_dump())
            session.add(stmt)
            session.commit()
            session.refresh(stmt)

            logger.info(f"{DATA_PERSISTENCE_FINISHED} {payload.model_dump()}")

            return stmt
        except IntegrityError as e:
            raise UniqueViolation() from e

    async def find_all(
        self,
        search: str,
        session: Session,
    ) -> PatientModel:

        logger.info(FIND_ALL_PATIENTS_SERVICE)

        stmt = select(self.patient)
        if search:
            stmt = stmt.where(
                or_(
                    self.patient.first_name.like(f"%{search}%"),
                    self.patient.last_name.like(f"%{search}%"),
                    self.patient.email.like(f"%{search}%"),
                    self.patient.cpf.like(f"%{search}%"),
                )
            )

        stmt = stmt.order_by(asc(self.patient.first_name))
        response = session.scalars(stmt).all()

        return response

    async def find_by_uuid(
        self,
        uuid: str,
        session: Session,
    ) -> PatientModel:

        try:

            logger.info(f"{FIND_PATIENT_BY_UUID}: {uuid}")

            stmt = select(self.patient).where(self.patient.uuid == uuid)
            response = session.scalars(stmt).one_or_none()

            if not response:
                raise NotFound()

            return response

        except StatementError as e:
            raise NotFound(message=PATIENT_NOT_FOUND) from e

    async def update(
        self,
        uuid: str,
        payload: PatientRequestSchema,
        session: Session,
    ) -> PatientModel:

        logger.info(f"{UPDATE_PATIENT}: {uuid}")
        stmt = (
            update(self.patient)
            .where(self.patient.uuid == uuid)
            .values(**payload.model_dump())
            .returning(self.patient)
        )

        execute_query = session.execute(stmt)
        session.commit()

        response = execute_query.scalar_one_or_none()
        if not response:
            raise NotFound(message=PATIENT_NOT_FOUND)

        return response

    async def delete(
        self,
        uuid: str,
        session: Session,
    ) -> bool:

        logger.info(f"{DELETE_PATIENT_BY_UUID}: {uuid}")
        try:
            search = select(self.patient).where(self.patient.uuid == uuid)
            search_execute = session.scalars(search).one_or_none()

            if not search_execute:
                raise NotFound(message=PATIENT_NOT_FOUND)

            stmt = delete(self.patient).where(self.patient.uuid == uuid)

            execute_query = session.execute(stmt)
            session.commit()

            if execute_query.rowcount > 0:
                return True
            return NotFound(message=UNABLE_TO_DELETE_RECORD)
        except Exception as e:
            raise NotFound(message=str(e)) from e

    async def import_patient(
        self,
        payload: List[PatientRequestSchema],
        session: Session,
    ) -> bool:

        logger.info(IMPORT_PATIENTS)
        try:
            for item in payload:
                stmt = self.patient(**item.model_dump())
                session.add(stmt)
                session.commit()
                session.refresh(stmt)

            return True
        except IntegrityError as e:
            raise UniqueViolation() from e
        except Exception as e:
            raise ValueError(str(e)) from e
