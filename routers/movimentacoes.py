from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import Optional

from database import get_db
import models

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/movimentacoes", response_class=HTMLResponse)
async def movimentacoes(request: Request, db: Session = Depends(get_db)):
    produtos = db.query(models.Produto).all()
    movimentacoes = db.query(models.Movimentacao).order_by(desc(models.Movimentacao.data)).limit(50).all()
    
    return templates.TemplateResponse("movimentacoes/index.html", {
        "request": request,
        "produtos": produtos,
        "movimentacoes": movimentacoes
    })

@router.post("/movimentacoes/entrada")
async def registrar_entrada(
    produto_id: int = Form(...),
    quantidade: int = Form(...),
    lote: str = Form(None),
    validade: str = Form(None),
    observacao: str = Form(None),
    db: Session = Depends(get_db)
):
    # Criar movimentação
    movimentacao = models.Movimentacao(
        produto_id=produto_id,
        tipo=models.TipoMovimentacao.ENTRADA,
        quantidade=quantidade,
        lote=lote,
        validade=datetime.strptime(validade, '%Y-%m-%d') if validade else None,
        observacao=observacao
    )
    db.add(movimentacao)
    
    # Atualizar estoque
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if produto:
        produto.quantidade_estoque += quantidade
    
    db.commit()
    
    return RedirectResponse(url="/movimentacoes", status_code=303)

@router.post("/movimentacoes/saida")
async def registrar_saida(
    produto_id: int = Form(...),
    quantidade: int = Form(...),
    observacao: str = Form(None),
    db: Session = Depends(get_db)
):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    
    if not produto or produto.quantidade_estoque < quantidade:
        return RedirectResponse(url="/movimentacoes?erro=estoque_insuficiente", status_code=303)
    
    # Criar movimentação
    movimentacao = models.Movimentacao(
        produto_id=produto_id,
        tipo=models.TipoMovimentacao.SAIDA,
        quantidade=quantidade,
        observacao=observacao
    )
    db.add(movimentacao)
    
    # Atualizar estoque
    produto.quantidade_estoque -= quantidade
    
    db.commit()
    
    return RedirectResponse(url="/movimentacoes", status_code=303)
