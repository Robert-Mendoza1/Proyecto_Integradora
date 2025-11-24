from tkinter import messagebox

class RegisterController:
    def __init__(self, view, db):
        self.view = view
        self.db = db
        self.view.set_save_callback(self.save)

    def save(self):
        data = self.view.get_form_data()
        required = ['nombre','username','email','password','confirm_password']
        for r in required:
            if not data.get(r):
                self.view.show_error(f'Por favor complete el campo: {r}')
                return
        if data['password'] != data['confirm_password']:
            self.view.show_error('Las contraseñas no coinciden')
            return
        user_data = {'nombre': data['nombre'], 'username': data['username'], 'email': data['email'], 'password': data['password'], 'rol': self.view.get_role()}
        ok = self.db.register_user(user_data)
        if ok:
            self.view.show_success('Usuario registrado correctamente')
            from auth.login_view import LoginView
            from auth.login_controller import LoginController
            lv = LoginView(self.view.root)
            LoginController(lv, self.db)
        else:
            self.view.show_error('Error al registrar usuario')
