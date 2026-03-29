from django.urls import path
from .import views

urlpatterns = [
    path('me/', views.user_cart, name='user_cart_me'),
    path('orders/', views.user_orders, name='user_orders'),
    path('orders/latest/', views.latest_order, name='latest_order'),
    path('orders/create/', views.create_order, name='create_order'),
    path('me/items/', views.add_cart_item, name='add_cart_item'),
    path('me/items/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('me/items/<int:item_id>/delete/', views.remove_cart_item, name='remove_cart_item'),
    path('<int:user_id>/', views.legacy_user_cart, name='user_cart'),
    path('add/<int:product_id>/<int:user_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/<int:user_id>/', views.remove_from_cart, name='remove_from_cart'),
]
