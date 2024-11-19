-- Crea la base de datos si no existe
CREATE DATABASE IF NOT EXISTS tareas_db;

-- Usa la base de datos
USE tareas_db;

-- Crea la tabla Usuarios
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,          -- Identificador único para cada usuario
    username VARCHAR(50) NOT NULL UNIQUE,       -- Nombre de usuario único
    password VARCHAR(255) NOT NULL              -- Contraseña (encriptar en la aplicación)
);

-- Crea la tabla Lista_Tareas
CREATE TABLE Lista_Tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,          -- Identificador único para cada tarea
    titulo VARCHAR(255) NOT NULL,               -- Título de la tarea
    descripcion TEXT,                           -- Descripción de la tarea
    fecha_vencimiento DATE,                     -- Fecha de vencimiento de la tarea
    usuario_id INT,                             -- Relaciona la tarea con un usuario
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) 
    ON DELETE CASCADE                           -- Elimina las tareas si se elimina el usuario
);
