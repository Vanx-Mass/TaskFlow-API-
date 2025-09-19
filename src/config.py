from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List

class Prioridade(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media" 
    ALTA = "alta"

class Status(str, Enum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"
