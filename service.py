from models import Order, DomainError
from repository import Repository

class Service:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_products(self):
        return self.repo.get_all_prod()

    def get_product(self, product_id: int):
        product = self.repo.get_prod_by_id(product_id)
        if not product:
            raise DomainError("Товар не найден")
        return product

    def add_to_cart(self, product_id: int, quantity: int):
        product = self.get_product(product_id)
        product.validate_quantity(quantity)
        self.repo.cart.add_product(product_id, quantity)
        return self.repo.cart

    def get_cart(self):
        return self.repo.cart

    def remove_from_cart(self, product_id: int, quantity: int = None):
        self.repo.cart.remove_product(product_id, quantity)
        return self.repo.cart


    def checkout(self):
        if not self.repo.cart.products:
            raise DomainError("Корзина пуста.")
        
        total = 0.0
        for prod_id, qty in self.repo.cart.products.items():
            product = self.repo.get_prod_by_id(prod_id)
            total += product.price * qty
            
        order_id = len(self.repo.orders) + 1
        new_order = Order(id=order_id, items=self.repo.cart.products.copy(), total_price=total)
        
        self.repo.save_order(new_order)
        self.repo.cart.clear() 
        return new_order

    def get_order(self, order_id: int):
        order = self.repo.get_order_by_id(order_id)
        if not order:
            raise DomainError("Заказ с таким ID не найден.")

        return order