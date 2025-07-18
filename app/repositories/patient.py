from sqlalchemy import asc, delete, select, update
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm import Session

from app.core import logger
from app.exceptions import NotFound, UniqueViolation
from app.models import PatientModel
from app.schemas import CreatePatientSchema


class PatientRepository:

    def __init__(
        self,
        patient: PatientModel = PatientModel,
    ):
        self.patient = patient

    async def create(
        self,
        payload: CreatePatientSchema,
        session: Session,
    ) -> PatientModel:

        try:
            logger.info(
                f"Initializing data persistence: {payload.model_dump()}"
            )

            stmt = self.patient(**payload.model_dump())
            session.add(stmt)
            session.commit()
            session.refresh(stmt)

            logger.info(f"Data persistence finished: {payload.model_dump()}")

            return stmt
        except IntegrityError as e:
            raise UniqueViolation() from e

    async def find_all(
        self,
        session: Session,
    ) -> PatientModel:

        logger.info(f"Find all user")

        stmt = select(self.patient).order_by(asc(self.patient.first_name))
        response = session.scalars(stmt).all()

        return response

    async def find_by_uuid(
        self,
        uuid: str,
        session: Session,
    ) -> PatientModel:

        try:

            logger.info(f"Find all user")

            stmt = select(self.patient).where(self.patient.uuid == uuid)
            response = session.scalars(stmt).one_or_none()

            if not response:
                raise NotFound()

            return response

        except StatementError as e:
            raise NotFound(message="Patient not found") from e

    async def update(
        self,
        uuid: str,
        payload: CreatePatientSchema,
        session: Session,
    ) -> PatientModel:

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
            raise NotFound(message="Patient not found")

        return response

    async def delete(
        self,
        uuid: str,
        session: Session,
    ) -> bool:

        try:
            search = select(self.patient).where(self.patient.uuid == uuid)
            search_execute = session.scalars(search).one_or_none()

            if not search_execute:
                raise NotFound(message="Patient not found")

            stmt = delete(self.patient).where(self.patient.uuid == uuid)

            execute_query = session.execute(stmt)
            session.commit()

            if execute_query.rowcount > 0:
                return True
            return NotFound(message="Unable to delete record")
        except Exception as e:
            raise NotFound(message=str(e)) from e
