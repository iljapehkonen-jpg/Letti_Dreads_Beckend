from django.contrib import admin
from .models import Cart, Order, OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']
    search_fields = ['id', 'user', 'product']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = [
        "product",
        "product_name",
        "product_image",
        "length",
        "color",
        "strand_quantity",
        "set_quantity",
        "unit_price",
    ]
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "nickname", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["id", "user__username", "nickname", "email", "phone"]
    inlines = [OrderItemInline]

