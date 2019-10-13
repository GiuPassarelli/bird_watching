import pymysql

#USUARIOS

def cria_usuario(connection, info):
    with connection.cursor() as cursor:
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

def cria_passaro(connection, info):
    with connection.cursor() as cursor:
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

def cria_post(connection, info):
    with connection.cursor() as cursor:
        try:
            cursor.execute("""INSERT INTO post (id_usuario, titulo, texto, foto, ativo)
                           VALUES (%s, %s, %s, %s, %s);""", 
                           (info["id_usuario"], info["titulo"], info["texto"], info["foto"], info["ativo"]))
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