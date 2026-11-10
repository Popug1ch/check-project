from models import Product, Cart


class ProductRepository:
    def __init__(self):
        self.products = {
                    1: Product(id=1, name="Клавиатура AJAZZ v3000", price=8000.0, stock=5),
                    2: Product(id=2, name="Мышь RAZEN 6 pro ", price=1000.0, stock=10),
                    3: Product(id=3, name="Коврик для мыши красный", price=299.99, stock=17)
                }
    def get_all(self):
            return list(self.products.values())
    
    def get_by_id(self, prod_id):
            return self.products.get(prod_id)

class CartRepository:
    def __init__(self):
        self.cart = Cart()

    def get(self):
     return self.cart

class OrderRepository:
    def __init__(self):
         self.orders = []

    def save(self, order):
        self.orders.append(order)

    def get_by_id(self, order_id):
        for order in self.orders:
             if order.id == order_id:
                  return order
        return None