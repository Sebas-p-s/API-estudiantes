from app.models.product import Product


class ProductRepository:
    def __init__(self):
        self._products: dict[int, Product] = {}
        self._next_id = 1

    def list_all(self) -> list[Product]:
        return list(self._products.values())

    def get_by_id(self, product_id: int) -> Product | None:
        return self._products.get(product_id)

    def exists_by_name(self, name: str) -> bool:
        return any(p.name.lower() == name.lower() for p in self._products.values())

    def create(self, product_data) -> Product:
        product = Product(id=self._next_id, **product_data.model_dump())
        self._products[self._next_id] = product
        self._next_id += 1
        return product

    def update(self, product_id: int, product_data) -> Product | None:
        product = self._products.get(product_id)
        if not product:
            return None
        data = product_data.model_dump(exclude_none=True)
        for key, value in data.items():
            setattr(product, key, value)
        return product

    def delete(self, product_id: int) -> bool:
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False
