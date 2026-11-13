from models import Product, Cart, Order, CartItem
import os


class ProductRepository:
    def __init__(self, filepath="storage/products.csv"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.filepath = filepath
        self.products = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.filepath):
            self.products = {
                1: Product(id=1, name="Клавиатура AJAZZ v3000", price=8000.0, stock=5),
                2: Product(id=2, name="Мышь RAZEN 6 pro ", price=1000.0, stock=10),
                3: Product(id=3, name="Коврик для мыши красный", price=299.99, stock=17)
            }
            self._save()
            return
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                p = Product(id=int(parts[0]), name=parts[1], price=float(parts[2]), stock=int(parts[3]))
                self.products[p.id] = p

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            for p in self.products.values():
                f.write(f"{p.id},{p.name},{p.price},{p.stock}\n")

    def get_all(self):
        return list(self.products.values())

    def get_by_id(self, prod_id):
        return self.products.get(prod_id)


class CartRepository:
    def __init__(self, filepath="storage/cart.csv", prod_repo=ProductRepository):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.filepath = filepath
        self.prod_repo = prod_repo()
        self.cart = Cart()
        self._load()

    def _load(self):
        if not os.path.exists(self.filepath):
            return
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                product = self.prod_repo.get_by_id(int(parts[0]))
                if product:
                    self.cart.items.append(CartItem(product=product, quantity=int(parts[1])))

    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            for item in self.cart.items:
                f.write(f"{item.product.id},{item.quantity}\n")

    def get(self):
        return self.cart


class OrderRepository:
    def __init__(
        self,
        orders_filepath="storage/orders.csv",
        order_items_filepath="storage/order_items.csv",
        meta_filepath="storage/meta.txt",
        prod_repo=ProductRepository,
    ):
        os.makedirs(os.path.dirname(orders_filepath), exist_ok=True)
        self.orders_filepath = orders_filepath
        self.order_items_filepath = order_items_filepath
        self.meta_filepath = meta_filepath
        self.prod_repo = prod_repo()
        self.orders = []
        self._load()

    def _get_next_id(self) -> int:
        if not os.path.exists(self.meta_filepath):
            return 1
        with open(self.meta_filepath, "r") as f:
            content = f.read().strip()
            if not content:
                return 1
            try:
                return int(content) + 1
            except ValueError:
                return 1

    def _update_meta(self, new_id):
        with open(self.meta_filepath, "w") as f:
            f.write(str(new_id))

    def _load(self):
        if not os.path.exists(self.orders_filepath):
            return
        with open(self.orders_filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                order_id = int(parts[0])
                total_price = float(parts[1])
                status = parts[2]
                self.orders.append(
                    Order(id=order_id, total_price=total_price, status=status))

        orders_dict = {order.id: order for order in self.orders}

        with open(self.order_items_filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                order_id = int(parts[0])
                product = self.prod_repo.get_by_id(int(parts[1]))
                product_quantity = int(parts[2])

                if product and order_id in orders_dict:
                    orders_dict[order_id].items.append(
                        CartItem(product=product, quantity=product_quantity))
    
    def save(self, order: Order):
        new_id = self._get_next_id()
        order.id = new_id
        self._update_meta(new_id=new_id)
        self.orders.append(order)

        with open(self.orders_filepath, 'a', encoding='utf-8') as f:
            f.write(f"{order.id},{order.total_price},{order.status}\n")

        with open(self.order_items_filepath, 'a', encoding='utf-8') as f:
            for item in order.items:
                f.write(f"{order.id},{item.product.id},{item.quantity}\n")

    def get_by_id(self, order_id: int):
        for order in self.orders:
            if order.id == order_id:
                return order
        return None
