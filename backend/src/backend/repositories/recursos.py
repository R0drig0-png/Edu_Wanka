"""Repositorio de recursos: CRUD sobre SQL Server con consultas parametrizadas."""

from pyodbc import Connection, Row

from backend.database import obtener_conexion
from backend.schemas.recursos import Recurso, RecursoCreate, RecursoUpdate
from backend.services.exceptions import CategoriaNotFoundError

_COLUMNAS = (
    "SELECT r.id, r.titulo, r.descripcion, c.nombre AS categoria, "
    "r.autor_fuente, r.archivo_url FROM dbo.Recursos AS r "
    "INNER JOIN dbo.Categorias AS c ON c.id_categoria = r.id_categoria"
)


def _a_recurso(fila: Row) -> Recurso:
    """Convierte una fila de SQL Server en el modelo de respuesta."""
    return Recurso(
        id=int(fila.id),
        titulo=fila.titulo,
        descripcion=fila.descripcion or "",
        categoria=fila.categoria,
        autor_fuente=fila.autor_fuente or "",
        archivo_url=fila.archivo_url,
    )


def _id_categoria(conexion: Connection, nombre: str) -> int:
    """Resuelve el nombre de categoria del formulario a su clave foranea."""
    cursor = conexion.cursor()
    cursor.execute("SELECT id_categoria FROM dbo.Categorias WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    if fila is None:
        raise CategoriaNotFoundError(nombre)
    return int(fila[0])


class RecursoRepository:
    """Operaciones CRUD sobre la tabla Recursos en SQL Server."""

    def list(self) -> list[Recurso]:
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(f"{_COLUMNAS} ORDER BY r.id")
            return [_a_recurso(fila) for fila in cursor.fetchall()]
        finally:
            conexion.close()

    def get(self, id: int) -> Recurso | None:
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(f"{_COLUMNAS} WHERE r.id = ?", (id,))
            fila = cursor.fetchone()
            return None if fila is None else _a_recurso(fila)
        finally:
            conexion.close()

    def add(self, recurso: RecursoCreate) -> Recurso:
        conexion = obtener_conexion()
        try:
            id_categoria = _id_categoria(conexion, recurso.categoria)
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO dbo.Recursos "
                "(titulo, descripcion, id_categoria, autor_fuente, archivo_url, id_usuario) "
                "OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?, ?)",
                (
                    recurso.titulo,
                    recurso.descripcion,
                    id_categoria,
                    recurso.autor_fuente,
                    recurso.archivo_url,
                    None,
                ),
            )
            nuevo_id = int(cursor.fetchone()[0])
            conexion.commit()
            return Recurso(
                id=nuevo_id,
                titulo=recurso.titulo,
                descripcion=recurso.descripcion,
                categoria=recurso.categoria,
                autor_fuente=recurso.autor_fuente,
                archivo_url=recurso.archivo_url,
            )
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def update(self, id: int, datos: RecursoUpdate) -> Recurso | None:
        conexion = obtener_conexion()
        try:
            id_categoria = _id_categoria(conexion, datos.categoria)
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE dbo.Recursos SET titulo = ?, descripcion = ?, "
                "id_categoria = ?, autor_fuente = ? WHERE id = ?",
                (
                    datos.titulo,
                    datos.descripcion,
                    id_categoria,
                    datos.autor_fuente,
                    id,
                ),
            )
            if cursor.rowcount == 0:
                conexion.rollback()
                return None
            conexion.commit()
            return Recurso(
                id=id,
                titulo=datos.titulo,
                descripcion=datos.descripcion,
                categoria=datos.categoria,
                autor_fuente=datos.autor_fuente,
                archivo_url=self._obtener_archivo_url(conexion, id),
            )
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def _obtener_archivo_url(self, conexion: Connection, id: int) -> str | None:
        cursor = conexion.cursor()
        cursor.execute("SELECT archivo_url FROM dbo.Recursos WHERE id = ?", (id,))
        fila = cursor.fetchone()
        return fila[0] if fila is not None else None

    def delete(self, id: int) -> bool:
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM dbo.Recursos WHERE id = ?", (id,))
            eliminado = cursor.rowcount > 0
            conexion.commit()
            return eliminado
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()


recurso_repository = RecursoRepository()
