from fastapi import FastAPI
from apis.productos_api import router as productos_router
from apis.clientes_api import router as clientes_router
from apis.pedidos_api import router as pedidos_router
from database import init_db

app = FastAPI(
    title="Proyecto con FastAPI, MySQL y arquitectura por capas",
    description="Una API para gestionar productos, clientes y pedidos",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(productos_router)
app.include_router(clientes_router)
app.include_router(pedidos_router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Productos, Clientes y Pedidos"}
