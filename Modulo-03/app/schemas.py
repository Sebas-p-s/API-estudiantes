from pydantic import BaseModel, Field

class ProductBase(BaseModel):

    name: str = Field(min_length=3, max_length=100, example="Portátil Lenovo") 
    price: float = Field(gt=0, example=2500000)
    stock: int = Field(ge=0, example=4)
    category: str = Field(min_length=3, max_length=50, example="Tecnologia") # <-- NUEVO CAMPO

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: str | None = Field(default=None, min_length=3, max_length=100, example="Portátil Lenovo")
    price: float | None = Field(default=None, gt=0, example=2500000)
    stock: int | None = Field(default=None, ge=0, example=4)
    category: str | None = Field(default=None, min_length=3, max_length=50, example="Tecnologia") # <-- NUEVO CAMPO

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True