USE bird_watching;

DROP PROCEDURE IF EXISTS lista_posts;

DELIMITER //
CREATE PROCEDURE lista_posts(IN nome VARCHAR(80))
    BEGIN
        SELECT post.titulo, post.texto, post.foto
        FROM post
        INNER JOIN usuario USING(id_usuario)
        WHERE usuario.nome = nome
        ORDER BY post.instante DESC;
    END//
DELIMITER ;