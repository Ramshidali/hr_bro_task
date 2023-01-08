from django import template
from customer.models import Customer, CartItem


register = template.Library()

@register.simple_tag
def get_have_cart(product, user):
    status = False
    qty = 0
    if CartItem.objects.filter(product__pk=product, customer__user=user).exists():
        status = True
        qty = CartItem.objects.get(product__pk=product, customer__user=user).qty
    return {
        'status' : status,
        'qty' : qty,
        }