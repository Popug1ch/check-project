from service import ProductService, CartService, OrderService
from models import DomainError

class CLI:
    def __init__(self, product_service: ProductService, cart_service: CartService, order_service: OrderService):
        self.product_service = product_service
        self.cart_service = cart_service
        self.order_service = order_service

    def display_products(self):
        for p in self.product_service.get_products():
            print(f"[{p.id}] {p.name} - {p.price} руб. Осталось: {p.stock} шт.")

    def display_product(self, p_id: int):
        product = self.product_service.get_product(p_id)
        print(f"\nНазвание: {product.name}\nЦена: {product.price} руб.\nОстаток: {product.stock} шт.")

    def display_cart(self):
        cart = self.cart_service.get_cart()
        if not cart.items:
            print("Корзина пуста.")
            return
        
        total = self.cart_service.get_cart_total()
        print("\nКОРЗИНА")
        for item in cart.items:
            print(f"[{item.product.id}] {item.product.name} | {item.quantity} шт. x {item.product.price} = {item.product.price * item.quantity:.2f} руб.")
        print(f"ИТОГО: {total:.2f} руб.")

    def display_order(self, o_id: int):
        order = self.order_service.get_order(o_id)
        print(f"\nЗАКАЗ {order.id}\nСтатус: {order.status}\nСостав:")
        for item in order.items:
            print(f"- {item.product.name} ({item.quantity} шт.)")
        print(f"ИТОГО: {order.total_price:.2f} руб.")

    def handle_list_products(self):
        self.display_products()

    def handle_view_product(self):
        p_id = int(input("Введите ID товара: "))
        self.display_product(p_id)

    def handle_add_to_cart(self):
        p_id = int(input("Введите ID товара: "))
        qty = int(input("Введите количество: "))
        self.cart_service.add_to_cart(p_id, qty)
        print("Товар добавлен в корзину.")

    def handle_view_cart(self):
        self.display_cart()

    def handle_remove_from_cart(self):
        p_id = int(input("Введите ID товара: "))
        print("1 - Удалить весь товар\n2 - Удалить определенное количество")
        sub_choice = input("Ваш выбор: ")
        if sub_choice == "1":
            self.cart_service.remove_from_cart(p_id)
            print("Товар полностью удален.")
        elif sub_choice == "2":
            qty = int(input("Сколько штук удалить? "))
            self.cart_service.remove_from_cart(p_id, qty)
            print("Товар частично удален.")
        else:
            print("Неверный выбор.")

    def handle_checkout(self):
        order = self.order_service.checkout()
        print(f"Заказ #{order.id} оформлен. Итоговая сумма: {order.total_price:.2f} руб.")

    def handle_view_order(self):
        o_id = int(input("Введите номер заказа: "))
        self.display_order(o_id)

    def handle_loop(self):
        while True:
            print("\nМЕНЮ")
            print("1 - Показать все товары")
            print("2 - Показать товар по ID")
            print("3 - Добавить в корзину")
            print("4 - Посмотреть корзину")
            print("5 - Удалить из корзины")
            print("6 - Оформить заказ")
            print("7 - Посмотреть заказ")
            print("8 - Выход")
            
            choice = input("Выберите действие: ")

            try:
                match choice:
                    case "1": self.handle_list_products()
                    case "2": self.handle_view_product()
                    case "3": self.handle_add_to_cart()
                    case "4": self.handle_view_cart()
                    case "5": self.handle_remove_from_cart()
                    case "6": self.handle_checkout()
                    case "7": self.handle_view_order()
                    case "8": 
                        break
                    case _: print("Неверный ввод, попробуйте еще раз.")
            except ValueError:
                print("Ошибка: нужно вводить числа.")
            except DomainError as e:
                print(f"Ошибка: {e}")