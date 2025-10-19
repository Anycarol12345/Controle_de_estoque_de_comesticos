from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta

from database import get_db
import models

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/alertas", response_class=HTMLResponse)
async def alertas(request: Request, db: Session = Depends(get_db)):
    # Produtos com estoque baixo
    produtos_baixo_estoque = db.query(models.Produto).filter(
        models.Produto.quantidade_estoque <= models.Produto.estoque_minimo
    ).all()
    
    # Produtos com estoque zerado
    produtos_sem_estoque = db.query(models.Produto).filter(
        models.Produto.quantidade_estoque == 0
    ).all()
    
    # Produtos próximos da validade (30 dias)
    data_limite = datetime.utcnow() + timedelta(days=30)
    produtos_vencendo = db.query(models.Movimentacao).filter(
        and_(
            models.Movimentacao.validade != None,
            models.Movimentacao.validade <= data_limite,
            models.Movimentacao.validade >= datetime.utcnow()
        )
    ).all()
    
    # Produtos vencidos
    produtos_vencidos = db.query(models.Movimentacao).filter(
        and_(
            models.Movimentacao.validade != None,
            models.Movimentacao.validade < datetime.utcnow()
        )
    ).all()
    
    # Produtos sem movimentação nos últimos 90 dias
    data_limite_movimento = datetime.utcnow() - timedelta(days=90)
    produtos_parados = db.query(models.Produto).outerjoin(
        models.Movimentacao
    ).filter(
        models.Movimentacao.data < data_limite_movimento
    ).all()
    
    total_alertas = (
        len(produtos_baixo_estoque) +
        len(produtos_sem_estoque) +
        len(produtos_vencendo) +
        len(produtos_vencidos) +
        len(produtos_parados)
    )
    
    return templates.TemplateResponse("alertas/index.html", {
        "request": request,
        "total_alertas": total_alertas,
        "produtos_baixo_estoque": produtos_baixo_estoque,
        "produtos_sem_estoque": produtos_sem_estoque,
        "produtos_vencendo": produtos_vencendo,
        "produtos_vencidos": produtos_vencidos,
        "produtos_parados": produtos_parados
    })
