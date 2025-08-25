
from .cart import Cart

def cart_item_count(request):
    try:
        return {'cart_item_count': len(Cart(request))}
    except Exception:
        return {'cart_item_count': 0}
