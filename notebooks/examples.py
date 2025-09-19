# Exemplos de como usar a API
examples = {
    "criar_usuario": {
        "url": "POST /usuarios",
        "payload": {
            "nome": "Maria Silva",
            "email": "maria@email.com"
        }
    },
    "criar_tarefa": {
        "url": "POST /tarefas", 
        "payload": {
            "titulo": "Estudar FastAPI",
            "descricao": "Aprender a criar APIs REST",
            "prioridade": "alta",
            "usuario_id": "uuid-do-usuario"
        }
    }
}

print("Exemplos de uso da API TaskFlow:")
for key, example in examples.items():
    print(f"\n{example['url']}")
    print(f"Payload: {json.dumps(example['payload'], indent=2)}")
