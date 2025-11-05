import type { Routes } from "@angular/router";

export const routes: Routes = [
  {
    path: "",
    loadComponent: () =>
      import("./pages/dashboard/dashboard.component").then(
        (m) => m.DashboardComponent
      ),
  },
  {
    path: "produtos",
    loadComponent: () =>
      import("./pages/produtos/produtos.component").then(
        (m) => m.ProdutosComponent
      ),
  },
  {
    path: "produtos/:id",
    loadComponent: () =>
      import("./pages/produto-detalhes/produto-detalhes.component").then(
        (m) => m.RelatoriosComponent
      ),
  },
  {
    path: "movimentacoes",
    loadComponent: () =>
      import("./pages/movimentacoes/movimentacoes.component").then(
        (m) => m.MovimentacoesComponent
      ),
  },
  {
    path: "relatorios",
    loadComponent: () =>
      import("./pages/relatorios/relatorios.component").then(
        (m) => m.RelatoriosComponent
      ),
  },
  {
    path: "alertas",
    loadComponent: () =>
      import("./pages/alertas/alertas.component").then(
        (m) => m.AlertasComponent
      ),
  },
  {
    path: "**",
    redirectTo: "",
  },
];
