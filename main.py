from fastapi import FastAPI
from infraestructura.persistencia.configuracion import engine, Base
from infraestructura.api import auth_router

# Crea las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Biblioteca Digital",
    description="Sistema de gestión para Biblioteca, Repositorio y Marketplace.",
    version="1.0.0"
)

app.include_router(auth_router.router)

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de la Biblioteca Digital"}