from django import template
from customer.models import Customer, CartItem
from product.models import Product


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


@register.simple_tag
def get_have_stock(product):
    status = False
    if Product.objects.filter(pk=product).exists():
        if not Product.objects.get(pk=product).stock==0 :
            status = True
    return status