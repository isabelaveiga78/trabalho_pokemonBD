CREATE DATABASE Pokedex;

USE Pokedex;

CREATE TABLE Geracao (
    Regiao VARCHAR(255),
    Numero INT PRIMARY KEY
);

CREATE TABLE Pokemon (
    Numero INT,
    Nome VARCHAR(255) PRIMARY KEY,
    HP INT,
    Defesa INT,
    Ataque INT,
    Ataque_Especial INT,
    Defesa_Especial INT,
    Velocidade INT,
    BST INT,
    idGeracao INT,
    FOREIGN KEY(idGeracao) REFERENCES Geracao (Numero)
);

CREATE TABLE Tipo (
    Imunidade VARCHAR(255),
    Nome VARCHAR(255) PRIMARY KEY,
    Nome_pt VARCHAR(255) UNIQUE
);

CREATE TABLE Habilidade (
    Nome VARCHAR(255) PRIMARY KEY,
    Descricao TEXT
);

CREATE TABLE Possui (
    Pokemon VARCHAR(255),
    Habilidade VARCHAR(255),
    PRIMARY KEY (Pokemon, Habilidade),
    FOREIGN KEY(Pokemon) REFERENCES Pokemon (Nome),
    FOREIGN KEY(Habilidade) REFERENCES Habilidade (Nome)
);

CREATE TABLE Pertence (
    Pokemon VARCHAR(255),
    Tipo VARCHAR(255),
    PRIMARY KEY (Pokemon, Tipo),
    FOREIGN KEY(Tipo) REFERENCES Tipo (Nome),
    FOREIGN KEY(Pokemon) REFERENCES Pokemon (Nome)
);

CREATE TABLE Efetividade (
    Multiplicador FLOAT,
    Atacante VARCHAR(255),
    Defensor VARCHAR(255),
    PRIMARY KEY (Atacante, Defensor),
    FOREIGN KEY(Atacante) REFERENCES Tipo (Nome),
    FOREIGN KEY(Defensor) REFERENCES Tipo (Nome)
);
