from .models import Order


def order_count(request):
    if not request.user.is_authenticated:
        return {"order_count": 0}

    count = Order.objects.filter(
        user=request.user,
    ).count()

    return {
        "order_count": count,
    }