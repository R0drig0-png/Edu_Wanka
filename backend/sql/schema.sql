/*
 * EduRed Huancayo - esquema de base de datos (SQL Server).
 * Normalizado hasta 3FN: los dominios repetidos (categorias y roles) se
 * guardan en tablas catalogo y se referencian con claves foraneas.
 * Este script reconstruye el esquema; ejecutarlo con:
 *   sqlcmd -S localhost -U sa -P <password> -i sql/schema.sql
 */

IF DB_ID('EduRedHuancayo') IS NULL
BEGIN
    CREATE DATABASE EduRedHuancayo;
END;
GO

USE EduRedHuancayo;
GO

DROP TABLE IF EXISTS dbo.Recursos;
DROP TABLE IF EXISTS dbo.Mentorias;
DROP TABLE IF EXISTS dbo.Usuarios;
DROP TABLE IF EXISTS dbo.Categorias;
DROP TABLE IF EXISTS dbo.Roles;
GO

CREATE TABLE dbo.Roles (
    id_rol INT IDENTITY(1, 1) PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL UNIQUE
);
GO

CREATE TABLE dbo.Categorias (
    id_categoria INT IDENTITY(1, 1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL UNIQUE
);
GO

CREATE TABLE dbo.Usuarios (
    id INT IDENTITY(1, 1) PRIMARY KEY,
    nombre NVARCHAR(120) NOT NULL,
    correo NVARCHAR(150) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    id_rol INT NOT NULL CONSTRAINT FK_Usuarios_Roles REFERENCES dbo.Roles(id_rol),
    fecha_registro DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    activo BIT NOT NULL DEFAULT 1
);
GO

CREATE TABLE dbo.Recursos (
    id INT IDENTITY(1, 1) PRIMARY KEY,
    titulo NVARCHAR(200) NOT NULL,
    descripcion NVARCHAR(MAX) NULL,
    id_categoria INT NOT NULL CONSTRAINT FK_Recursos_Categorias REFERENCES dbo.Categorias(id_categoria),
    autor_fuente NVARCHAR(150) NULL,
    archivo_url NVARCHAR(500) NULL,
    id_usuario INT NULL CONSTRAINT FK_Recursos_Usuarios REFERENCES dbo.Usuarios(id),
    fecha_publicacion DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

CREATE TABLE dbo.Mentorias (
    id INT IDENTITY(1, 1) PRIMARY KEY,
    nombre_estudiante NVARCHAR(120) NOT NULL,
    tema NVARCHAR(200) NOT NULL,
    id_usuario INT NULL CONSTRAINT FK_Mentorias_Usuarios REFERENCES dbo.Usuarios(id),
    atendida BIT NOT NULL DEFAULT 0,
    fecha_solicitud DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

CREATE INDEX IX_Recursos_Categoria ON dbo.Recursos(id_categoria);
GO

/* Catalogos: los valores deben coincidir con el select del frontend. */
INSERT INTO dbo.Roles (nombre) VALUES (N'estudiante'), (N'docente'), (N'administrador');
INSERT INTO dbo.Categorias (nombre)
VALUES (N'Programacion'), (N'BaseDeDatos'), (N'Matematicas'), (N'Comunicacion');
GO

/* Consulta de verificacion */
SELECT r.id, r.titulo, c.nombre AS categoria, r.autor_fuente, r.archivo_url
FROM dbo.Recursos AS r
INNER JOIN dbo.Categorias AS c ON c.id_categoria = r.id_categoria;
GO
