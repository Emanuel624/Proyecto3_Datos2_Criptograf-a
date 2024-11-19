import mysql.connector  # Conectar Python con la BD MySQL
import time  # Medir el tiempo de conexiones

# Configuración de la conexión con TLS
start_time = time.time()  # Comienza a medir el tiempo antes de conectar

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ema1234",
    database="tareas_db",
    ssl_ca=r"C:\mysql\ssl\ca-cert.pem",       # Certificado de la CA
    ssl_cert=r"C:\mysql\ssl\client-cert.pem",  # Certificado del cliente 
    ssl_key=r"C:\mysql\ssl\client-key.pem",    # Clave privada del cliente 
    ssl_verify_cert=True                      # Verificar la validez del certificado TLS
)
connection_time = time.time() - start_time  # Calcula el tiempo de conexión
print(f"Tiempo inicial de conexión a la base de datos: {connection_time:.4f} segundos")

# Insertar un nuevo usuario en la BD
def insertar_usuario(connection, username, password):
    start_time = time.time()  # Comienza a medir el tiempo de ejecución
    cursor = connection.cursor()
    query = "INSERT INTO Usuarios (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    connection.commit()
    cursor.close()
    elapsed_time = time.time() - start_time
    print(f"Usuario '{username}' insertado con éxito. Tiempo de ejecución: {elapsed_time:.4f} segundos")

# Consultar usuarios de la BD
def consultar_usuarios(connection):
    start_time = time.time()  # Comienza a medir el tiempo de ejecución
    cursor = connection.cursor()
    query = "SELECT * FROM Usuarios"
    cursor.execute(query)
    usuarios = cursor.fetchall()  # Recupera todos los usuarios
    cursor.close()
    elapsed_time = time.time() - start_time
    print("Usuarios registrados (cargados para validación):")
    for usuario in usuarios:
        print(f"ID: {usuario[0]}, Username: {usuario[1]}")
    print(f"Tiempo de consulta: {elapsed_time:.4f} segundos")
    return usuarios  # Devuelve la lista de usuarios

# Eliminar un usuario de la BD
def eliminar_usuario(connection, user_id):
    start_time = time.time()  # Comienza a medir el tiempo de ejecución
    cursor = connection.cursor()
    query = "DELETE FROM Usuarios WHERE id = %s"
    cursor.execute(query, (user_id,))
    connection.commit()
    cursor.close()
    elapsed_time = time.time() - start_time
    print(f"Usuario con ID {user_id} eliminado con éxito. Tiempo de ejecución: {elapsed_time:.4f} segundos")

# Insertar tarea a un usuario en la BD
def insertar_tarea(connection, titulo, descripcion, fecha_vencimiento, usuario_id):
    start_time = time.time()  # Comienza a medir el tiempo de ejecución
    cursor = connection.cursor()
    query = """
        INSERT INTO Lista_Tareas (titulo, descripcion, fecha_vencimiento, usuario_id)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (titulo, descripcion, fecha_vencimiento, usuario_id))
    connection.commit()
    cursor.close()
    elapsed_time = time.time() - start_time
    print(f"Tarea '{titulo}' insertada con éxito. Tiempo de ejecución: {elapsed_time:.4f} segundos")

# Consultar tareas de un usuario a la BD
def consultar_tareas_usuario(connection, usuario_id):
    start_time = time.time()  # Comienza a medir el tiempo de ejecución
    cursor = connection.cursor()
    query = "SELECT * FROM Lista_Tareas WHERE usuario_id = %s"
    cursor.execute(query, (usuario_id,))
    tareas = cursor.fetchall()
    cursor.close()
    elapsed_time = time.time() - start_time
    print(f"Tareas del usuario con ID {usuario_id}:")
    for tarea in tareas:
        print(f"ID: {tarea[0]}, Título: {tarea[1]}, Descripción: {tarea[2]}, Fecha de vencimiento: {tarea[3]}")
    print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")
    return tareas

#Funcion para editar una tarea ya existente
def editar_tarea(connection, tarea_id, nuevo_titulo, nueva_descripcion, nueva_fecha_vencimiento):
    """
    Edita una tarea en la base de datos.
    """
    start_time = time.time()  # Comienza a medir el tiempo de ejecución
    cursor = connection.cursor()
    query = """
        UPDATE Lista_Tareas
        SET titulo = %s, descripcion = %s, fecha_vencimiento = %s
        WHERE id = %s
    """
    cursor.execute(query, (nuevo_titulo, nueva_descripcion, nueva_fecha_vencimiento, tarea_id))
    connection.commit()
    cursor.close()
    elapsed_time = time.time() - start_time
    print(f"Tarea con ID {tarea_id} editada con éxito. Tiempo de ejecución: {elapsed_time:.4f} segundos")

# Eliminar tareas de un usuario de la BD
def eliminar_tarea(connection, tarea_id):
    start_time = time.time()  # Comienza a medir el tiempo de ejecución
    cursor = connection.cursor()
    query = "DELETE FROM Lista_Tareas WHERE id = %s"
    cursor.execute(query, (tarea_id,))
    connection.commit()
    cursor.close()
    elapsed_time = time.time() - start_time
    print(f"Tarea con ID {tarea_id} eliminada con éxito. Tiempo de ejecución: {elapsed_time:.4f} segundos")
