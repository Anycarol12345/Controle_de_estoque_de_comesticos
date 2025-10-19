from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db, Produto as ProdutoModel, Marca as MarcaModel, Categoria as CategoriaModel
from schemas import Produto, ProdutoCreate, ProdutoUpdate

router = APIRouter()

@router.get("/", response_model=List[Produto])
def listar_produtos(
    marca_id: Optional[int] = None,
    busca: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProdutoModel)
    
    if marca_id:
        query = query.filter(ProdutoModel.marca_id == marca_id)
    
    if busca:
        query = query.filter(
            (ProdutoModel.nome.contains(busca)) | 
            (ProdutoModel.codigo.contains(busca))
        )
    
    produtos = query.all()
    return produtos

@router.get("/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/", response_model=Produto)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    # Verifica se o código já existe
    existe = db.query(ProdutoModel).filter(ProdutoModel.codigo == produto.codigo).first()
    if existe:
        raise HTTPException(status_code=400, detail="Código de produto já existe")
    
    db_produto = ProdutoModel(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.put("/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto: ProdutoUpdate, db: Session = Depends(get_db)):
    db_produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    update_data = produto.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_produto, key, value)
    
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.delete("/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(db_produto)
    db.commit()
    return {"message": "Produto deletado com sucesso"}
