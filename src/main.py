from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from uuid import UUID
from typing import List

from models import UsuarioCreate, TarefaCreate, UsuarioResponse, TarefaResponse
from services import SistemaGerenciador

app = FastAPI(
    title="TaskFlow API",
    description="Sistema de gerenciamento de tarefas com FastAPI",
    version="1.0.0"
)

def get_sistema():
    return SistemaGerenciador()

@app.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario_data: UsuarioCreate, sistema: SistemaGerenciador = Depends(get_sistema)):
    if sistema.usuario_service.buscar_por_email(usuario_data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    usuario = sistema.usuario_service.criar_usuario(usuario_data.nome, usuario_data.email)
    return usuario

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: UUID, sistema: SistemaGerenciador = Depends(get_sistema)):
    usuario = sistema.usuario_service.buscar_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@app.post("/tarefas", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa_data: TarefaCreate, sistema: SistemaGerenciador = Depends(get_sistema)):
    if not sistema.usuario_service.buscar_por_id(tarefa_data.usuario_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    tarefa = sistema.tarefa_service.criar_tarefa(
        tarefa_data.titulo,
        tarefa_data.descricao or "",
        tarefa_data.prioridade,
        tarefa_data.usuario_id
    )
    return tarefa

@app.get("/tarefas/{tarefa_id}", response_model=TarefaResponse)
def buscar_tarefa(tarefa_id: UUID, sistema: SistemaGerenciador = Depends(get_sistema)):
    tarefa = sistema.tarefa_service.buscar_por_id(tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.get("/usuarios/{usuario_id}/tarefas", response_model=List[TarefaResponse])
def listar_tarefas_usuario(usuario_id: UUID, sistema: SistemaGerenciador = Depends(get_sistema)):
    if not sistema.usuario_service.buscar_por_id(usuario_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return sistema.tarefa_service.listar_por_usuario(usuario_id)

@app.patch("/tarefas/{tarefa_id}/concluir", response_model=TarefaResponse)
def concluir_tarefa(tarefa_id: UUID, sistema: SistemaGerenciador = Depends(get_sistema)):
    tarefa = sistema.tarefa_service.concluir_tarefa(tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.get("/estatisticas")
def obter_estatisticas(sistema: SistemaGerenciador = Depends(get_sistema)):
    return sistema.relatorio_estatisticas()

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
