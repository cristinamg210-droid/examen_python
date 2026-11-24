-- Base de datos para las facturas de SUPERMERCADOS EL AHORRO

-- ATENCIÓN: esta instrucción elimina la base de datos y todos sus datos.
-- Solo se debe ejecutar si queremos crearla de nuevo desde cero.
DROP DATABASE IF EXISTS supermercado;

-- Creamos la base de datos.
CREATE DATABASE supermercado
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

-- Seleccionamos la base de datos.
USE supermercado;


-- Tabla de empleados
CREATE TABLE empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL
);


-- Tabla de productos
CREATE TABLE producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(150) NOT NULL UNIQUE
);


-- Tabla de sucursales
CREATE TABLE sucursal (
    id_sucursal INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    cif VARCHAR(15) NOT NULL,
    telefono VARCHAR(15) NOT NULL
);


-- Tabla de tickets
CREATE TABLE ticket (
    id_ticket INT AUTO_INCREMENT PRIMARY KEY,
    numero_ticket VARCHAR(20) NOT NULL UNIQUE,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    iva DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    id_sucursal INT NOT NULL,
    id_empleado INT NOT NULL,
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
);


-- Tabla de pagos
CREATE TABLE pago (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_ticket INT NOT NULL UNIQUE,
    forma_pago VARCHAR(20) NOT NULL,
    autorizacion VARCHAR(30) DEFAULT NULL,
    FOREIGN KEY (id_ticket) REFERENCES ticket(id_ticket)
);


-- Tabla con las líneas de cada ticket
-- La cantidad admite 3 decimales porque hay productos que se venden por kg.
CREATE TABLE ticket_linea (
    id_linea INT AUTO_INCREMENT PRIMARY KEY,
    id_ticket INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad DECIMAL(10,3) NOT NULL,
    importe DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_ticket) REFERENCES ticket(id_ticket),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);
