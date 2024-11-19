USE tareas_db;

-- Inserta usuarios en la tabla Usuarios
INSERT INTO Usuarios (username, password)
VALUES
    ('Admin', '1234'),
    ('Usuario1', 'aeiou');

-- Inserta tareas vinculadas a los usuarios en la tabla Lista_Tareas
INSERT INTO Lista_Tareas (titulo, descripcion, fecha_vencimiento, usuario_id)
VALUES
    -- Tareas del usuario Admin
    ('Estudio semana 19', 'Estudiar Fisica2', '2023-12-01', 1),  -- Admin tiene ID 1
    ('Preparar informe', 'Completar informe semanal', '2024-01-10', 1),

    -- Tareas del usuario Usuario1
    ('Compra comestible', 'Comprar en Walmart mejores precios', '2024-01-15', 2),  -- Usuario1 tiene ID 2
    ('Llamar a soporte', 'Contactar soporte técnico por el servicio', '2023-11-20', 2);
