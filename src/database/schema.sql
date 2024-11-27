-- Criar banco de dados se não existir
CREATE DATABASE IF NOT EXISTS apiario_db;
USE apiario_db;

-- Criar tabelas
CREATE TABLE IF NOT EXISTS produtor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco TEXT NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS apiario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    localizacao TEXT NOT NULL,
    tamanho FLOAT NOT NULL,
    floracao VARCHAR(100) NOT NULL,
    produtor_id INT NOT NULL,
    FOREIGN KEY (produtor_id) REFERENCES produtor(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS colmeia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_abelhas INT NOT NULL,
    tipo_abelhas VARCHAR(50) NOT NULL,
    data_instalacao DATE NOT NULL,
    apiario_id INT NOT NULL,
    FOREIGN KEY (apiario_id) REFERENCES apiario(id)
        ON DELETE CASCADE
);