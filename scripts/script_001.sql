DROP DATABASE IF EXISTS bird_watching;
CREATE DATABASE bird_watching;
USE bird_watching;

CREATE TABLE usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(80) UNIQUE,
    email VARCHAR(80),
    cidade VARCHAR(80),
    ativo TINYINT(1) NOT NULL,
    PRIMARY KEY (id_usuario)
);

CREATE TABLE passaro (
    id_passaro INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(80) UNIQUE,
    ativo TINYINT(1) NOT NULL,
    PRIMARY KEY (id_passaro)
);

#PREFERENCIA
CREATE TABLE usuario_passaro (
    id_usuario INT NOT NULL,
    id_passaro INT NOT NULL,
    ativo TINYINT(1) NOT NULL,
    UNIQUE (id_passaro, id_usuario),
    PRIMARY KEY (id_usuario, id_passaro),
	CONSTRAINT fk_usuario_pref FOREIGN KEY (id_usuario) 
        REFERENCES usuario (id_usuario)
        ON DELETE CASCADE,
	CONSTRAINT fk_passaro_pref FOREIGN KEY (id_passaro) 
        REFERENCES passaro (id_passaro)
        ON DELETE CASCADE
);

CREATE TABLE post (
    id_post INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    titulo VARCHAR(80) NOT NULL,
    texto VARCHAR(240),
    foto VARCHAR(512),
    ativo TINYINT(1) NOT NULL,
    UNIQUE (id_usuario, titulo, texto),
    PRIMARY KEY (id_post),
    FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
);

#TAGS DE PASSARO (#)
CREATE TABLE post_passaro(
    id_passaro INT NOT NULL,
    id_post INT NOT NULL,
    ativo TINYINT(1) NOT NULL,
    UNIQUE (id_passaro, id_post),
    PRIMARY KEY (id_passaro, id_post),
    CONSTRAINT fk_post_tag FOREIGN KEY (id_post) 
        REFERENCES post (id_post)
        ON DELETE CASCADE,
	CONSTRAINT fk_passaro_tag FOREIGN KEY (id_passaro) 
        REFERENCES passaro (id_passaro)
        ON DELETE CASCADE
);

#MENÇÃO (@)
CREATE TABLE post_usuario(
    id_usuario INT NOT NULL,
    id_post INT NOT NULL,
    ativo TINYINT(1) NOT NULL,
    UNIQUE (id_usuario, id_post),
    PRIMARY KEY (id_usuario, id_post),
    CONSTRAINT fk_usuario_mencao FOREIGN KEY (id_usuario) 
        REFERENCES usuario (id_usuario)
        ON DELETE CASCADE,
	CONSTRAINT fk_post_mencao FOREIGN KEY (id_post) 
        REFERENCES post (id_post)
        ON DELETE CASCADE
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