from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel


class PatientModel(BaseModel):
    __tablename__ = "patients"

    first_name: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        nullable=False,
    )
    cpf: Mapped[str] = mapped_column(
        String(11),
        unique=True,
        nullable=False,
    )
    phone: Mapped[str] = mapped_column(
        String(11),
        nullable=False,
    )
    medical_record: Mapped["MedicalRecordModel"] = relationship(
        back_populates="patient",
        uselist=False,
    )

    def __repr__(self):
        return f"User(uuid={self.uuid}, first_name={self.first_name}, last_name={self.last_name})"
