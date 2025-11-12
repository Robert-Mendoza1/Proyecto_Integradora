import tkinter as tk

def create_rounded_entry(parent, width=300, height=40, radius=15, bg_color='#ecf0f1', **kwargs):
    """
    Crea un Entry con esquinas redondeadas
    """
    # Frame que actuará como contenedor redondeado
    frame = tk.Frame(parent, bg=parent.cget('bg'), height=height)
    frame.pack_propagate(False)
    
    # Canvas para los bordes redondeados
    canvas = tk.Canvas(
        frame, 
        width=width, 
        height=height, 
        bg=parent.cget('bg'),
        highlightthickness=0
    )
    canvas.pack()
    
    # Dibujar rectángulo redondeado
    canvas.create_rounded_rect = lambda x1, y1, x2, y2, radius, **kw: canvas.create_polygon(
        x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y2-radius, x2, y2, 
        x2-radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y1+radius, x1, y1,
        smooth=True, **kw
    )
    
    canvas.create_rounded_rect(0, 0, width, height, radius, fill=bg_color, outline='')
    
    # Crear el Entry sin borde
    entry = tk.Entry(frame, **kwargs)
    entry.configure(
        relief='flat',
        border=0,
        highlightthickness=0,
        bg=bg_color
    )
    
    # Posicionar el Entry dentro del frame
    entry.place(x=radius//2, y=height//2, width=width-radius, height=height-10, anchor='w')
    
    return frame, entry

def create_rounded_entry_simple(parent, **kwargs):
    """
    Versión simplificada con valores por defecto
    """
    return create_rounded_entry(
        parent, 
        width=300, 
        height=40, 
        radius=12,
        bg_color='#ecf0f1',
        **kwargs
    )