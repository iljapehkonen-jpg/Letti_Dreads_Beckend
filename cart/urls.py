from django.urls import path
from .import views

urlpatterns = [
    path('<int:user_id>', views.user_cart, name='user_cart'),
    path('add/<int:product_id>/<int:user_id>', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/<int:user_id>', views.remove_from_cart, name='remove_from_cart'),
]
