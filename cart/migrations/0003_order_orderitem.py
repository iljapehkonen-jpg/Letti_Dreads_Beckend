from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_homegalleryimage_homereviewimage"),
        ("cart", "0002_cart_color_cart_length_cart_strand_quantity"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.EmailField(max_length=254)),
                ("nickname", models.CharField(max_length=150)),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("postal_code", models.CharField(max_length=20)),
                ("phone", models.CharField(max_length=50)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("processing", "Order is being processed"),
                            ("assembling", "Order is being assembled"),
                            ("in_transit", "Order is on the way"),
                            ("ready_for_pickup", "Order is ready for pickup"),
                        ],
                        default="processing",
                        max_length=32,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="orders",
                        to="auth.user",
                    ),
                ),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("product_name", models.CharField(max_length=200)),
                ("product_image", models.URLField(blank=True, default="")),
                ("length", models.CharField(blank=True, default="", max_length=50)),
                ("color", models.CharField(blank=True, default="", max_length=50)),
                ("strand_quantity", models.IntegerField(default=10)),
                ("set_quantity", models.IntegerField(default=1)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="cart.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
