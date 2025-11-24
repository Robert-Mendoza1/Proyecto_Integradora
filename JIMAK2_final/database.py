import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime

class Database:
    def __init__(self, host='127.0.0.1', user='root', password='', database='jimak2'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except Error as e:
            print('DB connection error:', e)
            return None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # USERS
    def authenticate_user(self, username_or_email, password):
        conn = self.get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor(dictionary=True)
            hashed = self.hash_password(password)
            sql = """SELECT * FROM usuarios WHERE (username=%s OR email=%s) AND password=%s LIMIT 1"""
            cursor.execute(sql, (username_or_email, username_or_email, hashed))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except Error as e:
            print('authenticate_user error:', e)
            return None

    def register_user(self, user_data):
        conn = self.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            hashed = self.hash_password(user_data['password'])
            sql = """INSERT INTO usuarios (nombre, username, email, password, rol) VALUES (%s,%s,%s,%s,%s)"""
            cursor.execute(sql, (user_data['nombre'][:30], user_data['username'][:30], user_data['email'][:30], hashed, user_data.get('rol','vendedor')))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print('register_user error:', e)
            try: conn.rollback()
            except: pass
            return False

    # PROVIDERS
    def get_proveedores(self, term=''):
        conn = self.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            if term:
                like = f"%{term}%"
                sql = "SELECT * FROM proveedores WHERE nombre LIKE %s OR telefono LIKE %s ORDER BY nombre LIMIT 200"
                cursor.execute(sql, (like, like))
            else:
                sql = "SELECT * FROM proveedores ORDER BY nombre LIMIT 200"
                cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Error as e:
            print('get_proveedores error:', e)
            return []

    def insert_proveedor(self, nombre, telefono, empresa, notas):
        conn = self.get_connection()
        if not conn: return False, 'no connection'
        try:
            cursor = conn.cursor()
            sql = 'INSERT INTO proveedores (nombre, telefono, empresa, notas) VALUES (%s,%s,%s,%s)'
            cursor.execute(sql, (nombre[:30], telefono[:15], empresa[:30], notas[:255]))
            conn.commit()
            cursor.close()
            conn.close()
            return True, 'Proveedor agregado'
        except Error as e:
            print('insert_proveedor error:', e)
            try: conn.rollback()
            except: pass
            return False, str(e)

    # PRODUCTS minimal
    def get_products(self, search_term=''):
        conn = self.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            if search_term:
                like = f"%{search_term}%"
                sql = "SELECT * FROM productos WHERE nombre LIKE %s OR codigo_barras LIKE %s LIMIT 50"
                cursor.execute(sql, (like, like))
            else:
                sql = "SELECT * FROM productos LIMIT 50"
                cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Error as e:
            print('get_products error:', e)
            return []

    # SALES minimal
    def create_sale(self, usuario_id, cart_items, total):
        conn = self.get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            now = datetime.now()
            cursor.execute('INSERT INTO ventas (idUsuario, fecha, total) VALUES (%s,%s,%s)', (usuario_id, now, total))
            sale_id = cursor.lastrowid
            for item in cart_items:
                cursor.execute('INSERT INTO ventas_detalle (idVenta, idProducto, cantidad, precio_unitario) VALUES (%s,%s,%s,%s)',
                               (sale_id, item['producto_id'], item['cantidad'], item['precio_unitario']))
                cursor.execute('UPDATE productos SET stock = stock - %s WHERE idProducto = %s', (item['cantidad'], item['producto_id']))
            conn.commit()
            cursor.close()
            conn.close()
            return sale_id
        except Error as e:
            print('create_sale error:', e)
            try: conn.rollback()
            except: pass
            return None
