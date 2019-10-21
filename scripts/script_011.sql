USE bird_watching;

ALTER TABLE post
    ADD COLUMN (
        likes INT NOT NULL DEFAULT 0,
        dislikes INT NOT NULL DEFAULT 0
    );

DROP TRIGGER IF EXISTS count_joinhas_insert;

DELIMITER //
CREATE TRIGGER count_joinhas_insert
BEFORE INSERT ON joinha
FOR EACH ROW
BEGIN
	IF(NEW.joinha = 0) THEN
		UPDATE post SET post.dislikes = post.dislikes + 1 WHERE post.id_post = NEW.id_post;
	END IF;
    IF(NEW.joinha = 1) THEN
		UPDATE post SET post.likes = post.likes + 1 WHERE post.id_post = NEW.id_post;
	END IF;
END//
DELIMITER ;

DROP TRIGGER IF EXISTS count_joinhas_delete;

DELIMITER //
CREATE TRIGGER count_joinhas_delete
BEFORE DELETE ON joinha
FOR EACH ROW
BEGIN
	IF(OLD.joinha = 0) THEN
		UPDATE post SET post.dislikes = post.dislikes - 1 WHERE post.id_post = OLD.id_post;
	END IF;
    IF(OLD.joinha = 1) THEN
		UPDATE post SET post.likes = post.likes - 1 WHERE post.id_post = OLD.id_post;
	END IF;
END//
DELIMITER ;

DROP TRIGGER IF EXISTS count_joinhas_update;

DELIMITER //
CREATE TRIGGER count_joinhas_update
BEFORE UPDATE ON joinha
FOR EACH ROW
BEGIN
	IF(OLD.joinha = 0) THEN
		IF(NEW.joinha = 1) THEN
			UPDATE post SET post.likes = post.likes + 1 WHERE post.id_post = NEW.id_post;
			UPDATE post SET post.dislikes = post.dislikes - 1 WHERE post.id_post = NEW.id_post;
		END IF;
		IF(NEW.joinha = 2) THEN
			UPDATE post SET post.dislikes = post.dislikes - 1 WHERE post.id_post = NEW.id_post;
		END IF;
    END IF;
	IF(OLD.joinha = 1) THEN
		IF(NEW.joinha = 0) THEN
			UPDATE post SET post.likes = post.likes - 1 WHERE post.id_post = NEW.id_post;
			UPDATE post SET post.dislikes = post.dislikes + 1 WHERE post.id_post = NEW.id_post;
		END IF;
		IF(NEW.joinha = 2) THEN
			UPDATE post SET post.likes = post.likes - 1 WHERE post.id_post = NEW.id_post;
		END IF;
    END IF;
    IF(OLD.joinha = 2) THEN
		IF(NEW.joinha = 0) THEN
			UPDATE post SET post.dislikes = post.dislikes + 1 WHERE post.id_post = NEW.id_post;
		END IF;
		IF(NEW.joinha = 1) THEN
			UPDATE post SET post.likes = post.likes + 1 WHERE post.id_post = NEW.id_post;
		END IF;
    END IF;
END//
DELIMITER ;