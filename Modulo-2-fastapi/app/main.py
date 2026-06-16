from fastapi import FastAPI

from app.api.routes.product_routes import router as product_router

app = FastAPI(
    title="API de Productos V2",
    description="API REST con arquitectura por capas: routers, servicios y repositorios",
    version="2.0.0",
)

app.include_router(product_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}
