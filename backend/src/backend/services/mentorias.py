"""Reglas de negocio de las solicitudes de mentoría solidaria."""

from backend.repositories.mentorias import MentoriaRepository, mentoria_repository
from backend.schemas.mentorias import Mentoria, MentoriaCreate


class MentoriaService:
    """Registra solicitudes y opcionalmente las asocia al usuario autenticado."""

    def __init__(self, repository: MentoriaRepository | None = None) -> None:
        self._repository = repository or mentoria_repository

    def listar(self) -> list[Mentoria]:
        return self._repository.list()

    def solicitar(self, datos: MentoriaCreate, id_usuario: int | None = None) -> Mentoria:
        return self._repository.add(datos, id_usuario)


mentoria_service = MentoriaService()
