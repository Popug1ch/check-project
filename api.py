from fastapi import APIRouter, Request
from pydantic import BaseModel
from dataclasses import asdict

from repository import ProductRepository, CartRepository, OrderRepository
from service import ProductService, CartService, OrderService

prod_repo = ProductRepository()
cart_repo = CartRepository()
order_repo = OrderRepository()

product_service = ProductService(prod_repo)
cart_service = CartService(cart_repo, product_service)
order_service = OrderService(order_repo, cart_service)

router = APIRouter()


class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int

class RemoveFromCartRequest(BaseModel):
    product_id: int
    quantity: int | None = None


@router.get("/products")
def get_products():
        result: list = product_service.get_products()
        return [asdict(p) for p in result]

@router.get("/product/{p_id}")
def get_product(p_id: int):
     result = product_service.get_product(product_id=p_id)
     return asdict(result)

@router.get("/cart")
def get_cart():
     cart = cart_service.get_cart()
     return {
        "items": [
            {"product": asdict(item.product), "quantity": item.quantity}
            for item in cart.items
        ],
        "total": cart_service.get_cart_total()
    }

@router.post("/cart/add")
def add_2_cart(req: AddToCartRequest):
    cart_service.add_to_cart(req.product_id, req.quantity)
    return {"status": "OK", "message": "Товар добавлен"}

@router.post("/cart/remove")
def remove_from_cart(req: RemoveFromCartRequest):
    cart_service.remove_from_cart(req.product_id, req.quantity)
    return {"status": "OK", "message": "Товар удалён"}


@router.post("/orders/checkout")
def checkout():
    order = order_service.checkout()
    return {"status": "OK", "order_id": order.id, "total": order.total_price}


@router.get("/orders/{order_id}")
def get_order(order_id: int):
    order = order_service.get_order(order_id)
    return {
        "id": order.id,
        "status": order.status,
        "total": order.total_price,
        "items": [
            {"product": asdict(item.product), "quantity": item.quantity}
            for item in order.items
        ],
    }