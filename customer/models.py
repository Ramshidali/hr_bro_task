import uuid
#django
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator

from decimal import Decimal

from main.models import BaseModel
from product.models import Product



phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$', message="Not an valid number")

# Create your models here.
class Customer(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=10,null=True,blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    class Meta:
        db_table = 'customers_customer'
        verbose_name = ('Customer')
        verbose_name_plural = ('Customer')

    def __str__(self):
        return str(self.name)


class CustomerAddress(BaseModel):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10,null=True,blank=True, validators=[phone_regex],)
    pincode = models.IntegerField()
    locality = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)

    class Meta:
        db_table = 'customers_customer_address'
        verbose_name = ('Customer Address')
        verbose_name_plural = ('Customer Address')

    def __str__(self):
        return str(self.name)

class WhishlistItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        db_table = 'customers_whishlist'
        verbose_name = ('Whishlist')
        verbose_name_plural = ('Whishlist')

    def __str__(self):
        return f'{self.customer.name} - {self.product.name}'


class CartItem(BaseModel):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    unit_price = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'customers_cart_item'
        verbose_name = ('Cart Item')
        verbose_name_plural = ('Cart Item')

    def __str__(self):
        return f'{self.customer.name} - {self.product_varient.product.name}'