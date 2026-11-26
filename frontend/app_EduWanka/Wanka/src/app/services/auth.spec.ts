import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { environment } from '../../environments/environment';
import { AuthService } from './auth';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    sessionStorage.clear();
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    sessionStorage.clear();
  });

  it('debería guardar token y usuario tras iniciar sesión', () => {
    const respuesta = {
      token: 'token-de-prueba',
      usuario: {
        id: 3,
        nombre: 'Luis Rodrigo',
        correo: 'luis@edured.pe',
        rol: 'estudiante',
      },
    };

    service.login({ correo: 'luis@edured.pe', password: 'clave-segura-123' }).subscribe();

    const peticion = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    expect(peticion.request.method).toBe('POST');
    peticion.flush(respuesta);

    expect(service.token()).toBe('token-de-prueba');
    expect(service.usuario()?.nombre).toBe('Luis Rodrigo');
  });

  it('debería limpiar la sesión al cerrar', () => {
    service.logout();
    expect(service.token()).toBeNull();
    expect(service.usuario()).toBeNull();
  });
});
