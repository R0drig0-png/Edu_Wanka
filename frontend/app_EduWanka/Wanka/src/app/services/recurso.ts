import { HttpClient } from '@angular/common/http';
import { inject, Service } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { Recurso, RecursoCreate, RecursoUpdate } from '../interface/recurso';

@Service()
export class RecursoService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = `${environment.apiUrl}/recursos`;

  listar(): Observable<Recurso[]> {
    return this.http.get<Recurso[]>(this.apiUrl);
  }

  obtener(id: string): Observable<Recurso> {
    return this.http.get<Recurso>(`${this.apiUrl}/${encodeURIComponent(id)}`);
  }

  crear(datos: RecursoCreate, archivo: File | null = null): Observable<Recurso> {
    const formulario = new FormData();
    formulario.append('titulo', datos.titulo);
    formulario.append('categoria', datos.categoria);
    formulario.append('autorFuente', datos.autorFuente);
    formulario.append('descripcion', datos.descripcion);

    if (archivo) {
      formulario.append('archivo', archivo, archivo.name);
    }

    return this.http.post<Recurso>(this.apiUrl, formulario);
  }

  actualizar(id: string, datos: RecursoUpdate): Observable<Recurso> {
    return this.http.put<Recurso>(`${this.apiUrl}/${encodeURIComponent(id)}`, datos);
  }

  eliminar(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${encodeURIComponent(id)}`);
  }
}
