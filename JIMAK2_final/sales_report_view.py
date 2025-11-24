import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk

import pandas as pd
import os

# Importar funciones del controller
from sales_report_controller import (
    obtener_ventas_del_dia,
    exportar_ventas_excel
)

class SalesReportWindow:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.report_window = tk.Toplevel(parent)
        self.report_window.title("Ventas del Día")
        self.report_window.geometry("600x500")
        self.report_window.transient(parent)
        self.report_window.grab_set()
        
        self.setup_ui()
        self.load_sales()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.report_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Logo
        try:
            pil_image = Image.open("assets/logo.png")
            original_width, original_height = pil_image.size
            new_width = 300
            new_height = int((original_height / original_width) * new_width)

            resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(resized_image)
            logo_label = ttk.Label(main_frame, image=self.logo_image)
            logo_label.pack(pady=(0, 20))
            
        except Exception as e:
            print(f"Error cargando logo: {e}")
            logo_label = ttk.Label(main_frame, text="Ventas del Día",
                                   font=("Arial", 18, "bold"),
                                   foreground="#2c3e50")
            logo_label.pack(pady=(0, 30))
        
        # Tabla
        self.sales_tree = ttk.Treeview(
            main_frame,
            columns=('ID', 'Fecha', 'Total', 'Vendedor'),
            show='headings'
        )
        self.sales_tree.heading('ID', text='ID Venta')
        self.sales_tree.heading('Fecha', text='Fecha y Hora')
        self.sales_tree.heading('Total', text='Total')
        self.sales_tree.heading('Vendedor', text='Vendedor')

        self.sales_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame, text="Exportar a Excel",
            style="White.TButton",
            command=self.export_to_excel
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, text="Cerrar",
            style="White.TButton",
            command=self.report_window.destroy
        ).pack(side=tk.RIGHT, padx=5)

        # Estilos
        style = ttk.Style()
        style.configure("White.TButton",
                       background="white",
                       foreground="black",
                       bordercolor="black",
                       borderwidth=1,
                       relief="solid",
                       font=("Arial", 11))

        style.map(
            "White.TButton",
            background=[('active', '#eeeeee'), ('pressed', 'lightgray')],
            foreground=[('active', 'black')]
        )
    
    def load_sales(self):
        """Llama al controller para obtener ventas y llenar la tabla."""
        today = datetime.now().strftime('%Y-%m-%d')
        ventas = obtener_ventas_del_dia(self.db, today)

        for venta in ventas:
            self.sales_tree.insert(
                '',
                'end',
                values=(
                    venta['id'],
                    venta['fecha'].strftime('%Y-%m-%d %H:%M:%S'),
                    f"${venta['total']:.2f}",
                    venta['vendedor'] or 'N/A'
                )
            )

    def export_to_excel(self):
        """Llama al controller para exportar ventas."""
        resultado = exportar_ventas_excel(self.db)

        if resultado['status'] == 'ok':
            messagebox.showinfo("Éxito", resultado['message'])
        else:
            messagebox.showerror("Error", resultado['message'])
