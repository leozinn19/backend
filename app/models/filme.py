from pydantic import BaseModel
from typing import Optional

class Filme(BaseModel):
    id: Optional[str] = None
    titulo: str
    diretor: str
    ano: int
    genero: str