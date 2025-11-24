CREATE DATABASE IF NOT EXISTS jimak2;
USE jimak2;
CREATE TABLE usuarios (id INT PRIMARY KEY AUTO_INCREMENT, nombre VARCHAR(30) NOT NULL, username VARCHAR(30) NOT NULL UNIQUE, email VARCHAR(30) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, rol ENUM('admin','vendedor') NOT NULL);
CREATE TABLE productos (id INT PRIMARY KEY AUTO_INCREMENT, codigo_barras VARCHAR(20) NOT NULL UNIQUE, nombre VARCHAR(50) NOT NULL, categoria VARCHAR(20) NOT NULL, precio DECIMAL(6,2) NOT NULL, stock INT NOT NULL DEFAULT 0);
CREATE TABLE proveedores (id INT PRIMARY KEY AUTO_INCREMENT, nombre VARCHAR(30) NOT NULL, telefono VARCHAR(15) NOT NULL, empresa VARCHAR(30), notas VARCHAR(100));
CREATE TABLE ventas (idVenta INT PRIMARY KEY AUTO_INCREMENT, idUsuario INT, fecha DATETIME, total DECIMAL(6,2), FOREIGN KEY (idUsuario) REFERENCES usuarios(id));
CREATE TABLE ventas_detalle (idDetalle INT PRIMARY KEY AUTO_INCREMENT, idVenta INT, idProducto INT, cantidad INT, precio_unitario DECIMAL(6,2), FOREIGN KEY (idVenta) REFERENCES ventas(idVenta), FOREIGN KEY (idProducto) REFERENCES productos(id));
CREATE TABLE stock_movimientos (idMovimiento INT PRIMARY KEY AUTO_INCREMENT, idProducto INT, tipo ENUM('entrada','salida'), cantidad INT, fecha DATETIME, notas VARCHAR(255), FOREIGN KEY (idProducto) REFERENCES productos(id));
