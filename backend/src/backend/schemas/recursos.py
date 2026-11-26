"""Modelos Pydantic del dominio de recursos educativos."""

from pydantic import BaseModel, ConfigDict, Field


class RecursoBase(BaseModel):
    """Campos comunes de un recurso; el ID lo genera SQL Server."""

    model_config = ConfigDict(str_strip_whitespace=True, populate_by_name=True)

    titulo: str = Field(..., min_length=1, max_length=100, examples=["Guía de Álgebra"])
    categoria: str = Field(..., min_length=1, max_length=100, examples=["Matemáticas"])
    autor_fuente: str = Field(
        default="",
        alias="autorFuente",
        max_length=150,
        examples=["Elaboración propia (2026)"],
    )
    descripcion: str = Field(
        default="",
        max_length=500,
        examples=["Guía de consultas parametrizadas y diseño de tablas relacionales."],
    )
    archivo_url: str | None = Field(
        default=None,
        alias="archivoUrl",
        description="Ruta pública del archivo adjunto guardado en el servidor.",
    )


class RecursoCreate(RecursoBase):
    """Datos necesarios para crear un recurso."""


class RecursoUpdate(BaseModel):
    """Datos modificables de un recurso (el ID y el adjunto no se cambian)."""

    model_config = ConfigDict(str_strip_whitespace=True, populate_by_name=True)

    titulo: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Guía de Álgebra Avanzada"],
    )
    categoria: str = Field(..., min_length=1, max_length=100, examples=["Matemáticas"])
    autor_fuente: str = Field(
        default="",
        alias="autorFuente",
        max_length=150,
        examples=["Elaboración propia (2026)"],
    )
    descripcion: str = Field(default="", max_length=500)


class Recurso(RecursoBase):
    """Representacion de un recurso persistido en SQL Server."""

    id: int = Field(..., gt=0, description="Identificador generado por SQL Server.")
