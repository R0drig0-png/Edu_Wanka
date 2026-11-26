# Backend EduRed Huancayo

API REST construida con FastAPI y SQL Server para el catálogo de recursos educativos,
el registro/acceso de usuarios y las solicitudes de mentoría.

## Estructura

```
src/backend/
  apis/          rutas HTTP (recursos, usuarios/auth, mentorías)
  schemas/       modelos Pydantic de request/response
  services/      reglas de negocio, excepciones, Argon2 y JWT
  repositories/  consultas parametrizadas a SQL Server
  database.py    fábrica de conexiones pyodbc
  main.py        configuración de la app y manejo de errores
sql/schema.sql   esquema normalizado (3FN) y catálogos semilla
tests/           pruebas unitarias sin base de datos
uploads/         adjuntos (ignorado por Git)
```

## Puesta en marcha

1. Instalar dependencias: `uv sync`.
2. Crear la base de datos con `sql/schema.sql` (desde `sqlcmd` o SQL Server Management
   Studio). El script crea `EduRedHuancayo`, las tablas `Roles`, `Categorias`,
   `Usuarios`, `Recursos` y `Mentorias`, y siembra los catálogos.
3. Copiar/ajustar `.env`:

   ```env
   DB_DRIVER=ODBC Driver 17 for SQL Server
   DB_SERVER=localhost
   DB_DATABASE=EduRedHuancayo
   DB_USER=sa
   DB_PASSWORD=<tu-password>
   SECRETO_APP=<secreto-largo-para-firmar-tokens>
   ORIGENES_FRONTEND=http://localhost:4200,http://127.0.0.1:4200
   ```

4. Ejecutar: `uv run uvicorn backend.main:app --app-dir src --reload`.
5. Documentación interactiva: http://127.0.0.1:8000/docs.

Si Windows bloquea `.venv`, usar `$env:UV_PROJECT_ENVIRONMENT=".venv2"` antes de
`uv sync` y del comando de arranque.

## Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/recursos` | Lista recursos |
| POST | `/recursos` | Crea recurso (multipart/form-data, adjunto opcional) |
| GET/PUT/DELETE | `/recursos/{id}` | Consulta, actualiza o elimina |
| POST | `/usuarios` | Registro (siempre rol `estudiante`) |
| POST | `/auth/login` | Login, devuelve token Bearer y usuario |
| GET | `/auth/me` | Usuario autenticado |
| GET/POST | `/mentorias` | Lista / crea solicitudes de mentoría |

## Seguridad

- Las contraseñas se almacenan como hashes **Argon2id** (`argon2-cffi`), nunca en texto
  plano; `verificar_password` usa la comparación segura de la biblioteca.
- El login devuelve un **JWT HS256** (`PyJWT`) con `sub`, `rol`, `iat` y `exp` (8 horas).
  Enviarlo como `Authorization: Bearer <token>` en `/auth/me` y rutas protegidas.
- `SECRETO_APP` firma los tokens: usa un valor largo y aleatorio en producción (por
  ejemplo, generado con `python -c "import secrets; print(secrets.token_urlsafe(48))"`).
- El frontend guarda el JWT en `sessionStorage` y lo adjunta con un interceptor.

## Pruebas

```powershell
uv run python -m unittest discover -s tests -v
```

Las pruebas usan repositorios falsos, por lo que no requieren SQL Server en marcha.
