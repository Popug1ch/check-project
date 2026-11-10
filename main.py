from repository import ProductRepository, CartRepository, OrderRepository
from service import ProductService, CartService, OrderService
from cli import CLI

def main():
    prod_repo = ProductRepository()
    cart_repo = CartRepository()
    order_repo = OrderRepository()

    prod_service = ProductService(prod_repo)
    cart_service = CartService(cart_repo, prod_service)
    order_service = OrderService(order_repo, cart_service)

    cli = CLI(prod_service, cart_service, order_service)
    cli.handle_loop()

if __name__ == "__main__":
    main()