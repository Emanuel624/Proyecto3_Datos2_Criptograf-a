-- Crea la base de datos si no existe
CREATE DATABASE IF NOT EXISTS tareas_db;

-- Usa la base de datos
USE tareas_db;

-- Crea la tabla Lista_Tareas
CREATE TABLE Lista_Tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- Identificador único para cada tarea
    titulo VARCHAR(255) NOT NULL,             -- Título de la tarea
    descripcion TEXT,                         -- Descripción de la tarea
    fecha_vencimiento DATE                    -- Fecha de vencimiento de la tarea
);
