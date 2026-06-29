from dataclasses import dataclass

@dataclass # Decorador para convertir una clase en una clase de datos
class Product:
    id: int
    name: str
    price: float
    stock: int
    active: bool = True