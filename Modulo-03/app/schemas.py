from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):

    name: str = Field(min_length=3, max_length=100, example="Portátil Lenovo")
    price: float = Field(gt=0, le=10000000, example=2500000)
    stock: int = Field(ge=0, le=10000, example=4)
    category: str = Field(min_length=3, max_length=50, example="Tecnologia")  # <-- NUEVO CAMPO

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        name = value.strip()
        if name.lower() in ["test", "prueba", "producto"]:
            raise ValueError("El nombre del producto no esta permitido")
        if not name:
            raise ValueError("El nombre no puede estar vacío o contener solo espacios")
        return name

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str):
        category = value.strip()
        if not category:
            raise ValueError("La categoría no puede estar vacía o contener solo espacios")
        return category


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str | None = Field(default=None, min_length=3, max_length=100, example="Portátil Lenovo")
    price: float | None = Field(default=None, gt=0, le=10000000, example=2500000)
    stock: int | None = Field(default=None, ge=0, le=10000, example=4)
    category: str | None = Field(default=None, min_length=3, max_length=50, example="Tecnologia")  # <-- NUEVO CAMPO

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None):
        if value is None:
            return value
        name = value.strip()
        if name.lower() in ["test", "prueba", "producto"]:
            raise ValueError("El nombre del producto no esta permitido")
        if not name:
            raise ValueError("El nombre no puede estar vacío o contener solo espacios")
        return name

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str | None):
        if value is None:
            return value
        category = value.strip()
        if not category:
            raise ValueError("La categoría no puede estar vacía o contener solo espacios")
        return category


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True