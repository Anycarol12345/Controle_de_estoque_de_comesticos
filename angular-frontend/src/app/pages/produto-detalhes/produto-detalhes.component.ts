import { Component, type OnInit } from "@angular/core"
import { CommonModule } from "@angular/common"
import type { ApiService } from "../../services/api.service"

@Component({
  selector: "app-relatorios",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./relatorios.component.html",
  styleUrls: ["./relatorios.component.css"],
})
export class RelatoriosComponent implements OnInit {
  vendasPorMarca: any[] = []
  produtosMaisVendidos: any[] = []
  rentabilidade: any = null
  loading = true

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.carregarRelatorios()
  }

  carregarRelatorios() {
    this.loading = true

    this.apiService.getRelatorioVendasPorMarca().subscribe({
      next: (data) => (this.vendasPorMarca = data),
      error: (err) => console.error("Erro ao carregar vendas por marca:", err),
    })

    this.apiService.getRelatorioProdutosMaisVendidos().subscribe({
      next: (data) => (this.produtosMaisVendidos = data),
      error: (err) => console.error("Erro ao carregar produtos mais vendidos:", err),
    })

    this.apiService.getRelatorioRentabilidade().subscribe({
      next: (data) => {
        this.rentabilidade = data
        this.loading = false
      },
      error: (err) => {
        console.error("Erro ao carregar rentabilidade:", err)
        this.loading = false
      },
    })
  }

  formatarMoeda(valor: number): string {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(valor)
  }

  formatarPercentual(valor: number): string {
    return `${valor.toFixed(2)}%`
  }
}
