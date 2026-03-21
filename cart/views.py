from django.http import JsonResponse
from cart.models import Cart
from users.auth_utils import get_authenticated_user


def _serialize_cart_item(request, item):
    return {
        'id': item.id,
        'count': item.count,
        'product': {
            'id': item.product.id,
            'name': item.product.name,
            'description': item.product.description,
            'price': float(item.product.price),
            'in_stock': item.product.in_stock,
            'count': item.product.count,
            'photo': item.product.get_absolute_url(request),
            'images': item.product.get_gallery_urls(request),
            'category': item.product.category.name,
        },
        'user': item.user.id,
    }


def user_cart(request):
    user = get_authenticated_user(request)

    if not user or not user.is_authenticated:
        return JsonResponse({'error': 'User not logged in'}, status=401)

    cart = (
        Cart.objects.select_related('product', 'product__category', 'user')
        .prefetch_related('product__images')
        .filter(user=user)
    )
    cart_data = [_serialize_cart_item(request, item) for item in cart]

    return JsonResponse({
        'cart':cart_data,
    })


def legacy_user_cart(request, user_id):
    cart = (
        Cart.objects.select_related('product', 'product__category', 'user')
        .prefetch_related('product__images')
        .filter(user_id=user_id)
    )
    cart_data = [_serialize_cart_item(request, item) for item in cart]
    return JsonResponse({'cart': cart_data})
def add_to_cart(request, user_id, product_id):
    cart = Cart.objects.all()
    for item in cart:
        if item.user.id == user_id and item.product.id == product_id:
            item.count += 1
            item.save()
            return JsonResponse({'message': 'Product count incremented in cart.'})
    new_item = Cart.objects.create(
        user_id=user_id,
        product_id=product_id,
        count=1
    )
    return JsonResponse({'message': 'Product added to cart.'})
    
def remove_from_cart(request, user_id, product_id):
    cart = Cart.objects.all()
    for item in cart:
        if item.user.id == user_id and item.product.id == product_id:
            if item.count > 1:
                item.count -= 1
                item.save()
                return JsonResponse({'message': 'Product count decremented in cart.'})
            else:
                item.delete()
                return JsonResponse({'message': 'Product removed from cart.'})
    return JsonResponse({'message': 'Product not found in cart.'}, status=404)
