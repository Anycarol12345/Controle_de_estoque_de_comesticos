import { Component } from "@angular/core"
import { RouterLink, RouterLinkActive } from "@angular/router"
import { CommonModule } from "@angular/common"

@Component({
  selector: "app-sidebar",
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
    <aside class="w-64 bg-zinc-900 border-r border-zinc-800 flex flex-col">
      <div class="p-6 border-b border-zinc-800">
        <h1 class="text-2xl font-bold text-purple-400">Integra+</h1>
        <p class="text-sm text-zinc-400">Gestão de Estoque</p>
      </div>
      
      <nav class="flex-1 p-4">
        <a *ngFor="let item of menuItems" 
           [routerLink]="item.path"
           routerLinkActive="bg-purple-600 text-white"
           class="flex items-center gap-3 px-4 py-3 rounded-lg text-zinc-300 hover:bg-zinc-800 transition-colors mb-2">
          <span class="text-xl">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </a>
      </nav>
    </aside>
  `,
})
export class SidebarComponent {
  menuItems = [
    { path: "/", icon: "📊", label: "Dashboard" },
    { path: "/produtos", icon: "📦", label: "Produtos" },
    { path: "/movimentacoes", icon: "🔄", label: "Movimentações" },
    { path: "/relatorios", icon: "📈", label: "Relatórios" },
    { path: "/alertas", icon: "⚠️", label: "Alertas" },
  ]
}
