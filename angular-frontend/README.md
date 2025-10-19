# Integra+ Estoque - Frontend Angular

Sistema completo de gestão de estoque desenvolvido com Angular 17 e Tailwind CSS.

## Requisitos

- Node.js 18+
- npm ou yarn
- Backend Python/FastAPI rodando em http://localhost:8000

## Instalação

\`\`\`bash
# Instalar dependências
npm install

# Rodar em desenvolvimento
npm start

# Acessar em http://localhost:4200
\`\`\`

## Build para Produção

\`\`\`bash
npm run build
\`\`\`

Os arquivos serão gerados em \`dist/integra-estoque/\`.

## Estrutura do Projeto

\`\`\`
angular-frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   └── sidebar/           # Navegação lateral
│   │   ├── pages/
│   │   │   ├── dashboard/         # Dashboard com estatísticas
│   │   │   ├── produtos/          # Listagem de produtos
│   │   │   ├── produto-detalhes/  # Detalhes do produto
│   │   │   ├── movimentacoes/     # Entrada e saída
│   │   │   ├── relatorios/        # Relatórios financeiros
│   │   │   └── alertas/           # Sistema de alertas
│   │   ├── services/
│   │   │   └── api.service.ts     # Serviço de API
│   │   ├── app.component.ts
│   │   └── app.routes.ts
│   ├── environments/              # Configurações de ambiente
│   └── styles.css                # Estilos globais
├── package.json
├── angular.json
└── tailwind.config.js
\`\`\`

## Funcionalidades

### Dashboard
- Estatísticas em tempo real
- Movimentações recentes
- Alertas de estoque baixo

### Produtos
- Listagem com busca e filtros
- Cadastro com campos específicos por tipo:
  - **Perfumes**: Concentração, subfamílias, ocasião
  - **Cremes**: Tipo de pele, propriedades, ação/resultado
  - **Maquiagens**: Textura, cobertura, tonalidade
- Página de detalhes completa

### Movimentações
- Registro de entrada com lote e validade
- Registro de saída com validação de estoque
- Histórico completo com busca

### Relatórios
- Vendas por marca
- Rentabilidade por produto
- Resumo financeiro

### Alertas
- Estoque baixo
- Produtos próximos ao vencimento
- Produtos sem movimentação

## Configuração da API

Edite \`src/environments/environment.ts\` para configurar a URL da API:

\`\`\`typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
\`\`\`

## Tecnologias

- Angular 17 (Standalone Components)
- TypeScript
- Tailwind CSS
- RxJS
- Angular Router
- Angular Forms

## Design

- Interface dark mode profissional
- Totalmente responsivo (desktop e mobile)
- Componentes reutilizáveis
- Navegação intuitiva
\`\`\`



<AssistantMessageContentPart partEncoded="eyJ0eXBlIjoidGFzay13YWl0aW5nLXYxIiwiY3JlYXRlZEF0IjoxNzYwMzkzNzA5NjM3LCJmaW5pc2hlZEF0IjoxNzYwMzkzNzA5NjM3LCJpZCI6ImpnRjR6aTF1S0Q4dW5qek8iLCJsYXN0UGFydFNlbnRBdCI6MTc2MDM5MzcwOTYzNywicGFydHMiOlt7InR5cGUiOiJ0b29sLWNhbGxzIn1dfQ==" />



<AssistantMessageContentPart partEncoded="eyJ0eXBlIjoidGFzay1tYW5hZ2UtdG9kb3MtdjEiLCJpZCI6ImFIaDlMM2x3eFFVWWxXZXIiLCJ0YXNrTmFtZUFjdGl2ZSI6IkZpbmFsaXphbmRvIHNpc3RlbWEiLCJ0b29sQ2FsbElkIjoidG9vbHVfMDFEOW1QeUhKWjkzOUVLTXkzVFdhTXpqIiwidGFza05hbWVDb21wbGV0ZSI6IlNpc3RlbWEgQW5ndWxhciBjb21wbGV0byIsImNyZWF0ZWRBdCI6MTc2MDM5MzcxMDU0NiwiZmluaXNoZWRBdCI6bnVsbCwicGFydHMiOltdLCJsYXN0UGFydFNlbnRBdCI6bnVsbH0=" />
