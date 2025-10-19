from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db, Marca as MarcaModel
from schemas import Marca, MarcaCreate, MarcaUpdate

router = APIRouter()

@router.get("/", response_model=List[Marca])
def listar_marcas(db: Session = Depends(get_db)):
    marcas = db.query(MarcaModel).filter(MarcaModel.ativo == 1).all()
    return marcas

@router.get("/{marca_id}", response_model=Marca)
def obter_marca(marca_id: int, db: Session = Depends(get_db)):
    marca = db.query(MarcaModel).filter(MarcaModel.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    return marca

@router.post("/", response_model=Marca)
def criar_marca(marca: MarcaCreate, db: Session = Depends(get_db)):
    existe = db.query(MarcaModel).filter(MarcaModel.nome == marca.nome).first()
    if existe:
        raise HTTPException(status_code=400, detail="Marca já existe")
    
    db_marca = MarcaModel(**marca.model_dump())
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca

@router.put("/{marca_id}", response_model=Marca)
def atualizar_marca(marca_id: int, marca: MarcaUpdate, db: Session = Depends(get_db)):
    db_marca = db.query(MarcaModel).filter(MarcaModel.id == marca_id).first()
    if not db_marca:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    
    for key, value in marca.model_dump().items():
        setattr(db_marca, key, value)
    
    db.commit()
    db.refresh(db_marca)
    return db_marca
