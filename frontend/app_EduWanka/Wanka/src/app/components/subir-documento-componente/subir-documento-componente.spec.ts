import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { FormControl } from '@angular/forms';

import { SubirDocumentoComponente, validarArchivo } from './subir-documento-componente';

describe('SubirDocumentoComponente', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubirDocumentoComponente],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
  });

  it('debería crear el componente con el formulario inválido', () => {
    const fixture = TestBed.createComponent(SubirDocumentoComponente);
    const componente = fixture.componentInstance;
    expect(componente).toBeTruthy();
    expect(componente['formulario'].invalid).toBe(true);
  });

  it('debería rechazar un archivo con extensión no permitida', () => {
    const archivo = new File(['contenido'], 'virus.exe', {
      type: 'application/octet-stream',
    });
    expect(validarArchivo(new FormControl(archivo))).toEqual({ extension: true });
  });

  it('debería rechazar un archivo mayor a 10 MB', () => {
    const archivo = new File(['contenido'], 'guia.pdf', { type: 'application/pdf' });
    Object.defineProperty(archivo, 'size', { value: 10 * 1024 * 1024 + 1 });
    expect(validarArchivo(new FormControl(archivo))).toEqual({ tamano: true });
  });

  it('debería aceptar un PDF válido', () => {
    const archivo = new File(['contenido'], 'guia.pdf', { type: 'application/pdf' });
    expect(validarArchivo(new FormControl(archivo))).toBeNull();
  });
});
