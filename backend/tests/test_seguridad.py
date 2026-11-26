"""Pruebas unitarias de Argon2 y tokens JWT."""

from datetime import datetime, timedelta, timezone
import unittest

import jwt

from backend.config import SECRETO_APP
from backend.services.exceptions import TokenInvalidoError
from backend.services.seguridad import (
    crear_token,
    hash_password,
    validar_token,
    verificar_password,
)


class SeguridadTests(unittest.TestCase):
    def test_hash_argon2_y_verificacion_de_contrasena(self) -> None:
        almacenado = hash_password("clave-segura-123")
        self.assertTrue(almacenado.startswith("$argon2"))
        self.assertNotIn("clave-segura-123", almacenado)
        self.assertTrue(verificar_password("clave-segura-123", almacenado))
        self.assertFalse(verificar_password("otra-clave", almacenado))

    def test_token_jwt_valido_devuelve_identidad(self) -> None:
        token = crear_token(7, "estudiante")
        cabecera = jwt.get_unverified_header(token)
        self.assertEqual(cabecera["alg"], "HS256")
        self.assertEqual(validar_token(token), {"sub": 7, "rol": "estudiante"})

    def test_token_manipulado_se_rechaza(self) -> None:
        token = crear_token(7, "estudiante")
        manipulado = f"{token[:-1]}{'a' if token[-1] != 'a' else 'b'}"
        with self.assertRaises(TokenInvalidoError):
            validar_token(manipulado)

    def test_token_firmado_con_otro_secreto_se_rechaza(self) -> None:
        token = jwt.encode(
            {"sub": "7", "rol": "estudiante"},
            "secreto-de-prueba-suficientemente-largo-1234567890",
            algorithm="HS256",
        )
        with self.assertRaises(TokenInvalidoError):
            validar_token(token)

    def test_token_expirado_se_rechaza(self) -> None:
        ahora = datetime.now(timezone.utc)
        token = jwt.encode(
            {
                "sub": "7",
                "rol": "estudiante",
                "iat": ahora - timedelta(hours=2),
                "exp": ahora - timedelta(hours=1),
            },
            SECRETO_APP,
            algorithm="HS256",
        )
        with self.assertRaises(TokenInvalidoError):
            validar_token(token)

    def test_token_mal_formado_se_rechaza(self) -> None:
        with self.assertRaises(TokenInvalidoError):
            validar_token("sin-firma")
