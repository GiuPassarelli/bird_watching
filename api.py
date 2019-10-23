from fastapi import FastAPI
from uteis import *
import json
from pydantic import BaseModel
from starlette.requests import Request
import datetime

app = FastAPI()


with open('config_tests.json', 'r') as f:
    config = json.load(f)


conn = pymysql.connect(
    host=config['HOST'],
    user=config['USER'],
    password=config['PASS'],
    database='bird_watching'
)

class Usuario(BaseModel):
    nome: str
    email: str
    cidade: str
    ativo: bool

class Passaro(BaseModel):
    nome: str
    ativo: bool

class Post(BaseModel):
    id_usuario: int
    titulo: str
    texto: str 
    foto: str
    ativo: bool

class Visualizacao(BaseModel):
    id_usuario: int 
    id_post : int 
    instante: type(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    aparelho : str 
    browser : str
    ip : str 
    ativo: bool

class Joinha(BaseModel):
    id_usuario: int
    id_post: int
    joinha: int

#Usuário
@app.post("/user")
async def add_usuario(usuario: Usuario):
    info = {}
    info['nome'] = usuario.nome
    info['email'] = usuario.email
    info['cidade'] = usuario.cidade
    info['ativo'] = usuario.ativo

    return cria_usuario(conn, info)


@app.get('/user')
async def lista_todos_usuarios():
    return lista_usuarios(conn)
    

# Não deve ser permitido pelo sistema
@app.delete('/user/{id_usuario}')
async def deleta_usuario(id_usuario: int):
    return remove_usuario(conn, id_usuario)


@app.post('/user/{id_usuario}')
async def atualiza_usuario(id_usuario: int, usuario: Usuario):
    info = {}
    info['nome'] = usuario.nome
    info['email'] = usuario.email
    info['cidade'] = usuario.cidade
    info['ativo'] = usuario.ativo
    return muda_info_usuario(conn, id_usuario, info)


#Pássaros
@app.post("/bird")
async def add_passaro(passaro: Passaro):
    info = {}
    info['nome'] = passaro.nome
    info['ativo'] = passaro.ativo
    return cria_passaro(conn, info)


@app.get('/bird')
async def lista_todos_passaros():
    return lista_passaros(conn)
    

@app.delete('/bird/{id_passaro}')
async def deleta_passaro(id_passaro: int):
    return remove_passaro(conn, id_passaro)


@app.post('/bird/{id_passaro}')
async def atualiza_passaro(id_passaro: int, passaro: Passaro):
    info = {}
    info['nome'] = passaro.nome
    info['ativo'] = passaro.ativo
    return muda_info_passaro(conn, id_passaro, info)


#Post
@app.post("/post")
async def add_post(post: Post):
    info = {}
    info['id_usuario'] = post.id_usuario
    info['titulo'] = post.titulo
    info['texto'] = post.texto
    info['foto'] = post.foto
    info['ativo'] = post.ativo

    return cria_post(conn, info)


@app.get('/post')
async def lista_todos_posts():
    return lista_posts(conn)
    

@app.delete('/post/{id_post}')
async def deleta_post(id_post: int):
    return remove_post(conn, id_post)


@app.post('/post/{id_post}')
async def atualiza_post(id_post: int, post: Post):
    info = {}
    info['id_usuario'] = post.id_usuario
    info['titulo'] = post.titulo
    info['texto'] = post.texto
    info['foto'] = post.foto
    info['ativo'] = post.ativo

    return muda_info_post(conn, id_post, info)


#Visualizações
@app.post("/view")
async def add_visualizacao(visualizacao: Visualizacao):
    info = {}
    info['id_usuario'] = visualizacao.id_usuario
    info['id_post'] = visualizacao.id_post
    info['instante'] = visualizacao.instante
    info['aparelho'] = visualizacao.aparelho
    info['browser'] = visualizacao.browser
    info['ip'] = visualizacao.ip
    info['ativo'] = visualizacao.ativo

    return cria_visualizacao(conn, info)


@app.get('/view')
async def lista_todas_visualizacoes():
    return lista_visualizacao(conn)
    

@app.delete('/view/{id_vizualizacao}')
async def deleta_visualizacao(id_vizualizacao: int):
        return remove_visualizacao(conn, id_vizualizacao)


@app.post('/view/{id_post}')
async def atualiza_visualizacao(id_vizualizacao: int, visualizacao: Visualizacao):
    info = {}
    info['id_usuario'] = visualizacao.id_usuario
    info['id_post'] = visualizacao.id_post
    info['instante'] = visualizacao.instante
    info['aparelho'] = visualizacao.aparelho
    info['browser'] = visualizacao.browser
    info['ip'] = visualizacao.ip
    info['ativo'] = visualizacao.ativo

    return muda_info_visualizacao(conn, id_vizualizacao, info)

#Preferencia(usuario_passaro)
@app.post("/preferencia")
async def add_preferencia(id_usuario: int, id_passaro: int):
    return adiciona_usuario_passaro(conn, id_usuario, id_passaro)


@app.get('/preferencia/passaro/{id_passaro}')
async def lista_usuario_passaro(id_passaro: int):
    return lista_usuario_de_passaro(conn, id_passaro)

@app.get('/preferencia/usuario/{id_usuario}')
async def lista_passaro_usuario(id_usuario: int):
    return lista_passaro_de_usuario(conn, id_usuario)
    

@app.delete('/preferencia/{id_usuario}/{id_passaro}')
async def deleta_preferencia(id_usuario: int, id_passaro: int):
    return remove_usuario_passaro(conn, id_usuario, id_passaro)


#Tag(post_passaro)
@app.post("/tag")
async def add_tag(id_post: int, nome_passaro: str):
    return adiciona_post_passaro(conn, id_post, nome_passaro)


@app.get('/tag/passaro/{id_passaro}')
async def lista_post_passaro(id_passaro: int):
    return lista_post_de_passaro(conn, id_passaro)

@app.get('/tag/post/{id_post}')
async def lista_passaro_post(id_post: int):
    return lista_passaro_de_post(conn, id_post)


@app.delete('/tag/{id_post}/{id_passaro}')
async def deleta_tag(id_post: int, id_passaro: int):
    return remove_post_passaro(conn, id_post, id_passaro)


#Mencao(post_usuario)
@app.post("/mencao")
async def add_mencao(id_post: int, nome_usuario: str):
    return adiciona_post_usuario(conn, id_post, nome_usuario)


@app.get('/mencao/usuario/{id_usuario}')
async def lista_post_usuario(id_usuario: int):
    return lista_post_de_usuario(conn, id_usuario)

@app.get('/mencao/post/{id_post}')
async def lista_usuario_post(id_post: int):
    return lista_usuario_de_post(conn, id_post)


@app.delete('/mencao/{id_post}/{id_usuario}')
async def deleta_mencao(id_post: int, id_usuario: int):
    return remove_post_usuario(conn, id_post, id_usuario)


#Joinha
@app.post("/joinha")
async def add_joinha(joinha: Joinha):
    info = {}
    info['id_usuario'] = joinha.id_usuario
    info['id_post'] = joinha.id_post
    info['joinha'] = joinha.joinha
    return cria_joinha(conn, info)


@app.get('/joinha/{id_usuario}')
async def lista_joinha_usuario(id_usuario: int):
    return lista_joinha_de_usuario(conn, id_usuario)
    

@app.get('/joinha/{id_post}')
async def lista_joinha_post(id_post: int):
    return lista_joinha_de_post(conn, id_post)

@app.delete('/joinha/{id_usuario}/{id_post}')
async def deleta_joinha(id_usuario: int, id_post: int):
    return remove_joinha(conn, id_post, id_usuario)


@app.post('/joinha/{id_usuario}/{id_post}')
async def atualiza_joinha(id_joinha: int, joinha: Joinha):
    info = {}
    info['id_usuario'] = joinha.id_usuario
    info['id_post'] = joinha.id_post
    info['joinha'] = joinha.joinha
    return muda_info_joinha(conn, info)
