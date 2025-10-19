// Database schema and types for the inventory system

export interface Marca {
  id: string
  nome: string
  ativa: boolean
  createdAt: Date
}

export interface Produto {
  id: string
  nome: string
  marcaId: string
  categoria: string
  codigoBarras?: string
  precoCompra: number
  precoVenda: number
  estoqueMinimo: number
  estoqueAtual: number
  localizacao?: string
  ativo: boolean
  createdAt: Date
}

export interface Movimentacao {
  id: string
  produtoId: string
  tipo: "entrada" | "saida"
  quantidade: number
  valor: number
  lote?: string
  validade?: Date
  observacao?: string
  createdAt: Date
}

export interface Cliente {
  id: string
  nome: string
  telefone?: string
  email?: string
  endereco?: string
  ativo: boolean
  createdAt: Date
}

export interface Fornecedor {
  id: string
  nome: string
  telefone?: string
  email?: string
  cnpj?: string
  ativo: boolean
  createdAt: Date
}

// Mock data for demonstration
export const marcas: Marca[] = [
  { id: "1", nome: "Avon", ativa: true, createdAt: new Date() },
  { id: "2", nome: "O Boticário", ativa: true, createdAt: new Date() },
  { id: "3", nome: "Eudora", ativa: true, createdAt: new Date() },
  { id: "4", nome: "Quem disse Berenice?", ativa: true, createdAt: new Date() },
]

export const produtos: Produto[] = [
  {
    id: "1",
    nome: "Perfume Kaiak Masculino",
    marcaId: "2",
    categoria: "Perfumaria",
    codigoBarras: "7891010101010",
    precoCompra: 89.9,
    precoVenda: 139.9,
    estoqueMinimo: 5,
    estoqueAtual: 12,
    localizacao: "Prateleira A1",
    ativo: true,
    createdAt: new Date(),
  },
  {
    id: "2",
    nome: "Batom Matte Vermelho",
    marcaId: "4",
    categoria: "Maquiagem",
    codigoBarras: "7891020202020",
    precoCompra: 25.9,
    precoVenda: 45.9,
    estoqueMinimo: 10,
    estoqueAtual: 3,
    localizacao: "Gaveta B2",
    ativo: true,
    createdAt: new Date(),
  },
  {
    id: "3",
    nome: "Hidratante Corporal",
    marcaId: "1",
    categoria: "Cuidados",
    codigoBarras: "7891030303030",
    precoCompra: 18.5,
    precoVenda: 32.9,
    estoqueMinimo: 8,
    estoqueAtual: 15,
    localizacao: "Prateleira C1",
    ativo: true,
    createdAt: new Date(),
  },
]

export const movimentacoes: Movimentacao[] = [
  {
    id: "1",
    produtoId: "1",
    tipo: "entrada",
    quantidade: 10,
    valor: 899.0,
    lote: "L2024001",
    validade: new Date("2026-12-31"),
    observacao: "Compra mensal",
    createdAt: new Date("2025-01-15"),
  },
  {
    id: "2",
    produtoId: "1",
    tipo: "saida",
    quantidade: 2,
    valor: 279.8,
    observacao: "Venda cliente Maria",
    createdAt: new Date("2025-01-20"),
  },
]

// Helper functions
export function getMarcaNome(marcaId: string): string {
  return marcas.find((m) => m.id === marcaId)?.nome || "Desconhecida"
}

export function calcularMargemLucro(precoCompra: number, precoVenda: number): number {
  return ((precoVenda - precoCompra) / precoCompra) * 100
}

export function getProdutosEstoqueBaixo(): Produto[] {
  return produtos.filter((p) => p.estoqueAtual <= p.estoqueMinimo)
}

export function getValorTotalEstoque(): number {
  return produtos.reduce((total, p) => total + p.precoCompra * p.estoqueAtual, 0)
}
