from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.filter(
        category=category,
        is_active=True
    ).order_by("-created_at")

    context = {
        "category": category,
        "products": products,
    }

    return render(request, "products/category_detail.html", context)


def product_detail(request, slug):
    """
    Ürün detayını ve o ürüne ait aktif varyantları getirir.
    """

    # URL'den gelen slug ile aktif ürünü buluyoruz
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True,
    )

    # Sadece bu ürüne ait ve satışa açık varyantları çekiyoruz
    variants = product.variants.filter(
        is_active=True,
    )

    context = {
        "product": product,
        "variants": variants,
    }

    return render(
        request,
        "products/product_detail.html",
        context,
    )