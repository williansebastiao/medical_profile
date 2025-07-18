from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel


class MedicalRecordModel(BaseModel):
    __tablename__ = "medical_records"

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    patient_uuid: Mapped[UUID] = mapped_column(ForeignKey("patients.uuid"))
    patient: Mapped["PatientModel"] = relationship(
        back_populates="medical_record"
    )

    def __repr__(self):
        return f"User(uuid={self.uuid}, first_name={self.first_name}, last_name={self.last_name})"
