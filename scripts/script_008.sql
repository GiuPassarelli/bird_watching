USE bird_watching;

DROP VIEW IF EXISTS aparelho_browser;

CREATE VIEW aparelho_browser AS 
	SELECT aparelho, browser, COUNT(visualizacao.browser) AS total
    FROM visualizacao
    GROUP BY aparelho, browser;