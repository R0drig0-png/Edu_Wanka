"""Reglas de negocio de registro, login y sesion de usuarios."""

from backend.repositories.usuarios import UsuarioRepository, usuario_repository
from backend.schemas.usuarios import (
    RespuestaLogin,
    Usuario,
    UsuarioCreate,
    UsuarioLogin,
)
from backend.services.exceptions import (
    CredencialesInvalidasError,
    UsuarioAlreadyExistsError,
    UsuarioNotFoundError,
)
from backend.services.seguridad import (
    crear_token,
    hash_password,
    validar_token,
    verificar_password,
)


class UsuarioService:
    """Gestiona altas, autenticacion y validacion de token."""

    def __init__(self, repository: UsuarioRepository | None = None) -> None:
        self._repository = repository or usuario_repository

    def registrar(self, datos: UsuarioCreate) -> Usuario:
        if self._repository.existe_correo(datos.correo):
            raise UsuarioAlreadyExistsError(datos.correo)
        return self._repository.add(datos, hash_password(datos.password))

    def login(self, datos: UsuarioLogin) -> RespuestaLogin:
        credenciales = self._repository.get_credenciales(datos.correo)
        if credenciales is None:
            raise CredencialesInvalidasError()

        id_usuario, nombre, password_hash, rol = credenciales
        if not verificar_password(datos.password, password_hash):
            raise CredencialesInvalidasError()

        return RespuestaLogin(
            token=crear_token(id_usuario, rol),
            usuario=Usuario(id=id_usuario, nombre=nombre, correo=datos.correo, rol=rol),
        )

    def obtener(self, id: int) -> Usuario:
        usuario = self._repository.get_por_id(id)
        if usuario is None:
            raise UsuarioNotFoundError(id)
        return usuario

    def usuario_del_token(self, token: str) -> Usuario:
        return self.obtener(validar_token(token)["sub"])


usuario_service = UsuarioService()
