import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql
from uteis import *
import datetime

#TODO: testar update em id
#      update em coluna e linha que nao existe
#      triggers
#      testar o add de um post com tag ou mencao que nao existe
#      testar relação entre post e usuario (post contem id_usuario)  ????

#Avisar leca que tirei ativo das 3 tabelas de conexao
#Nao esquecer de fazer o dicionario de dados

#Triggers a serem feitos: nao pode adicionar uma coisa que ja existe
#                         nao pode dar update para uma coisa que ja existe
#                         nao pode deixar atualizar posts para um usuario inexistente
#                         nao deixa deletar ????

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='bird_watching'
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

    #Testes para usuario:

    def test_add_user(self):
        conn = self.__class__.connection

        info1 = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        info2 = {"nome": "Ale", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        info3 = {"nome": "Alessandra", "email": "ale@email.com", "cidade": "curitiba", "ativo": 1}
        info4 = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 0}

        # Adiciona um usuario não existente.
        cria_usuario(conn, info1)

        #Tenta adicionar o mesmo usuario duas vezes.
        try:
            cria_usuario(conn, info1)
            self.fail('Nao deveria ter adicionado o mesmo usuario duas vezes.')
        except ValueError as e:
            pass

        # Checa se o usuario existe.
        id = acha_usuario(conn, info1)
        self.assertIsNotNone(id)

        # Tenta achar um usuario com nome diferente.
        id = acha_usuario(conn, info2)
        self.assertIsNone(id)

        # Tenta achar um usuario com 2 informações diferentes.
        id = acha_usuario(conn, info3)
        self.assertIsNone(id)

        # Tenta achar um usuario com ativo diferente.
        id = acha_usuario(conn, info4)
        self.assertIsNone(id)

    def test_remove_user(self):
        conn = self.__class__.connection

        info = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}

        cria_usuario(conn, info)
        id = acha_usuario(conn, info)

        res = lista_usuarios(conn)
        self.assertCountEqual(res, (id,))

        remove_usuario(conn, id)

        res = lista_usuarios(conn)
        self.assertFalse(res)

    def test_list_users(self):
        conn = self.__class__.connection

        info1 = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        info2 = {"nome": "Mario", "email": "mario@email.com", "cidade": "curitiba", "ativo": 0}
        info3 = {"nome": "Ana", "email": "ana@gmail.com", "cidade": "rio branco", "ativo": 1}

        # Verifica que ainda não tem usuarios no sistema.
        res = lista_usuarios(conn)
        self.assertFalse(res)

        # Adiciona alguns usuarios.
        usuarios_id = []
        for p in (info1, info2, info3):
            cria_usuario(conn, p)
            usuarios_id.append(acha_usuario(conn, p))

        # Verifica se os usuarios foram adicionados corretamente.
        res = lista_usuarios(conn)
        self.assertCountEqual(res, usuarios_id)

        # Remove os usuarios.
        for p in usuarios_id:
            remove_usuario(conn, p)

        # Verifica que todos os usuarios foram removidos.
        res = lista_usuarios(conn)
        self.assertFalse(res)

    def test_update_user(self):
        conn = self.__class__.connection

        info1 = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        info2 = {"nome": "Mario", "email": "mario@email.com", "cidade": "curitiba", "ativo": 0}
        info3 = {"nome": "Ana", "email": "ana@gmail.com", "cidade": "rio branco", "ativo": 1}

        cria_usuario(conn, info1)

        cria_usuario(conn, info2)
        id = acha_usuario(conn, info2)

        # Tenta mudar info para um usuario já existente.
        try:
            muda_info_usuario(conn, id, info1)
            self.fail('Não deveria ter mudado os dados para o de um usuario ja existente.')
        except ValueError as e:
            pass

        # Tenta mudar info para um usuario inexistente.
        muda_info_usuario(conn, id, info3)

        # Verifica se mudou.
        id_novo = acha_usuario(conn, info3)
        self.assertEqual(id, id_novo)

    #Testes para passaro:

    def test_add_bird(self):
        conn = self.__class__.connection

        info1 = {"nome": "gaivota", "ativo": 1}
        info2 = {"nome": "canario", "ativo": 1}
        info3 = {"nome": "gaivota", "ativo": 0}

        # Adiciona um passaro não existente.
        cria_passaro(conn, info1)

        #Tenta adicionar o mesmo passaro duas vezes.
        try:
            cria_passaro(conn, info1)
            self.fail('Nao deveria ter adicionado o mesmo passaro duas vezes.')
        except ValueError as e:
            pass

        # Checa se o passaro existe.
        id = acha_passaro(conn, info1)
        self.assertIsNotNone(id)

        # Tenta achar um passaro com nome diferente.
        id = acha_passaro(conn, info2)
        self.assertIsNone(id)

        # Tenta achar um passaro com ativo diferente.
        id = acha_passaro(conn, info3)
        self.assertIsNone(id)

    def test_remove_bird(self):
        conn = self.__class__.connection

        info = {"nome": "gaivota", "ativo": 1}

        cria_passaro(conn, info)
        id = acha_passaro(conn, info)

        res = lista_passaros(conn)
        self.assertCountEqual(res, (id,))

        remove_passaro(conn, id)

        res = lista_passaros(conn)
        self.assertFalse(res)

    def test_list_birds(self):
        conn = self.__class__.connection

        info1 = {"nome": "gaivota", "ativo": 1}
        info2 = {"nome": "canario", "ativo": 0}
        info3 = {"nome": "beija-flor", "ativo": 1}

        # Verifica que ainda não tem passaros no sistema.
        res = lista_passaros(conn)
        self.assertFalse(res)

        # Adiciona alguns passaros.
        passaros_id = []
        for p in (info1, info2, info3):
            cria_passaro(conn, p)
            passaros_id.append(acha_passaro(conn, p))

        # Verifica se os passaros foram adicionados corretamente.
        res = lista_passaros(conn)
        self.assertCountEqual(res, passaros_id)

        # Remove os passaros.
        for p in passaros_id:
            remove_passaro(conn, p)

        # Verifica que todos os passaros foram removidos.
        res = lista_passaros(conn)
        self.assertFalse(res)

    def test_update_bird(self):
        conn = self.__class__.connection

        info1 = {"nome": "gaivota", "ativo": 1}
        info2 = {"nome": "canario", "ativo": 0}
        info3 = {"nome": "beija-flor", "ativo": 1}

        cria_passaro(conn, info1)

        cria_passaro(conn, info2)
        id = acha_passaro(conn, info2)

        # Tenta mudar info para um passaro já existente.
        try:
            muda_info_passaro(conn, id, info1)
            self.fail('Não deveria ter mudado os dados para o de um passaro ja existente.')
        except ValueError as e:
            pass

        # Tenta mudar info para um passaro inexistente.
        muda_info_passaro(conn, id, info3)

        # Verifica se mudou.
        id_novo = acha_passaro(conn, info3)
        self.assertEqual(id, id_novo)

    #Testes para post:

    def test_add_post(self):
        conn = self.__class__.connection

        # Adiciona um usuario não existente.
        info_user = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        cria_usuario(conn, info_user)
        id_usuario = acha_usuario(conn, info_user)

        info1 = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 1}
        info2 = {"id_usuario": id_usuario, "titulo": "odeio passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 1}
        info3 = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a gaivota", "foto":"img.jpeg", "ativo": 1}
        info4 = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 0}
        info5 = {"id_usuario": id_usuario + 50, "titulo": "amo passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 1}

        # Adiciona um post não existente.
        cria_post(conn, info1)

        #Tenta adicionar o mesmo post duas vezes.
        try:
            cria_post(conn, info1)
            self.fail('Nao deveria ter adicionado o mesmo post duas vezes.')
        except ValueError as e:
            pass

        #Tenta adicionar um post com usuario inexistente.
        try:
            cria_post(conn, info5)
            self.fail('Nao deveria ter adicionado um post com usuario inexistente.')
        except ValueError as e:
            pass

        # Checa se o post existe.
        id = acha_post(conn, info1)
        self.assertIsNotNone(id)

        # Tenta achar um post com titulo diferente.
        id = acha_post(conn, info2)
        self.assertIsNone(id)

        # Tenta achar um post com 2 informações diferentes.
        id = acha_post(conn, info3)
        self.assertIsNone(id)

        # Tenta achar um post com ativo diferente.
        id = acha_post(conn, info4)
        self.assertIsNone(id)

        # Tenta achar um post com usuario diferente.
        id = acha_post(conn, info5)
        self.assertIsNone(id)

    def test_remove_post(self):
        conn = self.__class__.connection

        # Adiciona um usuario não existente.
        info_user = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        cria_usuario(conn, info_user)
        id_usuario = acha_usuario(conn, info_user)

        info = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 1}

        cria_post(conn, info)
        id = acha_post(conn, info)

        res = lista_posts(conn)
        self.assertCountEqual(res, (id,))

        remove_post(conn, id)

        res = lista_posts(conn)
        self.assertFalse(res)

    def test_list_posts(self):
        conn = self.__class__.connection

        # Adiciona um usuario não existente.
        info_user = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        cria_usuario(conn, info_user)
        id_usuario = acha_usuario(conn, info_user)

        info1 = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 1}
        info2 = {"id_usuario": id_usuario, "titulo": "encontrei mais um", "texto": "vi um canario", "foto":"img2.jpg", "ativo": 0}
        info3 = {"id_usuario": id_usuario, "titulo": "conheça a Linda", "texto": "nova na familia", "foto":"img3.jpg", "ativo": 1}

        # Verifica que ainda não tem posts no sistema.
        res = lista_posts(conn)
        self.assertFalse(res)

        # Adiciona alguns posts.
        posts_id = []
        for p in (info1, info2, info3):
            cria_post(conn, p)
            posts_id.append(acha_post(conn, p))

        # Verifica se os posts foram adicionados corretamente.
        res = lista_posts(conn)
        self.assertCountEqual(res, posts_id)

        # Remove os posts.
        for p in posts_id:
            remove_post(conn, p)

        # Verifica que todos os posts foram removidos.
        res = lista_posts(conn)
        self.assertFalse(res)

    def test_update_post(self):
        conn = self.__class__.connection

        # Adiciona um usuario não existente.
        info_user = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        cria_usuario(conn, info_user)
        id_usuario = acha_usuario(conn, info_user)

        info1 = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 1}
        info2 = {"id_usuario": id_usuario, "titulo": "encontrei mais um", "texto": "vi um canario", "foto":"img2.jpg", "ativo": 0}
        info3 = {"id_usuario": id_usuario, "titulo": "conheça a Linda", "texto": "nova na familia", "foto":"img3.jpg", "ativo": 1}
        info4 = {"id_usuario": id_usuario + 50, "titulo": "encontrei mais um", "texto": "vi um canario", "foto":"img2.jpg", "ativo": 0}

        cria_post(conn, info1)

        cria_post(conn, info2)
        id = acha_post(conn, info2)

        # Tenta mudar info para um post já existente.
        try:
            muda_info_post(conn, id, info1)
            self.fail('Não deveria ter mudado os dados para o de um post ja existente.')
        except ValueError as e:
            pass

        # Tenta mudar info para um usuario inexistente.
        try:
            muda_info_post(conn, id, info4)
            self.fail('Não deveria ter mudado para um usuario inexistente.')
        except ValueError as e:
            pass

        # Tenta mudar info para um post inexistente.
        muda_info_post(conn, id, info3)

        # Verifica se mudou.
        id_novo = acha_post(conn, info3)
        self.assertEqual(id, id_novo)

    #Testes para visualizacao:

    def test_add_view(self):
        conn = self.__class__.connection

        # Adiciona um usuario não existente.
        info_user = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        cria_usuario(conn, info_user)
        id_usuario = acha_usuario(conn, info_user)

        # Adiciona um post não existente.
        info_post = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 1}
        cria_post(conn, info_post)
        id_post = acha_post(conn, info_post)

        info1 = {"id_usuario": id_usuario, "id_post": id_post, "aparelho": "samsung", "browser":"Firefox", "ip": "192.168.0.0", "ativo": 1}
        info2 = {"id_usuario": id_usuario, "id_post": id_post, "aparelho": "iphone", "browser":"Firefox", "ip": "192.168.0.0", "ativo": 1}
        info3 = {"id_usuario": id_usuario, "id_post": id_post, "aparelho": "samsung", "browser":"Chrome", "ip": "192.168.0.1", "ativo": 1}
        info4 = {"id_usuario": id_usuario + 50, "id_post": id_post, "aparelho": "samsung", "browser":"Firefox", "ip": "192.168.0.0", "ativo": 1}
        info5 = {"id_usuario": id_usuario, "id_post": id_post + 50, "aparelho": "samsung", "browser":"Firefox", "ip": "192.168.0.0", "ativo": 1}

        # Adiciona uma visualizacao não existente.
        cria_visualizacao(conn, info1)

        #Tenta adicionar a mesma visualizacao duas vezes.
        try:
            cria_visualizacao(conn, info1)
            self.fail('Nao deveria ter adicionado a mesma visualizacao duas vezes.')
        except ValueError as e:
            pass

        #Tenta adicionar uma visualizacao com usuario inexistente.
        try:
            cria_visualizacao(conn, info4)
            self.fail('Nao deveria ter adicionado uma visualizacao com usuario inexistente.')
        except ValueError as e:
            pass

        #Tenta adicionar uma visualizacao com post inexistente.
        try:
            cria_visualizacao(conn, info5)
            self.fail('Nao deveria ter adicionado uma visualizacao com post inexistente.')
        except ValueError as e:
            pass

        # Checa se a visualizacao existe.
        id = acha_visualizacao(conn, info1)
        self.assertIsNotNone(id)

        # Tenta achar uma visualizacao com aparelho diferente.
        id = acha_visualizacao(conn, info2)
        self.assertIsNone(id)

        # Tenta achar uma visualizacao com 2 informações diferentes.
        id = acha_visualizacao(conn, info3)
        self.assertIsNone(id)

        # Tenta achar uma visualizacao com usuario diferente.
        id = acha_visualizacao(conn, info4)
        self.assertIsNone(id)

        # Tenta achar uma visualizacao com post diferente.
        id = acha_visualizacao(conn, info5)
        self.assertIsNone(id)

    def test_remove_view(self):
        conn = self.__class__.connection

        # Adiciona um usuario não existente.
        info_user = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        cria_usuario(conn, info_user)
        id_usuario = acha_usuario(conn, info_user)

        # Adiciona um post não existente.
        info_post = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 1}
        cria_post(conn, info_post)
        id_post = acha_post(conn, info_post)

        info = {"id_usuario": id_usuario, "id_post": id_post, "aparelho": "samsung", "browser":"Firefox", "ip": "192.168.0.0", "ativo": 1}
        
        cria_visualizacao(conn, info)
        id = acha_visualizacao(conn, info)

        res = lista_visualizacao(conn)
        self.assertCountEqual(res, (id,))

        remove_visualizacao(conn, id)

        res = lista_visualizacao(conn)
        self.assertFalse(res)

    def test_list_view(self):
        conn = self.__class__.connection

        # Adiciona um usuario não existente.
        info_user = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        cria_usuario(conn, info_user)
        id_usuario = acha_usuario(conn, info_user)

        # Adiciona um usuario não existente.
        info_user2 = {"nome": "Ale", "email": "ale@email.com", "cidade": "curitiba", "ativo": 0}
        cria_usuario(conn, info_user2)
        id_usuario2 = acha_usuario(conn, info_user2)

        # Adiciona um post não existente.
        info_post = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 1}
        cria_post(conn, info_post)
        id_post = acha_post(conn, info_post)

        # Adiciona um post não existente.
        info_post2 = {"id_usuario": id_usuario2, "titulo": "odeio passaros", "texto": "odeio a gaivota", "foto":"img.jpeg", "ativo": 0}
        cria_post(conn, info_post2)
        id_post2 = acha_post(conn, info_post2)

        info1 = {"id_usuario": id_usuario, "id_post": id_post2, "aparelho": "samsung", "browser":"Firefox", "ip": "192.168.0.0", "ativo": 1}
        info2 = {"id_usuario": id_usuario2, "id_post": id_post2, "aparelho": "iphone", "browser":"Chrome", "ip": "192.168.0.1", "ativo": 0}
        info3 = {"id_usuario": id_usuario2, "id_post": id_post, "aparelho": "DELL", "browser":"Explorer", "ip": "192.168.0.2", "ativo": 1}

        # Verifica que ainda não tem visualizacoes no sistema.
        res = lista_visualizacao(conn)
        self.assertFalse(res)

        # Adiciona algumas visualizacoes.
        views_id = []
        for p in (info1, info2, info3):
            cria_visualizacao(conn, p)
            views_id.append(acha_visualizacao(conn, p))

        # Verifica se as visualizacoes foram adicionados corretamente.
        res = lista_visualizacao(conn)
        self.assertCountEqual(res, views_id)

        # Remove as visualizacoes.
        for p in views_id:
            remove_visualizacao(conn, p)

        # Verifica que todos as visualizacoes foram removidos.
        res = lista_visualizacao(conn)
        self.assertFalse(res)

    def test_update_view(self):
        conn = self.__class__.connection

        # Adiciona um usuario não existente.
        info_user = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        cria_usuario(conn, info_user)
        id_usuario = acha_usuario(conn, info_user)

        # Adiciona um post não existente.
        info_post = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a gaivota s2", "foto":"img.jpg", "ativo": 1}
        cria_post(conn, info_post)
        id_post = acha_post(conn, info_post)

        info1 = {"id_usuario": id_usuario, "id_post": id_post, "aparelho": "iphone", "browser":"Chrome", "ip": "192.168.0.1", "ativo": 1}
        info2 = {"id_usuario": id_usuario, "id_post": id_post, "aparelho": "DELL", "browser":"Explorer", "ip": "192.168.0.2", "ativo": 1}
        info3 = {"id_usuario": id_usuario + 50, "id_post": id_post, "aparelho": "samsung", "browser":"Firefox", "ip": "192.168.0.0", "ativo": 1}
        info4 = {"id_usuario": id_usuario, "id_post": id_post + 50, "aparelho": "samsung", "browser":"Firefox", "ip": "192.168.0.0", "ativo": 1}

        cria_visualizacao(conn, info1)
        id = acha_visualizacao(conn, info1)

        # Tenta mudar info para um usuario inexistente.
        try:
            muda_info_visualizacao(conn, id, info3)
            self.fail('Não deveria ter mudado para um usuario inexistente.')
        except ValueError as e:
            pass

        # Tenta mudar info para um post inexistente.
        try:
            muda_info_visualizacao(conn, id, info4)
            self.fail('Não deveria ter mudado para um usuario inexistente.')
        except ValueError as e:
            pass

        # Tenta mudar info para uma visualizacao inexistente.
        muda_info_visualizacao(conn, id, info2)

        # Verifica se mudou.
        id_novo = acha_visualizacao(conn, info2)
        self.assertEqual(id, id_novo)

    #Testes para preferencia(usuario_passaro):

    def test_tabela_usuario_passaro(self):
        conn = self.__class__.connection

        # Cria alguns usuarios.
        info_user_1 = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        info_user_2 = {"nome": "Mario", "email": "mario@email.com", "cidade": "curitiba", "ativo": 0}

        cria_usuario(conn, info_user_1)
        id_usuario1 = acha_usuario(conn, info_user_1)

        cria_usuario(conn, info_user_2)
        id_usuario2 = acha_usuario(conn, info_user_2)

        # Cria alguns passaros.
        info_bird_1 = {"nome": "gaivota", "ativo": 1}
        info_bird_2 = {"nome": "canario", "ativo": 0}
        info_bird_3 = {"nome": "beija-flor", "ativo": 1}
        info_bird_4 = {"nome": "papagaio", "ativo": 0}     

        cria_passaro(conn, info_bird_1)
        id_bird1 = acha_passaro(conn, info_bird_1)

        cria_passaro(conn, info_bird_2)
        id_bird2 = acha_passaro(conn, info_bird_2)

        cria_passaro(conn, info_bird_3)
        id_bird3 = acha_passaro(conn, info_bird_3)

        cria_passaro(conn, info_bird_4)
        id_bird4 = acha_passaro(conn, info_bird_4)

        # Conecta usuarios e passaros.
        adiciona_usuario_passaro(conn, id_usuario1, id_bird1)
        adiciona_usuario_passaro(conn, id_usuario2, id_bird1)
        adiciona_usuario_passaro(conn, id_usuario1, id_bird4)
        adiciona_usuario_passaro(conn, id_usuario2, id_bird4)
        adiciona_usuario_passaro(conn, id_usuario1, id_bird2)
        adiciona_usuario_passaro(conn, id_usuario2, id_bird3)

        res = lista_usuario_de_passaro(conn, id_bird1)
        self.assertCountEqual(res, (id_usuario1, id_usuario2))

        res = lista_usuario_de_passaro(conn, id_bird2)
        self.assertCountEqual(res, (id_usuario1,))

        res = lista_usuario_de_passaro(conn, id_bird3)
        self.assertCountEqual(res, (id_usuario2,))

        res = lista_usuario_de_passaro(conn, id_bird4)
        self.assertCountEqual(res, (id_usuario1, id_usuario2))

        res = lista_passaro_de_usuario(conn, id_usuario1)
        self.assertCountEqual(res, (id_bird1, id_bird2, id_bird4))

        res = lista_passaro_de_usuario(conn, id_usuario2)
        self.assertCountEqual(res, (id_bird1, id_bird3, id_bird4))

        # Testa se a remoção de um usuario causa a remoção das relações entre esse usuario e seus passaros.
        remove_usuario(conn, id_usuario1)

        res = lista_usuario_de_passaro(conn, id_bird1)
        self.assertCountEqual(res, (id_usuario2,))

        res = lista_usuario_de_passaro(conn, id_bird4)
        self.assertCountEqual(res, (id_usuario2,))

        res = lista_usuario_de_passaro(conn, id_bird2)
        self.assertFalse(res)

        # Testa se a remoção de um passaro causa a remoção das relações entre esse passaro e seus usuarios.
        remove_passaro(conn, id_bird4)

        res = lista_passaro_de_usuario(conn, id_usuario2)
        self.assertCountEqual(res, (id_bird1, id_bird3))

        # Testa a remoção específica de uma relação usuario-passaro.
        remove_usuario_passaro(conn, id_usuario2, id_bird1)

        res = lista_passaro_de_usuario(conn, id_usuario2)
        self.assertCountEqual(res, (id_bird3,))

    #Testes para tag(post_passaro):

    def test_tabela_post_passaro(self):
        conn = self.__class__.connection

        # Cria alguns passaros.
        info_bird_1 = {"nome": "gaivota", "ativo": 1}
        info_bird_2 = {"nome": "canario", "ativo": 1}
        info_bird_3 = {"nome": "arara", "ativo": 1}
        info_bird_4 = {"nome": "corvo", "ativo": 1}

        cria_passaro(conn, info_bird_1)
        id_bird1 = acha_passaro(conn, info_bird_1)

        cria_passaro(conn, info_bird_2)
        id_bird2 = acha_passaro(conn, info_bird_2)

        cria_passaro(conn, info_bird_3)
        id_bird3 = acha_passaro(conn, info_bird_3)

        cria_passaro(conn, info_bird_4)
        id_bird4 = acha_passaro(conn, info_bird_4)

        # Cria alguns posts.

        # Adiciona um usuario não existente.
        info_user = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        cria_usuario(conn, info_user)
        id_usuario = acha_usuario(conn, info_user)

        info_post_1 = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a #gaivota #arara #corvo s2", "foto":"img.jpg", "ativo": 1}
        info_post_2 = {"id_usuario": id_usuario, "titulo": "encontrei mais um", "texto": "vi um #arara #corvo #canario", "foto":"img2.jpg", "ativo": 1}

        cria_post(conn, info_post_1)
        id_post1 = acha_post(conn, info_post_1)

        cria_post(conn, info_post_2)
        id_post2 = acha_post(conn, info_post_2)

        # Testa se adicionou a tabela post_passaro
        res = lista_post_de_passaro(conn, id_bird1)
        self.assertCountEqual(res, (id_post1,))

        res = lista_post_de_passaro(conn, id_bird2)
        self.assertCountEqual(res, (id_post2,))

        res = lista_post_de_passaro(conn, id_bird3)
        self.assertCountEqual(res, (id_post1, id_post2))

        res = lista_post_de_passaro(conn, id_bird4)
        self.assertCountEqual(res, (id_post1, id_post2))

        res = lista_passaro_de_post(conn, id_post1)
        self.assertCountEqual(res, (id_bird1, id_bird3, id_bird4))

        res = lista_passaro_de_post(conn, id_post2)
        self.assertCountEqual(res, (id_bird2, id_bird3, id_bird4))

        # Testa se a remoção de um post causa a remoção das relações entre esse post e seus passaros.
        remove_post(conn, id_post2)

        res = lista_post_de_passaro(conn, id_bird3)
        self.assertCountEqual(res, (id_post1,))

        res = lista_post_de_passaro(conn, id_bird4)
        self.assertCountEqual(res, (id_post1,))

        res = lista_post_de_passaro(conn, id_bird2)
        self.assertFalse(res)

        # Testa se a remoção de um passaro causa a remoção das relações entre esse passaro e seus posts.
        remove_passaro(conn, id_bird4)

        res = lista_passaro_de_post(conn, id_post1)
        self.assertCountEqual(res, (id_bird1, id_bird3))

        # Testa a remoção específica de uma relação post-passaro.
        remove_post_passaro(conn, id_post1, id_bird1)

        res = lista_passaro_de_post(conn, id_post1)
        self.assertCountEqual(res, (id_bird3,))

    #Testes para mencao(post_usuario):

    def test_tabela_post_usuario(self):
        conn = self.__class__.connection

        # Cria alguns usuarios.
        info_user_1 = {"nome": "Mario", "email": "mario@email.com", "cidade": "curitiba", "ativo": 1}
        info_user_2 = {"nome": "Isabela", "email": "isabela@gmail.com", "cidade": "rio branco", "ativo": 1}
        info_user_3 = {"nome": "Marcia", "email": "marcia@email.com", "cidade": "rio de janeiro", "ativo": 1}
        info_user_4 = {"nome": "Joao", "email": "joao@gmail.com", "cidade": "salvador", "ativo": 1}

        cria_usuario(conn, info_user_1)
        id_user1 = acha_usuario(conn, info_user_1)

        cria_usuario(conn, info_user_2)
        id_user2 = acha_usuario(conn, info_user_2)

        cria_usuario(conn, info_user_3)
        id_user3 = acha_usuario(conn, info_user_3)

        cria_usuario(conn, info_user_4)
        id_user4 = acha_usuario(conn, info_user_4)

        # Cria alguns posts.

        # Adiciona um usuario não existente.
        info_user = {"nome": "Alessandra", "email": "email@email.com", "cidade": "sao paulo", "ativo": 1}
        cria_usuario(conn, info_user)
        id_usuario = acha_usuario(conn, info_user)

        info_post_1 = {"id_usuario": id_usuario, "titulo": "amo passaros", "texto": "adoro a @Mario @Marcia @Joao s2", "foto":"img.jpg", "ativo": 1}
        info_post_2 = {"id_usuario": id_usuario, "titulo": "encontrei mais um", "texto": "vi um @Marcia @Joao @Isabela", "foto":"img2.jpg", "ativo": 1}

        cria_post(conn, info_post_1)
        id_post1 = acha_post(conn, info_post_1)

        cria_post(conn, info_post_2)
        id_post2 = acha_post(conn, info_post_2)

        # Testa se adicionou a tabela post_usuario
        res = lista_post_de_usuario(conn, id_user1)
        self.assertCountEqual(res, (id_post1,))

        res = lista_post_de_usuario(conn, id_user2)
        self.assertCountEqual(res, (id_post2,))

        res = lista_post_de_usuario(conn, id_user3)
        self.assertCountEqual(res, (id_post1, id_post2))

        res = lista_post_de_usuario(conn, id_user4)
        self.assertCountEqual(res, (id_post1, id_post2))

        res = lista_usuario_de_post(conn, id_post1)
        self.assertCountEqual(res, (id_user1, id_user3, id_user4))

        res = lista_usuario_de_post(conn, id_post2)
        self.assertCountEqual(res, (id_user2, id_user3, id_user4))

        # Testa se a remoção de um post causa a remoção das relações entre esse post e seus usuarios.
        remove_post(conn, id_post2)

        res = lista_post_de_usuario(conn, id_user3)
        self.assertCountEqual(res, (id_post1,))

        res = lista_post_de_usuario(conn, id_user4)
        self.assertCountEqual(res, (id_post1,))

        res = lista_post_de_usuario(conn, id_user2)
        self.assertFalse(res)

        # Testa se a remoção de um usuario causa a remoção das relações entre esse usuario e seus posts.
        remove_usuario(conn, id_user4)

        res = lista_usuario_de_post(conn, id_post1)
        self.assertCountEqual(res, (id_user1, id_user3))

        # Testa a remoção específica de uma relação post-usuario.
        remove_post_usuario(conn, id_post1, id_user1)

        res = lista_usuario_de_post(conn, id_post1)
        self.assertCountEqual(res, (id_user3,))


def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir() 
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
