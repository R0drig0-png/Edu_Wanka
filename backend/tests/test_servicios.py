"""Pruebas unitarias de la capa de servicios (sin base de datos)."""

import unittest

from backend.schemas.recursos import Recurso, RecursoCreate, RecursoUpdate
from backend.schemas.usuarios import Usuario, UsuarioCreate, UsuarioLogin
from backend.services.exceptions import (
    CredencialesInvalidasError,
    RecursoNotFoundError,
    UsuarioAlreadyExistsError,
)
from backend.services.recursos import RecursoService
from backend.services.seguridad import hash_password
from backend.services.usuarios import UsuarioService


class RepositorioRecursosFalso:
    """Doble de prueba que simula la persistencia de recursos."""

    def __init__(self) -> None:
        self.datos: dict[int, Recurso] = {}
        self._siguiente = 1

    def list(self) -> list[Recurso]:
        return list(self.datos.values())

    def get(self, id: int) -> Recurso | None:
        return self.datos.get(id)

    def add(self, recurso: RecursoCreate) -> Recurso:
        guardado = Recurso(id=self._siguiente, **recurso.model_dump())
        self.datos[self._siguiente] = guardado
        self._siguiente += 1
        return guardado

    def update(self, id: int, datos: RecursoUpdate) -> Recurso | None:
        actual = self.datos.get(id)
        if actual is None:
            return None
        actualizada = Recurso(id=id, archivo_url=actual.archivo_url, **datos.model_dump())
        self.datos[id] = actualizada
        return actualizada

    def delete(self, id: int) -> bool:
        return self.datos.pop(id, None) is not None


class RepositorioUsuariosFalso:
    """Doble de prueba que simula la persistencia de usuarios."""

    def __init__(self) -> None:
        self.datos: dict[str, tuple[int, str, str, str]] = {}
        self._siguiente = 1

    def existe_correo(self, correo: str) -> bool:
        return correo in self.datos

    def get_por_id(self, id: int) -> Usuario | None:
        for correo, (uid, nombre, _, rol) in self.datos.items():
            if uid == id:
                return Usuario(id=uid, nombre=nombre, correo=correo, rol=rol)
        return None

    def get_credenciales(self, correo: str) -> tuple[int, str, str, str] | None:
        return self.datos.get(correo)

    def add(self, usuario: UsuarioCreate, password_hash: str) -> Usuario:
        uid = self._siguiente
        self._siguiente += 1
        self.datos[usuario.correo] = (
            uid,
            usuario.nombre,
            password_hash,
            usuario.rol,
        )
        return Usuario(
            id=uid,
            nombre=usuario.nombre,
            correo=usuario.correo,
            rol=usuario.rol,
        )


class RecursoServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repositorio = RepositorioRecursosFalso()
        self.servicio = RecursoService(self.repositorio)

    def test_crear_asigna_id_generado_y_persiste_adjunto(self) -> None:
        creado = self.servicio.crear(
            RecursoCreate(
                titulo="Guía de Álgebra",
                categoria="Matematicas",
                autor_fuente="Elaboración propia",
                descripcion="Resumen",
                archivo_url="/uploads/abc.pdf",
            )
        )
        self.assertEqual(creado.id, 1)
        self.assertEqual(creado.archivo_url, "/uploads/abc.pdf")
        self.assertEqual(len(self.servicio.listar()), 1)

    def test_obtener_inexistente_lanza_error_de_dominio(self) -> None:
        with self.assertRaises(RecursoNotFoundError):
            self.servicio.obtener(99)

    def test_eliminar_inexistente_lanza_error_de_dominio(self) -> None:
        with self.assertRaises(RecursoNotFoundError):
            self.servicio.eliminar(99)


class UsuarioServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repositorio = RepositorioUsuariosFalso()
        self.servicio = UsuarioService(self.repositorio)

    def test_registro_hash_no_guarda_claro_y_login_devuelve_token(self) -> None:
        registrado = self.servicio.registrar(
            UsuarioCreate(
                nombre="Luis Rodrigo",
                correo="luis@edured.pe",
                password="clave-segura-123",
            )
        )
        self.assertEqual(registrado.rol, "estudiante")
        guardado = self.repositorio.datos[registrado.correo][2]
        self.assertTrue(guardado.startswith("$argon2"))
        self.assertNotIn("clave-segura-123", guardado)

        respuesta = self.servicio.login(
            UsuarioLogin(correo="luis@edured.pe", password="clave-segura-123")
        )
        self.assertTrue(respuesta.token)
        self.assertEqual(respuesta.usuario.id, registrado.id)
        self.assertEqual(
            self.servicio.usuario_del_token(respuesta.token).correo,
            "luis@edured.pe",
        )

    def test_registro_duplicado_lanza_conflicto(self) -> None:
        datos = UsuarioCreate(
            nombre="Luis Rodrigo",
            correo="luis@edured.pe",
            password="clave-segura-123",
        )
        self.servicio.registrar(datos)
        with self.assertRaises(UsuarioAlreadyExistsError):
            self.servicio.registrar(datos)

    def test_login_con_clave_incorrecta_lanza_error_de_dominio(self) -> None:
        self.servicio.registrar(
            UsuarioCreate(
                nombre="Luis Rodrigo",
                correo="luis@edured.pe",
                password="clave-segura-123",
            )
        )
        with self.assertRaises(CredencialesInvalidasError):
            self.servicio.login(
                UsuarioLogin(correo="luis@edured.pe", password="incorrecta")
            )


if __name__ == "__main__":
    unittest.main()
