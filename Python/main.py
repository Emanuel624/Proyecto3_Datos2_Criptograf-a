import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import simpledialog

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("800x600")
        self.style = ttk.Style(theme="cosmo")

        # Simulación de base de datos
        self.tasks = []

        self.valid_username = "admin"
        self.valid_password = "1234"

        self.create_login_screen()

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

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == self.valid_username and password == self.valid_password:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

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

    def logout(self):
        """Cerrar sesión y regresar a la pantalla de inicio de sesión."""
        self.tasks = []  # Limpiar las tareas, opcional según el caso
        self.create_login_screen()

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

    def save_task(self, title_entry, description_entry, due_date_entry):
        task_name = title_entry.get()
        description = description_entry.get()
        due_date = due_date_entry.get()

        if task_name and description and due_date:
            self.tasks.append({
                "name": task_name,
                "description": description,
                "due_date": due_date
            })
            messagebox.showinfo("Éxito", f"Tarea '{task_name}' guardada con éxito")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def view_tasks_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            main_frame,
            text="Tareas Guardadas",
            font=("Arial", 18),
            bootstyle="info"
        ).pack(pady=10)

        if not self.tasks:
            ttk.Label(main_frame, text="No hay tareas disponibles.").pack(pady=10)
        else:
            for task in self.tasks:
                ttk.Label(main_frame, text=f"{task['name']} - {task['due_date']}").pack(pady=5)

        ttk.Button(
            main_frame,
            text="Volver al menú",
            command=self.create_main_menu,
            bootstyle="danger-outline"
        ).pack(pady=20)

    def update_task_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            main_frame,
            text="Actualizar Tarea",
            font=("Arial", 18),
            bootstyle="warning"
        ).pack(pady=10)

        task_name = self.prompt_user_input("Actualizar Tarea", "Ingresa el nombre de la tarea a actualizar:")

        if task_name in [task['name'] for task in self.tasks]:
            new_name = self.prompt_user_input("Actualizar Tarea", "Ingresa el nuevo nombre de la tarea:")
            for task in self.tasks:
                if task['name'] == task_name:
                    task['name'] = new_name
            messagebox.showinfo("Éxito", f"Tarea '{task_name}' actualizada a '{new_name}'")
        else:
            messagebox.showerror("Error", "Tarea no encontrada.")

        ttk.Button(
            main_frame,
            text="Volver al menú",
            command=self.create_main_menu,
            bootstyle="danger-outline"
        ).pack(pady=20)

    def delete_task_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            main_frame,
            text="Eliminar Tarea",
            font=("Arial", 18),
            bootstyle="danger"
        ).pack(pady=10)

        task_name = self.prompt_user_input("Eliminar Tarea", "Ingresa el nombre de la tarea a eliminar:")

        if task_name in [task['name'] for task in self.tasks]:
            self.tasks = [task for task in self.tasks if task['name'] != task_name]
            messagebox.showinfo("Éxito", f"Tarea '{task_name}' eliminada.")
        else:
            messagebox.showerror("Error", "Tarea no encontrada.")

        ttk.Button(
            main_frame,
            text="Volver al menú",
            command=self.create_main_menu,
            bootstyle="danger-outline"
        ).pack(pady=20)

    def prompt_user_input(self, title, prompt):
        input_value = simpledialog.askstring(title, prompt)
        return input_value


if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = TaskManagerApp(root)
    root.mainloop()
