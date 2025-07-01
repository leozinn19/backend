import sqlite3
import os
from typing import List
from app.models.filme import Filme

DATABASE_FILE = "data/filmes.db"

def init_database():
    """Inicializa o db e cria a tabela de filmes."""
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            diretor TEXT NOT NULL,
            ano INTEGER NOT NULL,
            genero TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def get_connection():
    """Retorna uma conexão com o db."""
    return sqlite3.connect(DATABASE_FILE)

def get_all_filmes() -> List[Filme]:
    """Lista todos os filmes."""
    init_database()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, titulo, diretor, ano, genero FROM filmes")
    rows = cursor.fetchall()
    
    conn.close()
    
    filmes = []
    for row in rows:
        filme = Filme(
            id=str(row[0]),
            titulo=row[1],
            diretor=row[2],
            ano=row[3],
            genero=row[4]
        )
        filmes.append(filme)
    
    return filmes

def get_filme_by_id(filme_id: str) -> Filme | None:
    """Buscar fime por ID."""
    init_database()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, titulo, diretor, ano, genero FROM filmes WHERE id = ?", (filme_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return Filme(
            id=str(row[0]),
            titulo=row[1],
            diretor=row[2],
            ano=row[3],
            genero=row[4]
        )
    
    return None

def add_filme(filme: Filme) -> Filme:
    """Adiciona um novo filme ao db."""
    init_database()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO filmes (titulo, diretor, ano, genero) VALUES (?, ?, ?, ?)",
        (filme.titulo, filme.diretor, filme.ano, filme.genero)
    )
    
    filme.id = str(cursor.lastrowid)
    
    conn.commit()
    conn.close()
    
    return filme