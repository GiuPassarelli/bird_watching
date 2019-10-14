# Bird Watching

Um mock de uma rede social de observadores de pássaros.

Na primeira imagem temos o modelo de entidade relacionamento da base de dados:

![Modelo_Entidade-Relacionamento](imgs/Modelo_Entidade-Relacionamento.jpeg)

Na segunda imagem temos o diagrama do modelo relacional:

![Diagrama_do_modelo_relacional](imgs/Diagrama_do_modelo_relacional.jpeg)

Por fim temos o dicionário de dados para melhor compreensão:
![dicionario_de_dados.png](dicionario_de_dados.png)

Informações adicionais:

Todos os PKs que não são FKs são auto-gerados por AUTO_INCREMENT, além de possuirem a restrição NOT NULL

O campo instante na visualização é auto-gerado por timestamp

Todas as tabelas possuem o campo ativo, que representa um delete lógico
