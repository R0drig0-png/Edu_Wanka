"""Configuracion compartida del backend."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Cargar variables de entorno desde .env (ubicado en la raiz del backend)
_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_ENV_PATH)

# Carpeta donde se guardan los archivos adjuntos subidos por los usuarios.
CARPETA_SUBIDAS = Path(__file__).resolve().parents[2] / "uploads"
CARPETA_SUBIDAS.mkdir(parents=True, exist_ok=True)

# Tamano maximo de un adjunto (10 MB), coherente con el mensaje del frontend.
MAX_TAMANO_ARCHIVO = 10 * 1024 * 1024

# Secreto para firmar los tokens de sesion. En produccion debe definirse en .env.
SECRETO_APP = os.getenv("SECRETO_APP", "edured-desarrollo-cambiar-este-valor")

# Origenes permitidos por CORS (separados por comas).
ORIGENES_FRONTEND = [
    origen.strip()
    for origen in os.getenv(
        "ORIGENES_FRONTEND",
        "http://localhost:4200,http://127.0.0.1:4200",
    ).split(",")
    if origen.strip()
]
