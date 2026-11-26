import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { AuthService } from '../../services/auth';

type Modo = 'login' | 'registro';

@Component({
  imports: [ReactiveFormsModule],
  selector: 'app-login-componente',
  styleUrl: './login-componente.css',
  templateUrl: './login-componente.html',
})
export class LoginComponente {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);

  protected readonly modo = signal<Modo>('login');
  protected readonly usuario = this.auth.usuario;
  protected readonly procesando = signal(false);
  protected readonly mensaje = signal<string | null>(null);
  protected readonly error = signal<string | null>(null);

  protected readonly formularioLogin = this.fb.nonNullable.group({
    correo: ['', [Validators.required, Validators.email]],
    password: ['', Validators.required],
  });

  protected readonly formularioRegistro = this.fb.nonNullable.group({
    nombre: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(120)]],
    correo: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(128)]],
  });

  protected cambiarModo(modo: Modo): void {
    this.modo.set(modo);
    this.mensaje.set(null);
    this.error.set(null);
  }

  protected campoInvalido(formulario: 'login' | 'registro', campo: string): boolean {
    const control =
      formulario === 'login'
        ? this.formularioLogin.get(campo)
        : this.formularioRegistro.get(campo);
    return !!control && control.invalid && (control.touched || control.dirty);
  }

  protected ingresar(): void {
    if (this.formularioLogin.invalid) {
      this.formularioLogin.markAllAsTouched();
      return;
    }

    this.procesando.set(true);
    this.error.set(null);
    this.auth.login(this.formularioLogin.getRawValue()).subscribe({
      next: (respuesta) => {
        this.procesando.set(false);
        this.mensaje.set(`Bienvenida/o, ${respuesta.usuario.nombre}.`);
        this.formularioLogin.reset({ correo: '', password: '' });
      },
      error: (respuesta: { error?: { detail?: string } }) => {
        this.procesando.set(false);
        this.error.set(respuesta.error?.detail ?? 'No se pudo iniciar sesión.');
      },
    });
  }

  protected registrar(): void {
    if (this.formularioRegistro.invalid) {
      this.formularioRegistro.markAllAsTouched();
      return;
    }

    this.procesando.set(true);
    this.error.set(null);
    this.auth.registrar(this.formularioRegistro.getRawValue()).subscribe({
      next: () => {
        this.procesando.set(false);
        this.formularioRegistro.reset({ nombre: '', correo: '', password: '' });
        this.formularioRegistro.markAsPristine();
        this.formularioRegistro.markAsUntouched();
        this.cambiarModo('login');
        this.mensaje.set('Cuenta creada correctamente. Ya puedes iniciar sesión.');
      },
      error: (respuesta: { error?: { detail?: string } }) => {
        this.procesando.set(false);
        this.error.set(respuesta.error?.detail ?? 'No se pudo crear la cuenta.');
      },
    });
  }

  protected salir(): void {
    this.auth.logout();
    this.mensaje.set('Sesión cerrada.');
  }
}
