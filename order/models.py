#django
from django.db import models
from django.core.validators import MinValueValidator
#local
from customer.models import Customer, CustomerAddress
from main.models import BaseModel
from payment.models import Payment
from product.models import Product
#thirdparty
from decimal import Decimal


# Create your models here.

ORDER_STATUS_CHOICE = (
    ('pending', 'Pending'),
    ('return', 'Return'),
    ('ordered', 'Ordered'),
    ('shipped', 'Shipped'),
    ('out_of_delivered', 'Out of Delivered'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

PAYMENT_STATUS_CHOICE = (
    ('pending','Pending'),
    ('received','Received'),
    ('failed','Failed'),
)


class Order(BaseModel):
    order_id = models.CharField(max_length=50)
    time = models.DateTimeField()
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,blank=True,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    billing_address = models.ForeignKey(CustomerAddress,on_delete=models.CASCADE)
    total_amount = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    payment_status = models.CharField(max_length=100,choices=PAYMENT_STATUS_CHOICE,default='failed')


    class Meta:
        db_table = 'orders_order'
        verbose_name = ('Order')
        verbose_name_plural = ('Order')

    def __str__(self):
        return str(self.order_id)

class OrderItem(BaseModel):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    subtotal = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    order_status = models.CharField(default="pending", max_length=100,choices=ORDER_STATUS_CHOICE)
    cancel_reason = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'orders_order_item'
        verbose_name = ('Order Item')
        verbose_name_plural = ('Order Item')

    def __str__(self):
        return str(self.order)