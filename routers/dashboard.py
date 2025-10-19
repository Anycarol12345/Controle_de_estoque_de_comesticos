```python file="routers/dashboard.py"
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

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    # Estatísticas
    total_produtos = db.query(models.Produto).count()
    valor_total = db.query(func.sum(models.Produto.preco_venda * models.Produto.quantidade_estoque)).scalar() or 0
    produtos_baixo_estoque = db.query(models.Produto).filter(
        models.Produto.quantidade_estoque <= models.Produto.estoque_minimo
    ).count()
    
    # Movimentações recentes
    movimentacoes_recentes = db.query(models.Movimentacao).order_by(
        desc(models.Movimentacao.data)
    ).limit(5).all()
    
    # Produtos com estoque baixo
    produtos_alerta = db.query(models.Produto).filter(
        models.Produto.quantidade_estoque <= models.Produto.estoque_minimo
    ).limit(5).all()
    
    # Top produtos por valor
    top_produtos = db.query(models.Produto).order_by(
        desc(models.Produto.preco_venda * models.Produto.quantidade_estoque)
    ).limit(5).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_produtos": total_produtos,
        "valor_total": valor_total,
        "produtos_baixo_estoque": produtos_baixo_estoque,
        "movimentacoes_recentes": movimentacoes_recentes,
        "produtos_alerta": produtos_alerta,
        "top_produtos": top_produtos
    })
