USE bird_watching;

DROP TABLE IF EXISTS joinha;

CREATE TABLE joinha (
    id_post INT NOT NULL,
    id_usuario INT NOT NULL,
    joinha TINYINT NOT NULL CHECK (joinha BETWEEN 0 and 2),        #0: dislike, 1: like, 2: cancela
    UNIQUE (id_usuario, id_post),
    PRIMARY KEY (id_usuario, id_post),
    CONSTRAINT fk_usuario_joinha FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
        ON DELETE CASCADE,
    CONSTRAINT fk_post_joinha FOREIGN KEY (id_post)
        REFERENCES post (id_post)
        ON DELETE CASCADE
);