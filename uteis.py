import pymysql

#USUARIOS

def cria_usuario(conn, info):
    with conn.cursor() as cursor:
        try:
            cursor.execute("""INSERT INTO usuario (nome, email, cidade, ativo)
                           VALUES (%s, %s, %s, %s);""", (info["nome"], info["email"], info["cidade"], info["ativo"]))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {info["nome"]} na tabela usuario')

def acha_usuario(conn, info):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario WHERE nome = %s AND email = %s AND cidade = %s AND ativo = %s', 
                      (info["nome"], info["email"], info["cidade"], info["ativo"]))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario from usuario')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def remove_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM usuario WHERE id_usuario=%s', (id))

def muda_info_usuario(conn, id, info):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nome = %s, email = %s, cidade = %s, ativo = %s where id_usuario = %s',
                          (info["nome"], info["email"], info["cidade"], info["ativo"], id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar info do id {id} na tabela usuario')

#PASSAROS

def cria_passaro(conn, info):
    with conn.cursor() as cursor:
        try:
            cursor.execute("""INSERT INTO passaro (nome, ativo)
                           VALUES (%s, %s);""", (info["nome"], info["ativo"]))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {info["nome"]} na tabela passaro')

def acha_passaro(conn, info):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM passaro WHERE nome = %s AND ativo = %s', 
                      (info["nome"], info["ativo"]))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def lista_passaros(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro from passaro')
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

def remove_passaro(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM passaro WHERE id_passaro=%s', (id))

def muda_info_passaro(conn, id, info):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE passaro SET nome = %s, ativo = %s where id_passaro = %s',
                          (info["nome"], info["ativo"], id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar info do id {id} na tabela passaro')

#POSTS

def cria_post(conn, info):
    with conn.cursor() as cursor:
        try:
            cursor.execute("""INSERT INTO post (id_usuario, titulo, texto, foto, ativo)
                           VALUES (%s, %s, %s, %s, %s);""", 
                           (info["id_usuario"], info["titulo"], info["texto"], info["foto"], info["ativo"]))
            cursor.execute('SELECT id_post FROM post WHERE id_post = LAST_INSERT_ID() LIMIT 1')
            id_post = cursor.fetchone()
            parser_texto(conn, info["texto"], id_post)
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {info["titulo"]} na tabela post')

def acha_post(conn, info):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT id_post FROM post 
                       WHERE id_usuario = %s AND titulo = %s AND texto = %s AND foto = %s AND ativo = %s""", 
                       (info["id_usuario"], info["titulo"], info["texto"], info["foto"], info["ativo"]))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def lista_posts(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post from post')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def remove_post(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM post WHERE id_post=%s', (id))

def muda_info_post(conn, id, info):
    with conn.cursor() as cursor:
        try:
            cursor.execute("""UPDATE post 
                           SET id_usuario = %s, titulo = %s, texto = %s, foto = %s, ativo = %s where id_post = %s""",
                           (info["id_usuario"], info["titulo"], info["texto"], info["foto"], info["ativo"], id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar info do id {id} na tabela post')

#Visualizações

def cria_visualizacao(conn, info):
    with conn.cursor() as cursor:
        try:
            cursor.execute("""INSERT INTO visualizacao (id_usuario, id_post, aparelho, browser, ip, ativo)
                           VALUES (%s, %s, %s, %s, %s, %s);""", 
                           (info["id_usuario"], info["id_post"], info["aparelho"], info["browser"], info["ip"], info["ativo"]))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {info["id_usuario"], info["id_post"]} na tabela visualizacao')

def acha_visualizacao(conn, info):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT id_usuario, id_post, instante FROM visualizacao 
                       WHERE id_usuario = %s AND id_post = %s AND aparelho = %s AND browser = %s AND ip = %s AND ativo = %s""", 
                       (info["id_usuario"], info["id_post"], info["aparelho"], info["browser"], info["ip"], info["ativo"]))
        res = cursor.fetchone()
        if res:
            return res
        else:
            return None

def lista_visualizacao(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario, id_post, instante from visualizacao')
        res = cursor.fetchall()
        visualizacoes = tuple((x[0],x[1],x[2]) for x in res)
        return visualizacoes

def remove_visualizacao(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM visualizacao WHERE id_usuario=%s AND id_post=%s AND instante=%s', (id[0], id[1], id[2]))

def muda_info_visualizacao(conn, id, info):
    with conn.cursor() as cursor:
        try:
            cursor.execute("""UPDATE visualizacao 
                           SET id_usuario = %s, id_post = %s, aparelho = %s, browser = %s, ip = %s, ativo = %s
                           where id_usuario=%s AND id_post=%s AND instante=%s""",
                           (info["id_usuario"], info["id_post"], info["aparelho"], 
                            info["browser"], info["ip"], info["ativo"], id[0], id[1], id[2]))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar info do id {id} na tabela visualizacao')

#Preferencia(usuario_passaro)

def adiciona_usuario_passaro(conn, id_usuario, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO usuario_passaro (id_usuario, id_passaro, ativo) VALUES (%s, %s, 1)', (id_usuario, id_passaro))

def lista_usuario_de_passaro(conn, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario_passaro WHERE id_passaro=%s', (id_passaro))
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def lista_passaro_de_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM usuario_passaro WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

def remove_usuario_passaro(conn, id_usuario, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM usuario_passaro WHERE id_usuario=%s AND id_passaro=%s',(id_usuario, id_passaro))

#Parser

def parser_texto(conn, texto, id_post):
    for word in texto.split():
        if(word[0] == '#'):
            adiciona_post_passaro(conn, id_post, word[1:])
        if(word[0] == '@'):
            adiciona_post_usuario(conn, id_post, word[1:])

#Tag(post_passaro)

def adiciona_post_passaro(conn, id_post, nome_passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM passaro WHERE nome = %s', (nome_passaro))
        id_passaro = cursor.fetchone()
        cursor.execute('INSERT INTO post_passaro (id_post, id_passaro, ativo) VALUES (%s, %s, 1)', (id_post, id_passaro))

def lista_post_de_passaro(conn, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post_passaro WHERE id_passaro=%s', (id_passaro))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def lista_passaro_de_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM post_passaro WHERE id_post=%s', (id_post))
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

def remove_post_passaro(conn, id_post, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM post_passaro WHERE id_post=%s AND id_passaro=%s', (id_post, id_passaro))

#Mencao(post_usuario)

def adiciona_post_usuario(conn, id_post, nome_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario WHERE nome = %s', (nome_usuario))
        id_usuario = cursor.fetchone()
        cursor.execute('INSERT INTO post_usuario (id_post, id_usuario, ativo) VALUES (%s, %s, 1)', (id_post, id_usuario))

def lista_post_de_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post_usuario WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def lista_usuario_de_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM post_usuario WHERE id_post=%s', (id_post))
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def remove_post_usuario(conn, id_post, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM post_usuario WHERE id_post=%s AND id_usuario=%s', (id_post, id_usuario))

#Joinha

def cria_joinha(conn, id_post, id_usuario, joinha):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO joinha (id_usuario, id_post, joinha) VALUES (%s, %s, %s)', (id_usuario, id_post, joinha))

def lista_joinha_de_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM joinha WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def lista_joinha_de_post(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM joinha WHERE id_post=%s', (id_post))
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def remove_joinha(conn, id_post, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM joinha WHERE id_usuario=%s AND id_post=%s',(id_usuario, id_post))
