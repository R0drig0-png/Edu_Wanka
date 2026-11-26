import { Component, ElementRef, inject, signal, viewChild } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormControl,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn,
  Validators,
} from '@angular/forms';

import { RecursoService } from '../../services/recurso';

const EXTENSIONES_PERMITIDAS = new Set(['.pdf', '.doc', '.docx', '.ppt', '.pptx']);
const TIPOS_PERMITIDOS = new Set([
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.ms-powerpoint',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  'application/octet-stream',
]);
const TAMANO_MAXIMO = 10 * 1024 * 1024;

/** Validador custom del adjunto: extension, tipo MIME y tamaño. */
export const validarArchivo: ValidatorFn = (
  control: AbstractControl,
): ValidationErrors | null => {
  const archivo = control.value as File | null;
  if (!archivo) {
    return null;
  }

  const nombre = archivo.name.toLowerCase();
  const indicePunto = nombre.lastIndexOf('.');
  const extension = indicePunto >= 0 ? nombre.slice(indicePunto) : '';

  if (!EXTENSIONES_PERMITIDAS.has(extension)) {
    return { extension: true };
  }
  if (archivo.type && !TIPOS_PERMITIDOS.has(archivo.type)) {
    return { tipo: true };
  }
  if (archivo.size > TAMANO_MAXIMO) {
    return { tamano: true };
  }
  return null;
};

@Component({
  imports: [ReactiveFormsModule],
  selector: 'app-subir-documento-componente',
  styleUrl: './subir-documento-componente.css',
  templateUrl: './subir-documento-componente.html',
})
export class SubirDocumentoComponente {
  private readonly fb = inject(FormBuilder);
  private readonly recursoService = inject(RecursoService);
  private readonly archivoInput = viewChild<ElementRef<HTMLInputElement>>('archivoInput');

  protected readonly guardando = signal(false);
  protected readonly mensaje = signal<string | null>(null);
  protected readonly errorSubida = signal<string | null>(null);
  protected readonly nombreArchivo = signal<string | null>(null);

  protected readonly formulario = this.fb.nonNullable.group({
    titulo: [
      '',
      [Validators.required, Validators.minLength(3), Validators.maxLength(100)],
    ],
    categoria: ['', Validators.required],
    autorFuente: ['', [Validators.required, Validators.maxLength(150)]],
    descripcion: ['', Validators.maxLength(500)],
    archivo: new FormControl<File | null>(null, {
      nonNullable: true,
      validators: [validarArchivo],
    }),
  });

  protected onArchivoSeleccionado(evento: Event): void {
    const input = evento.target as HTMLInputElement;
    const archivo = input.files?.[0] ?? null;
    this.formulario.controls.archivo.setValue(archivo);
    this.formulario.controls.archivo.markAsTouched();
    this.nombreArchivo.set(archivo?.name ?? null);
  }

  protected campoInvalido(nombre: string): boolean {
    const control = this.formulario.get(nombre);
    return !!control && control.invalid && (control.touched || control.dirty);
  }

  protected subir(): void {
    if (this.formulario.invalid) {
      this.formulario.markAllAsTouched();
      this.errorSubida.set('Revisa los campos marcados antes de publicar.');
      return;
    }

    const { archivo, ...datos } = this.formulario.getRawValue();
    this.guardando.set(true);
    this.mensaje.set(null);
    this.errorSubida.set(null);

    this.recursoService.crear(datos, archivo).subscribe({
      next: () => {
        this.guardando.set(false);
        this.mensaje.set('Documento publicado correctamente.');
        this.formulario.reset({
          titulo: '',
          categoria: '',
          autorFuente: '',
          descripcion: '',
          archivo: null,
        });
        this.formulario.markAsPristine();
        this.formulario.markAsUntouched();
        this.nombreArchivo.set(null);

        const input = this.archivoInput()?.nativeElement;
        if (input) {
          input.value = '';
        }
      },
      error: (respuesta: { error?: { detail?: string } }) => {
        this.guardando.set(false);
        this.errorSubida.set(
          respuesta.error?.detail ?? 'No se pudo publicar el documento. Intenta nuevamente.',
        );
      },
    });
  }
}
