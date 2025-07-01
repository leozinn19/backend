from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.models.filme import Filme
from app.db.database import get_all_filmes, get_filme_by_id, add_filme

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
    return get_all_filmes()

@app.post("/filmes", response_model=Filme)
def cadastrar_filme(filme: Filme):
    """Cadastra um filme."""
    return add_filme(filme)

@app.get("/filmes/{id}", response_model=Filme)
def obter_filme(id: str):
    """Retorna o filme com ID."""
    filme = get_filme_by_id(id)
    if filme is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)