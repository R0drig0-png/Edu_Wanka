"""Rutas HTTP de mentorías solidarias."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from backend.schemas.mentorias import Mentoria, MentoriaCreate
from backend.services.exceptions import TokenInvalidoError, UsuarioNotFoundError
from backend.services.mentorias import MentoriaService, mentoria_service
from backend.services.usuarios import usuario_service

router = APIRouter(prefix="/mentorias", tags=["mentorias"])


def get_mentoria_service() -> MentoriaService:
    return mentoria_service


ServiceDep = Annotated[MentoriaService, Depends(get_mentoria_service)]


def get_id_usuario_opcional(
    authorization: str | None = Header(default=None),
) -> int | None:
    """Asocia la solicitud al usuario si envio un token valido."""
    if authorization is None or not authorization.lower().startswith("bearer "):
        return None
    try:
        return usuario_service.usuario_del_token(
            authorization.split(" ", 1)[1].strip()
        ).id
    except (TokenInvalidoError, UsuarioNotFoundError):
        return None


IdUsuarioOpcional = Annotated[int | None, Depends(get_id_usuario_opcional)]


@router.get("", response_model=list[Mentoria], summary="Listar solicitudes de mentoría")
def listar(service: ServiceDep) -> list[Mentoria]:
    return service.listar()


@router.post(
    "",
    response_model=Mentoria,
    status_code=status.HTTP_201_CREATED,
    summary="Solicitar una mentoría",
)
def solicitar(
    datos: MentoriaCreate,
    service: ServiceDep,
    id_usuario: IdUsuarioOpcional,
) -> Mentoria:
    return service.solicitar(datos, id_usuario)
