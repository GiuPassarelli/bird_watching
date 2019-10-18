USE bird_watching;

DROP VIEW IF EXISTS popular_cidades;

CREATE VIEW popular_cidades AS
    SELECT views_user.cidade, views_user.nome, MAX(views_user.cnt_view)
    FROM (
        SELECT usuario.nome, usuario.cidade, COUNT(visualizacao.id_usuario) as cnt_view 
        FROM usuario
        INNER JOIN post USING (id_usuario)
        INNER JOIN visualizacao USING (id_post)
        GROUP BY usuario.nome) AS views_user
    GROUP BY views_user.cidade;