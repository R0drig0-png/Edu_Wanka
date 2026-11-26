export interface Usuario {
  id: number;
  nombre: string;
  correo: string;
  rol: string;
}

export interface RegistroUsuario {
  nombre: string;
  correo: string;
  password: string;
}

export interface Credenciales {
  correo: string;
  password: string;
}

export interface RespuestaLogin {
  token: string;
  usuario: Usuario;
}
