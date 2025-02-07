# database.py
import sqlite3
from sqlite3 import IntegrityError
from datetime import datetime
import pandas as pd

# Conecta ao banco de dados
def conecta_banco():
    conn = sqlite3.connect("campeonato_escalada.db")
    return conn

# Inicializa as tabelas do banco de dados com a estrutura correta
def inicializa_banco():
    conn = conecta_banco()
    cursor = conn.cursor()
    
    # Criação da tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT,
            sexo TEXT
        )
    ''')

    # Criação da tabela de boulders com coluna de pontuação
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boulders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            pontuacao INTEGER NOT NULL  -- Nova coluna de pontuação
        )
    ''')

    # Criação da tabela de pontuações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pontuacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            boulder_id INTEGER,
            tipo_pontuacao TEXT,
            data TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (boulder_id) REFERENCES boulders (id)
        )
    ''')

    conn.commit()
    conn.close()

# Funções de CRUD para a tabela de usuários
def adicionar_usuario(nome, categoria, sexo):
    conn = conecta_banco()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, categoria, sexo) VALUES (?, ?, ?)", (nome, categoria, sexo))
        conn.commit()
    except IntegrityError:
        print("Erro: Não foi possível cadastrar o usuário.")
    conn.close()

def listar_usuarios():
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def remover_usuario(usuario_id):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conn.commit()
    conn.close()

# Funções para a tabela de boulders
def adicionar_boulder(nome, pontuacao):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO boulders (nome, pontuacao) VALUES (?, ?)", (nome, pontuacao))
    conn.commit()
    conn.close()


def listar_boulders():
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM boulders")
    boulders = cursor.fetchall()
    conn.close()
    return boulders

def remover_boulder(boulder_id):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM boulders WHERE id = ?", (boulder_id,))
    conn.commit()
    conn.close()

# Funções para pontuações
def adicionar_pontuacao(usuario_id, boulder_id, tipo_pontuacao):
    conn = conecta_banco()
    cursor = conn.cursor()
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO pontuacoes (usuario_id, boulder_id, tipo_pontuacao, data) VALUES (?, ?, ?, ?)", 
                   (usuario_id, boulder_id, tipo_pontuacao, data))
    conn.commit()
    conn.close()

def listar_pontuacoes_por_usuario(usuario_id):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, b.nome, p.tipo_pontuacao, p.data
        FROM pontuacoes p
        JOIN boulders b ON p.boulder_id = b.id
        WHERE p.usuario_id = ?
        ORDER BY p.data DESC
    ''', (usuario_id,))
    pontuacoes = cursor.fetchall()
    conn.close()
    return pontuacoes

def atualizar_pontuacao(pontuacao_id, boulder_id, tipo_pontuacao):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE pontuacoes 
        SET boulder_id = ?, tipo_pontuacao = ?
        WHERE id = ?
    ''', (boulder_id, tipo_pontuacao, pontuacao_id))
    conn.commit()
    conn.close()

def remover_pontuacao(pontuacao_id):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pontuacoes WHERE id = ?", (pontuacao_id,))
    conn.commit()
    conn.close()

def verificar_nome_existente(nome):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] > 0

def verificar_boulder_existente(nome):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM boulders WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] > 0

def calcular_ranking():
    conn = conecta_banco()
    cursor = conn.cursor()
    
    cursor.execute('''
        WITH top_scores AS (
            SELECT u.id AS usuario_id, 
                   u.nome AS Nome,
                   u.categoria AS Categoria, 
                   u.sexo AS Sexo,
                   CASE 
                       WHEN p.tipo_pontuacao = 'Flash' THEN b.pontuacao
                       WHEN p.tipo_pontuacao = 'Cadena' THEN b.pontuacao - 200
                       ELSE 0
                   END AS Pontuacao,
                   ROW_NUMBER() OVER(PARTITION BY u.id ORDER BY 
                       CASE 
                           WHEN p.tipo_pontuacao = 'Flash' THEN b.pontuacao
                           WHEN p.tipo_pontuacao = 'Cadena' THEN b.pontuacao - 200
                           ELSE 0
                       END DESC) AS ranking_pontuacao
            FROM usuarios u
            LEFT JOIN pontuacoes p ON u.id = p.usuario_id
            LEFT JOIN boulders b ON p.boulder_id = b.id
        )
        SELECT Nome, Categoria, Sexo, 
               SUM(Pontuacao) as Pontuacao_Total
        FROM top_scores
        WHERE ranking_pontuacao <= 10
        GROUP BY usuario_id
        ORDER BY Pontuacao_Total DESC
    ''')
    
    ranking = cursor.fetchall()
    conn.close()

    # Convertendo os resultados em um DataFrame com rótulos de coluna e posição
    ranking_df = pd.DataFrame(ranking, columns=["Nome", "Categoria", "Gênero", "Pontuação Total"])
    ranking_df.index = ranking_df.index + 1
    ranking_df.index = ranking_df.index.astype(str) + "º"
    ranking_df.index.name = "Colocação"
    
    return ranking_df


    # Verifica se já existe uma pontuação do tipo "Flash" para o participante e boulder
def verificar_flash_existente(usuario_id, boulder_id):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM pontuacoes 
        WHERE usuario_id = ? AND boulder_id = ? AND tipo_pontuacao = "Flash"
    ''', (usuario_id, boulder_id))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado > 0  # Retorna True se já existe um lançamento "Flash"

# Verifica se já existe qualquer tipo de pontuação para o participante e boulder
def verificar_pontuacao_existente(usuario_id, boulder_id):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM pontuacoes 
        WHERE usuario_id = ? AND boulder_id = ?
    ''', (usuario_id, boulder_id))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado > 0  # Retorna True se já existe alguma pontuação

# Verifica se o participante tem apenas lançamentos de "Insucesso" para o boulder
def verificar_somente_insucesso(usuario_id, boulder_id):
    conn = conecta_banco()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tipo_pontuacao FROM pontuacoes 
        WHERE usuario_id = ? AND boulder_id = ?
    ''', (usuario_id, boulder_id))
    pontuacoes = cursor.fetchall()
    conn.close()

    # Retorna True apenas se todas as pontuações forem "Insucesso"
    return all(p[0] == "Insucesso" for p in pontuacoes)

# Inicialização do banco de dados na primeira execução
inicializa_banco()