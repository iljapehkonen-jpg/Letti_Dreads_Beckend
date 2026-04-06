import json
import logging

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from cart.models import Cart, Order, OrderItem
from products.models import Product
from users.auth_utils import get_authenticated_user

logger = logging.getLogger(__name__)


def _safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _serialize_cart_item(request, item):
    return {
        "id": item.id,
        "count": item.count,
        "length": item.length,
        "color": item.color,
        "strand_quantity": item.strand_quantity,
        "product": {
            "id": item.product.id,
            "name": item.product.name,
            "description": item.product.description,
            "price": float(item.product.price),
            "in_stock": item.product.in_stock,
            "count": item.product.count,
            "photo": item.product.get_absolute_url(request),
            "images": item.product.get_gallery_urls(request),
            "category": item.product.category.name,
        },
        "user": item.user.id,
    }


def _serialize_order_item(item):
    unit_price = _safe_float(item.unit_price)
    strand_quantity = _safe_int(item.strand_quantity, 0)
    set_quantity = _safe_int(item.set_quantity, 0)

    return {
        "id": item.id,
        "product_id": item.product_id,
        "product_name": item.product_name or "",
        "product_image": item.product_image or "",
        "length": item.length or "",
        "color": item.color or "",
        "strand_quantity": strand_quantity,
        "set_quantity": set_quantity,
        "unit_price": unit_price,
        "total_price": unit_price * strand_quantity * set_quantity,
    }


def _serialize_order(order):
    if not order:
        return None

    return {
        "id": order.id,
        "email": order.email or "",
        "nickname": order.nickname or "",
        "address": order.address or "",
        "city": order.city or "",
        "postal_code": order.postal_code or "",
        "phone": order.phone or "",
        "status": order.status or "",
        "status_label": order.get_status_display() if order.status else "",
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "items": [_serialize_order_item(item) for item in order.items.all()],
    }


def _get_request_user(request):
    user = get_authenticated_user(request)
    if not user or not user.is_authenticated:
        return None
    return user


def _get_user_cart_queryset(user):
    return (
        Cart.objects.select_related("product", "product__category", "user")
        .prefetch_related("product__images")
        .filter(user=user)
        .order_by("-id")
    )


def _get_user_orders_queryset(user):
    return Order.objects.prefetch_related("items").filter(user=user).order_by("-created_at", "-id")


@require_http_methods(["GET"])
def user_cart(request):
    user = _get_request_user(request)
    if not user:
        return JsonResponse({"error": "User not logged in"}, status=401)

    cart_items = _get_user_cart_queryset(user)
    return JsonResponse({"cart": [_serialize_cart_item(request, item) for item in cart_items]})


@require_http_methods(["GET"])
def user_orders(request):
    user = _get_request_user(request)
    if not user:
        return JsonResponse({"error": "User not logged in"}, status=401)

    orders = _get_user_orders_queryset(user)
    serialized_orders = []
    for order in orders:
        try:
            serialized_orders.append(_serialize_order(order))
        except Exception:
            logger.exception("Failed to serialize order %s for user %s", order.id, user.id)
    return JsonResponse({"orders": serialized_orders})


@require_http_methods(["GET"])
def latest_order(request):
    user = _get_request_user(request)
    if not user:
        return JsonResponse({"error": "User not logged in"}, status=401)

    orders = _get_user_orders_queryset(user)
    for order in orders:
        try:
            return JsonResponse({"order": _serialize_order(order)})
        except Exception:
            logger.exception("Failed to serialize latest order %s for user %s", order.id, user.id)

    return JsonResponse({"order": None})


@require_http_methods(["POST"])
def add_cart_item(request):
    user = _get_request_user(request)
    if not user:
        return JsonResponse({"error": "User not logged in"}, status=401)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    product_id = data.get("product_id")
    if not product_id:
        return JsonResponse({"error": "product_id is required"}, status=400)

    product = get_object_or_404(Product.objects.select_related("category"), id=product_id)
    length = str(data.get("length") or "")
    color = str(data.get("color") or "")
    strand_quantity = max(10, min(65, _safe_int(data.get("strand_quantity"), 10)))
    count = max(1, _safe_int(data.get("count"), 1))

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product,
        length=length,
        color=color,
        strand_quantity=strand_quantity,
        defaults={"count": count},
    )

    if not created:
        cart_item.count += count
        cart_item.save(update_fields=["count"])

    cart_item = _get_user_cart_queryset(user).get(id=cart_item.id)
    return JsonResponse(
        {
            "message": "Product added to cart",
            "cart_item": _serialize_cart_item(request, cart_item),
        },
        status=201 if created else 200,
    )


