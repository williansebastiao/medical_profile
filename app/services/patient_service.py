from io import StringIO

import pandas as pd
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core import logger
from app.enums import (
    DELETE_PATIENT_BY_UUID,
    FIND_ALL_PATIENTS_SERVICE,
    FIND_PATIENT_BY_UUID,
    IMPORT_PATIENTS,
    PATIENT_SERVICE_PAYLOAD,
    UPDATE_PATIENT,
)
from app.repositories import PatientRepository
from app.schemas import PatientRequestSchema


class PatientService:

    def __init__(
        self, patient_repository: PatientRepository = PatientRepository()
    ):
        self.patient_repository = patient_repository

    async def create(
        self,
        payload: PatientRequestSchema,
        session: Session,
    ):
        logger.info(f"{PATIENT_SERVICE_PAYLOAD} {payload.model_dump()}")
        return await self.patient_repository.create(
            payload=payload,
            session=session,
        )

    async def find_all(
        self,
        search: str,
        session: Session,
    ):
        logger.info(FIND_ALL_PATIENTS_SERVICE)
        return await self.patient_repository.find_all(
            search=search,
            session=session,
        )

    async def find_by_uuid(
        self,
        uuid: str,
        session: Session,
    ):
        logger.info(FIND_PATIENT_BY_UUID)
        return await self.patient_repository.find_by_uuid(
            uuid=uuid,
            session=session,
        )

    async def update(
        self,
        uuid: str,
        payload: PatientRequestSchema,
        session: Session,
    ):
        logger.info(f"{UPDATE_PATIENT} {payload.model_dump()}")
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
        logger.info(DELETE_PATIENT_BY_UUID)
        return await self.patient_repository.delete(
            uuid=uuid,
            session=session,
        )

    async def import_patient(
        self,
        file: UploadFile,
        session: Session,
    ) -> bool:
        logger.info(IMPORT_PATIENTS)
        contents = await file.read()
        decoded = contents.decode("utf-8")
        csv_file = pd.read_csv(StringIO(decoded))

        patients = []
        seek_patients_duplicate = set()
        for _, row in csv_file.iterrows():
            row_key = (
                row["first_name"],
                row["last_name"],
                row["email"],
                row["cpf"],
                row["phone"],
            )

            if row_key in seek_patients_duplicate:
                continue

            seek_patients_duplicate.add(row_key)

            patients.append(
                PatientRequestSchema(
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    email=row["email"],
                    cpf=row["cpf"],
                    phone=row["phone"],
                )
            )

        response = await self.patient_repository.import_patient(
            payload=patients,
            session=session,
        )

        return response
