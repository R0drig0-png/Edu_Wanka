"""Errores de dominio: la capa de API los traduce a codigos HTTP."""


class RecursoNotFoundError(Exception):
    """No existe un recurso con el ID solicitado."""

    def __init__(self, id: int) -> None:
        self.id = id
        super().__init__(f"No existe un recurso con ID '{id}'.")


class CategoriaNotFoundError(Exception):
    """La categoria indicada no esta en el catalogo."""

    def __init__(self, categoria: str) -> None:
        self.categoria = categoria
        super().__init__(f"La categoria '{categoria}' no esta registrada.")


class UsuarioNotFoundError(Exception):
    """No existe el usuario solicitado."""

    def __init__(self, id: int) -> None:
        self.id = id
        super().__init__(f"No existe un usuario con ID '{id}'.")


class UsuarioAlreadyExistsError(Exception):
    """El correo ya pertenece a otro usuario."""

    def __init__(self, correo: str) -> None:
        self.correo = correo
        super().__init__(f"Ya existe un usuario con el correo '{correo}'.")


class CredencialesInvalidasError(Exception):
    """Correo o contrasena incorrectos."""

    def __init__(self) -> None:
        super().__init__("Correo o contrasena incorrectos.")


class TokenInvalidoError(Exception):
    """El token de sesion no es valido o expiro."""

    def __init__(self) -> None:
        super().__init__("Sesion invalida o expirada. Inicia sesion nuevamente.")


class RolNotFoundError(Exception):
    """El rol indicado no esta en el catalogo."""

    def __init__(self, rol: str) -> None:
        self.rol = rol
        super().__init__(f"El rol '{rol}' no esta registrado.")
