from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import db, init_db
from models import Produto, Movimentacao, Marca
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sua-chave-secreta-aqui'

init_db(app)

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    total_produtos = Produto.query.count()
    valor_total = db.session.query(db.func.sum(Produto.quantidade_estoque * Produto.preco_venda)).scalar() or 0
    produtos_baixo_estoque = Produto.query.filter(Produto.quantidade_estoque <= Produto.estoque_minimo).count()
    
    movimentacoes_recentes = Movimentacao.query.order_by(Movimentacao.data.desc()).limit(5).all()
    produtos_alerta = Produto.query.filter(Produto.quantidade_estoque <= Produto.estoque_minimo).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_produtos=total_produtos,
                         valor_total=valor_total,
                         produtos_baixo_estoque=produtos_baixo_estoque,
                         movimentacoes_recentes=movimentacoes_recentes,
                         produtos_alerta=produtos_alerta)

@app.route('/produtos')
def produtos():
    marca_filtro = request.args.get('marca', '')
    busca = request.args.get('busca', '')
    
    query = Produto.query
    if marca_filtro:
        query = query.join(Marca).filter(Marca.nome == marca_filtro)
    if busca:
        query = query.filter(Produto.nome.contains(busca))
    
    produtos = query.all()
    marcas = Marca.query.all()
    
    return render_template('produtos.html', produtos=produtos, marcas=marcas, marca_filtro=marca_filtro, busca=busca)

@app.route('/produtos/novo', methods=['GET', 'POST'])
def produto_novo():
    if request.method == 'POST':
        produto = Produto(
            nome=request.form['nome'],
            sku=request.form['sku'],
            marca_id=request.form['marca_id'],
            categoria=request.form.get('categoria'),
            tipo_produto=request.form['tipo_produto'],
            preco_custo=float(request.form['preco_custo']),
            preco_venda=float(request.form['preco_venda']),
            estoque_minimo=int(request.form.get('estoque_minimo', 10)),
            concentracao=request.form.get('concentracao'),
            subfamilias=request.form.get('subfamilias'),
            ocasiao=request.form.get('ocasiao'),
            tipo_pele=request.form.get('tipo_pele'),
            acao_resultado=request.form.get('acao_resultado'),
            textura=request.form.get('textura'),
            cobertura=request.form.get('cobertura'),
            fundo_cor=request.form.get('fundo_cor'),
            tonalidade=request.form.get('tonalidade'),
            linha=request.form.get('linha'),
            propriedades=request.form.get('propriedades'),
            detalhes=request.form.get('detalhes'),
            ingredientes=request.form.get('ingredientes'),
            como_usar=request.form.get('como_usar')
        )
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('produtos'))
    
    marcas = Marca.query.all()
    return render_template('produto_form.html', marcas=marcas, produto=None)

@app.route('/produtos/<int:id>')
def produto_detalhes(id):
    produto = Produto.query.get_or_404(id)
    return render_template('produto_detalhes.html', produto=produto)

@app.route('/produtos/<int:id>/deletar', methods=['POST'])
def produto_deletar(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('produtos'))

@app.route('/movimentacoes')
def movimentacoes():
    movimentacoes = Movimentacao.query.order_by(Movimentacao.data.desc()).all()
    produtos = Produto.query.all()
    return render_template('movimentacoes.html', movimentacoes=movimentacoes, produtos=produtos)

@app.route('/movimentacoes/entrada', methods=['POST'])
def movimentacao_entrada():
    produto_id = int(request.form['produto_id'])
    quantidade = int(request.form['quantidade'])
    
    produto = Produto.query.get_or_404(produto_id)
    produto.quantidade_estoque += quantidade
    
    movimentacao = Movimentacao(
        produto_id=produto_id,
        tipo='entrada',
        quantidade=quantidade,
        lote=request.form.get('lote'),
        validade=datetime.strptime(request.form['validade'], '%Y-%m-%d').date() if request.form.get('validade') else None,
        observacao=request.form.get('observacao')
    )
    
    db.session.add(movimentacao)
    db.session.commit()
    return redirect(url_for('movimentacoes'))

@app.route('/movimentacoes/saida', methods=['POST'])
def movimentacao_saida():
    produto_id = int(request.form['produto_id'])
    quantidade = int(request.form['quantidade'])
    
    produto = Produto.query.get_or_404(produto_id)
    
    if produto.quantidade_estoque < quantidade:
        return "Estoque insuficiente", 400
    
    produto.quantidade_estoque -= quantidade
    
    movimentacao = Movimentacao(
        produto_id=produto_id,
        tipo='saida',
        quantidade=quantidade,
        observacao=request.form.get('observacao')
    )
    
    db.session.add(movimentacao)
    db.session.commit()
    return redirect(url_for('movimentacoes'))

@app.route('/relatorios')
def relatorios():
    vendas_marca = db.session.query(
        Marca.nome,
        db.func.sum(Movimentacao.quantidade).label('total')
    ).select_from(Marca).join(Produto).join(Movimentacao).filter(
        Movimentacao.tipo == 'saida'
    ).group_by(Marca.nome).all()
    
    produtos_vendidos = db.session.query(
        Produto.nome,
        Marca.nome.label('marca'),
        db.func.sum(Movimentacao.quantidade).label('total')
    ).select_from(Produto).join(Marca).join(Movimentacao).filter(
        Movimentacao.tipo == 'saida'
    ).group_by(Produto.id).order_by(db.desc('total')).limit(10).all()
    
    # Rentabilidade
    produtos_rentabilidade = Produto.query.filter(Produto.quantidade_estoque > 0).all()
    
    return render_template('relatorios.html', 
                         vendas_marca=vendas_marca,
                         produtos_vendidos=produtos_vendidos,
                         produtos_rentabilidade=produtos_rentabilidade)

@app.route('/alertas')
def alertas():
    # Produtos com estoque baixo
    estoque_baixo = Produto.query.filter(
        Produto.quantidade_estoque <= Produto.estoque_minimo
    ).all()
    
    # Produtos próximos ao vencimento (30 dias)
    data_limite = datetime.now().date() + timedelta(days=30)
    proximos_vencimento = Movimentacao.query.filter(
        Movimentacao.validade != None,
        Movimentacao.validade <= data_limite
    ).all()
    
    # Produtos sem movimentação (90 dias)
    data_limite_mov = datetime.now() - timedelta(days=90)
    produtos_sem_mov = Produto.query.filter(
        ~Produto.movimentacoes.any(Movimentacao.data >= data_limite_mov)
    ).all()
    
    return render_template('alertas.html',
                         estoque_baixo=estoque_baixo,
                         proximos_vencimento=proximos_vencimento,
                         produtos_sem_mov=produtos_sem_mov)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Criar marcas padrão se não existirem
        if Marca.query.count() == 0:
            marcas = ['Avon', 'O Boticário', 'Eudora', 'Quem disse Berenice?']
            for nome in marcas:
                marca = Marca(nome=nome)
                db.session.add(marca)
            db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
