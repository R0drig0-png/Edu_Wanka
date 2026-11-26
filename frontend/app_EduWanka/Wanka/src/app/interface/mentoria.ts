export interface MentoriaCreate {
  nombreEstudiante: string;
  tema: string;
}

export interface Mentoria extends MentoriaCreate {
  id: number;
  atendida: boolean;
  fechaSolicitud: string;
}
