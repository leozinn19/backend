import sqlite3
import os
from typing import List, Optional
from app.models.filme import Filme

DATABASE_FILE = "data/filmes.db"

class Database:
    def __init__(self, path: str = DATABASE_FILE):
        """Inicializa o db e cria a tabela de filmes."""
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._init_db()

    def _get_conn(self):
        """Retorna uma conexão com o db."""
        return sqlite3.connect(self.path)

    def _init_db(self):
        """Cria a tabela de filmes caso não exista."""
        conn = self._get_conn()
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

    def list_filmes(self) -> List[Filme]:
        """Lista todos os filmes."""
        conn = self._get_conn()
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

    def get_filme(self, filme_id: str) -> Optional[Filme]:
        """Buscar filme por ID."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, titulo, diretor, ano, genero FROM filmes WHERE id = ?",
            (filme_id,)
        )
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

    def add_filme(self, filme: Filme) -> Filme:
        """Adiciona um novo filme ao db."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO filmes (titulo, diretor, ano, genero) VALUES (?, ?, ?, ?)",
            (filme.titulo, filme.diretor, filme.ano, filme.genero)
        )
        filme.id = str(cursor.lastrowid)
        conn.commit()
        conn.close()
        return filme

    def update_filme(self, filme_id: str, dados: dict) -> Optional[Filme]:
        """Atualiza um filme existente."""
        campos = ", ".join(f"{k}=?" for k in dados.keys())
        valores = list(dados.values())
        valores.append(filme_id)
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE filmes SET {campos} WHERE id = ?", valores)
        conn.commit()
        updated = cursor.rowcount
        conn.close()
        if updated:
            return self.get_filme(filme_id)
        return None

    def delete_filme(self, filme_id: str) -> bool:
        """Remove um filme pelo ID."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM filmes WHERE id = ?", (filme_id,))
        conn.commit()
        deleted = cursor.rowcount
        conn.close()
        return bool(deleted)

db = Database()
