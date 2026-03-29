
from django.contrib.auth.models import User
from django.db import models
from products.models import Product


class Cart (models.Model):
    id = models.AutoField(primary_key=True)
    count = models.IntegerField(default=1)
    length = models.CharField(max_length=50, blank=True, default="")
    color = models.CharField(max_length=50, blank=True, default="")
    strand_quantity = models.IntegerField(default=10)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Order(models.Model):
    STATUS_PROCESSING = "processing"
    STATUS_ASSEMBLING = "assembling"
    STATUS_IN_TRANSIT = "in_transit"
    STATUS_READY_FOR_PICKUP = "ready_for_pickup"

    STATUS_CHOICES = [
        (STATUS_PROCESSING, "Order is being processed"),
        (STATUS_ASSEMBLING, "Order is being assembled"),
        (STATUS_IN_TRANSIT, "Order is on the way"),
        (STATUS_READY_FOR_PICKUP, "Order is ready for pickup"),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    email = models.EmailField()
    nickname = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=50)
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_PROCESSING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"Order #{self.id} for {self.user.username}"


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)
    product_image = models.URLField(blank=True, default="")
    length = models.CharField(max_length=50, blank=True, default="")
    color = models.CharField(max_length=50, blank=True, default="")
    strand_quantity = models.IntegerField(default=10)
    set_quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x{self.set_quantity}"



