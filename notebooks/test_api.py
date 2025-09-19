# Célula 1: Instalar dependências e iniciar API
!pip install fastapi uvicorn python-multipart requests
!uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload &

# Célula 2: Aguardar API e imports
import requests
import json
import time
from uuid import UUID

print("⏳ Aguardando API iniciar...")
time.sleep(5)  # Aguarda 5 segundos
BASE_URL = "http://localhost:8000"

# Testar se API está respondendo
try:
    health = requests.get(f"{BASE_URL}/health")
    print(f"✅ API Health: {health.status_code} - {health.json()}")
except:
    print("❌ API não está respondendo")
    print("Execute primeiro: !uvicorn src.main:app --reload")

# Célula 3: Testar criação de usuário
print("\n👤 Testando criação de usuário...")
payload = {"nome": "João Silva", "email": "joao@email.com"}
response = requests.post(f"{BASE_URL}/usuarios", json=payload)

if response.status_code == 201:
    print("✅ Usuário criado com sucesso!")
    usuario = response.json()
    print(f"ID: {usuario['id']}")
    print(f"Nome: {usuario['nome']}")
    print(f"Email: {usuario['email']}")
else:
    print(f"❌ Erro ao criar usuário: {response.status_code}")
    print(response.json())

# Célula 4: Testar criação de tarefa
print("\n📝 Testando criação de tarefa...")
usuario_id = response.json()["id"]
payload = {
    "titulo": "Estudar Python",
    "descricao": "Completar curso de FastAPI",
    "prioridade": "alta",
    "usuario_id": usuario_id
}

response = requests.post(f"{BASE_URL}/tarefas", json=payload)

if response.status_code == 201:
    print("✅ Tarefa criada com sucesso!")
    tarefa = response.json()
    print(f"ID: {tarefa['id']}")
    print(f"Título: {tarefa['titulo']}")
    print(f"Status: {tarefa['status']}")
    print(f"Prioridade: {tarefa['prioridade']}")
else:
    print(f"❌ Erro ao criar tarefa: {response.status_code}")
    print(response.json())

# Célula 5: Testar listagem
print("\n📋 Testando listagem de tarefas do usuário...")
response = requests.get(f"{BASE_URL}/usuarios/{usuario_id}/tarefas")
if response.status_code == 200:
    tarefas = response.json()
    print(f"✅ Usuário tem {len(tarefas)} tarefa(s):")
    for tarefa in tarefas:
        print(f"  - {tarefa['titulo']} ({tarefa['status']})")
else:
    print(f"❌ Erro ao listar tarefas: {response.status_code}")

print(f"\n🌐 Documentação disponível em: {BASE_URL}/docs")
