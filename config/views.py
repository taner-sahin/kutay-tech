from django.shortcuts import render
from products.models import Product

def home_view(request):
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by("-created_at")[:4]

    new_products = Product.objects.filter(
        is_active=True
    ).order_by("-created_at")[:8]

    context = {
        "featured_products": featured_products,
        "new_products": new_products,
    }

    return render(request, "home.html", context)