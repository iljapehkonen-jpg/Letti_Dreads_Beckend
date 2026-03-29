from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to="product/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def get_img_url(self):
        if self.photo and hasattr(self.photo, "url"):
            return self.photo.url
        return None

    def get_absolute_url(self, request):
        if self.photo and hasattr(self.photo, "url"):
            return request.build_absolute_uri(self.photo.url)
        return None

    def get_gallery_urls(self, request):
        gallery = []

        if self.photo and hasattr(self.photo, "url"):
            gallery.append(request.build_absolute_uri(self.photo.url))

        for image in self.images.all():
            if image.image and hasattr(image.image, "url"):
                gallery.append(request.build_absolute_uri(image.image.url))

        return gallery

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="product/gallery/")
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.name} image #{self.id}"


class HomeGalleryImage(models.Model):
    image = models.ImageField(upload_to="home/gallery/")
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Home gallery image"
        verbose_name_plural = "Home gallery images"

    def __str__(self):
        return f"Gallery image #{self.id}"


class HomeReviewImage(models.Model):
    image = models.ImageField(upload_to="home/reviews/")
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Home review image"
        verbose_name_plural = "Home review images"

    def __str__(self):
        return f"Review image #{self.id}"

