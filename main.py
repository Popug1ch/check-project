from repository import Repository
from service import Service

def main():
    repo = Repository()
    service = Service(repo)

    while True:
        print("\nМЕНЮ\n")
        print("1 - Показать все товары")
        print("2 - Показать товар по ID")
        print("3 - Добавить в корзину")
        print("4 - Посмотреть корзину")
        print("5 - Удалить из корзины")
        print("6 - Оформить заказ")
        print("7 - Посмотреть заказ")
        print("8 - Выход")
        
        choice = input("Выберите действие: ")

        match choice:
            case "1":
                for p in service.get_products():
                    print(f"[{p.id}] {p.name} - {p.price} руб. Осталось: {p.stock} шт.")
            
            case "2":
                try:
                    p_id = int(input("Введите ID товара: "))
                    product = service.get_product(p_id)
                    if product:
                        print(f"\nНазвание: {product.name}\nЦена: {product.price} руб.\nОстаток: {product.stock} шт.")
                    else:
                        print("Товар не найден.")
                except ValueError:
                    print("Ошибка: нужно вводить числа.")
            
            case "3":
                try:
                    p_id = int(input("Введите ID товара: "))
                    qty = int(input("Введите количество: "))
                    print(service.add_to_cart(p_id, qty))
                except ValueError:
                    print("Ошибка: нужно вводить числа.")
            
            case "4":
                print(service.view_cart())
            
            case "5":
                try:
                    p_id = int(input("Введите ID товара: "))
                    print("1 - Удалить весь товар из корзины")
                    print("2 - Удалить определенное количество")
                    sub_choice = input("Ваш выбор: ")
                    
                    if sub_choice == "1":
                        print(service.remove_from_cart(p_id))
                    elif sub_choice == "2":
                        qty = int(input("Сколько штук удалить? "))
                        print(service.remove_from_cart(p_id, qty))
                    else:
                        print("Неверный выбор.")
                except ValueError:
                    print("Ошибка: нужно вводить числа.")
            
            case "6":
                print(service.checkout())
            
            case "7":
                try:
                    o_id = int(input("Введите номер заказа: "))
                    print(service.get_order_status(o_id))
                except ValueError:
                    print("Ошибка: нужно вводить числа.")
            
            case "8":
                break
            
            case _:
                print("Неверный ввод, попробуйте еще раз.")

if __name__ == "__main__":
    main()