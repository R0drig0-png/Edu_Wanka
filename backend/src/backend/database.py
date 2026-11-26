"""Gestión de la conexión a SQL Server mediante pyodbc."""

import os

import pyodbc
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_DATABASE = os.getenv("DB_DATABASE", "EduRedHuancayo")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

CONNECTION_STRING = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_DATABASE};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    "TrustServerCertificate=yes;"
)


def obtener_conexion() -> pyodbc.Connection:
    """Abre y devuelve una nueva conexión a SQL Server."""
    return pyodbc.connect(CONNECTION_STRING)
