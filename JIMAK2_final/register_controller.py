from database import Database
from tkinter import messagebox

class RegisterController:
    def __init__(self, view):
        self.view = view
        self.db = Database()

    def register(self, form_data):
        """
        Recibe los datos desde el View y ejecuta validaciones + registro.
        form_data = {
            'nombre': str,
            'username': str,
            'email': str,
            'password': str,
            'confirm_password': str,
            'rol': str
        }
        """

        # Validación de campos vacíos
        for key, value in form_data.items():
            if not value.strip():
                messagebox.showerror("Error", f"Por favor complete el campo: {key}")
                return False

        # Validar contraseñas
        if form_data['password'] != form_data['confirm_password']:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return False

        # Preparar datos para la DB
        user_data = {
            'nombre': form_data['nombre'],
            'username': form_data['username'],
            'email': form_data['email'],
            'password': form_data['password'],
            'rol': form_data['rol']
        }

        # Intentar registrar en la base de datos
        if self.db.register_user(user_data):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            self.view.back_to_login()
            return True
        else:
            messagebox.showerror("Error", "Error al registrar usuario")
            return False

    def go_back(self):
        """Callback para botón 'Volver'."""
        self.view.back_to