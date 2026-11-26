"""Modelos Pydantic de usuarios y autenticacion."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CORREO_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class UsuarioBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, populate_by_name=True)

    nombre: str = Field(..., min_length=2, max_length=120, examples=["Luis Rodrigo"])
    correo: str = Field(
        ...,
        max_length=150,
        pattern=CORREO_PATTERN,
        examples=["luis@edured.pe"],
    )


class UsuarioCreate(UsuarioBase):
    """Registro publico: siempre se crea como estudiante."""

    password: str = Field(..., min_length=8, max_length=128)
    rol: Literal["estudiante"] = "estudiante"


class UsuarioLogin(BaseModel):
    correo: str = Field(..., max_length=150, pattern=CORREO_PATTERN)
    password: str = Field(..., min_length=1, max_length=128)


class Usuario(UsuarioBase):
    id: int = Field(..., gt=0)
    rol: str


class RespuestaLogin(BaseModel):
    token: str
    usuario: Usuario
