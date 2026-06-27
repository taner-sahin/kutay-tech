from .models import Category


def nav_categories(request):
    categories = Category.objects.all().order_by("name")

    return {
        "nav_categories": categories
    }