from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
import models

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/produtos", response_class=HTMLResponse)
async def listar_produtos(request: Request, marca: Optional[str] = None, busca: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Produto)
    
    if marca:
        query = query.join(models.Marca).filter(models.Marca.nome == marca)
    
    if busca:
        query = query.filter(models.Produto.nome.contains(busca))
    
    produtos = query.all()
    marcas = db.query(models.Marca).filter(models.Marca.ativo == 1).all()
    
    return templates.TemplateResponse("produtos/lista.html", {
        "request": request,
        "produtos": produtos,
        "marcas": marcas,
        "marca_selecionada": marca,
        "busca": busca or ""
    })

@router.get("/produtos/novo", response_class=HTMLResponse)
async def novo_produto_form(request: Request, db: Session = Depends(get_db)):
    marcas = db.query(models.Marca).filter(models.Marca.ativo == 1).all()
    return templates.TemplateResponse("produtos/form.html", {
        "request": request,
        "marcas": marcas,
        "produto": None
    })

@router.post("/produtos/novo")
async def criar_produto(
    nome: str = Form(...),
    sku: str = Form(...),
    tipo_produto: str = Form(...),
    marca_id: int = Form(...),
    categoria: str = Form(None),
    preco_custo: float = Form(...),
    preco_venda: float = Form(...),
    estoque_minimo: int = Form(5),
    # Campos específicos
    concentracao: str = Form(None),
    subfamilia: str = Form(None),
    ocasiao: str = Form(None),
    tipo_pele: str = Form(None),
    acao_resultado: str = Form(None),
    textura: str = Form(None),
    cobertura: str = Form(None),
    fundo_cor: str = Form(None),
    tonalidade: str = Form(None),
    linha: str = Form(None),
    propriedades: str = Form(None),
    detalhes: str = Form(None),
    ingredientes: str = Form(None),
    como_usar: str = Form(None),
    db: Session = Depends(get_db)
):
    produto = models.Produto(
        nome=nome,
        sku=sku,
        tipo_produto=tipo_produto,
        marca_id=marca_id,
        categoria=categoria,
        preco_custo=preco_custo,
        preco_venda=preco_venda,
        estoque_minimo=estoque_minimo,
        concentracao=concentracao,
        subfamilia=subfamilia,
        ocasiao=ocasiao,
        tipo_pele=tipo_pele,
        acao_resultado=acao_resultado,
        textura=textura,
        cobertura=cobertura,
        fundo_cor=fundo_cor,
        tonalidade=tonalidade,
        linha=linha,
        propriedades=propriedades,
        detalhes=detalhes,
        ingredientes=ingredientes,
        como_usar=como_usar
    )
    
    db.add(produto)
    db.commit()
    
    return RedirectResponse(url="/produtos", status_code=303)

@router.get("/produtos/{produto_id}", response_class=HTMLResponse)
async def detalhes_produto(request: Request, produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return templates.TemplateResponse("produtos/detalhes.html", {
        "request": request,
        "produto": produto
    })

@router.post("/produtos/{produto_id}/excluir")
async def excluir_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if produto:
        db.delete(produto)
        db.commit()
    return RedirectResponse(url="/produtos", status_code=303)
