from django.urls import path
from .views import register, user_login, user_logout, user_detail
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('me/', user_detail, name='detail'),
]  