from django.shortcuts import get_object_or_404, render
from reviews.forms import ReviewForm
from .models import Category, Product
from django.db.models import Avg


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.filter(
        category=category,
        is_active=True,
    ).order_by("-created_at")

    context = {
        "category": category,
        "products": products,
    }

    return render(
        request,
        "products/category_detail.html",
        context,
    )
def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True,
    )

    variants = product.variants.filter(
        is_active=True,
    )

    reviews = product.reviews.select_related("user")

    rating_summary = reviews.aggregate(
        average_rating=Avg("rating")
    )

    context = {
        "product": product,
        "variants": variants,
        "reviews": reviews,
        "review_form": ReviewForm(),
        "average_rating": rating_summary["average_rating"] or 0,
        "review_count": reviews.count(),
    }

    return render(
        request,
        "products/product_detail.html",
        context,
    )