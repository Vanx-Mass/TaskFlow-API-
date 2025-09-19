from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from config import Prioridade, Status

# Schemas de Entrada
class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class TarefaCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    descricao: Optional[str] = Field(None, max_length=1000)
    prioridade: Prioridade = Prioridade.MEDIA
    usuario_id: UUID

# Schemas de Resposta
class UsuarioResponse(BaseModel):
    id: UUID
    nome: str
    email: str
    data_cadastro: datetime
    
    class Config:
        orm_mode = True

class TarefaResponse(BaseModel):
    id: UUID
    titulo: str
    descricao: Optional[str]
    prioridade: Prioridade
    status: Status
    data_criacao: datetime
    data_conclusao: Optional[datetime]
    usuario_id: Optional[UUID]
    
    class Config:
        orm_mode = True

# Entidades de Domínio
class Usuario:
    def __init__(self, nome: str, email: str):
        self.id = uuid4()
        self.nome = nome
        self.email = email
        self.data_cadastro = datetime.now()

class Tarefa:
    def __init__(self, titulo: str, descricao: str = "", 
                 prioridade: Prioridade = Prioridade.MEDIA,
                 usuario_id: UUID = None):
        self.id = uuid4()
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.status = Status.PENDENTE
        self.data_criacao = datetime.now()
        self.data_conclusao = None
        self.usuario_id = usuario_id
