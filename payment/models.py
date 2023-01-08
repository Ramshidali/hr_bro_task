#django
from django.db import models
from django.core.validators import MinValueValidator
#third party
from decimal import Decimal
#local
from main.models import BaseModel


# Create your models here.
class Payment(BaseModel):
    order_id = models.CharField(max_length=200)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    currency = models.CharField(max_length=200,null=True,blank=True)
    language = models.CharField(max_length=200,null=True,blank=True)
    payment_type = models.CharField(max_length=200,null=True,blank=True)
    payment_mode = models.CharField(max_length=200,null=True,blank=True)
    card_name = models.CharField(max_length=200,null=True,blank=True)
    order_status = models.CharField(max_length=200,null=True,blank=True)
    transaction_id = models.CharField(max_length=200,null=True,blank=True)
    transaction_signature = models.CharField(max_length=200,null=True,blank=True)
    bank_ref_no = models.CharField(max_length=200,null=True,blank=True)
    bank_id = models.CharField(max_length=200,null=True,blank=True)
    payuid = models.CharField(max_length=200,null=True,blank=True)
    mihpayuid = models.CharField(max_length=200,null=True,blank=True)
    payment_order_id = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(max_length=200,null=True,blank=True)
    payment_channel = models.CharField(max_length=200,null=True,blank=True)
    payment_datetime = models.CharField(max_length=200,null=True,blank=True)
    response_code = models.CharField(max_length=200,null=True,blank=True)
    response_message = models.CharField(max_length=200,null=True,blank=True)
    error_desc = models.CharField(max_length=200,null=True,blank=True)
    cardmasked = models.CharField(max_length=200,null=True,blank=True)
    failure_message = models.TextField(max_length=200,null=True,blank=True)
    status_message = models.TextField(max_length=200,null=True,blank=True)

    class Meta:
        db_table = 'payment'
        verbose_name = ('Payment')
        verbose_name_plural = ('Payment')

    def __str__(self):
        return str(self.order_id)