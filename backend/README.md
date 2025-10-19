# Integra+ Backend API

Backend em Python com FastAPI para o sistema de controle de estoque.

## Instalação

1. Instale as dependências:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Executar o servidor

\`\`\`bash
cd backend
python main.py
\`\`\`

O servidor estará disponível em: http://localhost:8000

## Documentação da API

Acesse a documentação interativa em: http://localhost:8000/docs

## Estrutura

- `main.py` - Aplicação principal FastAPI
- `database.py` - Modelos e configuração do banco de dados
- `schemas.py` - Schemas Pydantic para validação
- `routers/` - Endpoints da API organizados por módulo
