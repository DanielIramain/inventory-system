-- DDL --
CREATE DATABASE productos;
USE productos;

CREATE TABLE Producto(
	codigo char(8) primary key,
    nombre varchar(50) not null,
    costo float(10) not null,
    precio float(10) not null,
    cantidad int(10) not null
);

CREATE TABLE ProductoElectronico(
	codigo char(8) primary key,
    categoria varchar(30),
    FOREIGN KEY (codigo) REFERENCES Producto(codigo)
);

CREATE TABLE ProductoAlimenticio(
	codigo char(8) primary key,  
    vencimiento char(20) not null,
    FOREIGN KEY (codigo) REFERENCES Producto(codigo)
);

-- Consultas --
SELECT * FROM producto;