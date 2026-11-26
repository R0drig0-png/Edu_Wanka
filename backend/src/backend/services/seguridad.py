"""Hash de contraseñas con Argon2 y tokens de sesion JWT (HS256)."""

from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from backend.config import SECRETO_APP
from backend.services.exceptions import TokenInvalidoError

ALGORITMO_JWT = "HS256"
DURACION_TOKEN_SEGUNDOS = 60 * 60 * 8

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Devuelve un hash Argon2id con sal y parametros incluidos."""
    return _hasher.hash(password)


def verificar_password(password: str, almacenado: str) -> bool:
    """Comprueba una contraseña contra el hash Argon2 almacenado."""
    try:
        return _hasher.verify(almacenado, password)
    except (VerifyMismatchError, InvalidHashError, VerificationError):
        return False


def crear_token(usuario_id: int, rol: str) -> str:
    """Genera un JWT firmado con HS256, con emision y vencimiento."""
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": str(usuario_id),
        "rol": rol,
        "iat": ahora,
        "exp": ahora + timedelta(seconds=DURACION_TOKEN_SEGUNDOS),
    }
    return jwt.encode(payload, SECRETO_APP, algorithm=ALGORITMO_JWT)


def validar_token(token: str) -> dict:
    """Valida firma, vencimiento y contenido del JWT."""
    try:
        payload = jwt.decode(
            token,
            SECRETO_APP,
            algorithms=[ALGORITMO_JWT],
            options={"require": ["exp", "iat", "sub"]},
        )
        usuario_id = int(payload["sub"])
        rol = str(payload["rol"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError) as exc:
        raise TokenInvalidoError() from exc

    if usuario_id <= 0:
        raise TokenInvalidoError()

    return {"sub": usuario_id, "rol": rol}
