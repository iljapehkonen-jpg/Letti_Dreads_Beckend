from django.http import JsonResponse
from django.shortcuts import render
from cart.models import Cart

def user_cart(request, user_id):
    cart = Cart.objects.all()
    cart_data = []
    for item in cart:
        if item.user.id != user_id:
            continue
        cart_data.append({
            'id': item.id,
            'count': item.count,
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'description': item.product.description,
                'price': float(item.product.price),
                'in_stock': item.product.in_stock,
                'count': item.product.count,
            },
            'user': item.user.id,
        })
    return JsonResponse({
        'cart':cart_data,
    })
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