from database import db
from datetime import datetime

class Marca(db.Model):
    __tablename__ = 'marcas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    produtos = db.relationship('Produto', backref='marca', lazy=True)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)
    categoria = db.Column(db.String(100))
    tipo_produto = db.Column(db.String(50))  # perfume, creme, maquiagem
    preco_custo = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=10)
    
    # Campos específicos para perfumes
    concentracao = db.Column(db.String(100))
    subfamilias = db.Column(db.String(200))
    ocasiao = db.Column(db.String(100))
    
    # Campos específicos para cremes
    tipo_pele = db.Column(db.String(100))
    acao_resultado = db.Column(db.String(200))
    
    # Campos específicos para maquiagens
    textura = db.Column(db.String(100))
    cobertura = db.Column(db.String(100))
    fundo_cor = db.Column(db.String(100))
    tonalidade = db.Column(db.String(100))
    
    # Campos comuns
    linha = db.Column(db.String(100))
    propriedades = db.Column(db.String(200))
    detalhes = db.Column(db.Text)
    ingredientes = db.Column(db.Text)
    como_usar = db.Column(db.Text)
    
    movimentacoes = db.relationship('Movimentacao', backref='produto', lazy=True)
    
    @property
    def margem_lucro(self):
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0

class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # entrada ou saida
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    lote = db.Column(db.String(50))
    validade = db.Column(db.Date)
    observacao = db.Column(db.Text)
