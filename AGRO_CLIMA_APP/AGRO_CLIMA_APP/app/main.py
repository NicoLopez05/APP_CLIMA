# app/main.py
from fastapi import FastAPI
from .routers import auth, sensores

app = FastAPI(title="Agro Clima API")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(sensores.router, prefix="/sensores", tags=["sensores"])
