from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from database import init_db
from routers import produtos, movimentacoes, marcas, relatorios, alertas, configuracoes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o banco de dados ao iniciar
    init_db()
    yield

app = FastAPI(
    title="Integra+ API",
    description="API para Sistema de Controle de Estoque de Cosméticos",
    version="1.0.0",
    lifespan=lifespan
)

# Configuração CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra os routers
app.include_router(produtos.router, prefix="/api/produtos", tags=["Produtos"])
app.include_router(movimentacoes.router, prefix="/api/movimentacoes", tags=["Movimentações"])
app.include_router(marcas.router, prefix="/api/marcas", tags=["Marcas"])
app.include_router(relatorios.router, prefix="/api/relatorios", tags=["Relatórios"])
app.include_router(alertas.router, prefix="/api/alertas", tags=["Alertas"])
app.include_router(configuracoes.router, prefix="/api/configuracoes", tags=["Configurações"])

@app.get("/")
def read_root():
    return {
        "message": "Integra+ API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
