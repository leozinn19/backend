Uma API REST para gerenciamento de filmes.
Desenvolvida com FastAPI, Docker e SQLite.

Funcionalidades:
- Crud - criar, ler, atualizar e deletar filmes.
- Api - endpoints bem definidos seguindo padrões REST.
- Persistência SQLite - dados salvos em banco de dados SQLite.
- Docker - containerização completa da aplicação

Execução com Docker:

    Pré requisitos (para executar):
    - docker e docker compose

    Execute a aplicação
    docker-compose up

    A API estará disponivel em: http://localhost:8000

Executando Localmente:

    Recomendado
    - inicie uma maquina virtual utilizando o comando: 
        python -m venv venv

    - Ative o ambiente virtual:
        Windows: venv\Scripts\activate. 
        macOS e Linux: source venv/bin/activate

    - Instale as dependências:
        pip install -r requirements.txt

    - Execute a aplicação:
        python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Após executar a aplicação, acesse:
http://localhost:8000/docs