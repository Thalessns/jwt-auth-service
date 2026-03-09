# JWT Auth Service

Serviço de autenticação JWT construído com FastAPI e SQLAlchemy.

## Descrição

Este é um serviço de autenticação que utiliza tokens JWT (JSON Web Token) para controle de acesso. O serviço permite criar tokens de autenticação, verificar sua validade e gerenciar grupos de acesso.

## Pré-requisitos

- Python 3.12+
- Docker e Docker Compose (opcional)
- UV (gerenciador de pacotes)

## Instalação

### Usando Docker (Recomendado)

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd jwt-auth-service
```

2. Inicie os containers:
```bash
docker compose up --build
```

3. O serviço estará disponível em: `http://localhost:5001`

### Instalação Local

1. Clone o repositório e entre no diretório:
```bash
git clone <url-do-repositorio>
cd jwt-auth-service
```

2. Instale as dependências usando UV:
```bash
pip install uv
uv sync
```

3. Configure as variáveis de ambiente (veja abaixo).

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações do aplicativo
APP_HOST=0.0.0.0
APP_PORT=5001
APP_RELOAD=False

# Configurações do JWT
JWT_KEY=sua-chave-secreta-aqui
JWT_ALGORITHM=HS256
JWT_VALID_TIME=120

# Configuração do banco de dados
CONN_URL=sqlite+aiosqlite:///src/database/data/db.sql
```

## Como Rodar a Aplicação

### Usando Docker Compose

```bash
docker-compose up --build -d
```

### Executando Localmente

```bash
# Ative o ambiente virtual (se necessário)
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Execute o servidor
uv run entrypoint.py
```

Ou diretamente com Python:
```bash
python entrypoint.py
```

O servidor será iniciado em `http://localhost:5001`

## Documentação da API

Exite uma coleção Postman na pasta `/postman` na raiz do projeto.
Após iniciar o serviço, você pode acessar a documentação interativa:

- **Swagger UI**: `http://localhost:5001/docs`
- **ReDoc**: `http://localhost:5001/redoc`

## Executando os Testes

```bash
# Usando UV
uv run pytest

# Com coverage
uv run pytest --cov=src
```
