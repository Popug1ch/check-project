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
class Cart:
    products: dict = field(default_factory=dict)

    def add_product(self, product_id:int, quantity: int):
        curr_q = self.products.get(product_id, 0)
        self.products[product_id] = curr_q + quantity

    def remove_product(self, product_id: int, quantity: None):
        if product_id not in self.products:
            raise DomainError("Этого товара нет в корзине")
        if quantity is None or quantity >= self.products[product_id]:
            del self.products[product_id]
        else:
            self.products[product_id] -= quantity

    def clear(self):
        self.products.clear()