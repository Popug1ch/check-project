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
            raise DomainError("Товара на складе всего {stock} шт.")

@dataclass
class Order:
    id: int
    items: dict
    total_price: float
    status: str = "В обработке"

@dataclass
class CartItem:
    product: Product
    quantity: int

@dataclass
class Cart:
    items: dict[CartItem] = field(default_factory=list)