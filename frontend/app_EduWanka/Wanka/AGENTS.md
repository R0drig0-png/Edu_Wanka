# AGENTS.md

## Layout

Two independent apps under one workspace root; there is no root `package.json`, Makefile, or task runner. Run commands from the app directory.

- `backend/` — FastAPI + SQL Server, `uv` project, `src/backend/` layout.
- `frontend/app_EduWanka/Wanka/` — Angular 22 standalone app with SSR (Express).
- Git: the root `.git` currently tracks **no files**. `backend/` and `frontend/app_EduWanka/Wanka/` are separate nested repos (the latter has a GitHub origin). Commit inside the repo you edited; adding these paths at the root records broken gitlinks instead of code.

## Commands

```powershell
cd frontend/app_EduWanka/Wanka
npm install
npm start                                              # ng serve, http://localhost:4200
npm test -- --watch=false                              # Vitest via @angular/build:unit-test
npm run build                                          # production SSR build; prerenders 5 routes
npm run serve:ssr:app_EduWanka                         # Express on PORT, default 4000
npx prettier --write src                               # no npm script for Prettier
```

- Build output is `dist/app_EduWanka/` (not `dist/Wanka`): the Angular project is named `app_EduWanka` in `angular.json`.
- Bootstrap 5.3 and Bootstrap Icons are loaded from CDN in `src/index.html`. Don't add them as npm dependencies or move those tags into component styles. The build prints "Unable to locate stylesheet" warnings for those CDN links; they are harmless.

## Architecture

- `src/app/app.routes.ts` has five lazy routes: `/inicio`, `/documentos`, `/subir`, `/mentorias`, `/login`. `app.html` renders Header, `<router-outlet>` and Footer inside a flex column.
- Feature components live under `src/app/components/<nombre>-componente/` with no `.component` suffix in filenames (e.g. `subir-documento-componente`). Keep Spanish identifiers, messages and comments.
- Forms are **Reactive Forms** (`ReactiveFormsModule`) with `Validators` and a custom file validator in `subir-documento-componente.ts`. Bootstrap `is-invalid` + `invalid-feedback` blocks show errors.
- `services/recurso.ts`, `services/auth.ts` and `services/mentoria.ts` use `HttpClient` against `${environment.apiUrl}`. `app.config.ts` registers `withFetch()` and `authInterceptor`, which adds the Bearer token from `sessionStorage`.
- `AuthService` stores the JWT (HS256, issued by the backend) and user in `sessionStorage` and exposes a `usuario` signal. `LoginComponente` supports login, registration and logout (server always assigns `estudiante`).
- IDs come from SQL Server as numbers; the frontend never sends an `id` on creation.
- HTTP calls run inside `afterNextRender` in `DocumentosComponente` so SSR prerender does not need the backend. Avoid touching `sessionStorage`/`document` during SSR; use `DOCUMENT` injection or guard with `typeof sessionStorage === 'undefined'`.
- `src/environments/environment*.ts` point to `http://127.0.0.1:8000`. Backend CORS allows `http://localhost:4200` and `http://127.0.0.1:4200` by default.
