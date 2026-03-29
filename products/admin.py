from django.contrib import admin
from .models import (
    Category,
    HomeGalleryImage,
    HomeReviewImage,
    Product,
    ProductImage,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image", "sort_order"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "count", "category", "in_stock"]
    search_fields = ["name"]
    list_filter = ["price", "count", "category", "in_stock"]
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(HomeGalleryImage)
class HomeGalleryImageAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]
    ordering = ["sort_order", "id"]
    fields = ["image"]


@admin.register(HomeReviewImage)
class HomeReviewImageAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]
    ordering = ["sort_order", "id"]
    fields = ["image"]