@require_http_methods(["POST"])
def create_order(request):
    user = _get_request_user(request)
    if not user:
        return JsonResponse({"error": "User not logged in"}, status=401)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    cart_items = list(_get_user_cart_queryset(user))
    if not cart_items:
        return JsonResponse({"error": "Cart is empty"}, status=400)

    email = str(data.get("email") or "").strip()
    nickname = str(data.get("nickname") or "").strip()
    address = str(data.get("address") or "").strip()
    city = str(data.get("city") or "").strip()
    postal_code = str(data.get("postal_code") or "").strip()
    phone = str(data.get("phone") or "").strip()

    if not all([email, nickname, address, city, postal_code, phone]):
        return JsonResponse({"error": "All fields are required"}, status=400)

    if nickname != user.username:
        return JsonResponse({"error": "Nickname does not match account username"}, status=400)

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            email=email,
            nickname=nickname,
            address=address,
            city=city,
            postal_code=postal_code,
            phone=phone,
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_image=cart_item.product.get_absolute_url(request) or "",
                length=cart_item.length,
                color=cart_item.color,
                strand_quantity=cart_item.strand_quantity,
                set_quantity=cart_item.count,
                unit_price=cart_item.product.price,
            )

        Cart.objects.filter(id__in=[item.id for item in cart_items]).delete()

    order = _get_user_orders_queryset(user).get(id=order.id)
    return JsonResponse({"message": "Order created", "order": _serialize_order(order)}, status=201)


@require_http_methods(["PATCH"])
def update_cart_item(request, item_id):
    user = _get_request_user(request)
    if not user:
        return JsonResponse({"error": "User not logged in"}, status=401)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    cart_item = get_object_or_404(_get_user_cart_queryset(user), id=item_id)
    count = max(1, _safe_int(data.get("count"), cart_item.count))
    length = str(data.get("length") or cart_item.length or "")
    color = str(data.get("color") or cart_item.color or "")
    strand_quantity = max(
        10,
        min(65, _safe_int(data.get("strand_quantity"), cart_item.strand_quantity)),
    )

    duplicate_item = (
        Cart.objects.filter(
            user=user,
            product=cart_item.product,
            length=length,
            color=color,
            strand_quantity=strand_quantity,
        )
        .exclude(id=cart_item.id)
        .first()
    )

    if duplicate_item:
        duplicate_item.count += count
        duplicate_item.save(update_fields=["count"])
        cart_item.delete()
        cart_item = _get_user_cart_queryset(user).get(id=duplicate_item.id)
    else:
        cart_item.count = count
        cart_item.length = length
        cart_item.color = color
        cart_item.strand_quantity = strand_quantity
        cart_item.save(update_fields=["count", "length", "color", "strand_quantity"])

    return JsonResponse(
        {
            "message": "Cart item updated",
            "cart_item": _serialize_cart_item(request, cart_item),
        }
    )


@require_http_methods(["DELETE"])
def remove_cart_item(request, item_id):
    user = _get_request_user(request)
    if not user:
        return JsonResponse({"error": "User not logged in"}, status=401)

    cart_item = get_object_or_404(Cart.objects.filter(user=user), id=item_id)
    cart_item.delete()
    return JsonResponse({"message": "Cart item removed"})


def legacy_user_cart(request, user_id):
    cart = (
        Cart.objects.select_related("product", "product__category", "user")
        .prefetch_related("product__images")
        .filter(user_id=user_id)
    )
    cart_data = [_serialize_cart_item(request, item) for item in cart]
    return JsonResponse({"cart": cart_data})


@require_http_methods(["GET"])
def add_to_cart(request, user_id, product_id):
    product = get_object_or_404(Product.objects.select_related("category"), id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user_id=user_id,
        product=product,
        length="",
        color="",
        strand_quantity=10,
        defaults={"count": 1},
    )

    if not created:
        cart_item.count += 1
        cart_item.save(update_fields=["count"])

    cart_item = (
        Cart.objects.select_related("product", "product__category", "user")
        .prefetch_related("product__images")
        .get(id=cart_item.id)
    )
    return JsonResponse(
        {
            "message": "Product added to cart.",
            "cart_item": _serialize_cart_item(request, cart_item),
        }
    )


@require_http_methods(["GET"])
def remove_from_cart(request, user_id, product_id):
    cart_item = (
        Cart.objects.filter(
            user_id=user_id,
            product_id=product_id,
            length="",
            color="",
            strand_quantity=10,
        )
        .order_by("-id")
        .first()
    )

    if not cart_item:
        return JsonResponse({"message": "Product not found in cart."}, status=404)

    if cart_item.count > 1:
        cart_item.count -= 1
        cart_item.save(update_fields=["count"])
        return JsonResponse({"message": "Product count decremented in cart."})

    cart_item.delete()
    return JsonResponse({"message": "Product removed from cart."})
