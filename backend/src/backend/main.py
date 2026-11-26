"""Punto de entrada de la API EduRed Huancayo (FastAPI + SQL Server)."""

import pyodbc
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.apis.mentorias import router as mentorias_router
from backend.apis.recursos import router as recursos_router
from backend.apis.usuarios import auth_router, router as usuarios_router
from backend.config import CARPETA_SUBIDAS, ORIGENES_FRONTEND
from backend.services.exceptions import (
    CategoriaNotFoundError,
    CredencialesInvalidasError,
    RecursoNotFoundError,
    RolNotFoundError,
    TokenInvalidoError,
    UsuarioAlreadyExistsError,
    UsuarioNotFoundError,
)

app = FastAPI(
    title="EduRed Huancayo API",
    version="1.0.0",
    description="API REST de recursos educativos, usuarios y mentorías con SQL Server.",
)

# Orígenes permitidos del frontend (configurables con ORIGENES_FRONTEND en .env).
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENES_FRONTEND,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir los archivos adjuntos guardados en la carpeta uploads.
app.mount("/uploads", StaticFiles(directory=CARPETA_SUBIDAS), name="uploads")

app.include_router(recursos_router)
app.include_router(usuarios_router)
app.include_router(auth_router)
app.include_router(mentorias_router)


@app.exception_handler(RecursoNotFoundError)
@app.exception_handler(UsuarioNotFoundError)
async def no_encontrado_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(UsuarioAlreadyExistsError)
async def ya_existe_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(CategoriaNotFoundError)
@app.exception_handler(RolNotFoundError)
async def catalogo_invalido_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(CredencialesInvalidasError)
@app.exception_handler(TokenInvalidoError)
async def no_autorizado_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(pyodbc.Error)
async def base_de_datos_handler(request: Request, exc: pyodbc.Error) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "La base de datos no está disponible."},
    )
