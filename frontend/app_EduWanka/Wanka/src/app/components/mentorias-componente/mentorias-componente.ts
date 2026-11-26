import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { MentoriaService } from '../../services/mentoria';
import { AuthService } from '../../services/auth';

@Component({
  imports: [ReactiveFormsModule],
  selector: 'app-mentorias-componente',
  styleUrl: './mentorias-componente.css',
  templateUrl: './mentorias-componente.html',
})
export class MentoriasComponente {
  private readonly fb = inject(FormBuilder);
  private readonly mentoriaService = inject(MentoriaService);
  private readonly auth = inject(AuthService);

  protected readonly enviando = signal(false);
  protected readonly mensaje = signal<string | null>(null);
  protected readonly error = signal<string | null>(null);

  protected readonly formulario = this.fb.nonNullable.group({
    nombreEstudiante: [
      this.auth.usuario()?.nombre ?? '',
      [Validators.required, Validators.minLength(2), Validators.maxLength(120)],
    ],
    tema: [
      '',
      [Validators.required, Validators.minLength(3), Validators.maxLength(200)],
    ],
  });

  protected campoInvalido(nombre: 'nombreEstudiante' | 'tema'): boolean {
    const control = this.formulario.get(nombre);
    return !!control && control.invalid && (control.touched || control.dirty);
  }

  protected enviar(): void {
    if (this.formulario.invalid) {
      this.formulario.markAllAsTouched();
      this.error.set('Completa los campos marcados para enviar la solicitud.');
      return;
    }

    this.enviando.set(true);
    this.mensaje.set(null);
    this.error.set(null);

    this.mentoriaService.crear(this.formulario.getRawValue()).subscribe({
      next: () => {
        this.enviando.set(false);
        this.mensaje.set('Solicitud registrada. Un mentor se pondrá en contacto contigo.');
        this.formulario.controls.tema.reset('');
        this.formulario.markAsPristine();
        this.formulario.markAsUntouched();
      },
      error: (respuesta: { error?: { detail?: string } }) => {
        this.enviando.set(false);
        this.error.set(respuesta.error?.detail ?? 'No se pudo enviar la solicitud.');
      },
    });
  }
}
