from typing import List, Optional
from uuid import UUID
from models import Usuario, Tarefa
from config import Status

class UsuarioService:
    def __init__(self):
        self.usuarios: List[Usuario] = []
    
    def criar_usuario(self, nome: str, email: str) -> Usuario:
        usuario = Usuario(nome, email)
        self.usuarios.append(usuario)
        return usuario
    
    def buscar_por_id(self, usuario_id: UUID) -> Optional[Usuario]:
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None
    
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        for usuario in self.usuarios:
            if usuario.email == email:
                return usuario
        return None

class TarefaService:
    def __init__(self):
        self.tarefas: List[Tarefa] = []
    
    def criar_tarefa(self, titulo: str, descricao: str = "", 
                    prioridade: Prioridade = Prioridade.MEDIA,
                    usuario_id: UUID = None) -> Tarefa:
        tarefa = Tarefa(titulo, descricao, prioridade, usuario_id)
        self.tarefas.append(tarefa)
        return tarefa
    
    def buscar_por_id(self, tarefa_id: UUID) -> Optional[Tarefa]:
        for tarefa in self.tarefas:
            if tarefa.id == tarefa_id:
                return tarefa
        return None
    
    def listar_por_usuario(self, usuario_id: UUID) -> List[Tarefa]:
        return [t for t in self.tarefas if t.usuario_id == usuario_id]
    
    def concluir_tarefa(self, tarefa_id: UUID) -> Optional[Tarefa]:
        tarefa = self.buscar_por_id(tarefa_id)
        if tarefa:
            tarefa.status = Status.CONCLUIDA
            tarefa.data_conclusao = datetime.now()
            return tarefa
        return None

class SistemaGerenciador:
    def __init__(self):
        self.usuario_service = UsuarioService()
        self.tarefa_service = TarefaService()
    
    def relatorio_estatisticas(self) -> dict:
        total_tarefas = len(self.tarefa_service.tarefas)
        concluidas = sum(1 for t in self.tarefa_service.tarefas 
                        if t.status == Status.CONCLUIDA)
        
        return {
            "total_usuarios": len(self.usuario_service.usuarios),
            "total_tarefas": total_tarefas,
            "tarefas_concluidas": concluidas,
            "tarefas_pendentes": total_tarefas - concluidas
        }
