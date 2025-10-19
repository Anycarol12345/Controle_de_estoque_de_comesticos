const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api"

export interface Produto {
  id: number
  codigo: string
  nome: string
  descricao?: string
  marca_id: number
  categoria_id: number
  preco_custo: number
  preco_venda: number
  estoque_atual: number
  estoque_minimo: number
  unidade: string
  ativo: number
  data_cadastro: string
  marca: {
    id: number
    nome: string
  }
  categoria: {
    id: number
    nome: string
  }
  tipo_produto?: "perfume" | "creme" | "maquiagem" | "outro"

  // Campos para Perfumes/Colônias
  concentracao?: string
  subfamilias?: string
  ocasiao?: string

  // Campos para Cremes
  tipo_pele?: string
  acao_resultado?: string

  // Campos para Maquiagens
  textura?: string
  cobertura?: string
  fundo_cor?: string
  tonalidade?: string

  // Campos comuns
  propriedades?: string
  linha?: string
  detalhes?: string
  ingredientes?: string
  como_usar?: string
}

export interface Movimentacao {
  id: number
  produto_id: number
  tipo: string
  quantidade: number
  valor_unitario: number
  valor_total: number
  lote?: string
  data_validade?: string
  observacao?: string
  data_movimentacao: string
  produto: Produto
}

export interface Marca {
  id: number
  nome: string
  descricao?: string
  ativo: number
}

export interface Categoria {
  id: number
  nome: string
  descricao?: string
}

export interface EstatisticasDashboard {
  total_produtos: number
  valor_total_estoque: number
  produtos_estoque_baixo: number
  movimentacoes_mes: number
}

// Produtos
export async function listarProdutos(marcaId?: number, busca?: string): Promise<Produto[]> {
  const params = new URLSearchParams()
  if (marcaId) params.append("marca_id", marcaId.toString())
  if (busca) params.append("busca", busca)

  const response = await fetch(`${API_URL}/produtos?${params}`)
  if (!response.ok) throw new Error("Erro ao buscar produtos")
  return response.json()
}

export async function obterProduto(id: number): Promise<Produto> {
  const response = await fetch(`${API_URL}/produtos/${id}`)
  if (!response.ok) throw new Error("Erro ao buscar produto")
  return response.json()
}

export async function criarProduto(
  produto: Omit<Produto, "id" | "estoque_atual" | "data_cadastro" | "marca" | "categoria">,
): Promise<Produto> {
  const response = await fetch(`${API_URL}/produtos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(produto),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Erro ao criar produto")
  }
  return response.json()
}

export async function atualizarProduto(id: number, produto: Partial<Produto>): Promise<Produto> {
  const response = await fetch(`${API_URL}/produtos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(produto),
  })
  if (!response.ok) throw new Error("Erro ao atualizar produto")
  return response.json()
}

export async function deletarProduto(id: number): Promise<void> {
  const response = await fetch(`${API_URL}/produtos/${id}`, {
    method: "DELETE",
  })
  if (!response.ok) throw new Error("Erro ao deletar produto")
}

// Movimentações
export async function listarMovimentacoes(tipo?: string, produtoId?: number): Promise<Movimentacao[]> {
  const params = new URLSearchParams()
  if (tipo) params.append("tipo", tipo)
  if (produtoId) params.append("produto_id", produtoId.toString())

  const response = await fetch(`${API_URL}/movimentacoes?${params}`)
  if (!response.ok) throw new Error("Erro ao buscar movimentações")
  return response.json()
}

export async function criarMovimentacao(movimentacao: {
  produto_id: number
  tipo: string
  quantidade: number
  valor_unitario: number
  lote?: string
  data_validade?: string
  observacao?: string
}): Promise<Movimentacao> {
  const response = await fetch(`${API_URL}/movimentacoes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(movimentacao),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Erro ao criar movimentação")
  }
  return response.json()
}

export async function movimentacoesRecentes(): Promise<Movimentacao[]> {
  const response = await fetch(`${API_URL}/movimentacoes/recentes/lista`)
  if (!response.ok) throw new Error("Erro ao buscar movimentações recentes")
  return response.json()
}

export const registrarMovimentacao = criarMovimentacao
export const excluirProduto = deletarProduto

// Marcas
export async function listarMarcas(): Promise<Marca[]> {
  const response = await fetch(`${API_URL}/marcas`)
  if (!response.ok) throw new Error("Erro ao buscar marcas")
  return response.json()
}

export async function criarMarca(marca: { nome: string; descricao?: string }): Promise<Marca> {
  const response = await fetch(`${API_URL}/marcas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...marca, ativo: 1 }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Erro ao criar marca")
  }
  return response.json()
}

// Categorias
export async function listarCategorias(): Promise<Categoria[]> {
  const response = await fetch(`${API_URL}/configuracoes/categorias`)
  if (!response.ok) throw new Error("Erro ao buscar categorias")
  return response.json()
}

export async function criarCategoria(categoria: { nome: string; descricao?: string }): Promise<Categoria> {
  const response = await fetch(`${API_URL}/configuracoes/categorias`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(categoria),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Erro ao criar categoria")
  }
  return response.json()
}

// Relatórios
export async function obterEstatisticasDashboard(): Promise<EstatisticasDashboard> {
  const response = await fetch(`${API_URL}/relatorios/dashboard`)
  if (!response.ok) throw new Error("Erro ao buscar estatísticas")
  return response.json()
}

export async function obterVendasPorMarca(): Promise<
  Array<{
    marca: string
    total_vendas: number
    quantidade_vendida: number
  }>
> {
  const response = await fetch(`${API_URL}/relatorios/vendas-por-marca`)
  if (!response.ok) throw new Error("Erro ao buscar vendas por marca")
  return response.json()
}

export async function obterRentabilidade(): Promise<
  Array<{
    produto: string
    codigo: string
    quantidade_vendida: number
    receita_total: number
    custo_total: number
    lucro: number
    margem_percentual: number
  }>
> {
  const response = await fetch(`${API_URL}/relatorios/rentabilidade`)
  if (!response.ok) throw new Error("Erro ao buscar rentabilidade")
  return response.json()
}

// Alertas
export async function obterAlertasEstoqueBaixo(): Promise<
  Array<{
    id: number
    codigo: string
    nome: string
    estoque_atual: number
    estoque_minimo: number
    tipo: string
  }>
> {
  const response = await fetch(`${API_URL}/alertas/estoque-baixo`)
  if (!response.ok) throw new Error("Erro ao buscar alertas de estoque baixo")
  return response.json()
}

export async function obterAlertasVencimento(): Promise<
  Array<{
    id: number
    produto_id: number
    produto_nome: string
    lote: string
    data_validade: string
    dias_restantes: number
    tipo: string
  }>
> {
  const response = await fetch(`${API_URL}/alertas/proximos-vencimento`)
  if (!response.ok) throw new Error("Erro ao buscar alertas de vencimento")
  return response.json()
}

export async function obterAlertasSemMovimentacao(): Promise<
  Array<{
    id: number
    codigo: string
    nome: string
    estoque_atual: number
    ultima_movimentacao: string | null
    dias_parado: number
    tipo: string
  }>
> {
  const response = await fetch(`${API_URL}/alertas/sem-movimentacao`)
  if (!response.ok) throw new Error("Erro ao buscar alertas sem movimentação")
  return response.json()
}
