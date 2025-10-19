from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

class TipoProduto(str, enum.Enum):
    PERFUME = "perfume"
    CREME = "creme"
    MAQUIAGEM = "maquiagem"
    OUTRO = "outro"

class TipoMovimentacao(str, enum.Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"

class Marca(Base):
    __tablename__ = "marcas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    ativo = Column(Integer, default=1)
    
    produtos = relationship("Produto", back_populates="marca")

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    tipo_produto = Column(SQLEnum(TipoProduto), default=TipoProduto.OUTRO)
    marca_id = Column(Integer, ForeignKey("marcas.id"))
    categoria = Column(String)
    preco_custo = Column(Float, nullable=False)
    preco_venda = Column(Float, nullable=False)
    quantidade_estoque = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=5)
    
    # Campos específicos para perfumes
    concentracao = Column(String)
    subfamilia = Column(String)
    ocasiao = Column(String)
    
    # Campos específicos para cremes
    tipo_pele = Column(String)
    acao_resultado = Column(String)
    
    # Campos específicos para maquiagens
    textura = Column(String)
    cobertura = Column(String)
    fundo_cor = Column(String)
    tonalidade = Column(String)
    
    # Campos comuns
    linha = Column(String)
    propriedades = Column(Text)
    detalhes = Column(Text)
    ingredientes = Column(Text)
    como_usar = Column(Text)
    
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    
    marca = relationship("Marca", back_populates="produtos")
    movimentacoes = relationship("Movimentacao", back_populates="produto")

class Movimentacao(Base):
    __tablename__ = "movimentacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    tipo = Column(SQLEnum(TipoMovimentacao), nullable=False)
    quantidade = Column(Integer, nullable=False)
    lote = Column(String)
    validade = Column(DateTime)
    observacao = Column(Text)
    data = Column(DateTime, default=datetime.utcnow)
    
    produto = relationship("Produto", back_populates="movimentacoes")
