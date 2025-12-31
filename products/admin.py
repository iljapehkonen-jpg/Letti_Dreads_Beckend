from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'count']
    search_fields = ['name',]
    list_filter = ['price', 'count']
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
