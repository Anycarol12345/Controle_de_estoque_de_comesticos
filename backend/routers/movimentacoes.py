from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import get_db, Movimentacao as MovimentacaoModel, Produto as ProdutoModel
from schemas import Movimentacao, MovimentacaoCreate

router = APIRouter()

@router.get("/", response_model=List[Movimentacao])
def listar_movimentacoes(
    tipo: Optional[str] = None,
    produto_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(MovimentacaoModel)
    
    if tipo:
        query = query.filter(MovimentacaoModel.tipo == tipo)
    
    if produto_id:
        query = query.filter(MovimentacaoModel.produto_id == produto_id)
    
    movimentacoes = query.order_by(MovimentacaoModel.data_movimentacao.desc()).limit(limit).all()
    return movimentacoes

@router.get("/{movimentacao_id}", response_model=Movimentacao)
def obter_movimentacao(movimentacao_id: int, db: Session = Depends(get_db)):
    movimentacao = db.query(MovimentacaoModel).filter(MovimentacaoModel.id == movimentacao_id).first()
    if not movimentacao:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    return movimentacao

@router.post("/", response_model=Movimentacao)
def criar_movimentacao(movimentacao: MovimentacaoCreate, db: Session = Depends(get_db)):
    # Verifica se o produto existe
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == movimentacao.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Calcula o valor total
    valor_total = movimentacao.quantidade * movimentacao.valor_unitario
    
    # Cria a movimentação
    db_movimentacao = MovimentacaoModel(
        **movimentacao.model_dump(),
        valor_total=valor_total
    )
    
    # Atualiza o estoque do produto
    if movimentacao.tipo == "entrada":
        produto.estoque_atual += movimentacao.quantidade
    elif movimentacao.tipo == "saida":
        if produto.estoque_atual < movimentacao.quantidade:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
        produto.estoque_atual -= movimentacao.quantidade
    
    db.add(db_movimentacao)
    db.commit()
    db.refresh(db_movimentacao)
    return db_movimentacao

@router.get("/recentes/lista", response_model=List[Movimentacao])
def movimentacoes_recentes(limit: int = 5, db: Session = Depends(get_db)):
    movimentacoes = db.query(MovimentacaoModel).order_by(
        MovimentacaoModel.data_movimentacao.desc()
    ).limit(limit).all()
    return movimentacoes
