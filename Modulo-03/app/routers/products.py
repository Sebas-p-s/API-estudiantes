from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[schemas.ProductResponse], status_code=status.HTTP_200_OK)
def list_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products

@router.get("/{product_id}", response_model=schemas.ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PRODUCT_NOT_FOUND",
                    "message": "El producto solicitado no existe"
                }
            }
        )
    return product

@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    existing_product = crud.get_product_by_name(db, product.name)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "PRODUCT_ALREADY_EXISTS",
                    "message": "Ya existe un producto con ese nombre"
                }
            }
        )
    return crud.create_product(db, product)

@router.put("/{product_id}", response_model=schemas.ProductResponse, status_code=status.HTTP_200_OK)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PRODUCT_NOT_FOUND",
                    "message": "El producto solicitado no existe"
                }
            }
        )

    # Paso 7: validar que el cuerpo de la petición no esté vacío
    update_data = product.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "EMPTY_UPDATE_BODY",
                    "message": "Debe enviar al menos un campo para actualizar"
                }
            }
        )

    # Paso 8: validar duplicados también al actualizar
    if "name" in update_data:
        existing_product = crud.get_product_by_name(db, update_data["name"])
        if existing_product and existing_product.id != product_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": {
                        "code": "PRODUCT_ALREADY_EXISTS",
                        "message": "Ya existe un producto con ese nombre"
                    }
                }
            )

    updated_product = crud.update_product(db, product_id, product)
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted_product = crud.delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PRODUCT_NOT_FOUND",
                    "message": "El producto solicitado no existe"
                }
            }
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)