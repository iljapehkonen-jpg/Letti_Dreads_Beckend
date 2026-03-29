from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_productimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomeGalleryImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="home/gallery/")),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Home gallery image",
                "verbose_name_plural": "Home gallery images",
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="HomeReviewImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="home/reviews/")),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Home review image",
                "verbose_name_plural": "Home review images",
                "ordering": ["sort_order", "id"],
            },
        ),
    ]
