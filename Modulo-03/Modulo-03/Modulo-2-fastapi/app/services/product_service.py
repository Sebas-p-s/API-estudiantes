from app.exceptions import ProductAlreadyExistsError, ProductNotFoundError
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def list_products(self):
        return self.repository.list_all()

    def get_product(self, product_id: int):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Producto con id {product_id} no encontrado")
        return product

    def create_product(self, product_data):
        if self.repository.exists_by_name(product_data.name):
            raise ProductAlreadyExistsError(f"Ya existe un producto con el nombre '{product_data.name}'")
        return self.repository.create(product_data)

    def update_product(self, product_id: int, product_data):
        self.get_product(product_id)  # Lanza ProductNotFoundError si no existe
        return self.repository.update(product_id, product_data)

    def delete_product(self, product_id: int):
        self.get_product(product_id)  # Lanza ProductNotFoundError si no existe
        self.repository.delete(product_id)
