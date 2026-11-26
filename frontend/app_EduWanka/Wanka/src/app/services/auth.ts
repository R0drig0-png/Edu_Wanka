import { HttpClient } from '@angular/common/http';
import { Service, inject, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';

import { environment } from '../../environments/environment';
import {
  Credenciales,
  RegistroUsuario,
  RespuestaLogin,
  Usuario,
} from '../interface/usuario';

const CLAVE_TOKEN = 'edured_token';
const CLAVE_USUARIO = 'edured_usuario';

@Service()
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  readonly usuario = signal<Usuario | null>(this.leerUsuario());

  registrar(datos: RegistroUsuario): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.apiUrl}/usuarios`, datos);
  }

  login(credenciales: Credenciales): Observable<RespuestaLogin> {
    return this.http
      .post<RespuestaLogin>(`${this.apiUrl}/auth/login`, credenciales)
      .pipe(
        tap((respuesta) => {
          const almacen = this.almacenamiento();
          if (almacen) {
            almacen.setItem(CLAVE_TOKEN, respuesta.token);
            almacen.setItem(CLAVE_USUARIO, JSON.stringify(respuesta.usuario));
          }
          this.usuario.set(respuesta.usuario);
        }),
      );
  }

  logout(): void {
    const almacen = this.almacenamiento();
    if (almacen) {
      almacen.removeItem(CLAVE_TOKEN);
      almacen.removeItem(CLAVE_USUARIO);
    }
    this.usuario.set(null);
  }

  token(): string | null {
    return this.almacenamiento()?.getItem(CLAVE_TOKEN) ?? null;
  }

  private almacenamiento(): Storage | null {
    return typeof sessionStorage === 'undefined' ? null : sessionStorage;
  }

  private leerUsuario(): Usuario | null {
    const datos = this.almacenamiento()?.getItem(CLAVE_USUARIO);
    if (!datos) {
      return null;
    }
    try {
      return JSON.parse(datos) as Usuario;
    } catch {
      return null;
    }
  }
}
