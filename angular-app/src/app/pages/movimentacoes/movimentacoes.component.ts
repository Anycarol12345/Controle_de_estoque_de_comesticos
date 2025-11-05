import { Component, type OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import type {
  ApiService,
  Movimentacao,
  Produto,
} from "../../service/api.service";

@Component({
  selector: "app-movimentacoes",
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: "./movimentacoes.component.html",
  styleUrls: ["./movimentacoes.component.css"],
})
export class MovimentacoesComponent implements OnInit {
  abaAtiva: "entrada" | "saida" | "historico" = "entrada";
  produtos: Produto[] = [];
  movimentacoes: Movimentacao[] = [];

  novaMovimentacao: Movimentacao = {
    produto_id: 0,
    tipo: "entrada",
    quantidade: 0,
    observacao: "",
    lote: "",
    validade: "",
  };

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.carregarDados();
  }

  carregarDados() {
    this.apiService.getProdutos().subscribe({
      next: (data: Produto[]) => (this.produtos = data),
      error: (err: unknown) => console.error("Erro ao carregar produtos:", err),
    });

    this.apiService.getMovimentacoes().subscribe({
      next: (data: Movimentacao[]) => (this.movimentacoes = data),
      error: (err: unknown) =>
        console.error("Erro ao carregar movimentações:", err),
    });
  }

  mudarAba(aba: "entrada" | "saida" | "historico") {
    this.abaAtiva = aba;
    this.resetarFormulario();
  }

  resetarFormulario() {
    this.novaMovimentacao = {
      produto_id: 0,
      tipo: this.abaAtiva === "entrada" ? "entrada" : "saida",
      quantidade: 0,
      observacao: "",
      lote: "",
      validade: "",
    };
  }

  registrarMovimentacao() {
    if (
      this.novaMovimentacao.produto_id === 0 ||
      this.novaMovimentacao.quantidade <= 0
    ) {
      alert("Preencha todos os campos obrigatórios");
      return;
    }

    const produto = this.produtos.find(
      (p) => p.id === this.novaMovimentacao.produto_id
    );
    if (
      this.abaAtiva === "saida" &&
      produto &&
      this.novaMovimentacao.quantidade > produto.quantidade_estoque
    ) {
      alert("Quantidade indisponível em estoque");
      return;
    }

    this.apiService.criarMovimentacao(this.novaMovimentacao).subscribe({
      next: () => {
        alert("Movimentação registrada com sucesso!");
        this.carregarDados();
        this.resetarFormulario();
      },
      error: (err: unknown) =>
        console.error("Erro ao registrar movimentação:", err),
    });
  }

  getProdutoSelecionado(): Produto | undefined {
    return this.produtos.find((p) => p.id === this.novaMovimentacao.produto_id);
  }

  formatarData(data: string | undefined): string {
    if (!data) return "-";
    return new Date(data).toLocaleDateString("pt-BR");
  }
}
