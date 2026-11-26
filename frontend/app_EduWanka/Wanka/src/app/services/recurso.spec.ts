import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { environment } from '../../environments/environment';
import { Recurso } from '../interface/recurso';
import { RecursoService } from './recurso';

describe('RecursoService', () => {
  let service: RecursoService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(RecursoService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('debería crearse', () => {
    expect(service).toBeTruthy();
  });

  it('debería listar los recursos del backend', () => {
    const esperado: Recurso[] = [
      {
        id: 1,
        titulo: 'Guía de Álgebra',
        categoria: 'Matematicas',
        autorFuente: 'Elaboración propia',
        descripcion: 'Guía de estudio.',
        archivoUrl: null,
      },
    ];

    service.listar().subscribe((recursos) => expect(recursos).toEqual(esperado));

    const peticion = httpMock.expectOne(`${environment.apiUrl}/recursos`);
    expect(peticion.request.method).toBe('GET');
    peticion.flush(esperado);
  });

  it('debería crear un recurso enviando FormData sin ID del cliente', () => {
    service
      .crear({
        titulo: 'Resumen de Algoritmos',
        categoria: 'Programacion',
        autorFuente: 'Elaboración propia',
        descripcion: 'Repaso de algoritmos.',
      })
      .subscribe();

    const peticion = httpMock.expectOne(`${environment.apiUrl}/recursos`);
    expect(peticion.request.method).toBe('POST');
    expect(peticion.request.body instanceof FormData).toBe(true);
    expect((peticion.request.body as FormData).has('id')).toBe(false);
    peticion.flush({
      id: 2,
      titulo: 'Resumen de Algoritmos',
      categoria: 'Programacion',
      autorFuente: 'Elaboración propia',
      descripcion: 'Repaso de algoritmos.',
      archivoUrl: null,
    });
  });
});
