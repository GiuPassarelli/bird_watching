USE bird_watching;

DROP TRIGGER IF EXISTS delecao_post;

DELIMITER //
CREATE TRIGGER delecao_post 
BEFORE UPDATE ON post
FOR EACH ROW
BEGIN
	IF NEW.ativo = 0 THEN
		UPDATE post_passaro
			SET ativo = 0
			WHERE id_post = NEW.id_post;
		UPDATE post_usuario
			SET ativo = 0
			WHERE id_post = NEW.id_post;
		UPDATE vizualizacao
			SET ativo = 0
			WHERE id_post = NEW.id_post;
	END IF;
END//