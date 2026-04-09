CREATE DATABASE hospital_db;
USE hospital_db;

CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ci VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20)
);

CREATE TABLE citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    medico VARCHAR(100),
    fecha DATE,
    hora TIME,
    estado VARCHAR(20) DEFAULT 'Activa',
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);
