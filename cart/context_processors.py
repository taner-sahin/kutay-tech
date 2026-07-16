from django.db.models import Sum

from .models import CartItem


def cart_count(request):
    """
    Navbar'da sepetteki toplam ürün adedini gösterir.
    """

    if not request.user.is_authenticated:
        return {"cart_count": 0}

    total = (
        CartItem.objects
        .filter(user=request.user)
        .aggregate(total=Sum("quantity"))["total"]
        or 0
    )

    return {
        "cart_count": total,
    }