# Guia de Instalação - Sistema de Inventário Angular

## Pré-requisitos

- Node.js 18+ instalado
- npm ou yarn
- Backend Flask rodando em `http://localhost:5000`

## Passo 1: Instalar Dependências

\`\`\`bash
cd angular-app
npm install
\`\`\`

## Passo 2: Verificar Configuração

O arquivo `src/app/services/api.service.ts` está configurado para conectar com:
\`\`\`
http://localhost:5000
\`\`\`

Se o backend Flask estiver em outra porta, edite este arquivo.

## Passo 3: Executar o Projeto

\`\`\`bash
npm start
\`\`\`

O aplicativo estará disponível em: `http://localhost:4200`

## Estrutura do Projeto

\`\`\`
angular-app/
├── src/
│   ├── app/
│   │   ├── components/          # Componentes reutilizáveis
│   │   │   └── sidebar/         # Sidebar de navegação
│   │   ├── pages/               # Páginas da aplicação
│   │   │   ├── dashboard/       # Dashboard principal
│   │   │   ├── produtos/        # Gestão de produtos
│   │   │   ├── produto-detalhes/# Detalhes do produto
│   │   │   ├── movimentacoes/   # Movimentações de estoque
│   │   │   ├── relatorios/      # Relatórios
│   │   │   └── alertas/         # Alertas
│   │   ├── services/            # Serviços (API)
│   │   ├── app.component.ts     # Componente raiz
│   │   └── app.routes.ts        # Configuração de rotas
│   ├── main.ts                  # Ponto de entrada
│   └── index.html               # HTML principal
├── angular.json                 # Configuração Angular
├── package.json                 # Dependências
└── tsconfig.json               # Configuração TypeScript
\`\`\`

## Arquitetura

- **Frontend**: Angular 17 com Standalone Components
- **Backend**: Flask (Python) - API REST
- **Estilização**: Tailwind CSS via CDN
- **Roteamento**: Lazy Loading para otimização

## Funcionalidades

1. Dashboard com estatísticas em tempo real
2. Gestão completa de produtos com campos específicos por tipo
3. Sistema de movimentações (entrada/saída)
4. Relatórios financeiros
5. Sistema de alertas inteligente

## Troubleshooting

### Erro de CORS
Se encontrar erros de CORS, certifique-se de que o backend Flask tem:
\`\`\`python
from flask_cors import CORS
CORS(app, origins=["http://localhost:4200"])
\`\`\`

### Porta já em uso
Se a porta 4200 estiver em uso:
\`\`\`bash
ng serve --port 4300
\`\`\`

### Erro de módulos
Se houver erros de módulos não encontrados:
\`\`\`bash
rm -rf node_modules package-lock.json
npm install
