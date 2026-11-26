# EduRed Huancayo (frontend)

Aplicación Angular 22 (standalone + SSR) para el catálogo de recursos educativos de
EduRed Huancayo. Usa Bootstrap 5.3 y Bootstrap Icons cargados desde CDN en
`src/index.html`.

## Requisitos

- Node.js y npm (el proyecto usa `npm@12.2.1`).
- Backend FastAPI en `http://127.0.0.1:8000` (ver `backend/README.md`).

## Comandos

```powershell
npm install
npm start                        # http://localhost:4200
npm test -- --watch=false
npm run build                    # genera dist/app_EduWanka y prerenderiza 5 rutas
npm run serve:ssr:app_EduWanka   # Express, http://localhost:4000
```

## Estructura

```
src/app/
  components/            inicio, documentos, subir-documento, mentorías, login, header, footer
  interceptors/          auth.interceptor.ts (cabecera Bearer)
  interface/             Recurso, Usuario, Mentoria
  services/              recurso, auth, mentoria
  app.routes.ts          rutas lazy
  app.config.ts          HttpClient + interceptor + router + hidratación SSR
src/environments/        apiUrl (development / production)
```

## Funcionalidades

- **Inicio:** presentación y accesos a documentos y subida.
- **Documentos:** lista desde `GET /recursos`, estados de carga/error y descarga del adjunto.
- **Subir documento:** Reactive Forms con validación de título, categoría, autoría y
  archivo (extensión, MIME y máximo 10 MB); envía `multipart/form-data`.
- **Mentorías:** formulario validado que envía `POST /mentorias`.
- **Acceso:** registro, inicio de sesión y cierre de sesión contra `/usuarios` y
  `/auth/login`; el **JWT** se guarda en `sessionStorage` y se adjunta automáticamente
  como `Bearer` a las peticiones. Las contraseñas se hashean con Argon2 en el backend.

## Notas

- Los valores del selector de categoría (`Programacion`, `BaseDeDatos`, `Matematicas`,
  `Comunicacion`) deben coincidir con los sembrados en `backend/sql/schema.sql`.
- `apiUrl` está fijo a `127.0.0.1:8000` en ambos environment; ajustarlo al desplegar.
- Criterio ético 7.3: la fuente/autoría es obligatoria y las herramientas externas se
  citan en el pie de página.
