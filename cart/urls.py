from django.urls import path
from .import views

urlpatterns = [
    path('me/', views.user_cart, name='user_cart_me'),
    path('<int:user_id>/', views.legacy_user_cart, name='user_cart'),
    path('add/<int:product_id>/<int:user_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/<int:user_id>/', views.remove_from_cart, name='remove_from_cart'),
]
