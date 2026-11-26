import { HttpClient } from '@angular/common/http';
import { Service, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { Mentoria, MentoriaCreate } from '../interface/mentoria';

@Service()
export class MentoriaService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = `${environment.apiUrl}/mentorias`;

  listar(): Observable<Mentoria[]> {
    return this.http.get<Mentoria[]>(this.apiUrl);
  }

  crear(datos: MentoriaCreate): Observable<Mentoria> {
    return this.http.post<Mentoria>(this.apiUrl, datos);
  }
}
