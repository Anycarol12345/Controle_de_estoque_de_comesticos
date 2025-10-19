from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db, Configuracao as ConfiguracaoModel, Categoria as CategoriaModel
from schemas import Configuracao, ConfiguracaoUpdate, Categoria, CategoriaCreate

router = APIRouter()

@router.get("/", response_model=List[Configuracao])
def listar_configuracoes(db: Session = Depends(get_db)):
    configs = db.query(ConfiguracaoModel).all()
    return configs

@router.put("/{config_id}", response_model=Configuracao)
def atualizar_configuracao(config_id: int, config: ConfiguracaoUpdate, db: Session = Depends(get_db)):
    db_config = db.query(ConfiguracaoModel).filter(ConfiguracaoModel.id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuração não encontrada")
    
    db_config.valor = config.valor
    db.commit()
    db.refresh(db_config)
    return db_config

@router.get("/categorias", response_model=List[Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(CategoriaModel).all()
    return categorias

@router.post("/categorias", response_model=Categoria)
def criar_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    existe = db.query(CategoriaModel).filter(CategoriaModel.nome == categoria.nome).first()
    if existe:
        raise HTTPException(status_code=400, detail="Categoria já existe")
    
    db_categoria = CategoriaModel(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria
