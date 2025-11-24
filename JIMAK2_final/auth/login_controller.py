from tkinter import messagebox

class LoginController:
    def __init__(self, view, db):
        self.view = view
        self.db = db
        self.view.set_login_callback(self.login)
        self.view.set_open_register_callback(self.open_register)

    def login(self):
        username = self.view.get_username()
        password = self.view.get_password()
        if not username or not password:
            messagebox.showerror('Error', 'Por favor complete todos los campos')
            return
        user = self.db.authenticate_user(username, password)
        if user:
            messagebox.showinfo('Éxito', f"Bienvenido {user.get('nombre')}")
            # Open POS
            from pos.pos_view import POSView
            from pos.pos_controller import POSController
            pos_view = POSView(self.view.root, user, self.db)
            POSController(pos_view, self.db)
        else:
            messagebox.showerror('Error', 'Credenciales incorrectas')

    def open_register(self):
        from auth.register_view import RegisterView
        from auth.register_controller import RegisterController
        rv = RegisterView(self.view.root)
        RegisterController(rv, self.db)
