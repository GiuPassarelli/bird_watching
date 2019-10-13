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

#TODO: testar update em id
#      update em coluna e linha que nao existe
#      triggers
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

        # Tenta achar um post com nome diferente.
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
        info4 = {"id_usuario": id_usuario + 10, "titulo": "encontrei mais um", "texto": "vi um canario", "foto":"img2.jpg", "ativo": 0}

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
            muda_info_post(conn, id, info1)
            self.fail('Não deveria ter mudado para um usuario inexistente.')
        except ValueError as e:
            pass

        # Tenta mudar info para um post inexistente.
        muda_info_post(conn, id, info3)

        # Verifica se mudou.
        id_novo = acha_post(conn, info3)
        self.assertEqual(id, id_novo)

    #Testes para visualizacao:


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
