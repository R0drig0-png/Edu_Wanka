"""Reglas de negocio del CRUD de recursos educativos."""

from backend.repositories.recursos import RecursoRepository, recurso_repository
from backend.schemas.recursos import Recurso, RecursoCreate, RecursoUpdate
from backend.services.exceptions import RecursoNotFoundError


class RecursoService:
    """Valida la existencia de los recursos antes de devolverlos o modificarlos."""

    def __init__(self, repository: RecursoRepository | None = None) -> None:
        self._repository = repository or recurso_repository

    def listar(self) -> list[Recurso]:
        return self._repository.list()

    def obtener(self, id: int) -> Recurso:
        recurso = self._repository.get(id)
        if recurso is None:
            raise RecursoNotFoundError(id)
        return recurso

    def crear(self, datos: RecursoCreate) -> Recurso:
        return self._repository.add(datos)

    def actualizar(self, id: int, datos: RecursoUpdate) -> Recurso:
        recurso = self._repository.update(id, datos)
        if recurso is None:
            raise RecursoNotFoundError(id)
        return recurso

    def eliminar(self, id: int) -> None:
        if not self._repository.delete(id):
            raise RecursoNotFoundError(id)


recurso_service = RecursoService()
