"""Repositorio de usuarios: consultas parametrizadas sobre SQL Server."""

from pyodbc import Connection

from backend.database import obtener_conexion
from backend.schemas.usuarios import Usuario, UsuarioCreate
from backend.services.exceptions import RolNotFoundError

_COLUMNAS = (
    "SELECT u.id, u.nombre, u.correo, r.nombre AS rol FROM dbo.Usuarios AS u "
    "INNER JOIN dbo.Roles AS r ON r.id_rol = u.id_rol"
)


def _id_rol(conexion: Connection, nombre: str) -> int:
    cursor = conexion.cursor()
    cursor.execute("SELECT id_rol FROM dbo.Roles WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    if fila is None:
        raise RolNotFoundError(nombre)
    return int(fila[0])


class UsuarioRepository:
    """Operaciones de persistencia para registro y autenticacion."""

    def get_por_id(self, id: int) -> Usuario | None:
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(f"{_COLUMNAS} WHERE u.id = ?", (id,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return Usuario(
                id=int(fila.id),
                nombre=fila.nombre,
                correo=fila.correo,
                rol=fila.rol,
            )
        finally:
            conexion.close()

    def get_credenciales(self, correo: str) -> tuple[int, str, str, str] | None:
        """Devuelve (id, nombre, password_hash, rol) para verificar el login."""
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT u.id, u.nombre, u.password_hash, r.nombre AS rol "
                "FROM dbo.Usuarios AS u "
                "INNER JOIN dbo.Roles AS r ON r.id_rol = u.id_rol "
                "WHERE u.correo = ? AND u.activo = 1",
                (correo,),
            )
            fila = cursor.fetchone()
            if fila is None:
                return None
            return (int(fila.id), fila.nombre, fila.password_hash, fila.rol)
        finally:
            conexion.close()

    def existe_correo(self, correo: str) -> bool:
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT 1 FROM dbo.Usuarios WHERE correo = ?", (correo,)
            )
            return cursor.fetchone() is not None
        finally:
            conexion.close()

    def add(self, usuario: UsuarioCreate, password_hash: str) -> Usuario:
        conexion = obtener_conexion()
        try:
            id_rol = _id_rol(conexion, usuario.rol)
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO dbo.Usuarios (nombre, correo, password_hash, id_rol) "
                "OUTPUT INSERTED.id VALUES (?, ?, ?, ?)",
                (usuario.nombre, usuario.correo, password_hash, id_rol),
            )
            nuevo_id = int(cursor.fetchone()[0])
            conexion.commit()
            return Usuario(
                id=nuevo_id,
                nombre=usuario.nombre,
                correo=usuario.correo,
                rol=usuario.rol,
            )
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()


usuario_repository = UsuarioRepository()
