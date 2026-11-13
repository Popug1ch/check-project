from dataclasses import dataclass, field

class DomainError(Exception):
    pass

@dataclass
class Product:
    id: int
    name: str 
    price: float
    stock: int

    def validate_quantity(self,quantity: int):
        if quantity <= 0:
            raise DomainError("Количество должно быть больше нуля.")
        if self.stock < quantity:
            raise DomainError(f"Товара на складе всего {self.stock} шт.")

@dataclass
class Order:
    id: int
    total_price: float
    items: list[CartItem] = field(default_factory=list)
    status: str = "В обработке"

@dataclass
class CartItem:
    product: Product
    quantity: int

@dataclass
class Cart:
    items: list[CartItem] = field(default_factory=list) 