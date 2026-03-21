from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }


def get_token_from_request(request):
    auth_header = request.headers.get("Authorization", "")
    prefix = "Token "

    if not auth_header.startswith(prefix):
        return None

    return auth_header[len(prefix) :].strip() or None


def get_authenticated_user(request):
    token_key = get_token_from_request(request)
    if not token_key:
        return request.user if getattr(request.user, "is_authenticated", False) else None

    try:
        token = Token.objects.select_related("user").get(key=token_key)
    except Token.DoesNotExist:
        return request.user if getattr(request.user, "is_authenticated", False) else None

    return token.user if token.user.is_active else AnonymousUser()
