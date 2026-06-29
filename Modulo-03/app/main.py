from fastapi import FastAPI

from app.database import engine, Base
from app.routers import products

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product API", description="A simple API for managing products")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product API!"}

app.include_router(products.router)
