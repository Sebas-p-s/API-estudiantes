from fastapi import APIRouter, HTTPException, status

from app.exceptions import ProductAlreadyExistsError, ProductNotFoundError
from app.repositories.product_repository import ProductRepository
from app.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Productos"])

repo = ProductRepository()
service = ProductService(repo)


@router.get("/", response_model=list[ProductResponse])
def list_products():
    return service.list_products()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    try:
        return service.get_product(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    try:
        return service.create_product(product)
    except ProductAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate):
    try:
        return service.update_product(product_id, product)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    try:
        service.delete_product(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
