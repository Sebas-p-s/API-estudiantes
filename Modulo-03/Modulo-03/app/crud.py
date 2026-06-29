from sqlalchemy.orm import Session
from app import models, schemas

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name, 
        price=product.price, 
        stock=product.stock,
        category=product.category # <-- INCLUIR EN CREACIÓN
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        if product.name is not None:
            db_product.name = product.name
        if product.price is not None:
            db_product.price = product.price
        if product.stock is not None:
            db_product.stock = product.stock
        if product.category is not None: 
            db_product.category = product.category
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product