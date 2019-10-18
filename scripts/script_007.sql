USE bird_watching;

DROP PROCEDURE IF EXISTS lista_referencias;

DELIMITER //
CREATE PROCEDURE lista_referencias(IN nome VARCHAR(80))
    BEGIN
		SELECT id_usuario INTO @id_user FROM usuario WHERE usuario.nome = nome;
		SELECT DISTINCT u.nome
        FROM usuario u,
			 post p,
			 post_usuario pu
		WHERE u.id_usuario = p.id_usuario AND p.id_post = pu.id_post AND pu.id_usuario = @id_user;
    END//
DELIMITER ;