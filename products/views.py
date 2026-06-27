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
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True
    )

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)