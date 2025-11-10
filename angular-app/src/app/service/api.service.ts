import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

export interface Produto {
  id?: number;
  nome: string;
  descricao?: string;
  sku: string;
  preco_custo: number;
  preco_venda: number;
  quantidade_estoque: number;
  estoque_minimo: number;
  marca_id: number;
  marca?: { id: number; nome: string };
  tipo_produto: "perfume" | "creme" | "maquiagem";
  concentracao?: string;
  subfamilias?: string;
  ocasiao?: string;
  tipo_pele?: string;
  propriedades?: string;
  linha?: string;
  ingredientes?: string;
  como_usar?: string;
  acao_resultado?: string;
  textura?: string;
  cobertura?: string;
  fundo_cor?: string;
  tonalidade?: string;
}

export interface Marca {
  id?: number;
  nome: string;
}

export interface Movimentacao {
  id?: number;
  produto_id: number;
  produto?: Produto;
  tipo: "entrada" | "saida";
  quantidade: number;
  data?: string;
  observacao?: string;
  lote?: string;
  validade?: string;
}

export interface Estatisticas {
  total_produtos: number;
  valor_total_estoque: number;
  produtos_estoque_baixo: number;
}

@Injectable({
  providedIn: "root",
})
export class ApiService {
  private apiUrl = "http://localhost:5000";

  constructor(private http: HttpClient) {}

  // Produtos
  getProdutos(): Observable<Produto[]> {
    return this.http.get<Produto[]>(`${this.apiUrl}/produtos`);
  }

  getProduto(id: number): Observable<Produto> {
    return this.http.get<Produto>(`${this.apiUrl}/produtos/${id}`);
  }

  criarProduto(produto: Produto): Observable<Produto> {
    return this.http.post<Produto>(`${this.apiUrl}/produtos`, produto);
  }

  atualizarProduto(id: number, produto: Produto): Observable<Produto> {
    return this.http.put<Produto>(`${this.apiUrl}/produtos/${id}`, produto);
  }

  deletarProduto(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/produtos/${id}`);
  }

  // Marcas
  getMarcas(): Observable<Marca[]> {
    return this.http.get<Marca[]>(`${this.apiUrl}/marcas`);
  }

  criarMarca(marca: Marca): Observable<Marca> {
    return this.http.post<Marca>(`${this.apiUrl}/marcas`, marca);
  }

  // Movimentações
  getMovimentacoes(): Observable<Movimentacao[]> {
    return this.http.get<Movimentacao[]>(`${this.apiUrl}/movimentacoes`);
  }

  criarMovimentacao(movimentacao: Movimentacao): Observable<Movimentacao> {
    return this.http.post<Movimentacao>(
      `${this.apiUrl}/movimentacoes`,
      movimentacao
    );
  }

  // Estatísticas
  getEstatisticas(): Observable<Estatisticas> {
    return this.http.get<Estatisticas>(`${this.apiUrl}/estatisticas`);
  }

  // Alertas
  getAlertasEstoqueBaixo(): Observable<Produto[]> {
    return this.http.get<Produto[]>(`${this.apiUrl}/alertas/estoque-baixo`);
  }

  getAlertasVencimento(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/alertas/vencimento`);
  }

  getAlertasSemMovimentacao(): Observable<Produto[]> {
    return this.http.get<Produto[]>(`${this.apiUrl}/alertas/sem-movimentacao`);
  }

  // Relatórios
  getRelatorioVendasPorMarca(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/relatorios/vendas-por-marca`);
  }

  getRelatorioProdutosMaisVendidos(): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.apiUrl}/relatorios/produtos-mais-vendidos`
    );
  }

  getRelatorioRentabilidade(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/relatorios/rentabilidade`);
  }
}
