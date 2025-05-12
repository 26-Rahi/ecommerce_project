# cart_utils.py
from .models import CartItem  # Make sure this is correct

def get_cart(user):
    cart_items = CartItem.objects.filter(user=user)
    return cart_items

def calculate_cart_total(user):
    cart_items = get_cart(user)
    return sum(item.product.price * item.quantity for item in cart_items)
