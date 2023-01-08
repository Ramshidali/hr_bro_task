# standerd
import uuid
import datetime
# django
from django.db import models
from django.core.validators import MinValueValidator
#third party
from decimal import Decimal
from versatileimagefield.fields import VersatileImageField
#local
from main.models import BaseModel

# Create your models here.

class Brand(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'product_brand'
        verbose_name = ('Brand')
        verbose_name_plural = ('Brand')

    def __str__(self):
        return str(self.name)

class Product(BaseModel):
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    starp_color = models.CharField(max_length=200)
    highlights = models.CharField(max_length=200)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    stock = models.DecimalField(default=0, decimal_places=0, max_digits=15, validators=[MinValueValidator(Decimal('0'))])
    status = models.BooleanField(default=False)
    image = VersatileImageField('Image', upload_to="product/product_cover", blank=True, null=True)

    class Meta:
        db_table = 'product_product'
        verbose_name = ('Product')
        verbose_name_plural = ('Product')

    def __str__(self):
        return str(self.name)