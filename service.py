from models import Order, DomainError, CartItem
from repository import ProductRepository, OrderRepository, CartRepository


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def get_products(self):
            return self.repo.get_all()
    
    def get_product(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise DomainError("Товар не найден")
        return product

class CartService:
    def __init__(self, cart_repo: CartRepository, product_service: ProductService):
        self.cart_repo = cart_repo
        self.product_service = product_service

    def get_cart(self):
        return self.cart_repo.get()

    def get_cart_total(self):
        total = 0.0
        for item in self.cart_repo.get().items:
            total += item.product.price * item.quantity
        return total

    def add_to_cart(self, product_id: int, quantity: int):
        product = self.product_service.get_product(product_id)
        product.validate_quantity(quantity)
        
        cart = self.cart_repo.get()
        for item in cart.items:
            if item.product.id == product_id:
                item.quantity += quantity
                return cart
        
        cart.items.append(CartItem(product=product, quantity=quantity))
        return cart

    def remove_from_cart(self, product_id: int, quantity: int = None):
        cart = self.cart_repo.get()
        for index, item in enumerate(cart.items):
            if item.product.id == product_id:
                if quantity is None or quantity >= item.quantity:
                    del cart.items[index]
                else:
                    item.quantity -= quantity
                return cart
        raise DomainError("Этого товара нет в корзине.")

    def clear_cart(self):
        self.cart_repo.get().items.clear()

class OrderService:
    def __init__(self, order_repo: OrderRepository, cart_service: CartService):
        self.order_repo = order_repo
        self.cart_service = cart_service

    def checkout(self):
        cart = self.cart_service.get_cart()
        if not cart.items:
            raise DomainError("Корзина пуста.")
        
        total = self.cart_service.get_cart_total()
        order_id = len(self.order_repo.orders) + 1
        
        new_order = Order(id=order_id, items=cart.items.copy(), total_price=total)
        
        self.order_repo.save(new_order)
        self.cart_service.clear_cart()
        return new_order

    def get_order(self, order_id: int):
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise DomainError("Заказ с таким ID не найден.")
        return order
