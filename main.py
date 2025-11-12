# main.py - Versión completa con diseño JIMAK Systems
import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar
from ventas import registrar_venta, registrar_venta_detalle, registrar_ventas_del_dia
from productos import buscar_producto_por_codigo, actualizar_stock, listar_productos, agregar_producto, editar_producto
from decimal import Decimal

from PIL import Image, ImageTk

# Lista en memoria para productos (simula la base de datos)
PRODUCTOS_EN_MEMORIA = [
    {"id": 1, "codigo": "7501234588773", "nombre": "CAFE MOLIDO 350g", "precio": Decimal('40.00'), "stock": 150},
    {"id": 2, "codigo": "87654310987", "nombre": "LECHE ENTERA 1L", "precio": Decimal('25.50'), "stock": 130},
    {"id": 3, "codigo": "23456789012", "nombre": "PAN DE MOLDE BLANCO", "precio": Decimal('30.00'), "stock": 95},
    {"id": 4, "codigo": "87564310987", "nombre": "MANZANA ROJA KG", "precio": Decimal('40.75'), "stock": 80},
    {"id": 5, "codigo": "12345678901", "nombre": "AGUACATE HASS PZA", "precio": Decimal('12.00'), "stock": 60}
]

class SistemaJimak:
    def __init__(self, root):
        self.root = root
        self.root.title("JIMAK Systems - Punto De Venta")
        self.root.geometry("1200x800")  # Aumentado para mejor visualización
        self.root.configure(bg='#D9D9D9')
        self.usuario_actual = None
        self.crear_login()
        
    def crear_login(self):
        self.limpiar_pantalla()
        
        # Frame principal del login
        login_frame = tk.Frame(self.root, bg='#D9D9D9', padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo/Título
        try:
            pil_image = Image.open("images/logo_jimak.png")
            pil_image = pil_image.resize((450, 150), Image.LANCZOS)
            logo_image = ImageTk.PhotoImage(pil_image)
    
            logo_label = tk.Label(login_frame, image=logo_image, bg='#D9D9D9')
            logo_label.pack(pady=0)
            self.logo_image = logo_image
    
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            titulo = tk.Label(login_frame, text="JIMAK Systems", 
                     font=('Arial', 28, 'bold'), fg='#000000', bg='#D9D9D9')
            titulo.pack(pady=0)

        # Subtítulo
        subtitulo = tk.Label(login_frame, text="Inicio de Sesión", 
            font=('Brush Script MT', 30), fg='#000000', bg='#D9D9D9')
        subtitulo.pack(pady=0)
            
        # Campos de entrada con diseño moderno
        tk.Label(login_frame, text="Correo Electrónico:", 
                font=('Arial', 12), fg='#000000', bg='#D9D9D9').pack(anchor='w', pady=(20,5))
        
        # Entrada de correo con borde redondeado
        self.email_entry = tk.Entry(login_frame, 
                                   font=('Arial', 12),
                                   bg='#ffffff',
                                   relief='flat',
                                   bd=0,
                                   width=35)
        self.email_entry.pack(pady=5, ipady=8, fill='x')
        self.email_entry.insert(0, "name@gmail.com")
        
        # Aplicar borde redondeado
        self.email_entry.configure(highlightbackground='#cccccc', highlightcolor='#3498db', highlightthickness=1)
        
        tk.Label(login_frame, text="Contraseña:", 
                font=('Arial', 12), fg='#000000', bg='#D9D9D9').pack(anchor='w', pady=(15,5))
        
        # Entrada de contraseña con borde redondeado
        self.password_entry = tk.Entry(login_frame, 
                                      font=('Arial', 12),
                                      bg='#ffffff',
                                      relief='flat',
                                      bd=0,
                                      width=35,
                                      show='*')
        self.password_entry.pack(pady=5, ipady=8, fill='x')
        self.password_entry.insert(0, "Ingrese su contraseña")
        
        # Aplicar borde redondeado
        self.password_entry.configure(highlightbackground='#cccccc', highlightcolor='#3498db', highlightthickness=1)
        
        # Botones con diseño moderno
        btn_frame = tk.Frame(login_frame, bg='#D9D9D9')
        btn_frame.pack(pady=30)
        
        # Botón Iniciar Sesión - Diseño moderno
        login_btn = tk.Button(btn_frame, 
                             text="Iniciar", 
                             font=('Arial', 12, 'bold'), 
                             bg='#A5BBF0', 
                             fg='black',
                             relief='flat',
                             bd=0,
                             width=15,
                             height=2,
                             command=self.iniciar_sesion)
        login_btn.pack(side=tk.LEFT, padx=10)
        
        # Botón Registrarse - Diseño moderno
        registro_btn = tk.Button(btn_frame, 
                               text="Registrarse", 
                               font=('Arial', 12, 'bold'), 
                               bg='#A5BBF0', 
                               fg='black',
                               relief='flat',
                               bd=0,
                               width=15,
                               height=2,
                               command=self.crear_registro)
        registro_btn.pack(side=tk.LEFT, padx=10)
    
    def crear_registro(self):
        self.limpiar_pantalla()
        
        registro_frame = tk.Frame(self.root, bg='#D9D9D9', padx=40, pady=40)
        registro_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        try:
            pil_image = Image.open("images/logo_jimak.png")
            pil_image = pil_image.resize((450, 150), Image.LANCZOS)
            logo_image = ImageTk.PhotoImage(pil_image)
    
            logo_label = tk.Label(registro_frame, image=logo_image, bg='#D9D9D9')
            logo_label.pack(pady=0)
            self.logo_image = logo_image
    
        except Exception as e:
            print(f"Error cargando imagen: {e}")

        subtitulo = tk.Label(registro_frame, text="Registrarse", 
                           font=('Brush Script MT', 30), fg='#000000', bg='#D9D9D9')
        subtitulo.pack(pady=(0, 30))
        
        # Campos de registro con diseño moderno
        campos = [
            ("Ingrese su nombre", "nombre"),
            ("Contraseña:", "password", True),
            ("Correo Electrónico:", "email"),
            ("Confirme la contraseña:", "confirm_password", True)
        ]
        
        self.registro_entries = {}
        
        for label_text, field_name, *is_password in campos:
            tk.Label(registro_frame, text=label_text, 
                    font=('Arial', 12), fg='#000000', bg='#D9D9D9').pack(anchor='w', pady=(10,0))
            
            entry = tk.Entry(registro_frame, 
                           font=('Arial', 12),
                           bg='#ffffff',
                           relief='flat',
                           bd=0,
                           width=35,
                           show='*' if is_password else None)
            entry.pack(pady=5, ipady=8, fill='x')
            
            # Aplicar borde redondeado
            entry.configure(highlightbackground='#cccccc', highlightcolor='#3498db', highlightthickness=1)
            
            if field_name == "nombre":
                entry.insert(0, "Ingrese su nombre")
            elif "password" in field_name:
                entry.insert(0, "Ingrese su contraseña")
            elif field_name == "email":
                entry.insert(0, "name@gmail.com")
                
            self.registro_entries[field_name] = entry
        
        # Botón Registrarse en pantalla de registro
        registro_btn = tk.Button(registro_frame, 
                               text="Registrarse", 
                               font=('Arial', 12, 'bold'), 
                               bg='#A5BBF0', 
                               fg='black',
                               relief='flat',
                               bd=0,
                               width=20,
                               height=2,
                               command=self.registrar_usuario)
        registro_btn.pack(pady=20)
        
        # Botón Volver
        volver_btn = tk.Button(registro_frame, 
                              text="← Volver", 
                              font=('Arial', 10, 'bold'), 
                              bg='#A5BBF0', 
                              fg='black',
                              relief='flat',
                              bd=0,
                              width=15,
                              height=1,
                              command=self.crear_login)
        volver_btn.pack()
    
    def iniciar_sesion(self):
        # Simulación de login - en producción validar contra BD
        self.usuario_actual = self.email_entry.get()
        self.crear_menu_principal()
    
    def registrar_usuario(self):
        # Simulación de registro - en producción guardar en BD
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        self.crear_login()
    
    def crear_menu_principal(self):
        self.limpiar_pantalla()
        
        # Header
        header_frame = tk.Frame(self.root, bg='#B2CFE8', height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        titulo = tk.Label(header_frame, text="JIMAK Systems - Punto De Venta", 
                         font=('Arial', 20, 'bold'), fg='#000000', bg='#B2CFE8')
        titulo.pack(side=tk.LEFT, pady=20)
        
        usuario_label = tk.Label(header_frame, text=f"Usuario: {self.usuario_actual}", 
                               font=('Arial', 12), fg='#000000', bg='#B2CFE8')
        usuario_label.pack(side=tk.RIGHT, pady=20)
        
        # Menú principal
        main_frame = tk.Frame(self.root, bg='#D9D9D9')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        titulo_menu = tk.Label(main_frame, text="PUNTOS DE VENTA", 
                              font=('Arial', 18, 'bold'), fg='#000000', bg='#D9D9D9')
        titulo_menu.pack(pady=20)
        
        # Botones de tipos de negocio con imágenes
        negocios = [
            ("MUEBLERÍA", "#e67e22", "muebleria"),
            ("CARNICERÍA", "#e74c3c", "carniceria"), 
            ("MISCELÁNEA", "#9b59b6", "miscelanea")
        ]
        
        btn_frame = tk.Frame(main_frame, bg='#D9D9D9')
        btn_frame.pack(expand=True)
        
        # Cargar y mostrar imágenes para cada categoría
        self.categoria_images = {}
        
        for i, (negocio, color, imagen_nombre) in enumerate(negocios):
            # Frame principal para cada categoría (clickeable)
            categoria_frame = tk.Frame(btn_frame, bg='#D9D9D9')
            categoria_frame.grid(row=0, column=i, padx=30, pady=20)
            
            try:
                # Intentar cargar la imagen específica de la categoría
                imagen_path = f"images/{imagen_nombre}.png"
                pil_image = Image.open(imagen_path)
                pil_image = pil_image.resize((150, 150), Image.LANCZOS)
                categoria_image = ImageTk.PhotoImage(pil_image)
                self.categoria_images[negocio] = categoria_image
                
                # Mostrar imagen (también clickeable)
                imagen_label = tk.Label(categoria_frame, 
                                      image=categoria_image, 
                                      bg='#D9D9D9',
                                      cursor="hand2")
                imagen_label.pack(pady=(0, 15))
                imagen_label.bind("<Button-1>", lambda e, n=negocio: self.abrir_terminal_venta(n))
                
            except Exception as e:
                print(f"Error cargando imagen de {negocio}: {e}")
                # Si no hay imagen, mostrar un círculo de color (también clickeable)
                canvas_frame = tk.Frame(categoria_frame, bg='#D9D9D9')
                canvas_frame.pack(pady=(0, 15))
                canvas_frame.bind("<Button-1>", lambda e, n=negocio: self.abrir_terminal_venta(n))
                canvas_frame.configure(cursor="hand2")
                
                canvas = tk.Canvas(canvas_frame, width=150, height=150, bg='#D9D9D9', highlightthickness=0)
                canvas.pack()
                canvas.create_oval(10, 10, 140, 140, fill=color, outline=color)
                canvas.bind("<Button-1>", lambda e, n=negocio: self.abrir_terminal_venta(n))
            
            # Nombre de la categoría (también clickeable)
            nombre_label = tk.Label(categoria_frame, 
                                  text=negocio, 
                                  font=('Arial', 16, 'bold'), 
                                  fg='#000000', 
                                  bg="#D9D9D9",
                                  cursor="hand2")
            nombre_label.pack(pady=(0, 15))
            nombre_label.bind("<Button-1>", lambda e, n=negocio: self.abrir_terminal_venta(n))
            
            # Botón visible pero con diseño mejorado
            btn_categoria = tk.Button(categoria_frame,
                                    text="Abrir Terminal",
                                    font=('Arial', 12, 'bold'),
                                    bg=color,
                                    fg='white',
                                    relief='flat',
                                    bd=0,
                                    width=15,
                                    height=1,
                                    cursor="hand2",
                                    command=lambda n=negocio: self.abrir_terminal_venta(n))
            btn_categoria.pack()
            
            # Hacer todo el frame clickeable
            categoria_frame.bind("<Button-1>", lambda e, n=negocio: self.abrir_terminal_venta(n))
            categoria_frame.configure(cursor="hand2")
        
        # Botones de sistema con diseño moderno
        sistema_frame = tk.Frame(main_frame, bg='#D9D9D9')
        sistema_frame.pack(pady=30)
        
        ventas_btn = tk.Button(sistema_frame, 
                              text="Ventas del Día", 
                              font=('Arial', 14, 'bold'),
                              bg='#B2CFE8', 
                              fg='black',
                              relief='flat',
                              bd=0,
                              width=18,
                              height=2,
                              command=self.mostrar_ventas_dia)
        ventas_btn.grid(row=0, column=0, padx=15)
        
        opciones_btn = tk.Button(sistema_frame, 
                               text="Opciones", 
                               font=('Arial', 14, 'bold'),
                               bg='#D9D9D9', 
                               fg='black',
                               relief='flat',
                              bd=0,
                              width=18,
                              height=2,
                              command=self.abrir_opciones)
        opciones_btn.grid(row=0, column=1, padx=15)
        
        cerrar_btn = tk.Button(sistema_frame, 
                             text="Cerrar Sesión", 
                             font=('Arial', 14, 'bold'),
                             bg='#e74c3c', 
                             fg='white',
                              relief='flat',
                              bd=0,
                              width=18,
                              height=2,
                              command=self.crear_login)
        cerrar_btn.grid(row=0, column=2, padx=15)
    
    def abrir_terminal_venta(self, tipo_negocio):
        ventana = tk.Toplevel(self.root)
        ventana.title(f"VENTA - {tipo_negocio}")
        ventana.geometry("1100x750")  # Aumentado para mejor visualización
        ventana.configure(bg='#D9D9D9')
        # Guardar referencia para evitar que se destruya
        self.terminal_venta = TerminalVenta(ventana, tipo_negocio)
    
    def mostrar_ventas_dia(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("VENTAS DEL DIA")
        ventana.geometry("1000x650")  # Aumentado
        ventana.configure(bg='#D9D9D9')
        VentasDia(ventana)
    
    def abrir_opciones(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("OPCIONES DE PRODUCTO")
        ventana.geometry("600x500")  # Aumentado
        ventana.configure(bg='#D9D9D9')
        OpcionesProductos(ventana)
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class TerminalVenta:
    def __init__(self, parent, tipo_negocio):
        self.parent = parent
        self.tipo_negocio = tipo_negocio
        self.venta_actual = []
        self.total = Decimal('0.00')
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Header
        header_frame = tk.Frame(self.parent, bg='#B2CFE8', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        titulo = tk.Label(header_frame, text=f"VENTA - {self.tipo_negocio}", 
                         font=('Arial', 18, 'bold'), fg='#000000', bg='#B2CFE8')
        titulo.pack(side=tk.LEFT, pady=20, padx=20)
        
        # Menú de navegación con botones modernos
        nav_frame = tk.Frame(header_frame, bg='#B2CFE8')
        nav_frame.pack(side=tk.RIGHT, pady=20, padx=20)
        
        ventas_btn = tk.Button(nav_frame, 
                              text="Ventas del día", 
                              font=('Arial', 11, 'bold'),
                              bg='#3498db', 
                              fg='white',
                              relief='flat',
                              bd=0,
                              width=12,
                              command=self.mostrar_ventas_dia)
        ventas_btn.pack(side=tk.LEFT, padx=8)
        
        opciones_btn = tk.Button(nav_frame, 
                               text="Opciones", 
                               font=('Arial', 11, 'bold'),
                               bg='#95a5a6', 
                               fg='white',
                               relief='flat',
                              bd=0,
                              width=12,
                              command=self.abrir_opciones)
        opciones_btn.pack(side=tk.LEFT, padx=8)
        
        # Contenido principal
        main_frame = tk.Frame(self.parent, bg='#D9D9D9')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Frame para búsqueda
        busqueda_frame = tk.Frame(main_frame, bg='#D9D9D9')
        busqueda_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Buscador por nombre
        tk.Label(busqueda_frame, text="Buscar por Nombre:", font=('Arial', 12), bg='#D9D9D9').pack(side=tk.LEFT)
        
        self.busqueda_entry = tk.Entry(busqueda_frame, 
                                      font=('Arial', 12),
                                      bg='#ffffff',
                                      relief='flat',
                                      bd=0,
                                      width=30)
        self.busqueda_entry.pack(side=tk.LEFT, padx=10, ipady=6)
        self.busqueda_entry.configure(highlightbackground='#cccccc', highlightcolor='#3498db', highlightthickness=1)
        self.busqueda_entry.bind('<KeyRelease>', self.buscar_productos)
        
        # Botón Buscar
        buscar_btn = tk.Button(busqueda_frame, 
                             text="Buscar", 
                             font=('Arial', 12, 'bold'),
                             bg='#A5BBF0', 
                             fg='white',
                             relief='flat',
                             bd=0,
                             width=10,
                             command=self.buscar_productos)
        buscar_btn.pack(side=tk.LEFT, padx=5)
        
        # Lista de productos encontrados
        self.lista_productos_frame = tk.Frame(main_frame, bg='#D9D9D9')
        self.lista_productos_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Frame para entrada de código de barras
        input_frame = tk.Frame(main_frame, bg='#D9D9D9')
        input_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(input_frame, text="Código de Barras:", font=('Arial', 12), bg='#D9D9D9').pack(side=tk.LEFT)
        
        self.codigo_entry = tk.Entry(input_frame, 
                                    font=('Arial', 12),
                                    bg='#ffffff',
                                    relief='flat',
                                    bd=0,
                                    width=25)
        self.codigo_entry.pack(side=tk.LEFT, padx=10, ipady=6)
        self.codigo_entry.configure(highlightbackground='#cccccc', highlightcolor='#3498db', highlightthickness=1)
        self.codigo_entry.bind('<Return>', self.agregar_producto)
        
        # Botón Agregar con diseño moderno
        agregar_btn = tk.Button(input_frame, 
                               text="Agregar", 
                               font=('Arial', 12, 'bold'),
                               bg='#A5BBF0', 
                               fg='white',
                               relief='flat',
                               bd=0,
                               width=12,
                               command=self.agregar_producto)
        agregar_btn.pack(side=tk.LEFT, padx=10)
        
        # Tabla de productos
        columns = ('Código de Barras', 'Producto', 'Precio Venta', 'Importe', 'Existencia')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Panel de totales
        total_frame = tk.Frame(main_frame, bg='#D9D9D9')
        total_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(total_frame, text="SUBTOTAL:", font=('Arial', 13, 'bold'), bg='#D9D9D9').pack(side=tk.LEFT)
        self.subtotal_label = tk.Label(total_frame, text="$ 0.00", font=('Arial', 13, 'bold'), bg='#D9D9D9')
        self.subtotal_label.pack(side=tk.LEFT, padx=10)
        
        tk.Label(total_frame, text="IVA:", font=('Arial', 13, 'bold'), bg='#D9D9D9').pack(side=tk.LEFT, padx=20)
        self.iva_label = tk.Label(total_frame, text="$ 0.00", font=('Arial', 13, 'bold'), bg='#D9D9D9')
        self.iva_label.pack(side=tk.LEFT, padx=10)
        
        tk.Label(total_frame, text="TOTAL:", font=('Arial', 15, 'bold'), bg='#D9D9D9').pack(side=tk.LEFT, padx=20)
        self.total_label = tk.Label(total_frame, text="$ 0.00", font=('Arial', 16, 'bold'), fg='#1764D1', bg='#D9D9D9')
        self.total_label.pack(side=tk.LEFT, padx=10)
        
        # Botones finales con diseño moderno
        btn_frame = tk.Frame(main_frame, bg='#D9D9D9')
        btn_frame.pack(fill=tk.X, pady=15)
        
        terminar_btn = tk.Button(btn_frame, 
                               text="Terminar Venta", 
                               font=('Arial', 13, 'bold'),
                               bg='#A5BBF0', 
                               fg='black',
                               relief='flat',
                               bd=0,
                               width=18,
                               height=2,
                               command=self.terminar_venta)
        terminar_btn.pack(side=tk.RIGHT, padx=15)
        
        reiniciar_btn = tk.Button(btn_frame, 
                                text="Reiniciar", 
                                font=('Arial', 13, 'bold'),
                                bg='#A5BBF0', 
                                fg='black',
                                relief='flat',
                                bd=0,
                                width=18,
                                height=2,
                                command=self.reiniciar_venta)
        reiniciar_btn.pack(side=tk.RIGHT, padx=15)
    
    def buscar_productos(self, event=None):
        """Busca productos por nombre y los muestra en botones"""
        # Limpiar frame anterior
        for widget in self.lista_productos_frame.winfo_children():
            widget.destroy()
        
        texto_busqueda = self.busqueda_entry.get().strip().lower()
        
        if not texto_busqueda:
            return
        
        # Buscar productos que coincidan
        productos_encontrados = []
        for producto in PRODUCTOS_EN_MEMORIA:
            if texto_busqueda in producto["nombre"].lower():
                productos_encontrados.append(producto)
        
        # Mostrar máximo 5 productos
        productos_encontrados = productos_encontrados[:5]
        
        if productos_encontrados:
            tk.Label(self.lista_productos_frame, 
                    text="Productos encontrados:", 
                    font=('Arial', 11, 'bold'), 
                    bg='#D9D9D9').pack(anchor='w')
            
            # Frame para botones de productos
            botones_frame = tk.Frame(self.lista_productos_frame, bg='#D9D9D9')
            botones_frame.pack(fill=tk.X, pady=8)
            
            for producto in productos_encontrados:
                btn_text = f"{producto['nombre']} - ${float(producto['precio']):.2f}"
                producto_btn = tk.Button(botones_frame,
                                       text=btn_text,
                                       font=('Arial', 10),
                                       bg='#A5BBF0',
                                       fg='black',
                                       relief='flat',
                                       bd=0,
                                       width=35,
                                       height=1,
                                       command=lambda p=producto: self.seleccionar_producto(p))
                producto_btn.pack(side=tk.LEFT, padx=8, pady=3)
    
    def seleccionar_producto(self, producto):
        """Selecciona un producto de la lista de búsqueda"""
        self.codigo_entry.delete(0, tk.END)
        self.codigo_entry.insert(0, producto["codigo"])
        self.busqueda_entry.delete(0, tk.END)
        
        # Limpiar lista de productos encontrados
        for widget in self.lista_productos_frame.winfo_children():
            widget.destroy()
    
    def buscar_producto_en_memoria(self, codigo):
        """Busca producto en la lista en memoria"""
        for producto in PRODUCTOS_EN_MEMORIA:
            if producto["codigo"] == codigo:
                return (
                    producto["id"],
                    producto["nombre"],
                    producto["precio"],
                    producto["stock"]
                )
        return None
    
    def agregar_producto(self, event=None):
        codigo = self.codigo_entry.get().strip()
        if not codigo:
            messagebox.showwarning("Advertencia", "Ingrese un código de barras")
            return
        
        # Buscar producto en memoria
        producto = self.buscar_producto_en_memoria(codigo)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        id_prod, nombre, precio, stock = producto
        cantidad = 1  # Por defecto 1 unidad
        
        if cantidad > stock:
            messagebox.showerror("Error", "Stock insuficiente")
            return
        
        subtotal = precio * Decimal(cantidad)
        self.venta_actual.append((id_prod, nombre, precio, cantidad, subtotal, stock))
        self.total += subtotal
        
        # Agregar a la tabla
        self.tree.insert('', 'end', values=(
            codigo, nombre, f"${float(precio):.2f}", f"${float(subtotal):.2f}", stock
        ))
        
        self.actualizar_totales()
        self.codigo_entry.delete(0, tk.END)
    
    def actualizar_totales(self):
        subtotal = float(self.total)
        iva = subtotal * 0.16  # 16% IVA
        total = subtotal + iva
        
        self.subtotal_label.config(text=f"$ {subtotal:.2f}")
        self.iva_label.config(text=f"$ {iva:.2f}")
        self.total_label.config(text=f"$ {total:.2f}")
    
    def reiniciar_venta(self):
        self.venta_actual.clear()
        self.total = Decimal('0.00')
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.actualizar_totales()
        
        # Limpiar también la lista de productos encontrados
        for widget in self.lista_productos_frame.winfo_children():
            widget.destroy()
    
    def terminar_venta(self):
        if not self.venta_actual:
            messagebox.showwarning("Advertencia", "No hay productos en la venta")
            return
        
        # Mostrar ventana de pago
        self.mostrar_ventana_pago()
    
    def mostrar_ventana_pago(self):
        pago_window = tk.Toplevel(self.parent)
        pago_window.title("Pago")
        pago_window.geometry("400x250")  # Aumentado
        pago_window.configure(bg='#D9D9D9')
        
        total = float(self.total) * 1.16  # Total con IVA
        
        tk.Label(pago_window, text="Pagó Con:", font=('Arial', 14), bg='#D9D9D9').pack(pady=15)
        
        self.pago_entry = tk.Entry(pago_window, 
                                  font=('Arial', 16), 
                                  justify='center',
                                  bg='#ffffff',
                                  relief='flat',
                                  bd=0)
        self.pago_entry.pack(pady=15, ipady=10)
        self.pago_entry.configure(highlightbackground='#cccccc', highlightcolor='#3498db', highlightthickness=1)
        self.pago_entry.focus()
        
        tk.Label(pago_window, text=f"TOTAL: ${total:.2f}", 
                font=('Arial', 14, 'bold'), fg='#e74c3c', bg='#D9D9D9').pack(pady=10)
        
        # Botón OK con diseño moderno
        ok_btn = tk.Button(pago_window, 
                          text="OK", 
                          font=('Arial', 14, 'bold'),
                          bg='#27ae60', 
                          fg='white',
                          relief='flat',
                          bd=0,
                          width=12,
                          height=2,
                          command=lambda: self.procesar_pago(pago_window, total))
        ok_btn.pack(pady=15)
    
    def procesar_pago(self, pago_window, total):
        try:
            pago = float(self.pago_entry.get())
            if pago < total:
                messagebox.showerror("Error", "Pago insuficiente")
                return
            
            cambio = pago - total
            
            # Actualizar stock en memoria
            for item in self.venta_actual:
                id_prod, nombre, precio, cantidad, subtotal, stock = item
                # Buscar y actualizar el producto en memoria
                for producto in PRODUCTOS_EN_MEMORIA:
                    if producto["id"] == id_prod:
                        producto["stock"] -= cantidad
                        break
            
            # Mostrar cambio
            cambio_window = tk.Toplevel(self.parent)
            cambio_window.title("Cambio")
            cambio_window.geometry("350x200")  # Aumentado
            cambio_window.configure(bg='#D9D9D9')
            
            tk.Label(cambio_window, text="Su Cambio Es:", 
                    font=('Arial', 16), bg='#D9D9D9').pack(pady=25)
            
            tk.Label(cambio_window, text=f"${cambio:.2f}", 
                    font=('Arial', 20, 'bold'), fg='#27ae60', bg='#D9D9D9').pack(pady=15)
            
            # Botón Terminar con diseño moderno
            terminar_btn = tk.Button(cambio_window, 
                                   text="Terminar", 
                                   font=('Arial', 14, 'bold'),
                                   bg='#3498db', 
                                   fg='white',
                                   relief='flat',
                                   bd=0,
                                   width=12,
                                   height=2,
                                   command=lambda: [cambio_window.destroy(), pago_window.destroy(), self.reiniciar_venta()])
            terminar_btn.pack(pady=15)
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido")
    
    def mostrar_ventas_dia(self):
        VentasDia(tk.Toplevel(self.parent))
    
    def abrir_opciones(self):
        OpcionesProductos(tk.Toplevel(self.parent))

class VentasDia:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("VENTAS DEL DIA")
        self.parent.geometry("1000x650")
        self.parent.configure(bg='#D9D9D9')
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Header con fecha
        header_frame = tk.Frame(self.parent, bg='#B2CFE8', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        from datetime import datetime
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        
        tk.Label(header_frame, text=f"VENTAS DEL DIA - FECHA {fecha_actual}", 
                font=('Arial', 18, 'bold'), fg='#000000', bg='#B2CFE8').pack(pady=20)
        
        # Contenido principal
        main_frame = tk.Frame(self.parent, bg='#D9D9D9')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Tabla de ventas
        columns = ('Código de Barras', 'Producto', 'Precio Venta', 'Importe')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)
        
        # Mostrar productos de ejemplo
        for producto in PRODUCTOS_EN_MEMORIA[:3]:  # Mostrar primeros 3 productos como ejemplo
            tree.insert('', 'end', values=(
                producto["codigo"],
                producto["nombre"],
                f"${float(producto['precio']):.2f}",
                f"${float(producto['precio']):.2f}"
            ))
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Total del día
        total_frame = tk.Frame(main_frame, bg='#D9D9D9')
        total_frame.pack(fill=tk.X, pady=15)
        
        total_dia = sum(float(producto["precio"]) for producto in PRODUCTOS_EN_MEMORIA[:3])
        tk.Label(total_frame, text=f"TOTAL DEL DIA: ${total_dia:.2f}", 
                font=('Arial', 16, 'bold'), fg='#e74c3c', bg='#D9D9D9').pack(side=tk.LEFT)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='#D9D9D9')
        btn_frame.pack(fill=tk.X, pady=15)
        
        tk.Button(btn_frame, text="← REGRESAR", font=('Arial', 13),
                 bg='#95a5a6', fg='white', width=15, height=2,
                 command=self.parent.destroy).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="EXPORTAR", font=('Arial', 13),
                 bg='#3498db', fg='white', width=15, height=2,
                 command=self.exportar).pack(side=tk.RIGHT, padx=10)
    
    def exportar(self):
        messagebox.showinfo("JIMAK Systems", "Se está exportando archivo")

class OpcionesProductos:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("OPCIONES DE PRODUCTO")
        self.parent.geometry("600x500")
        self.parent.configure(bg='#D9D9D9')
        self.crear_interfaz()
    
    def crear_interfaz(self):
        main_frame = tk.Frame(self.parent, bg='#D9D9D9')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(main_frame, text="OPCIONES DE PRODUCTO", 
                font=('Arial', 20, 'bold'), fg='#000000', bg='#D9D9D9').pack(pady=25)
        
        # Botones de opciones
        opciones = [
            ("AGREGAR", "#27ae60", self.agregar_producto),
            ("ADMINISTRAR", "#3498db", self.administrar_productos),
            ("ACTUALIZAR", "#e67e22", self.actualizar_producto),
            ("VER STOCK", "#9b59b6", self.ver_stock)
        ]
        
        for texto, color, comando in opciones:
            btn = tk.Button(main_frame, text=texto, font=('Arial', 16, 'bold'),
                          bg=color, fg='white', width=25, height=2,
                          command=comando)
            btn.pack(pady=15)
    
    def agregar_producto(self):
        ventana = tk.Toplevel(self.parent)
        ventana.title("AGREGAR PRODUCTOS")
        ventana.geometry("500x450")  # Aumentado
        ventana.configure(bg='#D9D9D9')
        AgregarProducto(ventana)
    
    def administrar_productos(self):
        messagebox.showinfo("Administrar", "Funcionalidad de administración de productos")
    
    def actualizar_producto(self):
        ventana = tk.Toplevel(self.parent)
        ventana.title("ACTUALIZAR PRODUCTO")
        ventana.geometry("500x450")  # Aumentado
        ventana.configure(bg='#D9D9D9')
        ActualizarProducto(ventana)
    
    def ver_stock(self):
        ventana = tk.Toplevel(self.parent)
        ventana.title("VER STOCK")
        ventana.geometry("700x550")  # Aumentado
        ventana.configure(bg='#D9D9D9')
        VerStock(ventana)

class AgregarProducto:
    def __init__(self, parent):
        self.parent = parent
        self.crear_interfaz()
    
    def crear_interfaz(self):
        main_frame = tk.Frame(self.parent, padx=30, pady=30, bg='#D9D9D9')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="AGREGAR PRODUCTOS", 
                font=('Arial', 18, 'bold'), bg='#D9D9D9').pack(pady=20)
        
        campos = [
            ("Nombre de producto:", "nombre"),
            ("Precio del Producto:", "precio"),
            ("Stock inicial:", "stock"),
            ("Código de barras:", "codigo")
        ]
        
        self.entries = {}
        
        for label_text, field_name in campos:
            tk.Label(main_frame, text=label_text, font=('Arial', 12), bg='#D9D9D9').pack(anchor='w', pady=(15,0))
            
            entry = tk.Entry(main_frame, font=('Arial', 12), width=35, bg='#ffffff', relief='flat', bd=0)
            entry.pack(pady=8, ipady=6, fill='x')
            entry.configure(highlightbackground='#cccccc', highlightcolor='#3498db', highlightthickness=1)
            
            if field_name == "nombre":
                entry.insert(0, "Ingrese el nombre")
            elif field_name == "precio":
                entry.insert(0, "0.00")
            elif field_name == "stock":
                entry.insert(0, "0")
            elif field_name == "codigo":
                entry.insert(0, "ejemplo: 1213547")
                
            self.entries[field_name] = entry
        
        tk.Button(main_frame, text="AGREGAR", font=('Arial', 14, 'bold'),
                 bg='#27ae60', fg='white', width=20, height=2,
                 command=self.agregar).pack(pady=25)
    
    def agregar(self):
        try:
            # Obtener datos de los campos
            nombre = self.entries["nombre"].get()
            precio = Decimal(self.entries["precio"].get())
            stock = int(self.entries["stock"].get())
            codigo = self.entries["codigo"].get()
            
            if not all([nombre, codigo]):
                messagebox.showerror("Error", "Complete todos los campos")
                return
            
            # Agregar producto a la lista en memoria
            nuevo_id = max([p["id"] for p in PRODUCTOS_EN_MEMORIA]) + 1 if PRODUCTOS_EN_MEMORIA else 1
            nuevo_producto = {
                "id": nuevo_id,
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "stock": stock
            }
            PRODUCTOS_EN_MEMORIA.append(nuevo_producto)
            
            messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente")
            self.parent.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos")

class ActualizarProducto:
    def __init__(self, parent):
        self.parent = parent
        self.crear_interfaz()
    
    def crear_interfaz(self):
        main_frame = tk.Frame(self.parent, padx=30, pady=30, bg='#D9D9D9')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="ACTUALIZAR PRODUCTO", 
                font=('Arial', 18, 'bold'), bg='#D9D9D9').pack(pady=20)
        
        # Mostrar lista de productos para seleccionar
        tk.Label(main_frame, text="Seleccione producto:", font=('Arial', 12), bg='#D9D9D9').pack(anchor='w', pady=(15,0))
        
        self.producto_var = tk.StringVar()
        producto_combobox = ttk.Combobox(main_frame, textvariable=self.producto_var, state="readonly", font=('Arial', 12))
        producto_combobox['values'] = [f"{p['codigo']} - {p['nombre']}" for p in PRODUCTOS_EN_MEMORIA]
        producto_combobox.pack(pady=8, fill='x', ipady=5)
        
        campos = [
            ("Nuevo nombre:", "nombre"),
            ("Nuevo precio:", "precio"),
            ("Nuevo stock:", "stock")
        ]
        
        self.entries = {}
        
        for label_text, field_name in campos:
            tk.Label(main_frame, text=label_text, font=('Arial', 12), bg='#D9D9D9').pack(anchor='w', pady=(15,0))
            
            entry = tk.Entry(main_frame, font=('Arial', 12), width=35, bg='#ffffff', relief='flat', bd=0)
            entry.pack(pady=8, ipady=6, fill='x')
            entry.configure(highlightbackground='#cccccc', highlightcolor='#3498db', highlightthickness=1)
                
            self.entries[field_name] = entry
        
        tk.Button(main_frame, text="ACTUALIZAR", font=('Arial', 14, 'bold'),
                 bg='#e67e22', fg='white', width=20, height=2).pack(pady=25)

class VerStock:
    def __init__(self, parent):
        self.parent = parent
        self.crear_interfaz()
    
    def crear_interfaz(self):
        main_frame = tk.Frame(self.parent, bg='#D9D9D9')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        tk.Label(main_frame, text="VER STOCK", 
                font=('Arial', 18, 'bold'), bg='#D9D9D9').pack(pady=20)
        
        # Tabla de stock
        columns = ('Código', 'Producto', 'Precio', 'Stock')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=18)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Mostrar productos de la lista en memoria
        for producto in PRODUCTOS_EN_MEMORIA:
            tree.insert('', 'end', values=(
                producto["codigo"],
                producto["nombre"],
                f"${float(producto['precio']):.2f}",
                f"{producto['stock']} pzs"
            ))
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        tk.Button(main_frame, text="EDITAR", font=('Arial', 13),
                 bg='#3498db', fg='white', width=15, height=2).pack(pady=15)

if __name__ == "__main__":
    try:
        # Verificar conexión a BD
        con = conectar()
        if con.is_connected():
            print("✅ Conectado correctamente a MySQL")
        con.close()
        
        # Iniciar aplicación
        root = tk.Tk()
        app = SistemaJimak(root)
        root.mainloop()
        
    except Exception as err:
        print(f"❌ Error al conectar a MySQL: {err}")
        # Iniciar aplicación incluso sin conexión a BD
        root = tk.Tk()
        app = SistemaJimak(root)
        root.mainloop()