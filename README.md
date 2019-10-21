# Bird Watching

Um mock de uma rede social de observadores de pássaros.

## Modelo de entidade relacionamento da base de dados:

![Modelo_Entidade-Relacionamento](imgs/Modelo_Entidade-Relacionamento.jpeg)

## Diagrama do modelo relacional:

![Diagrama_do_modelo_relacional](imgs/Diagrama_do_modelo_relacional_2.png)

## Dicionário de dados:
![dicionario_de_dados.png](imgs/dicionario_de_dados.png)

Informações adicionais:

Todos os PKs que não são FKs são auto-gerados por AUTO_INCREMENT, além de possuirem a restrição NOT NULL

O campo instante na visualização é auto-gerado por timestamp

Todas as tabelas possuem o campo ativo, que representa um delete lógico
