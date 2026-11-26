export interface Recurso {
  id: number;
  titulo: string;
  categoria: string;
  autorFuente: string;
  descripcion: string;
  archivoUrl: string | null;
}

export interface RecursoCreate {
  titulo: string;
  categoria: string;
  autorFuente: string;
  descripcion: string;
}

export interface RecursoUpdate {
  titulo: string;
  categoria: string;
  autorFuente: string;
  descripcion: string;
}
