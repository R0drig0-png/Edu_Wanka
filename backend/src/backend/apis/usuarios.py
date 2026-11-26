"""Rutas HTTP de registro, login y sesion de usuarios."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status

from backend.schemas.usuarios import RespuestaLogin, Usuario, UsuarioCreate, UsuarioLogin
from backend.services.exceptions import TokenInvalidoError, UsuarioNotFoundError
from backend.services.usuarios import UsuarioService, usuario_service

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
auth_router = APIRouter(prefix="/auth", tags=["autenticacion"])


def get_usuario_service() -> UsuarioService:
    return usuario_service


ServiceDep = Annotated[UsuarioService, Depends(get_usuario_service)]


def get_usuario_actual(
    authorization: str | None = Header(default=None),
    service: UsuarioService = Depends(get_usuario_service),
) -> Usuario:
    """Extrae y valida el token Bearer de la cabecera Authorization."""
    if authorization is None or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere un token Bearer.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ", 1)[1].strip()
    try:
        return service.usuario_del_token(token)
    except (TokenInvalidoError, UsuarioNotFoundError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


UsuarioActual = Annotated[Usuario, Depends(get_usuario_actual)]


@router.post(
    "",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
)
def registrar(datos: UsuarioCreate, service: ServiceDep) -> Usuario:
    return service.registrar(datos)


@auth_router.post(
    "/login",
    response_model=RespuestaLogin,
    summary="Iniciar sesion",
)
def login(datos: UsuarioLogin, service: ServiceDep) -> RespuestaLogin:
    return service.login(datos)


@auth_router.get(
    "/me",
    response_model=Usuario,
    summary="Obtener el usuario autenticado",
)
def me(usuario: UsuarioActual) -> Usuario:
    return usuario
