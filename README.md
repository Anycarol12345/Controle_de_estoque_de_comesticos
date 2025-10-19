# Integra+ Estoque - Sistema de Gestão de Inventário

Sistema completo 100% Python para gerenciamento de estoque de produtos cosméticos usando FastAPI, Jinja2 e HTMX.

## 🚀 Tecnologias

- **Python 3.8+** - Linguagem principal
- **FastAPI** - Framework web moderno e rápido
- **Jinja2** - Templates HTML
- **HTMX** - Interatividade sem JavaScript complexo
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados embutido
- **Tailwind CSS** - Estilização via CDN
- **Uvicorn** - Servidor ASGI

## 📦 Estrutura do Projeto

\`\`\`
.
├── app.py                  # Aplicação principal FastAPI
├── database.py             # Configuração do banco de dados
├── models.py               # Modelos SQLAlchemy
├── requirements.txt        # Dependências Python
├── routers/                # Rotas da aplicação
│   ├── dashboard.py       # Dashboard e estatísticas
│   ├── produtos.py        # Gestão de produtos
│   ├── movimentacoes.py   # Movimentação de estoque
│   ├── relatorios.py      # Relatórios e análises
│   └── alertas.py         # Sistema de alertas
└── templates/              # Templates Jinja2
    ├── base.html          # Template base
    ├── dashboard.html     # Dashboard
    ├── produtos/          # Templates de produtos
    ├── movimentacoes/     # Templates de movimentação
    ├── relatorios/        # Templates de relatórios
    └── alertas/           # Templates de alertas
\`\`\`

## 🔧 Instalação e Execução

### 1. Clone o repositório

\`\`\`bash
git clone <seu-repositorio>
cd integra-estoque
\`\`\`

### 2. Crie um ambiente virtual

\`\`\`bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
\`\`\`

### 3. Instale as dependências

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Execute a aplicação

\`\`\`bash
python app.py
\`\`\`

A aplicação estará disponível em `http://localhost:8000`

## 🎯 Funcionalidades

### 📊 Dashboard
- Visão geral do estoque em tempo real
- Total de produtos e valor do inventário
- Alertas de estoque baixo
- Movimentações recentes
- Top produtos mais valiosos

### 📦 Gestão de Produtos
- Cadastro completo de produtos
- Campos específicos por tipo:
  - **Perfumes/Colônias**: Concentração, Subfamília, Ocasião
  - **Cremes**: Tipo de Pele, Ação/Resultado
  - **Maquiagens**: Textura, Cobertura, Fundo de Cor, Tonalidade
- Busca e filtros por marca
- Controle de preços (custo e venda)
- Cálculo automático de margem de lucro
- Gestão de estoque mínimo

### 🔄 Movimentação de Estoque
- Registro de entradas com lote e validade
- Registro de saídas com validação de estoque
- Histórico completo de movimentações
- Atualização automática do estoque

### 📈 Relatórios
- Resumo financeiro (valor total, custo, lucro potencial)
- Movimentações dos últimos 30 dias
- Distribuição de produtos por tipo
- Análise por marca
- Top 10 produtos mais movimentados
- Produtos com estoque baixo
- Produtos sem movimentação

### 🔔 Alertas
- Produtos sem estoque (crítico)
- Produtos com estoque baixo
- Produtos vencidos
- Produtos próximos do vencimento (30 dias)
- Produtos sem movimentação (90+ dias)
- Contador total de alertas ativos

## 🎨 Design

- Interface dark mode moderna
- Totalmente responsivo (desktop e mobile)
- Navegação lateral para desktop
- Navegação inferior para mobile
- Cores temáticas consistentes
- Feedback visual para ações

## 🗄️ Banco de Dados

O sistema usa SQLite com as seguintes tabelas:

### Marcas
- id, nome, ativo

### Produtos
- Informações básicas: nome, SKU, tipo, marca, categoria, linha
- Preços: custo, venda
- Estoque: quantidade, mínimo
- Campos específicos por tipo de produto
- Informações adicionais: propriedades, detalhes, ingredientes, como usar

### Movimentações
- produto_id, tipo (entrada/saída), quantidade
- lote, validade, observação, data

## 🔌 Rotas Principais

### Dashboard
- `GET /` - Dashboard principal

### Produtos
- `GET /produtos` - Lista de produtos (com filtros)
- `GET /produtos/novo` - Formulário de novo produto
- `POST /produtos/novo` - Criar produto
- `GET /produtos/{id}` - Detalhes do produto
- `POST /produtos/{id}/excluir` - Excluir produto

### Movimentações
- `GET /movimentacoes` - Página de movimentação
- `POST /movimentacoes/entrada` - Registrar entrada
- `POST /movimentacoes/saida` - Registrar saída

### Relatórios
- `GET /relatorios` - Página de relatórios

### Alertas
- `GET /alertas` - Página de alertas

## 💡 Características Técnicas

- **100% Python**: Sem necessidade de Node.js ou npm
- **Server-Side Rendering**: Templates renderizados no servidor
- **HTMX**: Interatividade moderna sem JavaScript complexo
- **Responsivo**: Funciona perfeitamente em desktop e mobile
- **Banco de dados embutido**: SQLite, sem necessidade de servidor externo
- **Validação automática**: FastAPI valida dados automaticamente
- **Documentação automática**: API docs em `/docs`

## 🚀 Deploy

### Opção 1: Servidor Local
\`\`\`bash
python app.py
\`\`\`

### Opção 2: Servidor de Produção
\`\`\`bash
uvicorn app:app --host 0.0.0.0 --port 8000
\`\`\`

### Opção 3: Docker (opcional)
\`\`\`dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
\`\`\`

## 📝 Primeiros Passos

1. Execute a aplicação
2. Acesse `http://localhost:8000`
3. O banco de dados será criado automaticamente
4. Cadastre suas primeiras marcas e produtos
5. Registre movimentações de estoque
6. Acompanhe relatórios e alertas

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📄 Licença

Este projeto está sob a licença MIT.

---

Desenvolvido com Python, FastAPI e HTMX
