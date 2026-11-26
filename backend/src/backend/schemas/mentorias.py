"""Modelos Pydantic de solicitudes de mentoría solidaria."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MentoriaBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, populate_by_name=True)

    nombre_estudiante: str = Field(
        ...,
        alias="nombreEstudiante",
        min_length=2,
        max_length=120,
        examples=["Luis Rodrigo"],
    )
    tema: str = Field(
        ...,
        min_length=3,
        max_length=200,
        examples=["Conexión de FastAPI con SQL Server"],
    )


class MentoriaCreate(MentoriaBase):
    """Datos enviados por el formulario de mentorías."""


class Mentoria(MentoriaBase):
    id: int = Field(..., gt=0)
    atendida: bool
    fecha_solicitud: datetime = Field(alias="fechaSolicitud")
