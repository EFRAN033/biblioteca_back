# efran033/biblioteca_back/biblioteca_back-e45426e2e00fbbc201232909bbf09d0ca9ea44ce/main.py

from fastapi import FastAPI
# --- 1. Importa el Middleware de CORS ---
from fastapi.middleware.cors import CORSMiddleware 
from infraestructura.persistencia.configuracion import engine, Base
from infraestructura.api import auth_router, market_router, libro_router, alquiler_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Biblioteca Digital",
    description="Sistema de gestión para Biblioteca, Repositorio y Marketplace.",
    version="1.0.0"
)

# --- 2. Define los orígenes permitidos (tu frontend) ---
# (Revisa el puerto de tu frontend. El default de Vite es 5173)
origins = [
    "http://localhost:5173",
    "http://localhost:3000", # Si usas otro puerto
    "http://localhost:8080", # Si usas otro puerto
]

# --- 3. Añade el Middleware de CORS a tu app ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Permite estos orígenes
    allow_credentials=True,    # Permite cookies (importante para auth)
    allow_methods=["*"],       # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],       # Permite todos los headers
)

# --- 4. Tus routers (esto ya lo tenías) ---
app.include_router(auth_router.router)
app.include_router(market_router.router)
app.include_router(libro_router.router)
app.include_router(alquiler_router.router)


@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de la Biblioteca Digital"}