import { Component, type OnInit } from "@angular/core"
import { CommonModule } from "@angular/common"
import { RouterLink } from "@angular/router"
import type { ApiService, Produto } from "../../services/api.service"

@Component({
  selector: "app-alertas",
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="p-8">
      <h1 class="text-3xl font-bold mb-8">Alertas</h1>

      <div class="space-y-8">
        <!-- Estoque Baixo -->
        <div class="bg-zinc-900 rounded-lg p-6 border border-zinc-800">
          <div class="flex items-center gap-3 mb-6">
            <span class="text-3xl">⚠️</span>
            <div>
              <h2 class="text-xl font-bold">Estoque Baixo</h2>
              <p class="text-sm text-zinc-400">Produtos abaixo do estoque mínimo</p>
            </div>
          </div>

          <div class="space-y-3">
            <div *ngFor="let produto of estoqueBaixo" 
                 class="flex items-center justify-between p-4 bg-zinc-800 rounded-lg hover:bg-zinc-700 transition-colors">
              <div class="flex-1">
                <p class="font-medium">{{ produto.nome }}</p>
                <p class="text-sm text-zinc-400">{{ produto.marca?.nome }} - {{ produto.sku }}</p>
              </div>
              <div class="text-right mr-4">
                <p class="text-yellow-500 font-bold">{{ produto.quantidade_estoque }} un</p>
                <p class="text-sm text-zinc-400">Mínimo: {{ produto.estoque_minimo }}</p>
              </div>
              <a [routerLink]="['/produtos', produto.id]" 
                 class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-sm transition-colors">
                Ver Produto
              </a>
            </div>
            <p *ngIf="estoqueBaixo.length === 0" class="text-center py-8 text-zinc-400">
              Nenhum produto com estoque baixo
            </p>
          </div>
        </div>

        <!-- Produtos Próximos ao Vencimento -->
        <div class="bg-zinc-900 rounded-lg p-6 border border-zinc-800">
          <div class="flex items-center gap-3 mb-6">
            <span class="text-3xl">📅</span>
            <div>
              <h2 class="text-xl font-bold">Próximos ao Vencimento</h2>
              <p class="text-sm text-zinc-400">Produtos que vencem nos próximos 30 dias</p>
            </div>
          </div>

          <div class="space-y-3">
            <div *ngFor="let item of proximosVencimento" 
                 class="flex items-center justify-between p-4 bg-zinc-800 rounded-lg">
              <div class="flex-1">
                <p class="font-medium">{{ item.produto_nome }}</p>
                <p class="text-sm text-zinc-400">Lote: {{ item.lote }}</p>
              </div>
              <div class="text-right">
                <p class="text-orange-500 font-bold">{{ formatDate(item.validade) }}</p>
                <p class="text-sm text-zinc-400">{{ getDiasRestantes(item.validade) }} dias</p>
              </div>
            </div>
            <p *ngIf="proximosVencimento.length === 0" class="text-center py-8 text-zinc-400">
              Nenhum produto próximo ao vencimento
            </p>
          </div>
        </div>

        <!-- Produtos Sem Movimentação -->
        <div class="bg-zinc-900 rounded-lg p-6 border border-zinc-800">
          <div class="flex items-center gap-3 mb-6">
            <span class="text-3xl">💤</span>
            <div>
              <h2 class="text-xl font-bold">Sem Movimentação</h2>
              <p class="text-sm text-zinc-400">Produtos sem saída nos últimos 30 dias</p>
            </div>
          </div>

          <div class="space-y-3">
            <div *ngFor="let produto of semMovimentacao" 
                 class="flex items-center justify-between p-4 bg-zinc-800 rounded-lg hover:bg-zinc-700 transition-colors">
              <div class="flex-1">
                <p class="font-medium">{{ produto.nome }}</p>
                <p class="text-sm text-zinc-400">{{ produto.marca?.nome }}</p>
              </div>
              <div class="text-right mr-4">
                <p class="font-bold">{{ produto.quantidade_estoque }} un</p>
                <p class="text-sm text-zinc-400">R$ {{ produto.preco_venda.toFixed(2) }}</p>
              </div>
              <a [routerLink]="['/produtos', produto.id]" 
                 class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-sm transition-colors">
                Ver Produto
              </a>
            </div>
            <p *ngIf="semMovimentacao.length === 0" class="text-center py-8 text-zinc-400">
              Todos os produtos têm movimentação recente
            </p>
          </div>
        </div>
      </div>
    </div>
  `,
})
export class AlertasComponent implements OnInit {
  estoqueBaixo: Produto[] = []
  proximosVencimento: any[] = []
  semMovimentacao: Produto[] = []

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadAlertas()
  }

  loadAlertas() {
    this.api.getAlertasEstoqueBaixo().subscribe((produtos) => {
      this.estoqueBaixo = produtos
    })

    this.api.getAlertasVencimento().subscribe((items) => {
      this.proximosVencimento = items
    })

    // Simular produtos sem movimentação (API precisa implementar)
    this.api.getProdutos().subscribe((produtos) => {
      this.semMovimentacao = produtos.filter((p) => p.quantidade_estoque > 0).slice(0, 5)
    })
  }

  formatDate(date: string): string {
    return new Date(date).toLocaleDateString("pt-BR")
  }

  getDiasRestantes(validade: string): number {
    const hoje = new Date()
    const dataValidade = new Date(validade)
    const diff = dataValidade.getTime() - hoje.getTime()
    return Math.ceil(diff / (1000 * 60 * 60 * 24))
  }
}
