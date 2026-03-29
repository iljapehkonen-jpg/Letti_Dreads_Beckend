from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Category, HomeGalleryImage, HomeReviewImage, Product


def product_list(request):
    products = Product.objects.select_related("category").prefetch_related("images")
    products_list = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "in_stock": product.in_stock,
            "category": product.category.name,
            "count": product.count,
            "images": product.get_gallery_urls(request),
        }
        if product.photo:
            product_data["photo"] = product.get_absolute_url(request)
        else:
            product_data["photo"] = None
        products_list.append(product_data)
    return JsonResponse({"products": products_list, "count": len(products_list)})


def category_list(request):
    categories = Category.objects.all()
    categories_list = []
    for category in categories:
        categories_list.append(
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
            }
        )
    return JsonResponse({"categories": categories_list, "count": len(categories_list)})


def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("images"),
        id=product_id,
    )
    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "photo": product.get_absolute_url(request) if product.photo else None,
        "images": product.get_gallery_urls(request),
        "in_stock": product.in_stock,
        "count": product.count,
        "category": {"id": product.category.id, "name": product.category.name},
    }
    return JsonResponse(product_data)


def home_media(request):
    gallery_images = [
        request.build_absolute_uri(image.image.url)
        for image in HomeGalleryImage.objects.all()
        if image.image and hasattr(image.image, "url")
    ]
    review_images = [
        request.build_absolute_uri(image.image.url)
        for image in HomeReviewImage.objects.all()
        if image.image and hasattr(image.image, "url")
    ]

    return JsonResponse(
        {
            "gallery": gallery_images,
            "reviews": review_images,
        }
    )
