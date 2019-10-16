USE bird_watching;

DROP TRIGGER IF EXISTS delecao_usuario;

DELIMITER //
CREATE TRIGGER delecao_usuario 
BEFORE UPDATE ON usuario
FOR EACH ROW
BEGIN
	IF NEW.ativo = 0 THEN
		UPDATE post
			SET post.ativo = 0
			WHERE id_usuario = NEW.id_usuario;
		UPDATE post_passaro
			SET post_passaro.ativo = 0
			where id_post IN (SELECT id_post FROM post WHERE id_usuario = NEW.id_usuario);
		UPDATE post_usuario
			SET post_usuario.ativo = 0
			where id_post IN (SELECT id_post FROM post WHERE id_usuario = NEW.id_usuario);
		UPDATE post_usuario
			SET post_usuario.ativo = 0
			WHERE id_usuario = NEW.id_usuario;
		UPDATE vizualizacao
			SET vizualizacao.ativo = 0
			where id_post IN (SELECT id_post FROM post WHERE id_usuario = NEW.id_usuario);
		UPDATE vizualizacao
			SET vizualizacao.ativo = 0
			WHERE id_usuario = NEW.id_usuario;
		UPDATE usuario_passaro
			SET usuario_passaro.ativo = 0
			WHERE id_usuario = NEW.id_usuario;
	END IF;
        
END//   