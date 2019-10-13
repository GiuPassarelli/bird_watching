DROP DATABASE IF EXISTS bird_watching;
CREATE DATABASE bird_watching;
USE bird_watching;

CREATE TABLE usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(80),
    email VARCHAR(80),
    cidade VARCHAR(80),
    ativo TINYINT(1) NOT NULL,
    PRIMARY KEY (id_usuario)
);

CREATE TABLE passaro (
    id_passaro INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(80),
    ativo TINYINT(1) NOT NULL,
    PRIMARY KEY (id_passaro)
);

#PREFERENCIA
CREATE TABLE usuario_passaro (
    id_usuario INT NOT NULL,
    id_passaro INT NOT NULL,
    PRIMARY KEY (id_usuario, id_passaro),
    FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_passaro)
        REFERENCES passaro (id_passaro)
);

CREATE TABLE post (
    id_post INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    titulo VARCHAR(80) NOT NULL,
    texto VARCHAR(240),
    foto VARCHAR(512),
    ativo TINYINT(1) NOT NULL,
    PRIMARY KEY (id_post),
    FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
);

#TAGS DE PASSARO (#)
CREATE TABLE post_passaro(
    id_passaro INT NOT NULL,
    id_post INT NOT NULL,
    PRIMARY KEY (id_passaro, id_post),
    FOREIGN KEY (id_passaro)
        REFERENCES passaro (id_passaro),
    FOREIGN KEY (id_post)
        REFERENCES post (id_post)
);

#MENÇÃO (@)
CREATE TABLE post_usuario(
    id_usuario INT NOT NULL,
    id_post INT NOT NULL,
    PRIMARY KEY (id_usuario, id_post),
    FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_post)
        REFERENCES post (id_post)
);

CREATE TABLE visualizacao(
    id_usuario INT NOT NULL,
    id_post INT NOT NULL,
    instante DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    aparelho VARCHAR(80),
    browser VARCHAR(80),
    ip VARCHAR(80),
    ativo TINYINT(1) NOT NULL,
    PRIMARY KEY (id_usuario, id_post, instante),
    FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_post)
        REFERENCES post (id_post)
);