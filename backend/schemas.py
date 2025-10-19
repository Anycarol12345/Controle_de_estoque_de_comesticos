from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schemas para Marca
class MarcaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    ativo: int = 1

class MarcaCreate(MarcaBase):
    pass

class MarcaUpdate(MarcaBase):
    pass

class Marca(MarcaBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para Categoria
class CategoriaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para Produto
class ProdutoBase(BaseModel):
    codigo: str
    nome: str
    descricao: Optional[str] = None
    marca_id: int
    categoria_id: int
    preco_custo: float
    preco_venda: float
    estoque_minimo: int = 5
    unidade: str = "UN"
    ativo: int = 1

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    codigo: Optional[str] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    marca_id: Optional[int] = None
    categoria_id: Optional[int] = None
    preco_custo: Optional[float] = None
    preco_venda: Optional[float] = None
    estoque_minimo: Optional[int] = None
    unidade: Optional[str] = None
    ativo: Optional[int] = None

class Produto(ProdutoBase):
    id: int
    estoque_atual: int
    data_cadastro: datetime
    marca: Marca
    categoria: Categoria
    
    class Config:
        from_attributes = True

# Schemas para Movimentação
class MovimentacaoBase(BaseModel):
    produto_id: int
    tipo: str  # "entrada" ou "saida"
    quantidade: int
    valor_unitario: float
    lote: Optional[str] = None
    data_validade: Optional[datetime] = None
    observacao: Optional[str] = None

class MovimentacaoCreate(MovimentacaoBase):
    pass

class Movimentacao(MovimentacaoBase):
    id: int
    valor_total: float
    data_movimentacao: datetime
    produto: Produto
    
    class Config:
        from_attributes = True

# Schemas para Configuração
class ConfiguracaoBase(BaseModel):
    chave: str
    valor: str
    descricao: Optional[str] = None

class ConfiguracaoCreate(ConfiguracaoBase):
    pass

class ConfiguracaoUpdate(BaseModel):
    valor: str

class Configuracao(ConfiguracaoBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para Relatórios
class EstatisticasDashboard(BaseModel):
    total_produtos: int
    valor_total_estoque: float
    produtos_estoque_baixo: int
    movimentacoes_mes: int

class VendasPorMarca(BaseModel):
    marca: str
    total_vendas: float
    quantidade_vendida: int

class ProdutoRentabilidade(BaseModel):
    produto: str
    codigo: str
    quantidade_vendida: int
    receita_total: float
    custo_total: float
    lucro: float
    margem_percentual: float
