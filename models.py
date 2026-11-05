from dataclasses import dataclass, field


@dataclass
class Product:
    id: int
    name: str 
    price: float
    stock: int

@dataclass
class Order:
    id: int
    items: dict
    total_price: float
    status: str = "В обработке"

@dataclass
class Cart:
    products: dict = field(default_factory=dict)