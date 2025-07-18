import re

from pydantic import BaseModel, EmailStr, field_validator


class PatientRequestSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    cpf: str
    phone: str

    @field_validator("cpf", "phone", mode="after")
    @classmethod
    def remove_special_characters(cls, value: str) -> str:
        return re.sub(r"\D", "", value)


class PatienResponseSchema(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    email: EmailStr
    cpf: str
    phone: str

    @field_validator("uuid", mode="before")
    @classmethod
    def convert_uuid_to_str(cls, value: str) -> str:
        return str(value)
