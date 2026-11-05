from models import Order
from repository import Repository

class Service:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_products(self):
        return self.repo.get_all_prod()

    def get_product(self, product_id: int):
        return self.repo.get_prod_by_id(product_id)

    def add_to_cart(self, product_id: int, quantity: int):
        product = self.repo.get_prod_by_id(product_id)
        
        if not product:
            return "Товар не найден"
        
        if quantity <= 0:
            return "Количество должно быть больше нуля"
        
        if product.stock < quantity:
            return f'Товара на складе всего {product.stock} шт.'

        curr_q = self.repo.cart.products.get(product_id, 0)
        self.repo.cart.products[product_id] = curr_q + quantity
        return f"Товар '{product.name}' добавлен в корзину."

    def view_cart(self):
        if not self.repo.cart.products:
            return "Корзина пуста."
        
        result = "\nКОРЗИНА"
        total = 0.0
        for prod_id, qty in self.repo.cart.products.items():
            product = self.repo.get_prod_by_id(prod_id)
            item_total = product.price * qty
            total += item_total
            result += f"\n[{product.id}] {product.name} | {qty} шт. x {product.price} = {item_total:.2f} руб."
        
        result += f"\nИТОГО: {total:.2f} руб."
        return result

    def remove_from_cart(self, product_id: int, quantity: int = None):
        if product_id not in self.repo.cart.products:
            return "Этого товара нет в корзине."
        
        if quantity is None or quantity >= self.repo.cart.products[product_id]:
            del self.repo.cart.products[product_id]
            return "Товар полностью удален из корзины."
        else:
            self.repo.cart.products[product_id] -= quantity
            return f"Удалено {quantity} шт. товара из корзины."

    def checkout(self):
        if not self.repo.cart.products:
            return "Корзина пуста."
        
        total = 0.0
        for prod_id, qty in self.repo.cart.products.items():
            product = self.repo.get_prod_by_id(prod_id)
            total += product.price * qty
            
        order_id = len(self.repo.orders) + 1
        new_order = Order(id=order_id, items=self.repo.cart.products.copy(), total_price=total)
        
        self.repo.save_order(new_order)
        self.repo.cart.products.clear() 
        
        return f"Заказ {order_id} оформлен. Итоговая сумма: {total:.2f} руб."

    def get_order_status(self, order_id: int):
        order = self.repo.get_order_by_id(order_id)
        if not order:
            return "Заказ с таким ID не найден."
        
        result = f"\nЗАКАЗ {order.id}\nСтатус: {order.status}\nСостав:"
        for prod_id, qty in order.items.items():
            product = self.repo.get_prod_by_id(prod_id)
            result += f"\n- {product.name} ({qty} шт.)"
        result += f"\nИТОГО: {order.total_price:.2f} руб."
        return result