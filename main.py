from repository import Repository
from service import Service
from models import DomainError

class CLI:
    def __init__(self, service: Service):
        self.service = service

    def print_products(self):
        for p in self.service.get_products():
            print(f"[{p.id}] {p.name} - {p.price} руб. Осталось: {p.stock} шт.")

    def print_product(self, p_id: int):
        product = self.service.get_product(p_id)
        print(f"\nНазвание: {product.name}\nЦена: {product.price} руб.\nОстаток: {product.stock} шт.")

    def print_cart(self):
        cart = self.service.get_cart()
        if not cart.products:
            print("Корзина пуста.")
            return
        
        print("\nКОРЗИНА")
        total = 0.0
        for prod_id, qty in cart.products.items():
            product = self.service.get_product(prod_id)
            item_total = product.price * qty
            total += item_total
            print(f"[{product.id}] {product.name} | {qty} шт. x {product.price} = {item_total:.2f} руб.")
        print(f"ИТОГО: {total:.2f} руб.")

    def print_order(self, o_id: int):
        order = self.service.get_order(o_id)
        print(f"\nЗАКАЗ {order.id}\nСтатус: {order.status}\nСостав:")
        for prod_id, qty in order.items.items():
            product = self.service.get_product(prod_id)
            print(f"- {product.name} ({qty} шт.)")
        print(f"ИТОГО: {order.total_price:.2f} руб.")

    def handle_loop(self):
        while True:
            print("\nМЕНЮ ")
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
                    case "1":
                        self.print_products()
                    case "2":
                        p_id = int(input("Введите ID товара: "))
                        self.print_product(p_id)
                    case "3":
                        p_id = int(input("Введите ID товара: "))
                        qty = int(input("Введите количество: "))
                        self.service.add_to_cart(p_id, qty)
                        print("Товар добавлен в корзину.")
                    case "4":
                        self.print_cart()
                    case "5":
                        p_id = int(input("Введите ID товара: "))
                        print("1 - Удалить весь товар\n2 - Удалить определенное количество")
                        sub_choice = input("Ваш выбор: ")
                        if sub_choice == "1":
                            self.service.remove_from_cart(p_id)
                            print("Товар полностью удален.")
                        elif sub_choice == "2":
                            qty = int(input("Сколько штук удалить? "))
                            self.service.remove_from_cart(p_id, qty)
                            print("Товар частично удален.")
                        else:
                            print("Неверный выбор.")
                    case "6":
                        order = self.service.checkout()
                        print(f"Заказ #{order.id} оформлен. Итоговая сумма: {order.total_price:.2f} руб.")
                    case "7":
                        o_id = int(input("Введите номер заказа: "))
                        self.print_order(o_id)
                    case "8":
                        break
                    case _:
                        print("Неверный ввод, попробуйте еще раз.")
            except ValueError:
                print("Ошибка: нужно вводить числа.")
            except DomainError as e:
                print(f"Ошибка: {e}")


def main():
    repo = Repository()
    service = Service(repo)
    cli = CLI(service)
    cli.handle_loop()

if __name__ == "__main__":
    main()