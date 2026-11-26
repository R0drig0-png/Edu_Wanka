import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'inicio' },
  {
    path: 'inicio',
    title: 'Inicio · EduRed Huancayo',
    loadComponent: () =>
      import('./components/inicio-componente/inicio-componente').then(
        (modulo) => modulo.InicioComponente,
      ),
  },
  {
    path: 'documentos',
    title: 'Documentos · EduRed Huancayo',
    loadComponent: () =>
      import('./components/documentos-componente/documentos-componente').then(
        (modulo) => modulo.DocumentosComponente,
      ),
  },
  {
    path: 'subir',
    title: 'Subir documento · EduRed Huancayo',
    loadComponent: () =>
      import('./components/subir-documento-componente/subir-documento-componente').then(
        (modulo) => modulo.SubirDocumentoComponente,
      ),
  },
  {
    path: 'mentorias',
    title: 'Mentorías · EduRed Huancayo',
    loadComponent: () =>
      import('./components/mentorias-componente/mentorias-componente').then(
        (modulo) => modulo.MentoriasComponente,
      ),
  },
  {
    path: 'login',
    title: 'Acceso · EduRed Huancayo',
    loadComponent: () =>
      import('./components/login-componente/login-componente').then(
        (modulo) => modulo.LoginComponente,
      ),
  },
  { path: '**', redirectTo: 'inicio' },
];
