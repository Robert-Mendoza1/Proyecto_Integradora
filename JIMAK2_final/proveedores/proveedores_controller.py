from proveedores.proveedores_view import ProveedoresView
from database import Database
import tkinter as tk
from tkinter import ttk

class ProveedoresController:
    def __init__(self, root, db=None, view_instance=None):
        self.root = root
        self.db = db or Database()
        self.view = view_instance or ProveedoresView(root, self.db)
        self.view.set_search_callback(self.buscar)
        self.view.set_add_callback(self.abrir_agregar)
        for w in self.view.window.winfo_children():
            for child in w.winfo_children():
                try:
                    if hasattr(child, 'cget') and child.cget('text').lower()=='buscar':
                        child.configure(command=self.buscar)
                    if hasattr(child, 'cget') and child.cget('text').lower()=='agregar proveedor':
                        child.configure(command=self.abrir_agregar)
                except Exception:
                    pass
        self.buscar()

    def buscar(self):
        term = self.view.get_search_text()
        rows = self.db.get_proveedores(term)
        self.view.populate(rows)

    def abrir_agregar(self):
        win = tk.Toplevel(self.view.window); win.title('Agregar Proveedor'); win.geometry('400x320')
        frm = ttk.Frame(win, padding=10); frm.pack(fill='both', expand=True)
        ttk.Label(frm, text='Nombre:').pack(anchor='w'); name = ttk.Entry(frm); name.pack(fill='x')
        ttk.Label(frm, text='Teléfono:').pack(anchor='w'); phone = ttk.Entry(frm); phone.pack(fill='x')
        ttk.Label(frm, text='Empresa:').pack(anchor='w'); company = ttk.Entry(frm); company.pack(fill='x')
        ttk.Label(frm, text='Notas:').pack(anchor='w'); notes = ttk.Entry(frm); notes.pack(fill='x')
        def guardar():
            n = name.get().strip(); t = phone.get().strip(); e = company.get().strip(); no = notes.get().strip()
            if not n:
                self.view.show_error('Nombre es obligatorio'); return
            ok, msg = self.db.insert_proveedor(n, t, e, no)
            if ok:
                self.view.show_message(msg); win.destroy(); self.buscar()
            else:
                self.view.show_error(msg)
        btn_frame = ttk.Frame(frm); btn_frame.pack(pady=10, fill='x')
        ttk.Button(btn_frame, text='Guardar', command=guardar).pack(side='left', expand=True, fill='x', padx=5)
        ttk.Button(btn_frame, text='Cancelar', command=win.destroy).pack(side='left', expand=True, fill='x', padx=5)
