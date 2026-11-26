"""Repositorio de solicitudes de mentoría sobre SQL Server."""

from backend.database import obtener_conexion
from backend.schemas.mentorias import Mentoria, MentoriaCreate


class MentoriaRepository:
    """Persistencia de mentorías solidarias."""

    def list(self) -> list[Mentoria]:
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre_estudiante, tema, atendida, fecha_solicitud "
                "FROM dbo.Mentorias ORDER BY id"
            )
            return [
                Mentoria(
                    id=int(fila.id),
                    nombreEstudiante=fila.nombre_estudiante,
                    tema=fila.tema,
                    atendida=bool(fila.atendida),
                    fechaSolicitud=fila.fecha_solicitud,
                )
                for fila in cursor.fetchall()
            ]
        finally:
            conexion.close()

    def add(self, datos: MentoriaCreate, id_usuario: int | None = None) -> Mentoria:
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO dbo.Mentorias "
                "(nombre_estudiante, tema, id_usuario) "
                "OUTPUT INSERTED.id, INSERTED.atendida, INSERTED.fecha_solicitud "
                "VALUES (?, ?, ?)",
                (datos.nombre_estudiante, datos.tema, id_usuario),
            )
            fila = cursor.fetchone()
            conexion.commit()
            return Mentoria(
                id=int(fila.id),
                nombreEstudiante=datos.nombre_estudiante,
                tema=datos.tema,
                atendida=bool(fila.atendida),
                fechaSolicitud=fila.fecha_solicitud,
            )
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()


mentoria_repository = MentoriaRepository()
