from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uvicorn

from database import engine, get_db, Base
import models

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Integra+ Estoque")

# Templates
templates = Jinja2Templates(directory="templates")

# Rotas
from routers import dashboard, produtos, movimentacoes, relatorios, alertas

app.include_router(dashboard.router)
app.include_router(produtos.router)
app.include_router(movimentacoes.router)
app.include_router(relatorios.router)
app.include_router(alertas.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
