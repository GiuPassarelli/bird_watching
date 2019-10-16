USE bird_watching;

DROP TRIGGER IF EXISTS delecao_passaro;

DELIMITER //
CREATE TRIGGER delecao_passaro 
BEFORE UPDATE ON passaro
FOR EACH ROW
BEGIN
	IF NEW.ativo = 0 THEN
		UPDATE post_passaro
			SET ativo = 0
			WHERE id_passaro = NEW.id_passaro;
		UPDATE usuario_passaro
			SET usuario_passaro.ativo = 0
			WHERE id_passaro = NEW.id_passaro;
	END IF;
END//