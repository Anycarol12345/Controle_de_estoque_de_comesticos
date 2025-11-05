import { Component, type OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { RouterModule } from "@angular/router";
import type { ApiService, Produto, Marca } from "../../services/api.service";

@Component({
  selector: "app-produtos",
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: "./produtos.component.html",
  styleUrls: ["./produtos.component.css"],
})
export class ProdutosComponent implements OnInit {
  produtos: Produto[] = [];
  produtosFiltrados: Produto[] = [];
  marcas: Marca[] = [];
  busca = "";
  marcaSelecionada = "";
  mostrarModal = false;
  produtoEditando: Produto | null = null;

  novoProduto: Produto = this.criarProdutoVazio();

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.carregarDados();
  }

  carregarDados() {
    this.apiService.getProdutos().subscribe({
      next: (data: Produto[]) => {
        this.produtos = data;
        this.filtrarProdutos();
      },
      error: (err: unknown) => console.error("Erro ao carregar produtos:", err),
    });

    this.apiService.getMarcas().subscribe({
      next: (data: Marca[]) => (this.marcas = data),
      error: (err: unknown) => console.error("Erro ao carregar marcas:", err),
    });
  }

  filtrarProdutos() {
    this.produtosFiltrados = this.produtos.filter((p) => {
      const matchBusca =
        !this.busca ||
        p.nome.toLowerCase().includes(this.busca.toLowerCase()) ||
        p.sku.toLowerCase().includes(this.busca.toLowerCase());

      const matchMarca =
        !this.marcaSelecionada ||
        p.marca_id.toString() === this.marcaSelecionada;

      return matchBusca && matchMarca;
    });
  }

  abrirModal(produto?: Produto) {
    if (produto) {
      this.produtoEditando = produto;
      this.novoProduto = { ...produto };
    } else {
      this.produtoEditando = null;
      this.novoProduto = this.criarProdutoVazio();
    }
    this.mostrarModal = true;
  }

  fecharModal() {
    this.mostrarModal = false;
    this.produtoEditando = null;
    this.novoProduto = this.criarProdutoVazio();
  }

  salvarProduto() {
    if (this.produtoEditando) {
      this.apiService
        .atualizarProduto(this.produtoEditando.id!, this.novoProduto)
        .subscribe({
          next: () => {
            this.carregarDados();
            this.fecharModal();
          },
          error: (err: unknown) =>
            console.error("Erro ao atualizar produto:", err),
        });
    } else {
      this.apiService.criarProduto(this.novoProduto).subscribe({
        next: () => {
          this.carregarDados();
          this.fecharModal();
        },
        error: (err: unknown) => console.error("Erro ao criar produto:", err),
      });
    }
  }

  deletarProduto(id: number) {
    if (confirm("Tem certeza que deseja deletar este produto?")) {
      this.apiService.deletarProduto(id).subscribe({
        next: () => this.carregarDados(),
        error: (err: unknown) => console.error("Erro ao deletar produto:", err),
      });
    }
  }

  criarProdutoVazio(): Produto {
    return {
      nome: "",
      sku: "",
      preco_custo: 0,
      preco_venda: 0,
      quantidade_estoque: 0,
      estoque_minimo: 0,
      marca_id: 0,
      tipo_produto: "perfume",
    };
  }

  formatarMoeda(valor: number): string {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(valor);
  }

  getNomeMarca(marcaId: number): string {
    const marca = this.marcas.find((m) => m.id === marcaId);
    return marca?.nome || "-";
  }
}
