import { Component } from "@angular/core"
import { CommonModule } from "@angular/common"
import { RouterModule } from "@angular/router"

@Component({
  selector: "app-sidebar",
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: "./sidebar.component.html",
  styleUrls: ["./sidebar.component.css"],
})
export class SidebarComponent {
  menuItems = [
    { path: "/", icon: "📊", label: "Dashboard" },
    { path: "/produtos", icon: "📦", label: "Produtos" },
    { path: "/movimentacoes", icon: "📝", label: "Movimentações" },
    { path: "/relatorios", icon: "📈", label: "Relatórios" },
    { path: "/alertas", icon: "🔔", label: "Alertas" },
  ]
}
