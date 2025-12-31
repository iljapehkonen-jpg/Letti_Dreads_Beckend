
from django.contrib.auth.models import User
from django.db import models
from products.models import Product


class Cart (models.Model):
    id = models.AutoField(primary_key=True)
    count = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)



