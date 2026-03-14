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
    photo = models.ImageField(upload_to='product/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    def get_img_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return None
    def get_absolute_url(self, request):
        if self.photo and hasattr(self.photo, 'url'):
            return request.build_absolute_uri(self.photo.url)
        return None
    def __str__(self):
        return self.name

