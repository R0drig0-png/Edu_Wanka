import { HttpInterceptorFn } from '@angular/common/http';

import { environment } from '../../environments/environment';

/** Adjunta el token de sesion a todas las peticiones de la API. */
export const authInterceptor: HttpInterceptorFn = (peticion, siguiente) => {
  const token =
    typeof sessionStorage === 'undefined'
      ? null
      : sessionStorage.getItem('edured_token');

  if (!token || !peticion.url.startsWith(environment.apiUrl)) {
    return siguiente(peticion);
  }

  return siguiente(
    peticion.clone({ setHeaders: { Authorization: `Bearer ${token}` } }),
  );
};
