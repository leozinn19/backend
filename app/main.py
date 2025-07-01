from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.models.filme import Filme
from app.db.database import db

app = FastAPI(
    title="API de Filmes",
    description="API REST que gerenciar filmes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API funcionando!!!"}

@app.get("/filmes", response_model=List[Filme])
def listar_filmes():
    """Retorna todos os filmes."""
    return db.list_filmes()

@app.post("/filmes", response_model=Filme)
def cadastrar_filme(filme: Filme):
    """Cadastra um filme."""
    return db.add_filme(filme)

@app.get("/filmes/{id}", response_model=Filme)
def obter_filme(id: str):
    """Retorna o filme com ID."""
    filme = db.get_filme(id)
    if filme is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme

@app.put("/filmes/{id}", response_model=Filme)
def editar_filme(id: str, filme: Filme):
    """Edita filme com ID."""
    atualizado = db.update_filme(id, filme.dict(exclude_unset=True, exclude={"id"}))
    if not atualizado:
        raise HTTPException(status_code=404, detail="Filme não encontrado para atualização")
    return atualizado

@app.delete("/filmes/{id}", status_code=204)
def remover_filme(id: str):
    """Deleta o filme com ID."""
    sucesso = db.delete_filme(id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Filme não encontrado para remoção")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)