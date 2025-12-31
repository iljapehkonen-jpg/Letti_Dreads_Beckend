from django.urls import path
from .import views

urlpatterns = [
    path('<int:user_id>', views.user_cart, name='user_cart'),
]
