from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./integra_estoque.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelos do Banco de Dados

class Marca(Base):
    __tablename__ = "marcas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    descricao = Column(Text, nullable=True)
    ativo = Column(Integer, default=1)
    
    produtos = relationship("Produto", back_populates="marca")

class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    descricao = Column(Text, nullable=True)
    
    produtos = relationship("Produto", back_populates="categoria")

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(Text, nullable=True)
    marca_id = Column(Integer, ForeignKey("marcas.id"))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    preco_custo = Column(Float)
    preco_venda = Column(Float)
    estoque_atual = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=5)
    unidade = Column(String, default="UN")
    ativo = Column(Integer, default=1)
    data_cadastro = Column(DateTime, default=datetime.now)
    
    marca = relationship("Marca", back_populates="produtos")
    categoria = relationship("Categoria", back_populates="produtos")
    movimentacoes = relationship("Movimentacao", back_populates="produto")

class Movimentacao(Base):
    __tablename__ = "movimentacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    tipo = Column(String)  # "entrada" ou "saida"
    quantidade = Column(Integer)
    valor_unitario = Column(Float)
    valor_total = Column(Float)
    lote = Column(String, nullable=True)
    data_validade = Column(DateTime, nullable=True)
    observacao = Column(Text, nullable=True)
    data_movimentacao = Column(DateTime, default=datetime.now)
    
    produto = relationship("Produto", back_populates="movimentacoes")

class Configuracao(Base):
    __tablename__ = "configuracoes"
    
    id = Column(Integer, primary_key=True, index=True)
    chave = Column(String, unique=True, index=True)
    valor = Column(String)
    descricao = Column(Text, nullable=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Adiciona dados iniciais
    db = SessionLocal()
    
    # Verifica se já existem marcas
    if db.query(Marca).count() == 0:
        marcas_iniciais = [
            Marca(nome="Avon", descricao="Produtos Avon", ativo=1),
            Marca(nome="O Boticário", descricao="Produtos O Boticário", ativo=1),
            Marca(nome="Eudora", descricao="Produtos Eudora", ativo=1),
            Marca(nome="Quem disse Berenice", descricao="Produtos Quem disse Berenice", ativo=1),
        ]
        db.add_all(marcas_iniciais)
    
    # Verifica se já existem categorias
    if db.query(Categoria).count() == 0:
        categorias_iniciais = [
            Categoria(nome="Perfumaria", descricao="Perfumes e colônias"),
            Categoria(nome="Maquiagem", descricao="Produtos de maquiagem"),
            Categoria(nome="Cuidados Pessoais", descricao="Cremes, loções e cuidados"),
            Categoria(nome="Cabelos", descricao="Produtos para cabelos"),
        ]
        db.add_all(categorias_iniciais)
    
    # Configurações padrão
    if db.query(Configuracao).count() == 0:
        configs_iniciais = [
            Configuracao(chave="dias_alerta_validade", valor="30", descricao="Dias antes do vencimento para alertar"),
            Configuracao(chave="dias_sem_movimentacao", valor="90", descricao="Dias sem movimentação para alertar"),
        ]
        db.add_all(configs_iniciais)
    
    db.commit()
    db.close()
