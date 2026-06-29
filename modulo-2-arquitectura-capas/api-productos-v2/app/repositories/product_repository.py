from app.models.product import Product
from app.services.schemas import ProductCreate


class ProductRepository:
    def __init__(self):
        self._products: dict[int, Product] = {}
        self._next_id = 1

    def list_all(self) -> list[Product]:
        return list(self._products.values())

    def get_by_id(self, product_id: int) -> Product | None:
        return self._products.get(product_id)