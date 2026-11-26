import { Component, afterNextRender, inject, signal } from '@angular/core';

import { environment } from '../../../environments/environment';
import { Recurso } from '../../interface/recurso';
import { RecursoService } from '../../services/recurso';

@Component({
  selector: 'app-documentos-componente',
  styleUrl: './documentos-componente.css',
  templateUrl: './documentos-componente.html',
})
export class DocumentosComponente {
  private readonly recursoService = inject(RecursoService);

  protected readonly recursos = signal<Recurso[]>([]);
  protected readonly cargando = signal(false);
  protected readonly error = signal<string | null>(null);

  constructor() {
    afterNextRender(() => this.cargarRecursos());
  }

  protected cargarRecursos(): void {
    this.cargando.set(true);
    this.error.set(null);

    this.recursoService.listar().subscribe({
      next: (recursos) => {
        this.recursos.set(recursos);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set(
          'No se pudieron cargar los recursos. Verifica que el backend esté en ejecución.',
        );
        this.cargando.set(false);
      },
    });
  }

  protected urlArchivo(ruta: string): string {
    return `${environment.apiUrl}${ruta}`;
  }
}
