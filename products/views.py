from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Category, Product

def product_list(request):
    products = Product.objects.all()
    products_list = []
    for product in products:
        products_list.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'photo': product.photo.url if product.photo else None,
            'in_stock' : product.in_stock,
            'category': product.category.name,
            'count': product.count,
        })
    return JsonResponse({'products': products_list, 'count': len(products_list)})

def category_list(request):
    categories = Category.objects.all()
    categories_list = []
    for category in categories:
        categories_list.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
        })
    return JsonResponse({'categories': categories_list, 'count': len(categories_list)})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'photo': product.photo.url if product.photo else None,
        'in_stock': product.in_stock,
        'count': product.count,
        'category': { 'id': product.category.id,'name': product.category.name },
    }
    return JsonResponse(product_data)



