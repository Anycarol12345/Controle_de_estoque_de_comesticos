from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict
from database import get_db, Produto as ProdutoModel, Movimentacao as MovimentacaoModel, Configuracao as ConfiguracaoModel

router = APIRouter()

@router.get("/estoque-baixo")
def alertas_estoque_baixo(db: Session = Depends(get_db)) -> List[Dict]:
    produtos = db.query(ProdutoModel).filter(
        ProdutoModel.estoque_atual <= ProdutoModel.estoque_minimo,
        ProdutoModel.ativo == 1
    ).all()
    
    return [
        {
            "id": p.id,
            "codigo": p.codigo,
            "nome": p.nome,
            "estoque_atual": p.estoque_atual,
            "estoque_minimo": p.estoque_minimo,
            "tipo": "estoque_baixo"
        }
        for p in produtos
    ]

@router.get("/proximos-vencimento")
def alertas_proximos_vencimento(db: Session = Depends(get_db)) -> List[Dict]:
    # Busca configuração de dias para alerta
    config = db.query(ConfiguracaoModel).filter(
        ConfiguracaoModel.chave == "dias_alerta_validade"
    ).first()
    dias_alerta = int(config.valor) if config else 30
    
    data_limite = datetime.now() + timedelta(days=dias_alerta)
    
    movimentacoes = db.query(MovimentacaoModel).filter(
        MovimentacaoModel.data_validade.isnot(None),
        MovimentacaoModel.data_validade <= data_limite,
        MovimentacaoModel.tipo == "entrada"
    ).all()
    
    return [
        {
            "id": m.id,
            "produto_id": m.produto_id,
            "produto_nome": m.produto.nome,
            "lote": m.lote,
            "data_validade": m.data_validade.isoformat(),
            "dias_restantes": (m.data_validade - datetime.now()).days,
            "tipo": "vencimento"
        }
        for m in movimentacoes
    ]

@router.get("/sem-movimentacao")
def alertas_sem_movimentacao(db: Session = Depends(get_db)) -> List[Dict]:
    # Busca configuração de dias sem movimentação
    config = db.query(ConfiguracaoModel).filter(
        ConfiguracaoModel.chave == "dias_sem_movimentacao"
    ).first()
    dias_sem_mov = int(config.valor) if config else 90
    
    data_limite = datetime.now() - timedelta(days=dias_sem_mov)
    
    # Busca produtos ativos
    produtos = db.query(ProdutoModel).filter(ProdutoModel.ativo == 1).all()
    
    resultado = []
    for produto in produtos:
        # Busca última movimentação do produto
        ultima_mov = db.query(MovimentacaoModel).filter(
            MovimentacaoModel.produto_id == produto.id
        ).order_by(MovimentacaoModel.data_movimentacao.desc()).first()
        
        if not ultima_mov or ultima_mov.data_movimentacao < data_limite:
            dias_parado = (datetime.now() - ultima_mov.data_movimentacao).days if ultima_mov else 999
            resultado.append({
                "id": produto.id,
                "codigo": produto.codigo,
                "nome": produto.nome,
                "estoque_atual": produto.estoque_atual,
                "ultima_movimentacao": ultima_mov.data_movimentacao.isoformat() if ultima_mov else None,
                "dias_parado": dias_parado,
                "tipo": "sem_movimentacao"
            })
    
    return resultado
