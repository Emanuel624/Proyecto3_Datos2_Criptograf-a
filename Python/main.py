import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import simpledialog

#Importar funciones de otro archivo
from mysql_connector import consultar_usuarios
from mysql_connector import insertar_tarea
from mysql_connector import consultar_tareas_usuario  
from mysql_connector import editar_tarea
from mysql_connector import eliminar_tarea
from mysql_connector import connection 



class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("800x600")
        self.style = ttk.Style(theme="cosmo")

        self.create_login_screen()


    #Ventana de registro de usuarios
    def create_login_screen(self): 
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            main_frame,
            text="Inicio de Sesión",
            font=("Arial", 20),
            bootstyle="primary"
        ).pack(pady=20)

        ttk.Label(main_frame, text="Usuario:", font=("Arial", 12)).pack(pady=5)
        self.username_entry = ttk.Entry(main_frame, width=40)
        self.username_entry.pack(pady=5)

        ttk.Label(main_frame, text="Contraseña:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = ttk.Entry(main_frame, show="*", width=40)
        self.password_entry.pack(pady=5)

        ttk.Button(
            main_frame,
            text="Iniciar Sesión",
            command=self.validate_login,
            bootstyle="success-outline"
        ).pack(pady=20)


    #Valida los datos de inicio de sesion
    def validate_login(self):
        # Obtener credenciales ingresadas por el usuario
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Consultar usuarios desde la base de datos
        usuarios = consultar_usuarios(connection)

        # Verificar si las credenciales coinciden
        for usuario in usuarios:
            if username == usuario[1] and password == usuario[2]:  # Comparar username y password
                self.logged_in_user_id = usuario[0]  # Guardar el ID del usuario conectado
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
                self.create_main_menu()  # Acceso al menú principal
                return

        # Si no se encontró el usuario
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


    #Ventana principal con funcionalidades
    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            main_frame,
            text="Gestor de Tareas",
            font=("Arial", 20),
            bootstyle="primary"
        ).pack(pady=20)

        ttk.Button(
            main_frame,
            text="Crear Tarea",
            command=self.create_task_screen,
            bootstyle="success-outline"
        ).pack(pady=10, fill='x')

        ttk.Button(
            main_frame,
            text="Ver Tareas",
            command=self.view_tasks_screen,
            bootstyle="info-outline"
        ).pack(pady=10, fill='x')

        ttk.Button(
            main_frame,
            text="Actualizar Tarea",
            command=self.update_task_screen,
            bootstyle="warning-outline"
        ).pack(pady=10, fill='x')

        ttk.Button(
            main_frame,
            text="Eliminar Tarea",
            command=self.delete_task_screen,
            bootstyle="danger-outline"
        ).pack(pady=10, fill='x')

        ttk.Button(
            main_frame,
            text="Cerrar Sesión",
            command=self.logout,
            bootstyle="secondary-outline"
        ).pack(pady=10, fill='x')


    #Funcion para cerrar sesion
    def logout(self):
        """Cerrar sesión y regresar a la pantalla de inicio de sesión."""
        self.tasks = []  # Limpiar las tareas, opcional según el caso
        self.create_login_screen()


    #Ventana para añadir una nueva tarea en la base de
    def create_task_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            main_frame,
            text="Crear Nueva Tarea",
            font=("Arial", 18),
            bootstyle="primary"
        ).pack(pady=10)

        ttk.Label(main_frame, text="Título:").pack(pady=5)
        title_entry = ttk.Entry(main_frame, width=40)
        title_entry.pack(pady=5)

        ttk.Label(main_frame, text="Descripción:").pack(pady=5)
        description_entry = ttk.Entry(main_frame, width=40)
        description_entry.pack(pady=5)

        ttk.Label(main_frame, text="Fecha de Vencimiento:").pack(pady=5)
        due_date_entry = ttk.Entry(main_frame, width=40)
        due_date_entry.pack(pady=5)

        ttk.Button(
            main_frame,
            text="Guardar",
            command=lambda: self.save_task(title_entry, description_entry, due_date_entry),
            bootstyle="success-outline"
        ).pack(pady=10)

        ttk.Button(
            main_frame,
            text="Volver al menú",
            command=self.create_main_menu,
            bootstyle="danger-outline"
        ).pack(pady=5)


    #Ventana para Agregar una tarea
    def save_task(self, title_entry, description_entry, due_date_entry):
        # Obtener los valores ingresados
        task_name = title_entry.get()
        description = description_entry.get()
        due_date = due_date_entry.get()

        if task_name and description and due_date:
            try:
                # Insertar la tarea en la base de datos
                insertar_tarea(connection, task_name, description, due_date, self.logged_in_user_id)
                messagebox.showinfo("Éxito", f"Tarea '{task_name}' guardada con éxito")
                self.create_main_menu()  # Regresar al menú principal después de guardar
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la tarea. Error: {e}")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")


    #Ventana para mirar las tareas activas
    def view_tasks_screen(self):
        # Limpiar la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()

        # Crear el marco principal para mostrar las tareas
        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            main_frame,
            text="Tareas Guardadas",
            font=("Arial", 18),
            bootstyle="info"
        ).pack(pady=10)

        # Consultar las tareas del usuario conectado
        tareas = consultar_tareas_usuario(connection, self.logged_in_user_id)

        # Mostrar las tareas sin el ID
        if not tareas:
            ttk.Label(main_frame, text="No hay tareas disponibles.").pack(pady=10)
        else:
            for tarea in tareas:
                ttk.Label(
                    main_frame,
                    text=f"Título: {tarea[1]}, Descripción: {tarea[2]}, Fecha de vencimiento: {tarea[3]}"
                ).pack(pady=5)

        # Botón para regresar al menú principal
        ttk.Button(
            main_frame,
            text="Volver al menú",
            command=self.create_main_menu,
            bootstyle="danger-outline"
        ).pack(pady=20)


    #Ventana para actualizar una tarea
    def update_task_screen(self):
        # Limpiar la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()

        # Crear el marco principal
        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            main_frame,
            text="Actualizar Tarea",
            font=("Arial", 18),
            bootstyle="warning"
        ).pack(pady=10)

        # Consultar las tareas del usuario conectado
        tareas = consultar_tareas_usuario(connection, self.logged_in_user_id)

        # Si no hay tareas disponibles
        if not tareas:
            ttk.Label(main_frame, text="No hay tareas disponibles para actualizar.").pack(pady=10)
            ttk.Button(
                main_frame,
                text="Volver al menú",
                command=self.create_main_menu,
                bootstyle="secondary-outline"
            ).pack(pady=20)
            return

        # Crear una lista desplegable con los títulos de las tareas
        task_titles = {tarea[1]: tarea[0] for tarea in tareas}  # Diccionario {título: id}
        selected_task = ttk.StringVar(value="Selecciona una tarea")

        ttk.Label(main_frame, text="Selecciona la tarea a actualizar:").pack(pady=5)
        task_dropdown = ttk.Combobox(main_frame, textvariable=selected_task, values=list(task_titles.keys()))
        task_dropdown.pack(pady=5)

        ttk.Label(main_frame, text="Nuevo Título:").pack(pady=5)
        new_title_entry = ttk.Entry(main_frame, width=40)
        new_title_entry.pack(pady=5)

        ttk.Label(main_frame, text="Nueva Descripción:").pack(pady=5)
        new_description_entry = ttk.Entry(main_frame, width=40)
        new_description_entry.pack(pady=5)

        ttk.Label(main_frame, text="Nueva Fecha de Vencimiento (YYYY-MM-DD):").pack(pady=5)
        new_due_date_entry = ttk.Entry(main_frame, width=40)
        new_due_date_entry.pack(pady=5)

        # Botón para confirmar la actualización
        def confirm_update():
            task_title = selected_task.get()
            new_title = new_title_entry.get()
            new_description = new_description_entry.get()
            new_due_date = new_due_date_entry.get()

            if task_title in task_titles and new_title and new_description and new_due_date:
                task_id = task_titles[task_title]
                try:
                    editar_tarea(connection, task_id, new_title, new_description, new_due_date)
                    messagebox.showinfo("Éxito", f"Tarea '{task_title}' actualizada con éxito")
                    self.create_main_menu()  # Regresar al menú principal
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar la tarea. Error: {e}")
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios y debes seleccionar una tarea válida")

        ttk.Button(
            main_frame,
            text="Actualizar Tarea",
            command=confirm_update,
            bootstyle="warning-outline"
        ).pack(pady=10)

        ttk.Button(
            main_frame,
            text="Volver al menú",
            command=self.create_main_menu,
            bootstyle="secondary-outline"
        ).pack(pady=20)


    #Ventana para eliminar una tarea.
    def delete_task_screen(self):
        # Limpiar la ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()

        # Crear el marco principal
        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            main_frame,
            text="Eliminar Tarea",
            font=("Arial", 18),
            bootstyle="danger"
        ).pack(pady=10)

        # Consultar las tareas del usuario conectado
        tareas = consultar_tareas_usuario(connection, self.logged_in_user_id)

        # Si no hay tareas disponibles
        if not tareas:
            ttk.Label(main_frame, text="No hay tareas disponibles para eliminar.").pack(pady=10)
            ttk.Button(
                main_frame,
                text="Volver al menú",
                command=self.create_main_menu,
                bootstyle="secondary-outline"
            ).pack(pady=20)
            return

        # Crear una lista desplegable con los títulos de las tareas
        task_titles = {tarea[1]: tarea[0] for tarea in tareas}  # Diccionario {título: id}
        selected_task = ttk.StringVar(value="Selecciona una tarea")

        ttk.Label(main_frame, text="Selecciona la tarea a eliminar:").pack(pady=5)
        task_dropdown = ttk.Combobox(main_frame, textvariable=selected_task, values=list(task_titles.keys()))
        task_dropdown.pack(pady=5)

        # Botón para confirmar la eliminación
        def confirm_delete():
            task_title = selected_task.get()
            if task_title in task_titles:
                task_id = task_titles[task_title]
                try:
                    eliminar_tarea(connection, task_id)
                    messagebox.showinfo("Éxito", f"Tarea '{task_title}' eliminada con éxito")
                    self.create_main_menu()  # Regresar al menú principal
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar la tarea. Error: {e}")
            else:
                messagebox.showerror("Error", "Selecciona una tarea válida")

        ttk.Button(
            main_frame,
            text="Eliminar Tarea",
            command=confirm_delete,
            bootstyle="danger-outline"
        ).pack(pady=10)

        ttk.Button(
            main_frame,
            text="Volver al menú",
            command=self.create_main_menu,
            bootstyle="secondary-outline"
        ).pack(pady=20)


    def prompt_user_input(self, title, prompt):
        input_value = simpledialog.askstring(title, prompt)
        return input_value


if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = TaskManagerApp(root)
    root.mainloop()
