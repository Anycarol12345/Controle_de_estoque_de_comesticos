import { Component, type OnInit } from "@angular/core"
import { CommonModule } from "@angular/common"
import { RouterModule } from "@angular/router"
import type { ApiService, Produto } from "../../services/api.service"

@Component({
  selector: "app-alertas",
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: "./alertas.component.html",
  styleUrls: ["./alertas.component.css"],
})
export class AlertasComponent implements OnInit {
  alertasEstoqueBaixo: Produto[] = []
  alertasVencimento: any[] = []
  alertasSemMovimentacao: Produto[] = []
  loading = true

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.carregarAlertas()
  }

  carregarAlertas() {
    this.loading = true

    this.apiService.getAlertasEstoqueBaixo().subscribe({
      next: (data) => (this.alertasEstoqueBaixo = data),
      error: (err) => console.error("Erro ao carregar alertas de estoque baixo:", err),
    })

    this.apiService.getAlertasVencimento().subscribe({
      next: (data) => (this.alertasVencimento = data),
      error: (err) => console.error("Erro ao carregar alertas de vencimento:", err),
    })

    this.apiService.getAlertasSemMovimentacao().subscribe({
      next: (data) => {
        this.alertasSemMovimentacao = data
        this.loading = false
      },
      error: (err) => {
        console.error("Erro ao carregar alertas sem movimentação:", err)
        this.loading = false
      },
    })
  }

  formatarData(data: string): string {
    return new Date(data).toLocaleDateString("pt-BR")
  }

  calcularDiasParaVencimento(validade: string): number {
    const hoje = new Date()
    const dataValidade = new Date(validade)
    const diff = dataValidade.getTime() - hoje.getTime()
    return Math.ceil(diff / (1000 * 60 * 60 * 24))
  }
}
