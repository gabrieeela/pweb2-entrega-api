cart = []


def get_cart_total() -> float:
    return sum(item["subtotal"] for item in cart)
