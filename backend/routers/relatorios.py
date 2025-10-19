from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from typing import List
from database import get_db, Produto as ProdutoModel, Movimentacao as MovimentacaoModel, Marca as MarcaModel
from schemas import EstatisticasDashboard, VendasPorMarca, ProdutoRentabilidade

router = APIRouter()

@router.get("/dashboard", response_model=EstatisticasDashboard)
def estatisticas_dashboard(db: Session = Depends(get_db)):
    # Total de produtos
    total_produtos = db.query(ProdutoModel).filter(ProdutoModel.ativo == 1).count()
    
    # Valor total do estoque
    produtos = db.query(ProdutoModel).all()
    valor_total_estoque = sum(p.estoque_atual * p.preco_custo for p in produtos)
    
    # Produtos com estoque baixo
    produtos_estoque_baixo = db.query(ProdutoModel).filter(
        ProdutoModel.estoque_atual <= ProdutoModel.estoque_minimo
    ).count()
    
    # Movimentações do mês atual
    primeiro_dia_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    movimentacoes_mes = db.query(MovimentacaoModel).filter(
        MovimentacaoModel.data_movimentacao >= primeiro_dia_mes
    ).count()
    
    return {
        "total_produtos": total_produtos,
        "valor_total_estoque": valor_total_estoque,
        "produtos_estoque_baixo": produtos_estoque_baixo,
        "movimentacoes_mes": movimentacoes_mes
    }

@router.get("/vendas-por-marca", response_model=List[VendasPorMarca])
def vendas_por_marca(db: Session = Depends(get_db)):
    # Últimos 30 dias
    data_inicio = datetime.now() - timedelta(days=30)
    
    resultado = db.query(
        MarcaModel.nome,
        func.sum(MovimentacaoModel.valor_total).label("total_vendas"),
        func.sum(MovimentacaoModel.quantidade).label("quantidade_vendida")
    ).join(
        ProdutoModel, MovimentacaoModel.produto_id == ProdutoModel.id
    ).join(
        MarcaModel, ProdutoModel.marca_id == MarcaModel.id
    ).filter(
        MovimentacaoModel.tipo == "saida",
        MovimentacaoModel.data_movimentacao >= data_inicio
    ).group_by(MarcaModel.nome).all()
    
    return [
        {
            "marca": r.nome,
            "total_vendas": r.total_vendas or 0,
            "quantidade_vendida": r.quantidade_vendida or 0
        }
        for r in resultado
    ]

@router.get("/rentabilidade", response_model=List[ProdutoRentabilidade])
def relatorio_rentabilidade(db: Session = Depends(get_db)):
    # Últimos 30 dias
    data_inicio = datetime.now() - timedelta(days=30)
    
    # Busca todas as saídas (vendas)
    vendas = db.query(
        ProdutoModel.nome,
        ProdutoModel.codigo,
        func.sum(MovimentacaoModel.quantidade).label("quantidade_vendida"),
        func.sum(MovimentacaoModel.valor_total).label("receita_total")
    ).join(
        MovimentacaoModel, ProdutoModel.id == MovimentacaoModel.produto_id
    ).filter(
        MovimentacaoModel.tipo == "saida",
        MovimentacaoModel.data_movimentacao >= data_inicio
    ).group_by(ProdutoModel.id).all()
    
    resultado = []
    for venda in vendas:
        produto = db.query(ProdutoModel).filter(ProdutoModel.codigo == venda.codigo).first()
        custo_total = venda.quantidade_vendida * produto.preco_custo
        lucro = venda.receita_total - custo_total
        margem_percentual = (lucro / venda.receita_total * 100) if venda.receita_total > 0 else 0
        
        resultado.append({
            "produto": venda.nome,
            "codigo": venda.codigo,
            "quantidade_vendida": venda.quantidade_vendida,
            "receita_total": venda.receita_total,
            "custo_total": custo_total,
            "lucro": lucro,
            "margem_percentual": margem_percentual
        })
    
    return sorted(resultado, key=lambda x: x["lucro"], reverse=True)
