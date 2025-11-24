import tkinter as tk
from tkinter import ttk, messagebox

class POSView:
    def __init__(self, root, user, db):
        self.root = root
        self.user = user
        self.db = db
        self._build_ui()

    def _build_ui(self):
        for w in self.root.winfo_children(): w.destroy()
        self.root.title(f"Punto de Venta - {self.user.get('nombre', 'Usuario')}")
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill='both', expand=True)
        header = ttk.Label(main, text=f"Bienvenido: {self.user.get('nombre', 'Usuario')}", font=('Arial',14))
        header.pack(anchor='e')
        btn_frame = ttk.Frame(main)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text='Proveedores', command=self.open_proveedores).pack(fill='x', pady=5)
        ttk.Button(btn_frame, text='Productos', command=self.open_productos_placeholder).pack(fill='x', pady=5)
        ttk.Button(btn_frame, text='Reportes', command=self.open_reportes_placeholder).pack(fill='x', pady=5)
        ttk.Button(btn_frame, text='Cerrar Sesión', command=self.logout).pack(fill='x', pady=5)

    def open_proveedores(self):
        from proveedores.proveedores_controller import ProveedoresController
        from proveedores.proveedores_view import ProveedoresView
        pv = ProveedoresView(self.root, self.db)
        ProveedoresController(self.root, self.db, pv)

    def open_productos_placeholder(self):
        messagebox.showinfo('Info', 'Módulo productos no implementado aquí')

    def open_reportes_placeholder(self):
        messagebox.showinfo('Info', 'Módulo reportes no implementado aquí')

    def logout(self):
        from auth.login_view import LoginView
        from auth.login_controller import LoginController
        lv = LoginView(self.root)
        LoginController(lv, self.db)
