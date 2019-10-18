USE bird_watching;

DROP VIEW IF EXISTS fotos_passaros;

CREATE VIEW fotos_passaros AS
    SELECT DISTINCT foto, passaro.nome
    FROM post
    INNER JOIN post_passaro USING(id_post)
    INNER JOIN passaro USING(id_passaro);