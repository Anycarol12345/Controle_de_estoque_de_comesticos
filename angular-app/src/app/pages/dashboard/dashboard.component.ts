import { Component, type OnInit } from "@angular/core"
import { CommonModule } from "@angular/common"
import type { ApiService, Estatisticas, Movimentacao, Produto } from "../../service/api.service"

@Component({
  selector: "app-dashboard",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./dashboard.component.html",
  styleUrls: ["./dashboard.component.css"],
})
export class DashboardComponent implements OnInit {
  estatisticas: Estatisticas = {
    total_produtos: 0,
    valor_total_estoque: 0,
    produtos_estoque_baixo: 0,
  }
  ultimasMovimentacoes: Movimentacao[] = []
  alertasEstoqueBaixo: Produto[] = []
  loading = true

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.carregarDados()
  }

  carregarDados() {
    this.loading = true

    this.apiService.getEstatisticas().subscribe({
      next: (data) => (this.estatisticas = data),
      error: (err) => console.error("Erro ao carregar estatísticas:", err),
    })

    this.apiService.getMovimentacoes().subscribe({
      next: (data) => {
        this.ultimasMovimentacoes = data.slice(0, 5)
        this.loading = false
      },
      error: (err) => console.error("Erro ao carregar movimentações:", err),
    })

    this.apiService.getAlertasEstoqueBaixo().subscribe({
      next: (data) => (this.alertasEstoqueBaixo = data.slice(0, 5)),
      error: (err) => console.error("Erro ao carregar alertas:", err),
    })
  }

  formatarData(data: string | undefined): string {
    if (!data) return "-"
    return new Date(data).toLocaleDateString("pt-BR")
  }

  formatarMoeda(valor: number): string {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(valor)
  }
}
