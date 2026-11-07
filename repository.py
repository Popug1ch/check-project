from models import Product, Cart

class Repository:
    def __init__(self):
        self.products = {
            1: Product(id=1, name="Клавиатура AJAZZ v3000", price=8000.0, stock=5),
            2: Product(id=2, name="Мышь RAZEN 6 pro ", price=1000.0, stock=10),
            3: Product(id=3, name="Коврик для мыши красный", price=299.99, stock=17)
        }
        self.cart = Cart()
        self.orders = []

    def get_all_prod(self):
        return list(self.products.values())

    def get_prod_by_id(self, prod_id):
        return self.products.get(prod_id)

    def save_order(self, order):
        self.orders.append(order)

    def get_order_by_id(self, order_id):
        for order in self.orders:
            if order.id == order_id:
                return order
        return None