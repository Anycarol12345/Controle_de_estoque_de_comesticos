from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from database import get_db
import models

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/relatorios", response_class=HTMLResponse)
async def relatorios(request: Request, db: Session = Depends(get_db)):
    # Valor total do estoque
    valor_total = db.query(
        func.sum(models.Produto.preco_venda * models.Produto.quantidade_estoque)
    ).scalar() or 0
    
    valor_custo = db.query(
        func.sum(models.Produto.preco_custo * models.Produto.quantidade_estoque)
    ).scalar() or 0
    
    # Produtos por tipo
    produtos_por_tipo = db.query(
        models.Produto.tipo_produto,
        func.count(models.Produto.id).label('total')
    ).group_by(models.Produto.tipo_produto).all()
    
    # Produtos por marca
    produtos_por_marca = db.query(
        models.Marca.nome,
        func.count(models.Produto.id).label('total'),
        func.sum(models.Produto.quantidade_estoque).label('estoque')
    ).join(models.Produto).group_by(models.Marca.nome).all()
    
    # Movimentações dos últimos 30 dias
    data_limite = datetime.utcnow() - timedelta(days=30)
    movimentacoes_mes = db.query(models.Movimentacao).filter(
        models.Movimentacao.data >= data_limite
    ).all()
    
    entradas_mes = sum(m.quantidade for m in movimentacoes_mes if m.tipo == models.TipoMovimentacao.ENTRADA)
    saidas_mes = sum(m.quantidade for m in movimentacoes_mes if m.tipo == models.TipoMovimentacao.SAIDA)
    
    # Produtos mais movimentados
    produtos_movimentados = db.query(
        models.Produto.nome,
        models.Marca.nome.label('marca'),
        func.count(models.Movimentacao.id).label('movimentacoes'),
        func.sum(models.Movimentacao.quantidade).label('quantidade_total')
    ).join(models.Movimentacao).join(models.Marca).group_by(
        models.Produto.id
    ).order_by(desc('movimentacoes')).limit(10).all()
    
    # Produtos com estoque baixo
    produtos_baixo_estoque = db.query(models.Produto).filter(
        models.Produto.quantidade_estoque <= models.Produto.estoque_minimo
    ).all()
    
    # Produtos sem movimentação
    produtos_sem_movimento = db.query(models.Produto).outerjoin(
        models.Movimentacao
    ).filter(
        models.Movimentacao.id == None
    ).all()
    
    return templates.TemplateResponse("relatorios/index.html", {
        "request": request,
        "valor_total": valor_total,
        "valor_custo": valor_custo,
        "lucro_potencial": valor_total - valor_custo,
        "produtos_por_tipo": produtos_por_tipo,
        "produtos_por_marca": produtos_por_marca,
        "entradas_mes": entradas_mes,
        "saidas_mes": saidas_mes,
        "produtos_movimentados": produtos_movimentados,
        "produtos_baixo_estoque": produtos_baixo_estoque,
        "produtos_sem_movimento": produtos_sem_movimento
    })
