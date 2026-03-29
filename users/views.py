from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
import json

from .auth_utils import get_authenticated_user, serialize_user

@require_http_methods(["POST"]) 
def register(request):
    try:
        data= json.loads(request.body)
    except: 
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    password_confirm = data.get('password_confirm')

    if not all([username, password, email, password_confirm]):
        return JsonResponse({'error': 'All fields are required'}, status=400)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already registered'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already taken'}, status=400)
    
    if password != password_confirm:
        return JsonResponse({'error': 'Passwords do not match'}, status=400)
    
    if len(password) < 6:
        return JsonResponse({'error': 'Password must be at least 6 characters long'}, status=400)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    login(request, user)
    return JsonResponse(
        {
            'message': 'User registered successfully',
            'token': token.key,
            'user': serialize_user(user),
        }
    )
    
@require_http_methods(["POST"])
def user_login(request):
    try:
        data= json.loads(request.body)
    except: 
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return JsonResponse({'error': 'Username and password are required'}, status=400)
    
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
    login(request, user)
    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse(
        {
            'message': 'Login successful',
            'token': token.key,
            'user': serialize_user(user),
        }
    )

@require_http_methods(["POST"])
def user_logout(request):
    user = get_authenticated_user(request)

    if not user or not user.is_authenticated:
        return JsonResponse({'error': 'User not logged in'}, status=400)

    Token.objects.filter(user=user).delete()
    logout(request)
    return JsonResponse({'message': 'Logout successful'})

@require_http_methods(["GET"])
def user_detail(request):
    user = get_authenticated_user(request)

    if not user or not user.is_authenticated:
        return JsonResponse({'error': 'User not logged in'}, status=400)

    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse({'user': serialize_user(user), 'token': token.key})
