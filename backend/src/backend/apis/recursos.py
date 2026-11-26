"""Rutas HTTP del catalogo de recursos educativos."""

from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from backend.config import CARPETA_SUBIDAS, MAX_TAMANO_ARCHIVO
from backend.schemas.recursos import Recurso, RecursoCreate, RecursoUpdate
from backend.services.recursos import RecursoService, recurso_service

router = APIRouter(prefix="/recursos", tags=["recursos"])

EXTENSIONES_PERMITIDAS = {".pdf", ".doc", ".docx", ".ppt", ".pptx"}
TIPOS_PERMITIDOS = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/octet-stream",
}
TAMANO_BLOQUE = 1024 * 1024


def get_recurso_service() -> RecursoService:
    return recurso_service


ServiceDep = Annotated[RecursoService, Depends(get_recurso_service)]


async def guardar_archivo(archivo: UploadFile) -> str:
    """Valida el adjunto, lo guarda en disco y devuelve su ruta publica."""
    nombre_original = Path(archivo.filename or "").name
    extension = Path(nombre_original).suffix.lower()

    if extension not in EXTENSIONES_PERMITIDAS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Formato de archivo no permitido. "
                f"Usa uno de: {', '.join(sorted(EXTENSIONES_PERMITIDAS))}."
            ),
        )

    tipo = (archivo.content_type or "").split(";")[0].strip().lower()
    if tipo not in TIPOS_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El tipo MIME del archivo no corresponde a un documento permitido.",
        )

    contenido = bytearray()
    while bloque := await archivo.read(TAMANO_BLOQUE):
        contenido.extend(bloque)
        if len(contenido) > MAX_TAMANO_ARCHIVO:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="El archivo supera el tamaño máximo de 10 MB.",
            )

    CARPETA_SUBIDAS.mkdir(parents=True, exist_ok=True)
    nombre_guardado = f"{uuid4().hex}{extension}"
    (CARPETA_SUBIDAS / nombre_guardado).write_bytes(contenido)

    return f"/uploads/{nombre_guardado}"


@router.get("", response_model=list[Recurso], summary="Listar recursos educativos")
def listar_recursos(service: ServiceDep) -> list[Recurso]:
    return service.listar()


@router.get("/{id}", response_model=Recurso, summary="Obtener un recurso por ID")
def obtener_recurso(id: int, service: ServiceDep) -> Recurso:
    return service.obtener(id)


@router.post(
    "",
    response_model=Recurso,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un recurso",
)
async def crear_recurso(
    service: ServiceDep,
    titulo: str = Form(..., min_length=1, max_length=100),
    categoria: str = Form(..., min_length=1, max_length=100),
    autor_fuente: str = Form("", alias="autorFuente", max_length=150),
    descripcion: str = Form("", max_length=500),
    archivo: UploadFile | None = File(default=None),
) -> Recurso:
    archivo_url = await guardar_archivo(archivo) if archivo is not None else None

    datos = RecursoCreate(
        titulo=titulo,
        categoria=categoria,
        autor_fuente=autor_fuente,
        descripcion=descripcion,
        archivo_url=archivo_url,
    )
    return service.crear(datos)


@router.put("/{id}", response_model=Recurso, summary="Actualizar un recurso")
def actualizar_recurso(
    id: int, datos: RecursoUpdate, service: ServiceDep
) -> Recurso:
    return service.actualizar(id, datos)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un recurso",
)
def eliminar_recurso(id: int, service: ServiceDep) -> None:
    service.eliminar(id)
